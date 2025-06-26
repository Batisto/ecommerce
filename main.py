from src.models import Product, Category


if __name__ == "__main__":
    p1 = Product("Книга", "Грокаем алгоритмы", 1999.99, 2)
    p2 = Product("Книга", "Финансист", 799.99, 3)

    c1 = Category("Книги", "Литература", [p1, p2])

    print(f"Категорий: {Category.category_count}")
    print(f"Товаров: {Category.product_count}")

