# from decimal import Decimal
# from django.shortcuts import get_object_or_404
# from main.models import Product


# class Cart:
#     def __init__(self, request):
#         # Використовуємо сесію користувача для збереження корзини
#         self.session = request.session
#         cart = self.session.get('cart')

#         # Якщо корзини ще нема — створюємо нову порожню
#         if not cart:
#             cart = self.session['cart'] = {}

#         self.cart = cart

#     def add(self, product, size, quantity=1, override_quantity=False):
#         # Створюємо унікальний ключ для товару з урахуванням його розміру
#         product_id = str(product.id)
#         size_name = str(size)
#         cart_key = f"{product_id}_{size_name}"

#         # Якщо товару ще нема в корзині — додаємо його з нульовою кількістю
#         if cart_key not in self.cart:
#             self.cart[cart_key] = {
#                 'quantity': 0,
#                 'price': str(product.price),  # Ціна зберігається як строка (для JSON-сумісності)
#                 'product_id': product_id,
#                 'size': size_name,
#             }

#         # Якщо передано override_quantity — замінюємо кількість
#         if override_quantity:
#             self.cart[cart_key]['quantity'] = override_quantity
#         else:
#             # Інакше просто додаємо кількість
#             self.cart[cart_key]['quantity'] += quantity

#         self.save()

#     def save(self):
#         # Позначаємо, що сесія була змінена
#         self.session.modified = True

#     def remove(self, product, size):
#         # Видаляємо товар з корзини за ключем
#         product_id = str(product.id)
#         size_name = str(size)
#         cart_key = f"{product_id}_{size_name}"

#         if cart_key in self.cart:
#             del self.cart[cart_key]
#             self.save()

#     def update(self, product, size, quantity):
#         # Якщо кількість < 1 — видаляємо товар
#         if quantity < 1:
#             self.remove(product, size)
#         else:
#             # Інакше просто оновлюємо кількість
#             self.add(product, size, quantity, override_quantity=True)

#     def __iter__(self):
#         # Ітеруємося по корзині, підвантажуючи повні дані про товари
#         product_ids = [item['product_id'] for item in self.cart.values()]
#         products = Product.objects.filter(id__in=product_ids)  # <-- тут було id_in (помилка), треба id__in
#         cart = self.cart.copy()

#         for product in products:
#             for cart_key, cart_item in cart.items():
#                 if cart_item['product_id'] == str(product.id):
#                     # Додаємо в об’єкт корзини сам продукт та підраховуємо суму
#                     cart_item['product'] = product
#                     cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
#                     yield cart_item

#     def __len__(self):
#         # Рахуємо загальну кількість товарів у корзині
#         return sum(item['quantity'] for item in self.cart.values())

#     def get_total_price(self):
#         # Повертаємо сумарну ціну всіх товарів у корзині
#         total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
#         return total

#     def clear(self):
#         # Повністю очищаємо корзину
#         del self.session['cart']
#         self.save()

#     def get_cart_items(self):
#         # Формуємо список товарів у корзині для відображення у шаблоні
#         items = []
#         for item in self:
#             items.append({
#                 'product': item['product'],
#                 'quantity': item['quantity'],
#                 'size': item['size'],
#                 'price': Decimal(item['price']),
#                 'total_price': item['total_price'],
#                 'cart_key': f"{item['product_id']}_{item['size']}",
#             })
#         return items
