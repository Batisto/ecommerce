import pytest
from src.models import Product, Category, Smartphone, LawnGrass

# ФИКСТУРЫ

@pytest.fixture
def simple_product():
    return Product(name="name", description="description", price=10.10, quantity=1)


@pytest.fixture
def category_with_products():
    p1 = Product("p1", "desc1", 100.00, 1)
    p2 = Product("p2", "desc2", 50.00, 2)
    return Category("Категория", "Описание", [p1, p2])


# ТЕСТЫ ДЛЯ КЛАССА PRODUCT

def test_product_initialization(simple_product):
    assert simple_product.name == "name"
    assert simple_product.description == "description"
    assert simple_product.price == 10.10
    assert simple_product.quantity == 1


def test_product_str():
    p = Product("Товар", "Описание", 100, 5)
    assert str(p) == "Товар, 100 руб. Остаток: 5 шт."


def test_product_addition():
    p1 = Product("Товар1", "Описание", 100, 2)  # 200
    p2 = Product("Товар2", "Описание", 150, 1)  # 150
    assert p1 + p2 == 350


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
        "description": "смартфон",
        "price": 35000,
        "quantity": 2
    }
    p2 = Product.new_product(data, [p1])
    assert p2 is p1
    assert p1.quantity == 7
    assert p1.price == 35000


def test_price_getter_setter_valid():
    p = Product("Наушники", "описание", 2000, 1)
    p.price = 2500
    assert p.price == 2500


def test_price_setter_zero_or_negative(capsys):
    p = Product("Мышь", "описание", 1000, 1)
    p.price = -100
    captured = capsys.readouterr()
    assert "Цена не может быть нулевая или отрицательная" in captured.out
    assert p.price == 1000


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
    assert p.price == 10000


# ТЕСТЫ ДЛЯ КЛАССА CATEGORY

def test_category_initialization(category_with_products):
    assert category_with_products.name == "Категория"
    assert category_with_products.description == "Описание"
    # 1 товар + 2 товара = 3 всего
    assert "3 шт" in str(category_with_products)


def test_category_str_total_quantity():
    p1 = Product("Товар 1", "Описание", 80, 5)
    p2 = Product("Товар 2", "Описание", 150, 2)
    c = Category("Тест", "Описание", [p1, p2])
    assert str(c) == "Тест, количество продуктов: 7 шт"


def test_add_product_affects_internal_list():
    c = Category("Тест", "Описание", [])
    p = Product("Товар", "Описание", 100, 1)
    c.add_product(p)
    assert "Товар" in c.products


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
    invalid_product = "строка, а не Product"

    cat.add_product(valid_product)
    assert "Товар" in cat.products

    with pytest.raises(TypeError):
        cat.add_product(invalid_product)


def test_class_counters_reset_and_counting():
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Товар 1", "описание", 100.0, 3)
    p2 = Product("Товар 2", "описание", 200.0, 2)

    c1 = Category("Кат1", "Описание", [p1])
    c2 = Category("Кат2", "Описание", [p2])

    assert Category.category_count == 2
    assert Category.product_count == 5


# ТЕСТЫ НАСЛЕДНИКОВ Product

def test_smartphone_inherits_product():
    phone = Smartphone(
        efficiency=95,
        model="iPhone 15",
        memory="256GB",
        color="Black",
        name="Смартфон",
        description="Флагман",
        price=99999,
        quantity=5
    )
    assert isinstance(phone, Product)
    assert phone.name == "Смартфон"
    assert phone.model == "iPhone 15"
    assert phone.color == "Black"
    assert phone.price == 99999


def test_lawngrass_inherits_product():
    grass = LawnGrass(
        name="Газон",
        description="Для дачи",
        price=199.99,
        quantity=10,
        country="Россия",
        germination_period="7 дней",
        color="Зелёный"
    )
    assert isinstance(grass, Product)
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.price == 199.99


def test_adding_smartphone_to_category():
    cat = Category("Гаджеты", "Смартфоны", [])
    phone = Smartphone(95, "Samsung", "128GB", "Blue", "Galaxy", "Описание", 50000, 2)
    cat.add_product(phone)
    assert "Galaxy" in cat.products


def test_adding_lawngrass_to_category():
    cat = Category("Растения", "Газонная трава", [])
    grass = LawnGrass("Газон", "Описание", 300, 4, "Германия", "5 дней", "Зелёный")
    cat.add_product(grass)
    assert "Газон" in cat.products


@pytest.fixture
def sample_data():
    return {
        "name": "TestProduct",
        "description": "A test product",
        "price": 100.0,
        "quantity": 10
    }

@pytest.fixture
def existing_product():
    return [
        Product(name="TestProduct", description="Old product", price=80.0, quantity=5)
    ]

def test_new_product_existing(sample_data, existing_product):
    product = Product.new_product(sample_data, existing_product)
    assert product.quantity == 15
    assert product.price == 100.0

def test_new_product_new_instance(sample_data):
    result = Product.new_product(sample_data, [])
    assert isinstance(result, Product)
    assert result.name == "TestProduct"
    assert result.description == "A test product"
    assert result.price == 100.0
    assert result.quantity == 10
