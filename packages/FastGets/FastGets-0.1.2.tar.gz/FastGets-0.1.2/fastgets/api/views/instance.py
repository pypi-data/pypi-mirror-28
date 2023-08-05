# coding: utf8

from flask import Blueprint, jsonify, request

from fastgets.models.instance import Instance
from fastgets.stats import InstanceStats
from fastgets.pool import RunningPool, ProcessErrorPool, CrawlErrorPool
from fastgets.core.errors import ApiError
from fastgets.process import Process


instance_blueprint = Blueprint('instance', __name__, url_prefix='/instance')


@instance_blueprint.route('')
def instance_view():
    id = request.args.get('id')
    if not id:
        raise ApiError('ID 不能为空')

    instance = Instance.get(id)
    if not instance:
        raise ApiError('爬虫实例不存在')

    instance = instance.to_api_json()
    return jsonify(instance=instance)


@instance_blueprint.route('/tasks')
def instance_tasks_view():
    id = request.args.get('id')
    if not id:
        raise ApiError('ID 不能为空')

    instance = Instance.get(id)
    if not instance:
        raise ApiError('爬虫实例不存在')

    crawl_tasks, process_tasks = InstanceStats.get_top_tasks(instance.id)
    running_tasks = RunningPool.get_tasks(instance.id)

    crawl_error_tasks = CrawlErrorPool.get_tasks(instance.id)
    process_error_tasks = ProcessErrorPool.get_tasks(instance.id)

    crawl_tasks = [
        task.to_api_json()
        for task in crawl_tasks
    ]
    process_tasks = [
        task.to_api_json()
        for task in process_tasks
    ]
    running_tasks = [
        task.to_api_json()
        for task in running_tasks
    ]

    crawl_error_tasks = [
        task.to_api_json()
        for task in crawl_error_tasks
    ]

    process_error_tasks = [
        task.to_api_json()
        for task in process_error_tasks
    ]

    return jsonify(crawl_tasks=crawl_tasks, process_tasks=process_tasks, running_tasks=running_tasks,
                   crawl_error_tasks=crawl_error_tasks, process_error_tasks=process_error_tasks)


@instance_blueprint.route('/list')
def instance_list_view():
    process_dict = {
        id: process.to_api_json()
        for id, process in Process.get_dict().items()
    }

    instances = Instance.objects.order_by('-start_at').skip(request.start).limit(request.limit)
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
