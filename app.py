from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import pandas

app = Flask(__name__)
app.debug = True

data = pandas.read_csv('static/superstore.csv')
data_dict = data.to_dict(orient = 'records')
print(data.shape)
print(data_dict)

def get_users(offset=0, per_page=20):
    return data_dict[offset: offset + per_page]

@app.route('/')
def index():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    print(page, per_page, offset)
    total = len(data_dict)
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('index.html',
                           data=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)