import pytest

from src.models import Product
from src.models import Category

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