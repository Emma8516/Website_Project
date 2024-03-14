from flask import Blueprint, render_template,  request, session, flash,url_for,redirect,jsonify
from .models import Product, Cart, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = db.session.scalars(db.select(Product).order_by(Product.id)).all()
    #title = "Fashion Lookout Home"
    return render_template('ecommerce.html', products=products)


#@main_bp.route('/products/<int:product_id>')
#def products(product_id):
    #products = db.session.scalars(db.select(Product).where(Product.product_id==product_id)).all()
    products = Product.query.order_by(Product.id).all()
    return render_template('products.html', products=products)

#@main_bp.route('/products', methods=['GET'])
#def all_products():
    # 假設你的資料庫模型名稱為Product
    products = Product.query.all() 
    return render_template('products.html', products=products)

@main_bp.route('/products/', defaults={'product_id': None})
@main_bp.route('/products/<int:product_id>')
def products(product_id):
    
    if product_id is None:
        # get all products
        products = Product.query.all()
    else:
        products = Product.query.filter(Product.id == product_id)
   
    #productDetails = db.session.scalar(db.select(Product).where(Product.id==product_id))
    return render_template('products.html', products=products)


# ****** SEARCH ROUTE *******
@main_bp.route('/products')
def search():
 search = request.args.get('search')
 search = '%{}%'.format(search)
 products = Product.query.filter(Product.description.like(search)).all()
 return render_template('products.html', products=products)


# Referred to as "Basket" to the user
@main_bp.route('/shoppingbasket', methods=['POST', 'GET'])
def shoppingbasket():
    title = "Fashion Lookout Shopping Basket"
    product_id = request.values.get('product_id')
    print(f'Values: {product_id}')

 # retrieve order if there is one
    if 'order_id' in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id/session is stale
    else:
            # there is no order
            order = None
    
    
    # create new order if needed
    if order is None:
        order = Order(status=False, date=datetime.now(), total_cost=0, first_name='', surname='', email='', phone='', address='')
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Failed trying to create a new order!')
            order = None
    
    # calculate total price
    total_cost = 0
    if order is not None:
        for product in order.products:
            total_cost += product.price
    
# are we adding an item?
    if product_id is not None and order is not None:
        product = db.session.scalar(db.select(Product).where(Product.id==product_id))
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                flash('There was an issue adding the item to your basket',category='danger')
            return redirect(url_for('main.shoppingbasket'))
        
    return render_template('shoppingbasket.html', order=order, total_cost=total_cost, title=title)


# Delete specific basket items
# Note this route cannot accept GET requests now
@main_bp.route('/deletebasketitem', methods=['POST'])
def deletebasketitem():
    id = request.form['id']
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        product_to_delete = db.session.scalar(db.select(Product).where(Product.id==id))
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.shoppingbasket'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.shoppingbasket'))

# Scrap basket
@main_bp.route('/deletebasket')
def deletebasket():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

# FINAL CHECKOUT ROUTE Complete the order
@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.date = datetime.now()
            order.first_name = form.first_name.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            order.address = form.address.data
            total_cost = 0
            for product in order.products:
                total_cost += product.price
            order.total_cost = total_cost
            
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for your purchase! Order is being processed. We will notify you when it is shipped.')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

