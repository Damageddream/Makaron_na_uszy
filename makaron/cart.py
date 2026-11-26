from dataclasses import dataclass
from decimal import Decimal

from .dish import Dish


@dataclass(frozen=True)
class CartItem:
    dish: Dish
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return self.dish.unit_price * self.quantity


class Cart:
    def __init__(self) -> None:
        self._quantities: dict[Dish, int] = {}

    def add(self, dish: Dish, quantity: int = 1) -> None:
        if type(quantity) is not int or quantity <= 0:
            raise ValueError(
                "Liczba porcji musi być dodatnią liczbą całkowitą."
            )
        self._quantities[dish] = self._quantities.get(dish, 0) + quantity

    def remove(self, dish: Dish) -> None:
        """Usuwa wszystkie porcje wybranego wariantu dania."""
        del self._quantities[dish]

    @property
    def items(self) -> tuple[CartItem, ...]:
        return tuple(
            CartItem(dish, quantity)
            for dish, quantity in self._quantities.items()
        )

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0.00"))
