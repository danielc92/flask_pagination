#imports
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_

# app settings
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'asfkjhalsiuh34jqthluih4gliu3qg4vlkqh3b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flask'
config_pp = 20
db = SQLAlchemy(app)

# instantiate database model for orders_cleaned table
class Orders(db.Model):

    __tablename__ = 'orders_cleaned'
    
    row_id = db.Column('row_id', db.Integer, primary_key = True)
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
    product_sub_category= db.Column('product_sub_category', db.Text)
    product_name = db.Column('product_name', db.Text)
    product_container = db.Column('product_container', db.Text)

# default route will redirect to orders page 1
@app.route('/')
def reroute():
    session['search_term'] = ''
    return redirect(url_for('home', page_num = 1))

# order route shows orders paginated
@app.route('/orders/<int:page_num>', methods = ['POST','GET'])

def home(page_num):

    # IF SEARCH BUTTON IS PRESSED STORE SEARCH TERM IN SESSION AND REDIRECT
    if request.method == 'POST' and len(request.form['search']) > 0:
        session['search_term'] = request.form['search'].split(' ') 
        return redirect(url_for('home', page_num = 1))

    # IF SEARCH BUTTON IS NOT PRESS, RETAIN SEARCH
    elif request.method == 'GET' and len(session['search_term']) > 0:

        conditions = []
        for name in session['search_term']:
            conditions.append(Orders.customer_name.ilike('%{}%'.format(name)))

        orders = Orders.query.filter(or_(*conditions))\
        .paginate(page = page_num, per_page = config_pp, error_out = True)
        print(orders.total)
        return render_template('home.html', orders = orders, session = session)

    # IF SEARCH BUTTON IS NOT PRESSED AND SEARCH IS EMPTY
    else:

        orders = Orders.query.\
        order_by(Orders.order_id).\
        paginate(page = page_num, per_page = config_pp, error_out = True)
        print(orders.total)
        return render_template('home.html', orders = orders, session = session)









#
'''
QUERYING EXAMPLES
- Model.query.filter(Model.columnName.contains('sub_string'))
- orders = Orders.query.filter(Orders.customer_name.ilike('H%%')).paginate(1,8,False).items


from sqlalchemy import or_

conditions = []
for name in names:
    conditions.append(Detail.sellers.ilike('%{}%'.format(name)))

q = session.query(Detail).filter(
    or_(*conditions)
)



'''
