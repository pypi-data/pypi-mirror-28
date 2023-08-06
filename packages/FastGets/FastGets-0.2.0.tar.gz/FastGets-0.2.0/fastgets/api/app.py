# coding: utf8

import json
from flask import Flask, request, jsonify
from fastgets.core import config_parse


def create_app():
    app = Flask(__name__)

    from fastgets.api.views.cluster import cluster_blueprint
    from fastgets.api.views.fatal_error import fatal_error_blueprint
    from fastgets.api.views.instance import instance_blueprint
    from fastgets.api.views.job import job_blueprint
    from fastgets.api.views.process import process_blueprint
    from fastgets.api.views.template import template_blueprint

    app.register_blueprint(cluster_blueprint)
    app.register_blueprint(fatal_error_blueprint)
    app.register_blueprint(instance_blueprint)
    app.register_blueprint(job_blueprint)
    app.register_blueprint(process_blueprint)
    app.register_blueprint(template_blueprint)

    return app


def run():
    from fastgets import env
    env.mode = env.API
    config_parse()

    app = create_app()

    @app.before_request
    def before_request():
        request.start = int(request.args.get('start') or 0)
        request.limit = int(request.args.get('limit') or 20)

    @app.after_request
    def after_request(response):

        # 正常返回的接口自动加上 error_code=0
        if response.status_code in [200, 304]:
            dct = json.loads(response.get_data())
            if 'error_code' not in dct:
                dct['error_code'] = 0
            response = jsonify(dct)

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')

        return response

    app.run(env.API_CONFIG['host'], env.API_CONFIG['port'], debug=True)


if __name__ == '__main__':
    run()

