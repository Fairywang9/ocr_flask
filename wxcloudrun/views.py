from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask import Flask
import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res, PaddleOCR


import numpy as np
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


app = Flask(__name__)
table_engine = PPStructure(show_log=False)




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p >"



@app.route("/receive", methods=['POST', 'GET'])
def receive():
    img_path =  "https://636c-cloud1-9g31hv999af9dd5c-1313358468.tcb.qcloud.la/my-photo.png?sign=5d0ff1562354b4a8816f362e99f13dde&t=1662945841"
    img = cv2.imread(img_path)
    result = table_engine(img)
    print('==============')
    print(result)
    return json.dumps(result, cls=MyEncoder)




# @app.route('/api/count', methods=['POST'])
# def count():
#     """
#     :return:计数结果/清除结果
#     """
#
#     # 获取请求体参数
#     params = request.get_json()
#
#     # 检查action参数
#     if 'action' not in params:
#         return make_err_response('缺少action参数')
#
#     # 按照不同的action的值，进行不同的操作
#     action = params['action']
#
#     # 执行自增操作
#     if action == 'inc':
#         counter = query_counterbyid(1)
#         if counter is None:
#             counter = Counters()
#             counter.id = 1
#             counter.count = 1
#             counter.created_at = datetime.now()
#             counter.updated_at = datetime.now()
#             insert_counter(counter)
#         else:
#             counter.id = 1
#             counter.count += 1
#             counter.updated_at = datetime.now()
#             update_counterbyid(counter)
#         return make_succ_response(counter.count)
#
#     # 执行清0操作
#     elif action == 'clear':
#         delete_counterbyid(1)
#         return make_succ_empty_response()
#
#     # action参数错误
#     else:
#         return make_err_response('action参数错误')
#
#
# @app.route('/api/count', methods=['GET'])
# def get_count():
#     """
#     :return: 计数的值
#     """
#     counter = Counters.query.filter(Counters.id == 1).first()
#     return make_succ_response(0) if counter is None else make_succ_response(counter.count)
