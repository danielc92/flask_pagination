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
pp = 20
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

@app.route('/')
def backtohome():

    return redirect(url_for('home', pn = 1))

@app.route('/orders/<int:pn>', methods = ['POST','GET'])
def home(pn):

    if request.method == 'POST':
        s = request.form['search']
        if len(s)>0:
            return redirect(url_for('search', search = s, pn = 1))
        else:
            return redirect(url_for('backtohome'))
    else:

        orders = Orders.query.paginate(page = pn, per_page = pp, error_out = True)
        return render_template('home.html', orders = orders)



@app.route('/orders/<search>/<int:pn>', methods= ['POST','GET'])
def search(search, pn):
    
    print("Entering search route.")
    
    if request.method == 'POST':
        s = request.form['search']
        orders = Orders.query.filter(Orders.region.contains(s)).paginate(page = 1,
            per_page =pp, error_out = True)
        return redirect(url_for('search', search = s, pn = 1))
    else:
        orders = Orders.query.filter(Orders.region.contains(search)).paginate(page = pn, per_page = pp, error_out = True)
        return render_template('home.html', orders = orders, search_flag = search)











#
'''
QUERYING EXAMPLES
- Model.query.filter(Model.columnName.contains('sub_string'))
- orders = Orders.query.filter(Orders.customer_name.ilike('H%%')).paginate(1,8,False).items


from sqlalchemy import or_

conditions = []
        for name in session['search_term']:
            conditions.append(Orders.customer_name.ilike('%{}%'.format(name)))

        orders = Orders.query.filter(or_(*conditions))\
        .paginate(page = page_num, per_page = config_pp, error_out = True)
        print(orders.total)
        return render_template('home.html', orders = orders, session = session)


'''
