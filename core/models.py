"""
core/models.py — Data models and enums for Xpedious.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class OrderStatus(str, Enum):
    PENDING    = "Pending"
    PROCESSING = "Processing"
    SOURCED    = "Sourced"
    DISPATCHED = "Dispatched"
    DELIVERED  = "Delivered"
    CANCELLED  = "Cancelled"


class InvoiceStatus(str, Enum):
    UNPAID  = "Unpaid"
    PAID    = "Paid"
    OVERDUE = "Overdue"


class DeliveryStatus(str, Enum):
    SCHEDULED = "Scheduled"
    EN_ROUTE  = "En Route"
    DELIVERED = "Delivered"
    FAILED    = "Failed"


@dataclass
class LineItem:
    name: str
    quantity: int
    unit: str = "ea"

    @property
    def display(self) -> str:
        return f"{self.quantity}× {self.name}"


@dataclass
class VendorQuote:
    vendor_name: str
    unit_price: float
    lead_days: int
    in_stock: bool = True
    notes: str = ""

    @property
    def total(self) -> float:
        return self.unit_price


@dataclass
class Delivery:
    status: DeliveryStatus = DeliveryStatus.SCHEDULED
    eta: str = "Tomorrow 9AM"
    carrier: str = "Internal Fleet"
    tracking_id: str = field(default_factory=lambda: f"TRK-{uuid.uuid4().hex[:8].upper()}")
    address: str = "Job Site — TBD"


@dataclass
class Invoice:
    subtotal: float
    tax_rate: float = 0.085
    status: InvoiceStatus = InvoiceStatus.UNPAID
    invoice_id: str = field(default_factory=lambda: f"INV-{uuid.uuid4().hex[:6].upper()}")
    due_date: str = ""
    paid_at: Optional[datetime] = None

    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)


@dataclass
class Order:
    items: list[LineItem]
    quotes: list[VendorQuote]
    selected_quote: VendorQuote
    delivery: Delivery
    invoice: Invoice
    order_id: str = field(default_factory=lambda: f"ORD-{uuid.uuid4().hex[:6].upper()}")
    status: OrderStatus = OrderStatus.PROCESSING
    created_at: datetime = field(default_factory=datetime.now)
    source: str = "SMS"
    notes: str = ""

    @property
    def savings(self) -> float:
        if len(self.quotes) < 2:
            return 0.0
        worst = max(q.unit_price for q in self.quotes)
        return round(worst - self.selected_quote.unit_price, 2)

    @property
    def created_display(self) -> str:
        return self.created_at.strftime("%b %d, %Y  %H:%M")
