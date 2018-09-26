#imports
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# app settings
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/flask'
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
def home():
    return redirect(url_for('index', page_num = 1))

# order route shows orders paginated
@app.route('/order/<int:page_num>')

def index(page_num):

    orders = Orders.query.\
    order_by(Orders.order_id).\
    paginate(page = page_num, per_page = config_pp, error_out = True)

    return render_template('index.html', orders = orders)

# search route?




#
'''
QUERYING EXAMPLES
- Model.query.filter(Model.columnName.contains('sub_string'))
- orders = Orders.query.filter(Orders.customer_name.ilike('H%%')).paginate(1,8,False).items
'''