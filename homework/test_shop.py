"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(-1) is True
        assert product.check_quantity(0) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False
        assert product.check_quantity(1500) is False
        assert product.check_quantity(product.quantity) is True

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.buy(product.quantity) == 0
        assert product.buy(0) == product.quantity

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        try:
            assert product.buy(1500)
        except ValueError:
            print("Too much")


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_add_product(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] > 0
        count_before_add = cart.products[product]
        cart.add_product_filled_cart(product)
        assert cart.products[product] > count_before_add

    def test_cart_add_overhead_product(self, cart, product):
        try:
            assert cart.add_product(product, 1500)
        except ValueError:
            print("Единомоментное наполнение корзины сверх нормы")
        try:
            cart.add_product(product)
            cart.add_product_filled_cart(product, 1500)
        except ValueError:
            print("Постепенное наполнение корзины сверх нормы")

    def test_cart_remove_product_with_count(self, cart, product):
        cart.add_product(product)
        count_before_remove, count_remove = cart.products[product], 1
        cart.remove_product(product, count_remove)
        assert cart.products[product] == count_before_remove-count_remove

    def test_cart_remove_product_without_count(self, cart, product):
        cart.add_product(product)
        cart.remove_product(product)
        assert cart.products[product] == 0

    def test_cart_remove_product_more_than_available(self, cart, product):
        cart.add_product(product)
        cart.remove_product(product, product.quantity+1)
        assert cart.products[product] == 0

    def test_cart_clear(self, cart, product):
        cart.add_product(product)
        cart.clear()
        assert cart.products == {}

    def test_cart_get_total_price(self, cart, product):
        cart.add_product(product)
        excepted_count = float(cart.products[product]*product.price)
        assert cart.get_total_price() == excepted_count

    def test_cart_buy(self, cart, product):
        cart.add_product(product)
        prod_count = product.quantity
        cart.buy()
        assert cart.products == {}
        assert product.quantity < prod_count