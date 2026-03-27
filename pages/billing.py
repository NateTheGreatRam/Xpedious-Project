"""
pages/billing.py — Invoice management.
"""

import streamlit as st
from core.models import InvoiceStatus
from core.state import get_orders
from components.order_card import render_order_card


def render() -> None:
    orders  = get_orders()
    unpaid  = [o for o in orders if o.invoice.status == InvoiceStatus.UNPAID]
    paid    = [o for o in orders if o.invoice.status == InvoiceStatus.PAID]
    overdue = [o for o in orders if o.invoice.status == InvoiceStatus.OVERDUE]

    total_unpaid = sum(o.invoice.total for o in unpaid)
    total_paid   = sum(o.invoice.total for o in paid)

    st.markdown("""
    <div class="page-hdr">
        <div class="page-eyebrow">💰 Finance</div>
        <div class="page-title">Billing & <em>Invoices</em></div>
        <div class="page-sub">Track and settle outstanding invoices</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-icon">🧾</div><div class="stat-val amber">{len(unpaid)}</div><div class="stat-lbl">Unpaid</div></div>
        <div class="stat-card"><div class="stat-icon">💵</div><div class="stat-val amber">${total_unpaid:,.2f}</div><div class="stat-lbl">Outstanding</div></div>
        <div class="stat-card"><div class="stat-icon">✅</div><div class="stat-val green">{len(paid)}</div><div class="stat-lbl">Paid</div></div>
        <div class="stat-card"><div class="stat-icon">💰</div><div class="stat-val green">${total_paid:,.2f}</div><div class="stat-lbl">Collected</div></div>
    </div>
    """, unsafe_allow_html=True)

    if overdue:
        st.markdown('<div class="sec-label" style="color:#f87171;">Overdue</div>', unsafe_allow_html=True)
        for i, o in enumerate(overdue):
            render_order_card(o, i)

    st.markdown('<div class="sec-label">Unpaid</div>', unsafe_allow_html=True)
    if not unpaid:
        st.markdown('<div class="order-card"><div class="empty"><div class="empty-icon">✅</div><div class="empty-title">All clear</div><div class="empty-sub">No outstanding invoices</div></div></div>', unsafe_allow_html=True)
    else:
        for i, o in enumerate(unpaid):
            render_order_card(o, i)

    if paid:
        st.markdown('<div class="sec-label">Paid</div>', unsafe_allow_html=True)
        for i, o in enumerate(paid):
            render_order_card(o, i)
