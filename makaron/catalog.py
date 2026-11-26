from decimal import Decimal

from .menu import Extra, Menu, MenuItem


def create_menu() -> Menu:
    extras = (
        Extra("Grana padano", Decimal("4.00")),
        Extra("Mozzarella", Decimal("5.00")),
        Extra("Pieczarki", Decimal("4.00")),
        Extra("Suszone pomidory", Decimal("5.00")),
        Extra("Oliwki", Decimal("3.00")),
    )
    return Menu([
        MenuItem(
            "Bruschetta", "Przystawki", Decimal("18.00"),
            "Grzanki z pomidorami, czosnkiem i bazylią",
        ),
        MenuItem(
            "Caprese", "Przystawki", Decimal("24.00"),
            "Pomidory, mozzarella, bazylia i oliwa",
        ),
        MenuItem(
            "Spaghetti pomodoro", "Makarony", Decimal("29.00"),
            "Sos pomidorowy i bazylia", extras,
        ),
        MenuItem(
            "Tagliatelle al ragù", "Makarony", Decimal("36.00"),
            "Sos pomidorowy z mięsem wołowym", extras,
        ),
        MenuItem(
            "Penne al pesto", "Makarony", Decimal("32.00"),
            "Pesto bazyliowe, grana padano i pomidorki", extras,
        ),
        MenuItem(
            "Margherita", "Pizza", Decimal("30.00"),
            "Pizza 30 cm z sosem pomidorowym, mozzarellą i bazylią", extras,
        ),
        MenuItem(
            "Diavola", "Pizza", Decimal("36.00"),
            "Pizza 30 cm z sosem pomidorowym, mozzarellą i pikantnym salami",
            extras,
        ),
        MenuItem(
            "Tiramisu", "Desery", Decimal("19.00"),
            "Biszkopty, kawa, krem mascarpone i kakao",
        ),
        MenuItem(
            "Panna cotta", "Desery", Decimal("17.00"),
            "Deser śmietankowy z sosem owocowym",
        ),
    ])
