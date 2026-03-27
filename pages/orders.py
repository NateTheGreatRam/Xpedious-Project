"""
pages/orders.py — Full order list with search, filter, sort.
"""

import streamlit as st
from core.models import OrderStatus
from core.state import filtered_orders
from components.order_card import render_order_card

STATUS_OPTIONS = ["All"] + [s.value for s in OrderStatus]
SORT_OPTIONS   = ["Newest", "Oldest", "Highest Value", "Most Savings"]


def render() -> None:
    st.markdown("""
    <div class="page-hdr">
        <div class="page-eyebrow">📦 Pipeline</div>
        <div class="page-title">All <em>Orders</em></div>
        <div class="page-sub">Search, filter, and manage every order</div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns([3, 2, 2])
    with f1:
        st.session_state.search_query = st.text_input("Search", value=st.session_state.search_query, placeholder="Order ID, item, vendor…")
    with f2:
        st.session_state.status_filter = st.selectbox("Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(st.session_state.status_filter))
    with f3:
        st.session_state.sort_by = st.selectbox("Sort by", SORT_OPTIONS, index=SORT_OPTIONS.index(st.session_state.sort_by))

    orders = filtered_orders()
    st.markdown(f'<div class="sec-label">Results — {len(orders)} order{"s" if len(orders)!=1 else ""}</div>', unsafe_allow_html=True)

    if not orders:
        st.markdown('<div class="order-card"><div class="empty"><div class="empty-icon">🔍</div><div class="empty-title">No orders match</div><div class="empty-sub">Try adjusting your search or filter</div></div></div>', unsafe_allow_html=True)
    else:
        for i, order in enumerate(orders):
            render_order_card(order, i)
