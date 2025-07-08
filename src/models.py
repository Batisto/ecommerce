from typing import List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, Product):
            return self.__price * self.quantity + other.price * other.quantity
        return NotImplemented

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не может быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            user_input = input(
                f"Вы действительно хотите снизить цену с {self.__price} до {new_price}? (y/n)"
            )
            if user_input.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price


    @classmethod
    def new_product(cls, data: dict, existing_product: List["Product"]) -> "Product":
        for product in existing_product:
            if product.name == data["name"]:
                product.quantity += data["quantity"]
                if data["price"] > product.price:
                    product.price = data["price"]
                return product

        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = []

        for product in products:
            self.add_product(product)

        Category.category_count += 1

    def __str__(self):
        return f"{self.name}, количество продуктов: {sum(product.quantity for product in self.__products)} шт"

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только экземпляры Product или его наследников")
        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> str:
        return '\n'.join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )

product1 = Product("p1", "d1", 10, 2)
product2 = Product("p2", "d2", 20, 3)

print(product1 + product2)