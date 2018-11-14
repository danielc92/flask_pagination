"""Imports."""
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
import os

# App settings
app=Flask(__name__, static_folder='static')
app.debug=True
app.config['SECRET_KEY']='topsecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SESSION_COOKIE_SECURE']=True
app.config['REMEMBER_COOKIE_SECURE']=True
current_directory=os.getcwd()
database_path='/tmp/superstore'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + current_directory + database_path

'''The old postgres database'''
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345@localhost/flask'

pp=20
db=SQLAlchemy(app)

# Instantiate database model for orders_cleaned table
class Orders(db.Model):

    __tablename__='orders_subset_cleaned'
    
    row_id=db.Column('row_id', db.Integer, primary_key=True)
    order_id=db.Column('order_id', db.Integer)
    order_date=db.Column('order_date', db.Text)
    order_priority=db.Column('order_priority', db.Text)
    order_quantity=db.Column('order_quantity', db.Integer)
    sales=db.Column('sales', db.Float)
    ship_mode=db.Column('ship_mode', db.Text)
    profit=db.Column('profit', db.Float)
    unit_price=db.Column('unit_price', db.Float)
    customer_name=db.Column('customer_name', db.Text)
    province=db.Column('province', db.Text)
    region=db.Column('region', db.Text)
    customer_segment=db.Column('customer_segment', db.Text)
    product_category=db.Column('product_category', db.Text)
    product_sub_category= db.Column('product_sub_category', db.Text)
    product_name=db.Column('product_name', db.Text)
    product_container=db.Column('product_container', db.Text)

# Searches must be above 0 chars and less than 100
# Less than 100 chars reduces overhead when querying wildcard terms.
def stripsearch(item):

    strip=item.strip()
    if len(strip) >0 and len(strip) < 100:
        return True
    else:
        return False

# Splits search into single items for wildcard searching
def create_search_terms(search_result):

    if search_result == '':
        return [search_result]
    else:
        terms=search_result.split(' ')
        terms_stripped=list(map(str.strip, terms))
        terms_final=[term for term in terms_stripped if term != '']
        return terms_final

def return_page_int(pn):
    try:
        int_pn = int(pn)
    except:
        return 1

def return_clean_search(search):
    if len(search) > 100:
        return ''
    else:
        return search

@app.route('/orders/',methods=['POST','GET'])
def home(pn = 1, search = ''):

    pn_raw = request.args.get('pn', '1')
    pn = return_page_int(pn_raw)

    search_raw =request.args.get('search', '')
    search = return_clean_search(search_raw)


    if request.method == 'POST':

        search=request.form['search']
        print('stored search term, redirecting to home')
        return redirect(url_for('home', search=search, pn=1))

    elif request.method == 'GET':
        
        terms = create_search_terms(search)
        search_conditions=[Orders.customer_name.ilike('%{}%'.format(term)) for term in terms]
        orders=Orders.query.filter(and_(*search_conditions)).paginate(page=pn, per_page =pp, error_out=True)
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