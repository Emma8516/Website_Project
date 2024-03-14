from flask import Blueprint
from . import db
from .models import Product,Cart,Order
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dbseed')
def dbseed():
    product1 = Product(name='Nylon Hooded Coat', category='Outerwear', description='A durable water-repellent coat. Crisp matte fabric creates a lovely silhouette. This collection is the realization of a dedicated and skilled team of international designers based at our research and development center.', image='coat.png', price=49.90, color='pink/green', size='XS/S/M/L/XL/XXL', material='Nylon')
    
    product2 = Product(name='Sheer Long Sleeve Shirt', category='Tops',description='With a button front, relaxed fit and long sleeves, you can wear this collared shirt so many ways.',image='shirt.png', price=39.90, color='green/blue/black/white',size='XS/S/M/L/XL/XXL',material='Cotton')
    
    product3 = Product(name='Baggy Jacket', category='Outerwear',description='You can`t go wrong with a loose fit and our Baggy Jacket is here to serve.',image='black.png', price=49.90, color='grey/brown/black',size='XS/S/M/L/XL/XXL',material='Cotton')
    
    product4 = Product(name='Mini Bag', category='Accessories',description='Small bag with a shoulder strap and a zip at the top.',image='bag.png', price=59.90, color='green/black',size='Mini',material='Leather')
    
    try:
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.add(product4)
        db.session.commit()
    
    except:
        return 'There was an issue adding the products in dbseed function'
    return 'DATA LOADED'