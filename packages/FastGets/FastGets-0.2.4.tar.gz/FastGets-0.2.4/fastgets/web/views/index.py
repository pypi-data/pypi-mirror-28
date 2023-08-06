# coding: utf8

import datetime
from mongoengine import Q
from flask import Blueprint, jsonify, request, render_template


index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def index():

    return render_template('index.html')
