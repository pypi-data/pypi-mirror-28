# coding: utf8

from flask import Blueprint, jsonify, request

task_blueprint = Blueprint('task', __name__, url_prefix='/task')


@task_blueprint.route('/page_raw')
def task_page_raw_view():

    # find_by_id
    # 遍历 process error task pool

    jobs = Job.objects.order_by('-created_at').skip(request.start).limit(request.limit)
    job_ids = [job.id for job in jobs]

    job_dict_dict = JobStats.get_job_dict_dict(job_ids)

    jobs = [
        job.to_api_json(**job_dict_dict.get(job.id, {}))
        for job in jobs
    ]

    return jsonify(dict(jobs=jobs))

