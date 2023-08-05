# coding: utf8

from flask import Blueprint, jsonify, request

from fastgets.core.errors import ApiError
from fastgets.models.instance import Instance
from fastgets.process import Process

instance_blueprint = Blueprint('instance', __name__, url_prefix='/instance')


@instance_blueprint.route('/list')
def instance_list_view():
    process_dict = {
        id: process.to_api_json()
        for id, process in Process.get_dict().items()
    }

    instances = Instance.objects.order_by('-create_at').skip(request.start).limit(request.limit)
    instances = [
        instance.to_api_json(process=process_dict.get(instance.process_id))
        for instance in instances
    ]

    return jsonify(dict(instances=instances))


@instance_blueprint.route('/stop')
def instance_stop_view():
    id = request.args.get('id')
    if not id:
        raise ApiError('ID 不能为空')

    instance = Instance.get(id)
    if not instance:
        raise ApiError('实例不存在')

    instance.stop()
    return jsonify()
