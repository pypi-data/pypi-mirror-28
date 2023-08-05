# coding: utf8
import json
import uuid
import random

from flask import Blueprint, jsonify, request, redirect, abort
from fastgets.core.errors import ApiError
from fastgets.template import Template
from fastgets.job import Job
from fastgets.process import Process


process_blueprint = Blueprint('process', __name__, url_prefix='/process')


@process_blueprint.route('/add')
def process_add_view():
    name = request.args.get('name')
    type = request.args.get('type')

    Process.add(name, type)
    return jsonify()
