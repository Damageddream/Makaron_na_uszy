from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from .menu import Extra, Menu, MenuItem


@dataclass(frozen=True)
class Dish:
    item: MenuItem
    extras: tuple[Extra, ...]

    @property
    def unit_price(self) -> Decimal:
        return sum((extra.price for extra in self.extras), self.item.price)


class DishFactory:
    def __init__(self, menu: Menu) -> None:
        self._menu = menu

    def create(self, name: str, extra_names: Iterable[str] = ()) -> Dish:
        """Tworzy jedną porcję. Każdy dostępny dodatek można wybrać raz."""
        item = self._menu.get_item(name)
        names = tuple(extra_names)
        selected = set(names)
        if len(selected) != len(names):
            raise ValueError("Ten sam dodatek można wybrać tylko raz.")

        extras = tuple(
            extra for extra in item.available_extras if extra.name in selected
        )
        if len(extras) != len(selected):
            raise ValueError(f"Wybrano niedostępny dodatek do dania {name}.")
        return Dish(item, extras)
