from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args, request
import pandas
import re


app = Flask(__name__)
app.debug = True

data = pandas.read_csv('static/superstore.csv')
data_dict = data.to_dict(orient = 'records')

def get_users(offset=0, per_page=10):

    return data_dict[offset: offset + per_page]


@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':

        print('Search was posted.')
        # Store search 
        search = request.form['search']
        subset_data = data[data['Customer Name'].str.contains(search, 
          regex = True, 
          flags = re.IGNORECASE)]

        subset_data_dict = subset_data.to_dict(orient = 'records')

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        total = len(subset_data_dict)
        pagination_users = subset_data_dict[0:0+10]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('index.html', data=pagination_users, page=page,per_page=per_page, pagination=pagination)

    else:

      page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
      total = len(data_dict)
      pagination_users = get_users(offset=offset, per_page=per_page)
      pagination = Pagination(page=page, per_page=per_page, total=total,
                              css_framework='bootstrap4')

      return render_template('index.html',
                               data=pagination_users,
                               page=page,
                               per_page=per_page,
                               pagination=pagination)