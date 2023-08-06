import click
import logging
import json
import os
import mimetypes

from . import load_cfg, die, bye
from archivant import Archivant
from archivant.exceptions import NotFoundException, ConflictException
from conf.defaults import get_def_conf, get_help
from utils.loggers import initLoggers
from custom_types import StringList


conf = dict()
arc = None


@click.group(name="libreant-db", help="command line program to manage libreant database")
@click.version_option()
@click.option('-s', '--settings', type=click.Path(exists=True, readable=True), help='file from which load settings')
@click.option('-d', '--debug', is_flag=True, help=get_help('DEBUG'))
@click.option('--fsdb-path', type=click.Path(), metavar="<path>", help=get_help('FSDB_PATH'))
@click.option('--es-indexname', type=click.STRING, metavar="<name>", help=get_help('ES_INDEXNAME'))
@click.option('--es-hosts', type=StringList(), metavar="<host>..", help=get_help('ES_HOSTS'))
def libreant_db(debug, settings, fsdb_path, es_indexname, es_hosts):
    initLoggers(logNames=['config_utils'])
    global conf
    conf = get_def_conf()
    conf.update(load_cfg(settings, debug=debug))
    cliConf = {}
    if debug:
        cliConf['DEBUG'] = True
    if fsdb_path:
        cliConf['FSDB_PATH'] = fsdb_path
    if es_indexname:
        cliConf['ES_INDEXNAME'] = es_indexname
    if es_hosts:
        cliConf['ES_HOSTS'] = es_hosts
    conf.update(cliConf)
    initLoggers(logging.DEBUG if conf.get('DEBUG', False) else logging.INFO)

    try:
        global arc
        arc = Archivant(conf=conf)
    except Exception as e:
        if conf.get('DEBUG', False):
            raise
        else:
            die(str(e))


@libreant_db.command(name="upgrade")
@click.option('-c', '--check-only', is_flag=True,
              help='Does not perform any action on database, it will exit with code 123 if an upgraded is needed, and 0 if it\'s not. '+
                   'Any other exit code means that an error occurred.')
@click.option('-y', '--yes', is_flag=True, help='Assume Yes to all queries and do not prompt')
def upgrade(check_only, yes):
    '''
    Upgrade libreant database.

    This command can be used after an update of libreant
    in order to upgrade the database and make it aligned with the new version.
    '''
    from utils.es import Elasticsearch
    from libreantdb import DB, migration
    from libreantdb.exceptions import MappingsException

    try:
        db = DB(Elasticsearch(hosts=conf['ES_HOSTS']),
                              index_name=conf['ES_INDEXNAME'])
        if not db.es.indices.exists(db.index_name):
            die("The specified index does not exists: {}".format(db.index_name))

        # Migrate old special `_timestamp` field into the new `_insertion_date`
        num_to_update = migration.elements_without_insertion_date(db.es, db.index_name)
        if num_to_update > 0:
            if check_only:
                exit(123)

            if yes or click.confirm("{} entries miss the '_insertion_date' field. Do you want to proceed and update those entries?".format(num_to_update),
                             prompt_suffix='',
                             default=False):
                migration.migrate_timestamp(db.es, db.index_name)
            else:
                exit(0)

        # Upgrade the index mappings and reindex if necessary
        try:
            db.update_mappings()
        except MappingsException:
            if check_only:
                exit(123)
            count = db.es.count(index=db.index_name)['count']
            if yes or click.confirm("Some old or wrong mappings has been found for the index '"+ db.index_name +"'.\n"\
                                    "In order to upgrade them it is necessary to reindex '"+ str(count) +"' entries.\n"\
                                    "Are you sure you want to proceed?",
                                     prompt_suffix='',
                                     default=False):
                    db.reindex()

    except Exception as e:
        if conf.get('DEBUG', False):
            raise
        else:
            die(str(e))


@libreant_db.command(name="export-volume", help="export a volume")
@click.argument('volumeid')
@click.option('-p', '--pretty', is_flag=True, help='format the output on multiple lines')
def export_volume(volumeid, pretty):
    try:
        volume = arc.get_volume(volumeid)
    except NotFoundException as e:
        bye(str(e), exit_code=4)

    indent = 3 if pretty else None
    ouput = json.dumps(volume, indent=indent)
    click.echo(ouput)


