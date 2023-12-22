from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    # def __init__(self, name, price, description, quantity):
    #     self.name = name
    #     self.price = price
    #     self.description = description
    #     self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return True if self.quantity >= quantity else False

    def buy(self, quantity: int):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            self.quantity -= quantity
            print(f'Товар {self.name}, сумма: {self.price}, количество {quantity}')
            return self.quantity
        raise ValueError

    def __hash__(self):
        return hash(self.name + self.description)


@dataclass
class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if not product.check_quantity(buy_count):
            print(f"Too much, доступное количество товара - {product.quantity}, запрошено - {buy_count}")
            raise ValueError
        self.products[product] = buy_count

    def add_product_filled_cart(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в существующую корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        for added_cart_product in self.products.keys():
            if product.__eq__(added_cart_product):
                if not product.check_quantity(buy_count):
                    print(f"Too much, доступное количество товара - {product.quantity}, запрошено - {buy_count}")
                    raise ValueError
                self.products[product] += buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        for added_cart_product in self.products.keys():
            if product.__eq__(added_cart_product) is True:
                if remove_count and remove_count <= self.products[product]:
                    self.products[product] -= remove_count
                else:
                    self.products[product] = 0

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        price_info = 0
        for added_cart_product in self.products.keys():
            price_info += float(self.products[added_cart_product] * added_cart_product.price)
        return price_info

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        total_count = 0
        for added_cart_product in self.products.keys():
            added_cart_product.buy(self.products[added_cart_product])
            total_count += self.products[added_cart_product]

        print(f'Заказ оплачен, итоговая сумма: {self.get_total_price()}, итоговое количество товара: {total_count}')
        self.clear()