"""
pages/dashboard.py — KPI overview + recent orders.
"""

import streamlit as st
from core.services import compute_dashboard_stats
from core.state import get_orders
from components.order_card import render_order_card


def render() -> None:
    orders = get_orders()
    stats  = compute_dashboard_stats(orders)

    st.markdown("""
    <div class="page-hdr">
        <div class="page-eyebrow">⚡ Overview</div>
        <div class="page-title">Procurement <em>Dashboard</em></div>
        <div class="page-sub">Real-time view of orders, spend, and delivery pipeline</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-icon">📦</div><div class="stat-val accent">{stats['total_orders']}</div><div class="stat-lbl">Total Orders</div></div>
        <div class="stat-card"><div class="stat-icon">💰</div><div class="stat-val">${stats['total_spend']:,.0f}</div><div class="stat-lbl">Total Spend</div></div>
        <div class="stat-card"><div class="stat-icon">📉</div><div class="stat-val green">${stats['total_savings']:,.0f}</div><div class="stat-lbl">Savings Found</div></div>
        <div class="stat-card"><div class="stat-icon">🧾</div><div class="stat-val {'amber' if stats['unpaid_invoices'] > 0 else 'green'}">{stats['unpaid_invoices']}</div><div class="stat-lbl">Unpaid Invoices</div></div>
    </div>
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-icon">✅</div><div class="stat-val green">{stats['delivered']}</div><div class="stat-lbl">Delivered</div></div>
        <div class="stat-card"><div class="stat-icon">⚡</div><div class="stat-val">${stats['avg_order_value']:,.0f}</div><div class="stat-lbl">Avg Order Value</div></div>
        <div class="stat-card"><div class="stat-icon">🏭</div><div class="stat-val accent">{stats['total_orders'] - stats['delivered']}</div><div class="stat-lbl">In Pipeline</div></div>
        <div class="stat-card"><div class="stat-icon">📊</div><div class="stat-val">{'N/A' if not stats['total_spend'] else f"{(stats['total_savings'] / (stats['total_spend'] + stats['total_savings']) * 100):.1f}%"}</div><div class="stat-lbl">Savings Rate</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Recent Orders</div>', unsafe_allow_html=True)
    recent = orders[:5]
    if not recent:
        st.markdown('<div class="order-card"><div class="empty"><div class="empty-icon">⚡</div><div class="empty-title">No orders yet</div><div class="empty-sub">Go to New Order to get started</div></div></div>', unsafe_allow_html=True)
    else:
        for i, order in enumerate(recent):
            render_order_card(order, i)