@libreant_db.command(name="import")
@click.argument('source', type=click.File('r'), required=True)
@click.option('--ignore-conflicts', is_flag=True, help='Skip volumes with an already existent id')
@click.option('-y', '--yes', is_flag=True, help='Assume Yes to all queries and do not prompt')
def import_volumes(source, ignore_conflicts, yes):
    '''Import volumes

    SOURCE must be a json file and must follow the same structure used in `libreant-db export`.
    Pass - to read from standard input.
    '''
    volumes = json.load(source)
    tot = len(volumes)
    if not yes:
        click.confirm("Are you sure you want to import {} volumes into index '{}'".format(tot, arc._config['ES_INDEXNAME']))
    conflicts=0
    with click.progressbar(volumes, label='adding volumes') as bar:
        for v in bar:
            try:
                arc.import_volume(v)
            except ConflictException as ce:
                if not ignore_conflicts:
                    die(str(ce))
                conflicts += 1
            except Exception as e:
                if conf.get('DEBUG', False):
                    raise
                else:
                    die(str(e))

    if conflicts > 0:
        click.echo("{} volumes has been skipped beacause of a conflict".format(conflicts))


@libreant_db.command(name="remove", help="remove a volume")
@click.argument('volumeid')
def delete_volume(volumeid):
    try:
        arc.delete_volume(volumeid)
    except NotFoundException as e:
        bye(str(e), exit_code=4)


@libreant_db.command(help="search volumes by query")
@click.argument('query')
@click.option('-p', '--pretty', is_flag=True, help='format the output on multiple lines')
def search(query, pretty):
    results = arc._db.user_search(query)['hits']['hits']
    results = map(arc.normalize_volume, results)
    if not results:
        bye("No results found for '{}'".format(query), exit_code=4)
    indent = 3 if pretty else None
    output = json.dumps(results, indent=indent)
    click.echo(output)


@libreant_db.command(name='export-all', help="export all volumes")
@click.option('-p', '--pretty', is_flag=True, help='format the output on multiple lines')
def export_all(pretty):
    indent = 3 if pretty else None
    volumes = [vol for vol in arc.iter_all_volumes()]
    click.echo(json.dumps(volumes, indent=indent))


@libreant_db.command(name='attach', help='adds an attachment to an existing volume')
@click.argument('volumeid')
@click.option('-f', 'filepath', type=click.Path(exists=True, resolve_path=True), multiple=True, help='the path of the attachment')
@click.option('-t', '--notes', type=click.STRING, metavar='<string>', multiple=True, help='notes about the attachment')
def append_file(volumeid, filepath, notes):
    attachments = attach_list(filepath, notes)
    try:
        arc.insert_attachments(volumeid, attachments)
    except Exception:
        die('An upload error occurred in updating an attachment!', exit_code=4)


@libreant_db.command(name='insert-volume')
@click.option('-l', '--language', type=click.STRING, required=True,
              help='specify the language of the volume')
@click.option('-f', '--filepath',
              type=click.Path(exists=True, resolve_path=True),
              multiple=True, help='path to the attachment to be uploaded')
@click.option('-t', '--notes', type=click.STRING, multiple=True,
              help='notes about the attachment '
              '(ie: "complete version" or "poor quality"')
@click.argument('metadata', type=click.File('r'), required=False)
def insert_volume(language, filepath, notes, metadata):
    '''
    Add a new volume to libreant.

    The metadata of the volume are taken from a json file whose path must be
    passed as argument. Passing "-" as argument will read the file from stdin.
    language is an exception, because it must be set using --language

    For every attachment you must add a --file AND a --notes.

    \b
    Examples:
        Adds a volume with no metadata. Yes, it makes no sense but you can
          libreant-db insert-volume -l en - <<<'{}'
        Adds a volume with no files attached
          libreant-db insert-volume -l en - <<EOF
          {
            "title": "How to create volumes",
            "actors": ["libreant devs", "open access conspiration"]
          }
          EOF
        Adds a volume with one attachment but no metadata
          libreant-db insert-volume -l en -f /path/book.epub --notes 'poor quality'
        Adds a volume with two attachments but no metadata
          libreant-db insert-volume -l en -f /path/book.epub --notes 'poor quality' -f /path/someother.epub --notes 'preprint'

    '''
    meta = {"_language": language}
    if metadata:
        meta.update(json.load(metadata))
    attachments = attach_list(filepath, notes)
    try:
        out = arc.insert_volume(meta, attachments)
    except Exception:
        die('An upload error have occurred!', exit_code=4)
    click.echo(out)


def attach_list(filepaths, notes):
    '''
    all the arguments are lists
    returns a list of dictionaries; each dictionary "represent" an attachment
    '''
    assert type(filepaths) in (list, tuple)
    assert type(notes) in (list, tuple)

    # this if clause means "if those lists are not of the same length"
    if len(filepaths) != len(notes):
        die('The number of --filepath, and --notes must be the same')

    attach_list = []
    for fname, note in zip(filepaths, notes):
        name = os.path.basename(fname)
        assert os.path.exists(fname)
        mime = mimetypes.guess_type(fname)[0]
        if mime is not None and '/' not in mime:
            mime = None
        attach_list.append({
            'file': fname,
            'name': name,
            'mime': mime,
            'note': note
        })
    return attach_list


if __name__ == '__main__':
    libreant_db()
