E-commerce Products and Categories
Простой учебный проект на Python с реализацией классов Product и Category.

Структура проекта
.
├── src/
│   └── models.py
├── tests/
│   └── test_models.py
├── pyproject.toml
└── README.md

Возможности:
- Класс Product описывает товар.
- Класс Category содержит список товаров и считает общее количество.
- Проверка типов при добавлении товаров в категорию.
- Подсчет количества всех созданных товаров и категорий.
- Тесты с использованием pytest.

Установка и запуск тестов
poetry install
poetry run pytest