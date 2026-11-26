from decimal import Decimal

import pytest

from makaron import Cart, DishFactory, create_menu
from makaron.menu import Extra, Menu, MenuItem


@pytest.fixture
def factory():
    return DishFactory(create_menu())


def test_menu_lists_the_restaurants_dishes_by_category():
    menu = create_menu()
    expected = {
        "Przystawki": ["Bruschetta", "Caprese"],
        "Makarony": [
            "Spaghetti pomodoro", "Tagliatelle al ragù", "Penne al pesto"
        ],
        "Pizza": ["Margherita", "Diavola"],
        "Desery": ["Tiramisu", "Panna cotta"],
    }

    assert {
        category: [item.name for item in menu.items_in(category)]
        for category in menu.categories
    } == expected


def test_factory_creates_a_plain_dish_at_menu_price(factory):
    dish = factory.create("Tiramisu")

    assert dish.item.name == "Tiramisu"
    assert dish.extras == ()
    assert dish.unit_price == Decimal("19.00")


def test_two_customised_portions_match_the_report_example(factory):
    cart = Cart()
    extras = ["Grana padano", "Suszone pomidory"]
    dish = factory.create("Spaghetti pomodoro", extras)
    cart.add(dish, 2)

    assert [extra.name for extra in dish.extras] == extras
    assert dish.unit_price == Decimal("38.00")
    assert cart.items[0].subtotal == Decimal("76.00")
    assert cart.total == Decimal("76.00")


def test_factory_rejects_an_unknown_dish(factory):
    with pytest.raises(KeyError) as error:
        factory.create("Risotto")
    assert error.value.args == ("Risotto",)


@pytest.mark.parametrize(
    ("name", "extras", "message"),
    [
        ("Tiramisu", ["Mozzarella"], "niedostępny dodatek"),
        ("Diavola", ["Ananas"], "niedostępny dodatek"),
        ("Margherita", ["Oliwki", "Oliwki"], "tylko raz"),
    ],
)
def test_factory_rejects_invalid_extras(factory, name, extras, message):
    with pytest.raises(ValueError, match=message):
        factory.create(name, extras)


def test_reordered_extras_merge_but_plain_pizza_has_its_own_line(factory):
    cart = Cart()
    pizza = factory.create("Margherita", ["Oliwki", "Pieczarki"])
    plain = factory.create("Margherita")
    cart.add(pizza)
    cart.add(plain)
    cart.add(factory.create("Margherita", ["Pieczarki", "Oliwki"]), 2)

    assert [(line.dish, line.quantity) for line in cart.items] == [
        (pizza, 3), (plain, 1)
    ]
    assert cart.total == Decimal("141.00")

    cart.remove(pizza)
    assert [line.dish for line in cart.items] == [plain]
    assert cart.total == Decimal("30.00")
    cart.remove(plain)
    assert cart.items == ()
    assert cart.total == Decimal("0.00")


def test_prices_with_grosz_remain_exact_from_factory_to_cart():
    extra = Extra("Dodatek", Decimal("2.20"))
    item = MenuItem(
        "Danie", "Test", Decimal("1.10"), available_extras=(extra,)
    )
    factory = DishFactory(Menu([item]))
    cart = Cart()
    cart.add(factory.create("Danie", ["Dodatek"]), 3)
    cart.add(factory.create("Danie"))

    assert [line.subtotal for line in cart.items] == [
        Decimal("9.90"), Decimal("1.10")
    ]
    assert isinstance(cart.total, Decimal)
    assert cart.total == Decimal("11.00")


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_invalid_quantity_preserves_the_cart(factory, quantity):
    cart = Cart()
    dish = factory.create("Caprese")
    cart.add(dish, 2)

    with pytest.raises(ValueError, match="Liczba porcji"):
        cart.add(dish, quantity)
    assert cart.items[0].quantity == 2
    assert cart.total == Decimal("48.00")


def test_removing_missing_item_preserves_the_cart(factory):
    cart = Cart()
    plain = factory.create("Diavola")
    cart.add(plain)

    with pytest.raises(KeyError):
        cart.remove(factory.create("Diavola", ["Oliwki"]))
    assert [line.dish for line in cart.items] == [plain]
    assert cart.total == Decimal("36.00")


@pytest.mark.parametrize(
    ("price", "error"),
    [
        (1.1, TypeError),
        (Decimal("-0.01"), ValueError),
        (Decimal("0.001"), ValueError),
        (Decimal("NaN"), ValueError),
    ],
)
def test_invalid_catalog_prices_are_rejected(price, error):
    with pytest.raises(error):
        MenuItem("Danie", "Test", price)
    with pytest.raises(error):
        Extra("Dodatek", price)
