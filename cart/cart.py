CART_SESSION_ID = 'cart'
DISCOUNT_SESSION_ID = 'discount'
from stuff.models import Product,Color


class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

        # discount = self.session.get(DISCOUNT_SESSION_ID)
        # if not discount:
        #     discount = self.session[DISCOUNT_SESSION_ID] = {}
        # self.discount = discount

    def add(self,product,quantity=1,color="custom"):
        product_cart_id = f"{product.id}-{color}"

        if(color == None):
            color = 'custom'
        

        if product_cart_id not in self.cart:
            self.cart[product_cart_id] = {'quantity':0,'price':str(product.discounted_price_int),'color':color,
            'color_per':Color.objects.get(en=color).name,'id':product_cart_id}
        self.cart[product_cart_id]['quantity'] += quantity
        
        
        self.save()

    def remove(self,product_cart_id):
        if product_cart_id in self.cart:
            quantity = int(self.cart[product_cart_id]['quantity'])
            del self.cart[product_cart_id]
            self.save()
            return quantity


    
    # def apply_coupon(self,coupon):
    #     coupon_str = str(coupon.code)

    #     if coupon_str not in self.discount:
    #         self.discount[coupon_str] = {'active':1,'discount':str(coupon.discount)}
    #     self.save()

    # def unactive_coupon(self,coupon):
    #     coupon_str = str(coupon.code)

    #     if coupon_str in self.discount:
    #         self.discount[coupon_str] = {'active':0,'discount':str(coupon.discount)}
        
    #     self.save()



    def save(self):
        self.session.modified = True

    def __iter__(self):
        cart = self.cart.copy()
        for key in cart:
            cart[key]['product'] = Product.objects.get(id=int(key.split('-')[0]))

        for item in cart.values():
            item['total_price'] = int(item['price'])*item['quantity']
            yield item


    def get_total_price(self):
        total = sum(int(item['price'])*item['quantity'] for item in self.cart.values())
        # if self.discount:
        #     discount_price = (self.discount/100)* total
        #     return total - discount_price
        return total
        
    def get_total_count(self):
        return sum(item['quantity'] for item in self.cart.values())    
    
    def get_count(self):
        return sum(1 for item in self.cart.values())  


    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
