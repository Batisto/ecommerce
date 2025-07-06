import pytest

from src.models import Product
from src.models import Category

#Фикстуры
@pytest.fixture
def simple_product():
    return Product(
        name="name",
        description="description",
        price=10.10,
        quantity=1
    )

@pytest.fixture
def category_with_products():
    p1 = Product("p1", "desc1", 100.00, 1)
    p2 = Product("p2", "desc2", 50.00, 2)
    return Category("Категория", "Описание", [p1, p2])


#Тестируем инициализацию Product
def test_product_initialization(simple_product):
    assert simple_product.name == "name"
    assert simple_product.description == "description"
    assert simple_product.price == 10.10
    assert simple_product.quantity == 1


#Тестируем инициализацию Category
def test_category_initialization(category_with_products):
    assert category_with_products.name == "Категория"
    assert category_with_products.description == "Описание"
    assert len(category_with_products.products) == 2


#Тест количества категорий и товаров
def test_class_counters_reset_and_counting():
    # Сбросим счётчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Товар 1", "описание", 100.0, 3)
    p2 = Product("Товар 2", "описание", 200.0, 2)

    c1 = Category("Кат1", "Описание", [p1])
    c2 = Category("Кат2", "Описание", [p2])

    assert Category.category_count == 2
    assert Category.product_count == 5


#Category

def test_add_product_affects_internal_list():
    c = Category("Тест", "Описание", [])
    p = Product("Товар", "Описание", 100, 1)
    c.add_product(p)
    assert "Товар" in c.products  # проверка через геттер


def test_products_property_format():
    p1 = Product("Товар 1", "Описание", 80, 5)
    p2 = Product("Товар 2", "Описание", 150, 2)
    c = Category("Тест", "Описание", [p1, p2])

    result = c.products.split("\n")
    assert result[0] == "Товар 1, 80 руб. Остаток: 5 шт."
    assert result[1] == "Товар 2, 150 руб. Остаток: 2 шт."


def test_add_product_type_check():
    cat = Category("Категория", "Тест", [])
    valid_product = Product("Товар", "Описание", 100.0, 1)
    invalid_product = "Что угодно кроме экземпляра или наследника Product"

    # Корректный случай
    cat.add_product(valid_product)
    assert "Товар" in cat.products

    # Ошибка, если тип неверный
    with pytest.raises(TypeError):
        cat.add_product(invalid_product)


#Product.new_product

def test_new_product_creates_instance():
    data = {
        "name": "Товар",
        "description": "Описание",
        "price": 123.0,
        "quantity": 4
    }
    p = Product.new_product(data, [])
    assert isinstance(p, Product)
    assert p.name == "Товар"
    assert p.price == 123.0
    assert p.quantity == 4


def test_new_product_merges_existing():
    p1 = Product("Телефон", "смартфон", 30000, 5)
    data = {
        "name": "Телефон",
        "description": "смартфон",  # не используется
        "price": 35000,
        "quantity": 2
    }

    p2 = Product.new_product(data, [p1])

    assert p2 is p1
    assert p1.quantity == 7  # 5 + 2
    assert p1.price == 35000  # выбрана большая цена


#Product price property

def test_price_getter_setter_valid():
    p = Product("Наушники", "описание", 2000, 1)
    p.price = 2500
    assert p.price == 2500


def test_price_setter_zero_or_negative(capsys):
    p = Product("Мышь", "описание", 1000, 1)
    p.price = -100
    captured = capsys.readouterr()
    assert "Цена не может быть нулевая или отрицательная" in captured.out
    assert p.price == 1000  # не изменилось


def test_price_setter_confirmation_yes(monkeypatch):
    p = Product("Клавиатура", "описание", 3000, 1)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p.price = 2500
    assert p.price == 2500


def test_price_setter_confirmation_no(monkeypatch, capsys):
    p = Product("Монитор", "описание", 10000, 1)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p.price = 9000

    captured = capsys.readouterr()
    assert "Изменение цены отменено" in captured.out
    assert p.price == 10000  # цена не изменилась