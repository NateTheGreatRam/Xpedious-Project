"""
core/services.py — All business logic. Zero Streamlit imports.
"""

from __future__ import annotations
import random
import re
from datetime import datetime, timedelta
from typing import Optional

from core.models import (
    DeliveryStatus, Invoice, InvoiceStatus, LineItem,
    Order, OrderStatus, Delivery, VendorQuote,
)

VENDOR_CATALOGUE = {
    "Graybar": {"base_price_range": (80,  420), "lead_days_range": (1, 3)},
    "Rexel":   {"base_price_range": (70,  390), "lead_days_range": (1, 4)},
    "Platt":   {"base_price_range": (90,  450), "lead_days_range": (1, 2)},
    "Wesco":   {"base_price_range": (75,  410), "lead_days_range": (2, 5)},
    "CED":     {"base_price_range": (85,  400), "lead_days_range": (1, 3)},
}

ETA_OPTIONS = ["Today by 5PM", "Tomorrow 9AM", "Tomorrow 2PM", "In 2 days", "In 3 days"]


def parse_order_text(text: str) -> list[LineItem]:
    items: list[LineItem] = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        match = re.match(r"^(\d+)\s*(.+)$", chunk)
        if match:
            qty  = int(match.group(1))
            name = match.group(2).strip().title()
        else:
            match_end = re.match(r"^(.+?)\s+(\d+)$", chunk)
            if match_end:
                name = match_end.group(1).strip().title()
                qty  = int(match_end.group(2))
            else:
                qty  = 1
                name = chunk.title()
        if name:
            items.append(LineItem(name=name, quantity=qty))
    return items


def get_vendor_quotes(items: list[LineItem], num_vendors: int = 5) -> list[VendorQuote]:
    vendors = random.sample(list(VENDOR_CATALOGUE.keys()), k=min(num_vendors, len(VENDOR_CATALOGUE)))
    quotes: list[VendorQuote] = []
    for vendor in vendors:
        cfg = VENDOR_CATALOGUE[vendor]
        lo, hi = cfg["base_price_range"]
        ld_lo, ld_hi = cfg["lead_days_range"]
        total_qty = sum(i.quantity for i in items)
        base  = random.uniform(lo, hi)
        price = round(base * max(1, total_qty * 0.4), 2)
        quotes.append(VendorQuote(
            vendor_name=vendor,
            unit_price=price,
            lead_days=random.randint(ld_lo, ld_hi),
            in_stock=random.random() > 0.15,
        ))
    return sorted(quotes, key=lambda q: q.unit_price)


def select_best_quote(quotes: list[VendorQuote]) -> VendorQuote:
    in_stock = [q for q in quotes if q.in_stock]
    pool = in_stock if in_stock else quotes
    return min(pool, key=lambda q: q.unit_price)


def create_delivery(lead_days: int = 1) -> Delivery:
    eta = random.choice(ETA_OPTIONS[:lead_days + 1] or ETA_OPTIONS)
    return Delivery(status=DeliveryStatus.SCHEDULED, eta=eta)


def create_invoice(selected_quote: VendorQuote) -> Invoice:
    due = (datetime.now() + timedelta(days=30)).strftime("%b %d, %Y")
    return Invoice(subtotal=selected_quote.unit_price, status=InvoiceStatus.UNPAID, due_date=due)


def process_order(text: str, source: str = "SMS", notes: str = "") -> Optional[Order]:
    items = parse_order_text(text)
    if not items:
        return None
    quotes   = get_vendor_quotes(items)
    best     = select_best_quote(quotes)
    delivery = create_delivery(lead_days=best.lead_days)
    invoice  = create_invoice(best)
    return Order(
        items=items, quotes=quotes, selected_quote=best,
        delivery=delivery, invoice=invoice,
        status=OrderStatus.PROCESSING, source=source, notes=notes,
    )


def mark_paid(order: Order) -> Order:
    order.invoice.status  = InvoiceStatus.PAID
    order.invoice.paid_at = datetime.now()
    return order


def advance_status(order: Order) -> Order:
    transitions = {
        OrderStatus.PENDING:    OrderStatus.PROCESSING,
        OrderStatus.PROCESSING: OrderStatus.SOURCED,
        OrderStatus.SOURCED:    OrderStatus.DISPATCHED,
        OrderStatus.DISPATCHED: OrderStatus.DELIVERED,
    }
    if order.status in transitions:
        order.status = transitions[order.status]
        if order.status == OrderStatus.DISPATCHED:
            order.delivery.status = DeliveryStatus.EN_ROUTE
        elif order.status == OrderStatus.DELIVERED:
            order.delivery.status = DeliveryStatus.DELIVERED
    return order


def cancel_order(order: Order) -> Order:
    order.status = OrderStatus.CANCELLED
    return order


def compute_dashboard_stats(orders: list[Order]) -> dict:
    if not orders:
        return {"total_orders": 0, "total_spend": 0.0, "total_savings": 0.0,
                "unpaid_invoices": 0, "avg_order_value": 0.0, "delivered": 0}
    total_spend   = sum(o.invoice.total for o in orders)
    total_savings = sum(o.savings for o in orders)
    unpaid        = sum(1 for o in orders if o.invoice.status == InvoiceStatus.UNPAID)
    delivered     = sum(1 for o in orders if o.status == OrderStatus.DELIVERED)
    return {
        "total_orders":    len(orders),
        "total_spend":     round(total_spend, 2),
        "total_savings":   round(total_savings, 2),
        "unpaid_invoices": unpaid,
        "avg_order_value": round(total_spend / len(orders), 2),
        "delivered":       delivered,
    }
