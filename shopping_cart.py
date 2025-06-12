import uuid
class User:
    def __init__(self,name,email,userId):
        self.userId = userId
        self.name=name
        self.email = email
        self.Cart = Cart(self)
        self.Wishlist = Wishlist(self)
    def addToCart(self,product,quantity):
        self.Cart.addItem(product,quantity)
    def checkout(self):
        return self.Cart.checkout()
    def addReview(self,rating,product,comment):
        review = Review(self,product,rating,comment,user)
        product.addReview(review)
class Product:
    def __init__(self,productName,stock,cost,productId):
        self.productId = productId
        self.productName = productName
        self.stock = stock
        self.cost = cost
        self.reviews=[]
    def isAvailable(self,quantity):
        return self.stock>=quantity
    def reduceStock(self,quantity):
        self.stock-=quantity
    def addReview(self,review):
        self.reviews.append(review)
class Order:
    def __init__(self,user):
        self.orderId = str(uuid.uuid4())
        self.user = user
        self.items=[]
        self.status = 'PENDING'
        self.total=0
        self.payment=None
    def add_item(self,product,quantity):
        self.items.append(OrderItem(product,quantity))
        self.total+=(product.cost*quantity)
    def makePayment(self,method):
        self.status='PAID'
        payment = Payment(self.total,method)
class OrderItem:
    def __init__(self,product,quantity):
        self.product=product
        self.quantity =quantity
class Payment:
    def __init__(self,amount,method):
        self.amount = amount
        self.method = method
        self.paymentId = str(uuid.uuid4())
        self.completed='COMPLETED'
class CartItem:
    def __init__(self,product,quantity):
        self.product=product
        self.quantity =quantity
class Cart:
    def __init__(self,user):
        self.user=user
        self.items=[]
    def addItem(self,product,quantity):
        self.items.append(CartItem(product,quantity))
    def checkout(self):
        order = Order(self.user)
        for item in self.items:
            if item.product.isAvailable(item.quantity):
                item.product.reduceStock(item.quantity)
                order.add_item(item.product,item.quantity)
        self.items.clear()
        return order
class OrderItem:
    def __init__(self,product,quantity):
        self.product=product
        self.quantity =quantity
class Wishlist:
    def __init__(self,user):
        self.user=user
        self.products = set()
    def addProduct(self,product):
        self.products.add(product)
    def removeProduct(self,product):
        self.products.discard(product)
class Review:
    def __init__(self,user,rating,comment,product):
        self.user=user
        self.rating=rating
        self.comment=comment
        self.reviewId = str(uuid.uuid4())
        self.createdAt = dateTime.now()
        self.product=product
user1 = User('Vishali','rvishali1610@gmail.com','123')
dressProduct = Product('dress',4,100,'123p')
user1.addToCart(dressProduct,2)
user1.checkout()
print("User checked out")
                
