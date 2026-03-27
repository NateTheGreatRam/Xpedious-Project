"""
pages/new_order.py — SMS-style order intake with live parse preview.
"""

import streamlit as st
from core.services import parse_order_text, process_order
from core.state import add_order


def render() -> None:
    st.markdown("""
    <div class="page-hdr">
        <div class="page-eyebrow">📩 Intake</div>
        <div class="page-title">New <em>Order</em></div>
        <div class="page-sub">Enter an order the same way you'd text it — we handle the rest</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Order Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        message = st.text_input("Order message", placeholder="e.g.  3 breakers, 2 panels, 10 wire nuts", key="order_msg")
    with col2:
        source = st.selectbox("Source", ["SMS", "Email", "Phone", "Web", "Manual"], key="order_src")
    notes = st.text_input("Notes (optional)", placeholder="Job site, PO number, contact…", key="order_notes")
    st.markdown('</div>', unsafe_allow_html=True)

    if message:
        items = parse_order_text(message)
        if items:
            pills = "".join(f'<span class="item-pill"><span class="item-qty">{it.quantity}×</span> {it.name}</span>' for it in items)
            st.markdown(f'<div class="input-panel" style="padding:16px 24px;"><div class="mod-label" style="margin-bottom:10px;"><div class="mod-dot"></div>{len(items)} line item{"s" if len(items)!=1 else ""} detected</div>{pills}</div>', unsafe_allow_html=True)

    if st.button("⚡  Process Order", use_container_width=False):
        if not message:
            st.error("Please enter an order message.")
        else:
            with st.spinner("Sourcing quotes from vendors…"):
                order = process_order(text=message, source=source, notes=notes)
            if order is None:
                st.error("Could not parse any items.")
            else:
                add_order(order)
                st.success(f"Order **{order.order_id}** created — best quote: **{order.selected_quote.vendor_name}** at **${order.selected_quote.unit_price:,.2f}**")

    with st.expander("📖  Ordering tips"):
        st.markdown("""
**Format:** `[qty] [item], [qty] [item], ...`

**Examples**
- `3 breakers, 2 panels, 10 wire nuts`
- `5 conduit 1in, 2 junction boxes, 1 disconnect`

Qty can come before or after the item name. Bare names default to qty 1.
        """)
