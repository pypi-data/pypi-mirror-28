from webant.util import routes_collector
from util import ApiError, make_success_response, on_json_load_error
from flask import request, url_for, jsonify
import users.api
from users import Action
from flask import current_app

routes = []
route = routes_collector(routes)


@route('/users/<int:userID>', methods=['GET'])
def get_user(userID):
    current_app.authz.perform_authorization(('/users/{}'.format(userID), Action.READ))
    try:
        u = users.api.get_user(id=userID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': {'id': u.id, 'name': u.name}})


@route('/users/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    current_app.authz.perform_authorization(('/users/{}'.format(userID), Action.DELETE))
    try:
        users.api.delete_user(id=userID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("user has been successfully deleted")


@route('/users/', methods=['GET'])
def get_users():
    current_app.authz.perform_authorization(('/users/*', Action.READ))
    usrs = [{'id': u.id, 'name': u.name} for u in users.api.get_users()]
    return jsonify({'data': usrs})


@route('/users/', methods=['POST'])
def add_user():
    current_app.authz.perform_authorization(('/users/*', Action.CREATE))
    request.on_json_loading_failed = on_json_load_error
    userData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not userData:
        raise ApiError("Unsupported media type", 415)
    name = userData.get('name', None)
    if not name:
        raise ApiError("Bad Request", 400, details="missing 'name' parameter")
    password = userData.get('password', None)
    if not password:
        raise ApiError("Bad Request", 400, details="missing 'password' parameter")
    try:
        user = users.api.add_user(name=name, password=password)
    except users.api.ConflictException, e:
        raise ApiError("Conflict", 409, details=str(e))
    link_self = url_for('.get_user', userID=user.id, _external=True)
    response = jsonify({'data': {'id': user.id, 'link_self': link_self}})
    response.status_code = 201
    response.headers['Location'] = link_self
    return response


@route('/users/<int:userID>', methods=['PATCH'])
def update_user(userID):
    current_app.authz.perform_authorization(('/users/{}'.format(userID), Action.UPDATE))
    request.on_json_loading_failed = on_json_load_error
    userData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not userData:
        raise ApiError("Unsupported media type", 415)
    try:
        users.api.update_user(userID, userData)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("user has been successfully updated")


@route('/groups/<int:groupID>', methods=['GET'])
def get_group(groupID):
    current_app.authz.perform_authorization(('/groups/{}'.format(groupID), Action.READ))
    try:
        g = users.api.get_group(id=groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': {'id': g.id, 'name': g.name}})


@route('/groups/<int:groupID>', methods=['DELETE'])
def delete_group(groupID):
    current_app.authz.perform_authorization(('/groups/{}'.format(groupID), Action.DELETE))
    try:
        users.api.delete_group(id=groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("group has been successfully deleted")


@route('/groups/', methods=['GET'])
def get_groups():
    current_app.authz.perform_authorization(('/groups/*', Action.READ))
    groups = [ {'id': g.id, 'name': g.name } for g in users.api.get_groups() ]
    return jsonify({'data': groups})


@route('/groups/', methods=['POST'])
def add_group():
    current_app.authz.perform_authorization(('/groups/*', Action.CREATE))
    request.on_json_loading_failed = on_json_load_error
    groupData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not groupData:
        raise ApiError("Unsupported media type", 415)
    name = groupData.get('name', None)
    if not name:
        raise ApiError("Bad Request", 400, details="missing 'name' parameter")
    try:
        group = users.api.add_group(name=name)
    except users.api.ConflictException, e:
        raise ApiError("Conflict", 409, details=str(e))
    link_self = url_for('.get_group', groupID=group.id, _external=True)
    response = jsonify({'data': {'id': group.id, 'link_self': link_self}})
    response.status_code = 201
    response.headers['Location'] = link_self
    return response


@route('/groups/<int:groupID>', methods=['PATCH'])
def update_group(groupID):
    current_app.authz.perform_authorization(('/groups/{}'.format(groupID), Action.UPDATE))
    request.on_json_loading_failed = on_json_load_error
    groupData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not groupData:
        raise ApiError("Unsupported media type", 415)
    try:
        users.api.update_group(groupID, groupData)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("group has been successfully updated")


@route('/groups/<int:groupID>/users/<int:userID>', methods=['PUT'])
def add_user_to_group(groupID, userID):
    current_app.authz.perform_authorization(('/groups/{}/users/{}'.format(groupID, userID), Action.CREATE))
    try:
        users.api.add_user_to_group(userID, groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("user has been successfully added to group")


@route('/groups/<int:groupID>/users/<int:userID>', methods=['DELETE'])
def delete_user_from_group(groupID, userID):
    current_app.authz.perform_authorization(('/groups/{}/users/{}'.format(groupID, userID), Action.DELETE))
    try:
        users.api.remove_user_from_group(userID, groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("user has been successfully removed from group")


@route('/groups/<int:groupID>/users/', methods=['GET'])
def get_users_in_group(groupID):
    current_app.authz.perform_authorization(('/groups/{}/users/*'.format(groupID), Action.READ))
    try:
        us = [{'id': u.id} for u in users.api.get_users_in_group(groupID)]
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': us})


@route('/users/<int:userID>/groups/', methods=['GET'])
def get_groups_of_user(userID):
    current_app.authz.perform_authorization(('/users/{}/groups/*'.format(userID), Action.READ))
    try:
        groups = [{'id': g.id} for g in users.api.get_groups_of_user(userID)]
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': groups})


@route('/capabilities/', methods=['GET'])
def get_capabilities():
    current_app.authz.perform_authorization(('/capabilities/*', Action.READ))
    capabilities = [ c.to_dict() for c in users.api.get_capabilities()]
    return jsonify({'data': capabilities})


@route('/capabilities/<int:capID>', methods=['GET'])
def get_capability(capID):
    current_app.authz.perform_authorization(('/capabilities/{}'.format(capID), Action.READ))
    try:
        cap = users.api.get_capability(capID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': cap.to_dict()})


@route('/capabilities/<int:capID>', methods=['DELETE'])
def delete_capability(capID):
    current_app.authz.perform_authorization(('/capabilities/{}'.format(capID), Action.DELETE))
    try:
        users.api.delete_capability(capID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("capability has been successfully deleted")


@route('/capabilities/', methods=['POST'])
def add_capability():
    current_app.authz.perform_authorization(('/capabilities/*', Action.CREATE))
    request.on_json_loading_failed = on_json_load_error
    capData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not capData:
        raise ApiError("Unsupported media type", 415)
    domain = capData.get('domain', None)
    if not domain:
        raise ApiError("Bad Request", 400, details="missing 'domain' parameter")
    actions = capData.get('actions', None)
    if not actions:
        raise ApiError("Bad Request", 400, details="missing 'actions' parameter")
    cap = users.api.add_capability(domain=domain, action=Action.from_list(actions))
    link_self = url_for('.get_capability', capID=cap.id, _external=True)
    response = jsonify({'data': {'id': cap.id, 'link_self': link_self}})
    response.status_code = 201
    response.headers['Location'] = link_self
    return response


@route('/capabilities/<int:capID>', methods=['PATCH'])
def update_capability(capID):
    current_app.authz.perform_authorization(('/capabilities/{}'.format(capID), Action.UPDATE))
    request.on_json_loading_failed = on_json_load_error
    capData = request.get_json()
    # the next two lines should be removed when Flask version is >= 1.0
    if not capData:
        raise ApiError("Unsupported media type", 415)
    if 'actions' in capData:
        capData['action'] = Action.from_list(capData.pop('actions'))
    try:
        users.api.update_capability(capID, capData)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("capability has been successfully updated")


@route('/groups/<int:groupID>/capabilities/<int:capID>', methods=['PUT'])
def add_capability_to_group(groupID, capID):
    current_app.authz.perform_authorization(('/groups/{}/capabilities/{}'.format(groupID, capID), Action.CREATE))
    try:
        users.api.add_capability_to_group(capID, groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("capability has been successfully added to group")


@route('/groups/<int:groupID>/capabilities/<int:capID>', methods=['DELETE'])
def delete_capability_from_group(groupID, capID):
    current_app.authz.perform_authorization(('/groups/{}/capabilities/{}'.format(groupID, capID), Action.DELETE))
    try:
        users.api.remove_capability_from_group(capID, groupID)
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return make_success_response("capability has been successfully removed from group")


@route('/groups/<int:groupID>/capabilities/', methods=['GET'])
def get_capabilities_of_group(groupID):
    current_app.authz.perform_authorization(('/groups/{}/capabilities/*'.format(groupID), Action.READ))
    try:
        caps = [ cap.to_dict() for cap in users.api.get_capabilities_of_group(groupID)]
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': caps})


@route('/capabilities/<int:capID>/groups/', methods=['GET'])
def get_groups_with_capability(capID):
    current_app.authz.perform_authorization(('/capabilities/{}/groups/*'.format(capID), Action.READ))
    try:
        groups = [{'id': g.id} for g in users.api.get_groups_with_capability(capID)]
    except users.api.NotFoundException, e:
        raise ApiError("Not found", 404, details=str(e))
    return jsonify({'data': groups})
