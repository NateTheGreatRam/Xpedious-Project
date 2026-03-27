"""
components/order_card.py — Renders a single Order card + action buttons.
"""

from __future__ import annotations
import streamlit as st
from core.models import Order, OrderStatus, InvoiceStatus, DeliveryStatus
from core.state import pay_order, advance_order, cancel_order_by_id

STATUS_BADGE = {
    OrderStatus.PENDING:    ("badge-pending",    "● Pending"),
    OrderStatus.PROCESSING: ("badge-processing", "● Processing"),
    OrderStatus.SOURCED:    ("badge-sourced",    "● Sourced"),
    OrderStatus.DISPATCHED: ("badge-dispatched", "● Dispatched"),
    OrderStatus.DELIVERED:  ("badge-delivered",  "● Delivered"),
    OrderStatus.CANCELLED:  ("badge-cancelled",  "✕ Cancelled"),
}
INV_BADGE = {
    InvoiceStatus.UNPAID:  ("badge-unpaid", "● Unpaid"),
    InvoiceStatus.PAID:    ("badge-paid",   "✓ Paid"),
    InvoiceStatus.OVERDUE: ("badge-overdue","⚠ Overdue"),
}
DEL_COLOR = {
    DeliveryStatus.SCHEDULED: "#60a5fa",
    DeliveryStatus.EN_ROUTE:  "#a78bfa",
    DeliveryStatus.DELIVERED: "#34d399",
    DeliveryStatus.FAILED:    "#f87171",
}


def render_order_card(order: Order, index: int) -> None:
    items_html = "".join(
        f'<span class="item-pill"><span class="item-qty">{i.quantity}×</span> {i.name}</span>'
        for i in order.items
    )
    quotes_html = ""
    for q in order.quotes:
        is_best = q is order.selected_quote
        tag  = '<span class="vtag">Best</span>' if is_best else ""
        stk  = "" if q.in_stock else '<span class="vstock-no">Out of stock</span>'
        cls  = "vrow best" if is_best else "vrow"
        quotes_html += f'<div class="{cls}"><span>{q.vendor_name} {stk}</span><div style="display:flex;align-items:center;gap:8px;">{tag}<span class="vprice">${q.unit_price:,.0f}</span></div></div>'

    s_cls, s_txt = STATUS_BADGE.get(order.status, ("badge-pending", order.status.value))
    i_cls, i_txt = INV_BADGE.get(order.invoice.status, ("badge-unpaid", order.invoice.status.value))
    del_color = DEL_COLOR.get(order.delivery.status, "#60a5fa")
    savings_str = f"· ${order.savings:,.0f} saved" if order.savings > 0 else ""

    st.markdown(f"""
    <div class="order-card">
      <div class="order-hdr">
        <div><div class="oid">{order.order_id}</div><div class="ots">{order.created_display} · via {order.source}</div></div>
        <div class="order-meta">
          <span class="badge badge-sms">{order.source}</span>
          <span class="badge {s_cls}">{s_txt}</span>
          <span class="badge {i_cls}">{i_txt}</span>
        </div>
      </div>
      <div class="mod-grid">
        <div class="mod-cell">
          <div class="mod-label"><div class="mod-dot"></div>Ordering</div>
          {items_html}
        </div>
        <div class="mod-cell">
          <div class="mod-label"><div class="mod-dot"></div>Vendor Quotes</div>
          {quotes_html}
        </div>
        <div class="mod-cell" style="border-right:none;">
          <div class="mod-label"><div class="mod-dot"></div>Procurement</div>
          <div class="proc-winner">
            <div class="proc-icon">🏭</div>
            <div>
              <div class="proc-name">{order.selected_quote.vendor_name}</div>
              <div class="proc-sub">${order.selected_quote.unit_price:,.0f} · {order.selected_quote.lead_days}d lead {savings_str}</div>
            </div>
          </div>
        </div>
        <div class="mod-cell mod-cell-no-border-b">
          <div class="mod-label"><div class="mod-dot"></div>Delivery</div>
          <div class="del-status" style="color:{del_color};">{order.delivery.status.value}</div>
          <div class="del-eta">ETA — {order.delivery.eta}</div>
          <div class="del-track">{order.delivery.tracking_id}</div>
        </div>
        <div class="mod-cell mod-cell-no-border-b">
          <div class="mod-label"><div class="mod-dot"></div>Invoice · {order.invoice.invoice_id}</div>
          <div class="inv-amount">${order.invoice.total:,.2f}</div>
          <div class="inv-sub">Subtotal ${order.invoice.subtotal:,.2f} + tax ${order.invoice.tax:,.2f} · Due {order.invoice.due_date}</div>
        </div>
        <div class="mod-cell mod-cell-no-border-b" style="border-right:none;">
          <div class="mod-label"><div class="mod-dot"></div>Notes</div>
          <div style="font-size:11px;color:#2d3d52;">{order.notes if order.notes else '—'}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if order.status not in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
        c1, c2, c3, _ = st.columns([1, 1, 1, 4])
        with c1:
            if st.button("Advance →", key=f"adv_{order.order_id}_{index}"):
                advance_order(order.order_id)
                st.rerun()
        with c2:
            if order.invoice.status == InvoiceStatus.UNPAID:
                if st.button("Mark Paid", key=f"pay_{order.order_id}_{index}"):
                    pay_order(order.order_id)
                    st.rerun()
        with c3:
            if st.button("Cancel", key=f"cancel_{order.order_id}_{index}"):
                cancel_order_by_id(order.order_id)
                st.rerun()

    st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)
