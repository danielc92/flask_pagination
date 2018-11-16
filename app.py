"""Imports."""
from flask import Flask, request, redirect, render_template, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_


# App settings
app = Flask(__name__, static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = 'topsecret!'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True

# Db settings
cur_dir = os.getcwd()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_path = '/tmp/superstore'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + cur_dir + db_path
db = SQLAlchemy(app)

# Pagination setting
pp = 20


class Orders(db.Model):
    """Maps to orders_subset_cleaned table in sqlite database."""

    __tablename__ = 'orders_subset_cleaned'

    row_id = db.Column('row_id', db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer)
    order_date = db.Column('order_date', db.Text)
    order_priority = db.Column('order_priority', db.Text)
    order_quantity = db.Column('order_quantity', db.Integer)
    sales = db.Column('sales', db.Float)
    ship_mode = db.Column('ship_mode', db.Text)
    profit = db.Column('profit', db.Float)
    unit_price = db.Column('unit_price', db.Float)
    customer_name = db.Column('customer_name', db.Text)
    province = db.Column('province', db.Text)
    region = db.Column('region', db.Text)
    customer_segment = db.Column('customer_segment', db.Text)
    product_category = db.Column('product_category', db.Text)
    product_sub_category = db.Column('product_sub_category', db.Text)
    product_name = db.Column('product_name', db.Text)
    product_container = db.Column('product_container', db.Text)


def return_search_terms(search_string):
    """Return search terms as a list from a search string object."""
    if search_string == '':
        return [search_string]
    else:
        terms = search_string.split(' ')
        terms_stripped = list(map(str.strip, terms))
        search_list = [term for term in terms_stripped if term != '']
        return search_list


def return_search_conditions(search_list):
    """Return list of search conditions using sqlalchemy."""
    search_conditions = [Orders.customer_name.ilike('%{}%'.format(term)) for term in search_list]
    return search_conditions


def return_page_int(pn):
    """Return cleaned page number."""
    try:
        return int(pn)
    except:
        return 1


def clean_search(raw_search):
    """Return cleaned search item."""
    if len(raw_search.strip()) > 0:
        search = raw_search
    else:
        search = None

    return search


@app.route('/', methods=['POST', 'GET'])
def home():
    """The order route (also the home page)."""
    pn_raw = request.args.get('pn', '1')
    pn = return_page_int(pn_raw)

    if request.method == 'POST':
        raw_search = request.form['search']
        search = clean_search(raw_search)
        return redirect(url_for('home', search=search, pn=1))

    else:
        search = request.args.get('search', None)
        if search:
            search_terms = return_search_terms(search)
            search_conditions = return_search_conditions(search_terms)
            orders = Orders.query.filter(and_(*search_conditions)).paginate(page=pn, per_page=pp, error_out=True)
        else:
            orders = Orders.query.paginate(page=pn, per_page=pp, error_out=True)

        return render_template('test.html', orders=orders, search=search)


'''
QUERYING EXAMPLES
- Model.query.filter(Model.columnName.contains('sub_string'))
- orders=Orders.query.filter(Orders.customer_name.ilike('H%%')).paginate(1,8,False).items


from sqlalchemy import or_

conditions=[]
        for name in session['search_term']:
            conditions.append(Orders.customer_name.ilike('%{}%'.format(name)))

        orders=Orders.query.filter(or_(*conditions))\
        .paginate(page=page_num, per_page=config_pp, error_out=True)
        print(orders.total)
        return render_template('home.html', orders=orders, session=session)
'''
