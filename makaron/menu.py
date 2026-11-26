from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal


def _validate_price(price: Decimal) -> None:
    if not isinstance(price, Decimal):
        raise TypeError("Cena musi być typu Decimal.")
    if not price.is_finite() or price < 0:
        raise ValueError("Cena musi być skończona i nieujemna.")
    if price != price.quantize(Decimal("0.01")):
        raise ValueError("Cena musi być podana z dokładnością do grosza.")


@dataclass(frozen=True)
class Extra:
    name: str
    price: Decimal

    def __post_init__(self) -> None:
        _validate_price(self.price)


@dataclass(frozen=True)
class MenuItem:
    name: str
    category: str
    price: Decimal
    description: str = ""
    available_extras: tuple[Extra, ...] = ()

    def __post_init__(self) -> None:
        _validate_price(self.price)
        names = [extra.name for extra in self.available_extras]
        if len(names) != len(set(names)):
            raise ValueError("Nazwy dodatków danego dania muszą być unikalne.")


class Menu:
    def __init__(self, items: Iterable[MenuItem]) -> None:
        self._items: dict[str, MenuItem] = {}
        for item in items:
            if item.name in self._items:
                raise ValueError(f"Powtórzona nazwa dania: {item.name}")
            self._items[item.name] = item

    @property
    def categories(self) -> tuple[str, ...]:
        categories = (item.category for item in self._items.values())
        return tuple(dict.fromkeys(categories))

    def items_in(self, category: str) -> tuple[MenuItem, ...]:
        return tuple(
            item for item in self._items.values() if item.category == category
        )

    def get_item(self, name: str) -> MenuItem:
        return self._items[name]
