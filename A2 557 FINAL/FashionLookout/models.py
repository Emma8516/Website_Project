from . import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    category = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column((db.Float), nullable=False)
    color = db.Column(db.String(60), nullable=False)
    size = db.Column(db.String(60), nullable=False)
    material = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"ID: {self.id}\nCategory: {self.category}\nName: {self.name}\nDescription: {self.description}\n Image: {self.image}\n Price: {self.price}\nColor: {self.color}\nSize: {self.size}\nMaterial: {self.material}"


productdetails = db.Table('productdetails',
    db.Column('cart_id', db.Integer, db.ForeignKey('carts.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('cart_id', 'product_id'))


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    total_product = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    products = db.relationship('Product', secondary=productdetails, backref="carts")

    def __repr__(self):
        return f"Product ID: {self.product_id}\nTotal product: {self.total_product}\nTotal cost: {self.total_cost}\nDate created: {self.date_created}\nLast modified: {self.last_modified}"


orderdetails = db.Table('orderdetails',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id'))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    address = db.Column(db.String(128))
    products = db.relationship("Product", secondary=orderdetails, backref="orders")

    def __repr__(self):
        return f"ID: {self.id}\nProduct: {self.product}\nStatus: {self.status}\nDate: {self.date}\nTotal Cost: {self.total_cost}\nFirst Name: {self.first_name}\nSurname: {self.surname}\nAddress: {self.address}\n"