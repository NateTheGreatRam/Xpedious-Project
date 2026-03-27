"""
core/state.py — Centralised session-state management.
"""

from __future__ import annotations
import streamlit as st
from core.models import Order, InvoiceStatus, OrderStatus
from core.services import mark_paid, advance_status, cancel_order


def init_state() -> None:
    defaults = {
        "orders":        [],
        "active_page":   "dashboard",
        "search_query":  "",
        "status_filter": "All",
        "sort_by":       "Newest",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def add_order(order: Order) -> None:
    st.session_state.orders.insert(0, order)


def get_orders() -> list[Order]:
    return st.session_state.orders


def get_order_by_id(order_id: str) -> Order | None:
    return next((o for o in st.session_state.orders if o.order_id == order_id), None)


def _replace_order(updated: Order) -> None:
    orders = st.session_state.orders
    for i, o in enumerate(orders):
        if o.order_id == updated.order_id:
            orders[i] = updated
            return


def pay_order(order_id: str) -> None:
    order = get_order_by_id(order_id)
    if order:
        _replace_order(mark_paid(order))


def advance_order(order_id: str) -> None:
    order = get_order_by_id(order_id)
    if order:
        _replace_order(advance_status(order))


def cancel_order_by_id(order_id: str) -> None:
    order = get_order_by_id(order_id)
    if order:
        _replace_order(cancel_order(order))


def filtered_orders() -> list[Order]:
    orders = get_orders()
    query  = st.session_state.search_query.lower().strip()
    status = st.session_state.status_filter
    sort   = st.session_state.sort_by

    if query:
        orders = [o for o in orders if
                  query in o.order_id.lower() or
                  any(query in i.name.lower() for i in o.items) or
                  query in o.selected_quote.vendor_name.lower()]

    if status != "All":
        orders = [o for o in orders if o.status.value == status]

    if sort == "Newest":
        orders = sorted(orders, key=lambda o: o.created_at, reverse=True)
    elif sort == "Oldest":
        orders = sorted(orders, key=lambda o: o.created_at)
    elif sort == "Highest Value":
        orders = sorted(orders, key=lambda o: o.invoice.total, reverse=True)
    elif sort == "Most Savings":
        orders = sorted(orders, key=lambda o: o.savings, reverse=True)

    return orders


def set_page(page: str) -> None:
    st.session_state.active_page = page


def get_page() -> str:
    return st.session_state.active_page
