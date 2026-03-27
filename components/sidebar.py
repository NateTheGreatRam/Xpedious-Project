"""
components/sidebar.py
"""

import streamlit as st
from core.models import InvoiceStatus, OrderStatus
from core.state import get_orders, set_page, get_page


def render_sidebar() -> None:
    orders   = get_orders()
    n_total  = len(orders)
    n_unpaid = sum(1 for o in orders if o.invoice.status == InvoiceStatus.UNPAID)
    n_active = sum(1 for o in orders if o.status not in (OrderStatus.DELIVERED, OrderStatus.CANCELLED))
    total_spend = sum(o.invoice.total for o in orders)
    total_save  = sum(o.savings for o in orders)

    with st.sidebar:
        st.markdown("""
        <div class="sb-logo">
            <div class="sb-logo-mark">X<em>pedious</em></div>
            <div class="sb-tagline">Electrical Procurement Platform</div>
        </div>
        <div class="sb-section">Navigation</div>
        """, unsafe_allow_html=True)

        pages = [
            ("dashboard", "📊  Dashboard"),
            ("new_order", "📩  New Order"),
            ("orders",    "📦  All Orders"),
            ("billing",   "💰  Billing"),
            ("analytics", "📈  Analytics"),
        ]
        for pid, label in pages:
            if st.button(label, key=f"nav_{pid}", use_container_width=True):
                set_page(pid)
                st.rerun()

        st.markdown(f"""
        <div class="sb-section" style="margin-top:20px;">System</div>
        <div class="sb-stats">
            <div class="sb-stat-row"><span class="sb-stat-label">Total Spend</span><span class="sb-stat-val">${total_spend:,.0f}</span></div>
            <div class="sb-stat-row"><span class="sb-stat-label">Total Savings</span><span class="sb-stat-val">${total_save:,.0f}</span></div>
            <div class="sb-stat-row"><span class="sb-stat-label">Orders</span><span class="sb-stat-val">{n_total}</span></div>
            <div class="sb-stat-row"><span class="sb-stat-label">Unpaid</span><span class="sb-stat-val">{n_unpaid}</span></div>
        </div>
        """, unsafe_allow_html=True)
