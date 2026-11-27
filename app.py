from decimal import Decimal
import streamlit as st

from makaron import Cart, DishFactory, create_menu
from makaron.dish import Dish


def _format_pln(amount: Decimal) -> str:
    return f"{amount:.2f} zł"


def _init_state() -> None:
    if "menu" not in st.session_state:
        st.session_state.menu = create_menu()
    if "factory" not in st.session_state:
        st.session_state.factory = DishFactory(st.session_state.menu)
    if "cart" not in st.session_state:
        st.session_state.cart = Cart()


def _render_menu_column() -> None:
    menu = st.session_state.menu
    factory: DishFactory = st.session_state.factory
    cart: Cart = st.session_state.cart

    st.subheader("Menu")
    categories = menu.categories
    selected_category = st.selectbox("Kategoria", categories)

    dishes_in_category = menu.items_in(selected_category)
    dish_names = [item.name for item in dishes_in_category]
    selected_dish_name = st.selectbox("Danie", dish_names)

    menu_item = menu.get_item(selected_dish_name)
    if menu_item.description:
        st.caption(menu_item.description)

    selected_extra_names: list[str] = []
    if menu_item.available_extras:
        st.write("Dodatki:")
        for extra in menu_item.available_extras:
            checked = st.checkbox(
                f"{extra.name} (+{_format_pln(extra.price)})",
                key=f"extra_{menu_item.name}_{extra.name}",
            )
            if checked:
                selected_extra_names.append(extra.name)

    quantity = st.number_input(
        "Liczba porcji",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )

    preview_dish = factory.create(selected_dish_name, selected_extra_names)
    preview_total = preview_dish.unit_price * int(quantity)
    st.write(
        f"Cena jednostkowa: **{_format_pln(preview_dish.unit_price)}** | "
        f"Razem za pozycję: **{_format_pln(preview_total)}**"
    )

    if st.button("Dodaj do koszyka", type="primary"):
        dish = factory.create(selected_dish_name, selected_extra_names)
        cart.add(dish, int(quantity))
        st.success(f"Dodano do koszyka: {dish.item.name} (x{int(quantity)})")
        st.rerun()


def _render_cart_item(dish: Dish, quantity: int, index: int) -> None:
    cart: Cart = st.session_state.cart
    extras_label = (
        ", ".join(extra.name for extra in dish.extras)
        if dish.extras
        else "brak dodatków"
    )
    subtotal = dish.unit_price * quantity

    col_info, col_price, col_action = st.columns([5, 2, 2])
    with col_info:
        st.markdown(f"**{dish.item.name}** × {quantity}")
        st.caption(f"Dodatki: {extras_label} ({_format_pln(dish.unit_price)} / szt.)")
    with col_price:
        st.write(f"**{_format_pln(subtotal)}**")
    with col_action:
        if st.button("Usuń", key=f"remove_item_{index}"):
            cart.remove(dish)
            st.rerun()


def _render_cart_column() -> None:
    cart: Cart = st.session_state.cart
    st.subheader("Koszyk")

    items = cart.items
    if not items:
        st.info("Koszyk jest pusty. Wybierz danie z menu po lewej.")
        return

    for idx, item in enumerate(items):
        _render_cart_item(item.dish, item.quantity, idx)
        st.divider()

    st.metric("Łączna wartość zamówienia", _format_pln(cart.total))


def main() -> None:
    st.set_page_config(
        page_title="Makaron na uszy — Kiosk",
        layout="wide",
    )
    st.title("Makaron na uszy")
    st.caption("Samoobsługowy kiosk zamówień")

    _init_state()

    left_col, right_col = st.columns([3, 2], gap="large")
    with left_col:
        _render_menu_column()
    with right_col:
        _render_cart_column()


if __name__ == "__main__":
    main()
