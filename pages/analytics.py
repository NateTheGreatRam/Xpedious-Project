"""
pages/analytics.py — Vendor breakdown, spend trends, pipeline charts.
"""

from __future__ import annotations
import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
from core.models import OrderStatus
from core.state import get_orders


def render() -> None:
    orders = get_orders()

    st.markdown("""
    <div class="page-hdr">
        <div class="page-eyebrow">📈 Insights</div>
        <div class="page-title">Analytics & <em>Reporting</em></div>
        <div class="page-sub">Vendor performance, spend trends, and pipeline health</div>
    </div>
    """, unsafe_allow_html=True)

    if not orders:
        st.markdown('<div class="order-card"><div class="empty"><div class="empty-icon">📊</div><div class="empty-title">No data yet</div><div class="empty-sub">Create some orders to see analytics</div></div></div>', unsafe_allow_html=True)
        return

    vendor_wins  = Counter(o.selected_quote.vendor_name for o in orders)
    vendor_spend = defaultdict(float)
    for o in orders:
        vendor_spend[o.selected_quote.vendor_name] += o.invoice.total

    df_vendor = pd.DataFrame({
        "Vendor": list(vendor_wins.keys()),
        "Orders Won": list(vendor_wins.values()),
        "Total Spend ($)": [round(vendor_spend[v], 2) for v in vendor_wins.keys()],
    }).sort_values("Orders Won", ascending=False)

    st.markdown('<div class="sec-label">Vendor Performance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Orders Won")
        st.bar_chart(df_vendor.set_index("Vendor")["Orders Won"])
    with c2:
        st.caption("Total Spend ($)")
        st.bar_chart(df_vendor.set_index("Vendor")["Total Spend ($)"])

    st.markdown('<div class="sec-label">Order Status Pipeline</div>', unsafe_allow_html=True)
    status_counts = Counter(o.status.value for o in orders)
    df_status = pd.DataFrame({"Status": [s.value for s in OrderStatus], "Count": [status_counts.get(s.value, 0) for s in OrderStatus]})
    st.bar_chart(df_status.set_index("Status")["Count"])

    st.markdown('<div class="sec-label">Cumulative Spend Over Time</div>', unsafe_allow_html=True)
    sorted_orders = sorted(orders, key=lambda o: o.created_at)
    running = 0.0
    rows = []
    for o in sorted_orders:
        running += o.invoice.total
        rows.append({"Date": o.created_at.strftime("%m/%d %H:%M"), "Cumulative Spend": round(running, 2)})
    if rows:
        st.line_chart(pd.DataFrame(rows).set_index("Date"))

    st.markdown('<div class="sec-label">Top Orders by Savings</div>', unsafe_allow_html=True)
    top = sorted(orders, key=lambda o: o.savings, reverse=True)[:10]
    st.dataframe(pd.DataFrame({
        "Order ID": [o.order_id for o in top],
        "Vendor":   [o.selected_quote.vendor_name for o in top],
        "Savings ($)": [round(o.savings, 2) for o in top],
        "Total ($)":   [round(o.invoice.total, 2) for o in top],
    }), use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-label">Most Ordered Items</div>', unsafe_allow_html=True)
    item_counts: Counter = Counter()
    for o in orders:
        for item in o.items:
            item_counts[item.name] += item.quantity
    if item_counts:
        df_items = pd.DataFrame({"Item": list(item_counts.keys()), "Quantity": list(item_counts.values())}).sort_values("Quantity", ascending=False).head(15)
        st.bar_chart(df_items.set_index("Item")["Quantity"])
