import streamlit as st
import random
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Xpedious", layout="wide", page_icon="⚡")

# ===== STYLE =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #070a0f !important;
    color: #e8eaf0 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #0d2040 0%, #070a0f 60%) !important;
}

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
header { background: transparent !important; }

[data-testid="stSidebar"] {
    background: #0b0e16 !important;
    border-right: 1px solid #1a2030 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

.sidebar-logo {
    padding: 28px 24px 20px;
    border-bottom: 1px solid #1a2030;
    margin-bottom: 8px;
}
.sidebar-logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #fff;
}
.sidebar-logo-text span { color: #3d8fff; }
.sidebar-tagline {
    font-size: 10px;
    color: #4a5568;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 3px;
}

.nav-section-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #2d3748;
    padding: 18px 24px 8px;
    font-weight: 500;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 24px;
    font-size: 12px;
    color: #6b7a94;
    border-left: 2px solid transparent;
    letter-spacing: 0.5px;
}
.nav-item.active {
    color: #3d8fff;
    border-left-color: #3d8fff;
    background: linear-gradient(90deg, rgba(61,143,255,0.07) 0%, transparent 100%);
}
.nav-dot { width: 6px; height: 6px; border-radius: 50%; background: #1a2535; flex-shrink: 0; }
.nav-item.active .nav-dot { background: #3d8fff; box-shadow: 0 0 6px #3d8fff80; }

.block-container { max-width: 1100px !important; padding: 40px 40px 80px !important; }

.page-header { margin-bottom: 40px; padding-bottom: 28px; border-bottom: 1px solid #141824; }
.page-eyebrow { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #3d8fff; margin-bottom: 10px; font-weight: 500; }
.page-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #ffffff; letter-spacing: -1px; line-height: 1.1; }
.page-title span { color: #3d8fff; }
.page-subtitle { margin-top: 8px; font-size: 12px; color: #4a5568; letter-spacing: 0.3px; }

.section-label {
    font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #3d8fff;
    margin-bottom: 14px; font-weight: 500; display: flex; align-items: center; gap: 8px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #1a2535 0%, transparent 100%); }

.input-panel {
    background: #0d1119; border: 1px solid #1a2535; border-radius: 16px;
    padding: 28px 32px; margin-bottom: 32px; position: relative; overflow: hidden;
}
.input-panel::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #3d8fff40, transparent);
}

[data-testid="stTextInput"] > div > div > input {
    background: #080c14 !important; border: 1px solid #1e2a3a !important;
    border-radius: 10px !important; color: #c8d5e8 !important;
    font-family: 'DM Mono', monospace !important; font-size: 13px !important; padding: 12px 16px !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #3d8fff !important; box-shadow: 0 0 0 3px rgba(61,143,255,0.1) !important;
}
[data-testid="stTextInput"] label {
    font-family: 'DM Mono', monospace !important; font-size: 11px !important;
    color: #6b7a94 !important; letter-spacing: 1px; text-transform: uppercase;
}

[data-testid="stButton"] > button {
    background: #3d8fff !important; color: #ffffff !important; border: none !important;
    border-radius: 10px !important; padding: 10px 28px !important;
    font-family: 'DM Mono', monospace !important; font-size: 12px !important;
    font-weight: 500 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(61,143,255,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    background: #5a9fff !important; box-shadow: 0 6px 28px rgba(61,143,255,0.4) !important;
    transform: translateY(-1px) !important;
}

.order-card {
    background: #0c1018; border: 1px solid #161e2e; border-radius: 20px;
    margin-bottom: 24px; overflow: hidden; position: relative;
}
.order-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #3d8fff30, transparent);
}
.order-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 28px; border-bottom: 1px solid #111825;
}
.order-id { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #ffffff; letter-spacing: -0.3px; }
.order-ts { font-size: 11px; color: #2d3d52; letter-spacing: 0.5px; }
.badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }
.badge-processing { background: rgba(255,152,0,0.1); color: #ffb74d; border: 1px solid rgba(255,152,0,0.2); }

.module-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0; }
.module-cell { padding: 22px 28px; border-right: 1px solid #111825; border-bottom: 1px solid #111825; }
.module-cell-last-row { border-bottom: none !important; }
.module-eyebrow { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: #2d3d52; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }
.module-eyebrow-dot { width: 4px; height: 4px; border-radius: 50%; background: #3d8fff; flex-shrink: 0; }

.item-pill {
    display: inline-flex; align-items: center; gap: 6px; background: #0f1520;
    border: 1px solid #1a2535; border-radius: 8px; padding: 6px 12px;
    font-size: 12px; color: #8a9bb5; margin: 3px 4px 3px 0;
}
.item-qty { font-weight: 500; color: #3d8fff; font-family: 'Syne', sans-serif; }

.vendor-row { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #0f151f; font-size: 12px; color: #6b7a94; }
.vendor-row:last-child { border-bottom: none; }
.vendor-row.best { color: #c8d5e8; }
.vendor-price { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 14px; }
.vendor-row.best .vendor-price { color: #3d8fff; }
.best-tag { font-size: 8px; letter-spacing: 1.5px; text-transform: uppercase; color: #3d8fff; background: rgba(61,143,255,0.08); border: 1px solid rgba(61,143,255,0.2); border-radius: 4px; padding: 2px 7px; }

.pw-icon { width: 36px; height: 36px; border-radius: 10px; background: rgba(61,143,255,0.1); border: 1px solid rgba(61,143,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.pw-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; color: #fff; letter-spacing: -0.3px; }
.pw-sub { font-size: 11px; color: #3d5070; margin-top: 2px; }

.delivery-status { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; color: #66bb6a; margin-bottom: 4px; }
.delivery-eta { font-size: 11px; color: #4a6080; }

.invoice-amount { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 28px; color: #ffffff; letter-spacing: -1px; }
.invoice-status { display: inline-flex; align-items: center; gap: 5px; background: rgba(255,152,0,0.08); border: 1px solid rgba(255,152,0,0.2); color: #ffb74d; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; padding: 3px 10px; border-radius: 20px; margin-top: 6px; }

.empty-state { text-align: center; padding: 80px 40px; color: #2d3d52; }
.empty-title { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #2d3d52; margin-bottom: 8px; }
.empty-sub { font-size: 12px; color: #1e2a3a; letter-spacing: 0.3px; }

.stat-bar { display: flex; gap: 1px; margin-bottom: 32px; }
.stat-item { flex: 1; background: #0c1018; border: 1px solid #161e2e; padding: 18px 22px; border-radius: 4px; }
.stat-item:first-child { border-radius: 12px 4px 4px 12px; }
.stat-item:last-child { border-radius: 4px 12px 12px 4px; }
.stat-val { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 26px; color: #ffffff; letter-spacing: -1px; }
.stat-val.blue { color: #3d8fff; }
.stat-lbl { font-size: 10px; color: #2d3d52; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 3px; }
</style>
""", unsafe_allow_html=True)

# ===== STATE =====
if "orders" not in st.session_state:
    st.session_state.orders = []

# ===== FUNCTIONS =====
def parse_items(text):
    items = []
    for line in text.split(","):
        qty = "".join([c for c in line if c.isdigit()])
        qty = int(qty) if qty else 1
        name = "".join([c for c in line if not c.isdigit()]).strip()
        items.append({"name": name, "quantity": qty})
    return items

def generate_vendors():
    return [
        {"name": "Graybar", "price": random.randint(100, 400)},
        {"name": "Rexel", "price": random.randint(100, 400)},
        {"name": "Platt", "price": random.randint(100, 400)},
    ]

def pick_best(vendors):
    return min(vendors, key=lambda x: x["price"])

def create_delivery():
    return {"status": "Scheduled", "eta": "Tomorrow 9AM"}

def create_invoice(order):
    return {"total": order["selected"]["price"], "status": "Unpaid"}

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-text">X<span>pedious</span></div>
        <div class="sidebar-tagline">Electrical Procurement</div>
    </div>
    <div class="nav-section-label">Modules</div>
    <div class="nav-item active"><div class="nav-dot"></div>SMS Intake</div>
    <div class="nav-item"><div class="nav-dot"></div>Ordering</div>
    <div class="nav-item"><div class="nav-dot"></div>Sourcing</div>
    <div class="nav-item"><div class="nav-dot"></div>Procurement</div>
    <div class="nav-item"><div class="nav-dot"></div>Delivery</div>
    <div class="nav-item"><div class="nav-dot"></div>Billing</div>
    """, unsafe_allow_html=True)

# ===== PAGE HEADER =====
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">⚡ Platform</div>
    <div class="page-title">Electrical <span>Procurement</span></div>
    <div class="page-subtitle">Automated sourcing · vendor comparison · instant delivery scheduling</div>
</div>
""", unsafe_allow_html=True)

# ===== STATS =====
total_orders = len(st.session_state.orders)
total_spend = sum(o["selected"]["price"] for o in st.session_state.orders) if st.session_state.orders else 0
best_savings = sum(
    max(v["price"] for v in o["vendors"]) - o["selected"]["price"]
    for o in st.session_state.orders
) if st.session_state.orders else 0

st.markdown(f"""
<div class="stat-bar">
    <div class="stat-item">
        <div class="stat-val blue">{total_orders}</div>
        <div class="stat-lbl">Total Orders</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">${total_spend:,}</div>
        <div class="stat-lbl">Total Spend</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">${best_savings:,}</div>
        <div class="stat-lbl">Savings Found</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">{total_orders}</div>
        <div class="stat-lbl">Deliveries Scheduled</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== SMS INPUT PANEL =====
st.markdown('<div class="section-label">📩 SMS Ordering</div>', unsafe_allow_html=True)
st.markdown('<div class="input-panel">', unsafe_allow_html=True)

message = st.text_input(
    "Order message",
    placeholder="e.g.  3 breakers, 2 panels, 10 wire nuts",
)
process_btn = st.button("⚡  Process Order")
st.markdown('</div>', unsafe_allow_html=True)

if process_btn:
    if message:
        items = parse_items(message)
        vendors = generate_vendors()
        best = pick_best(vendors)

        order = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": items,
            "vendors": vendors,
            "selected": best,
            "delivery": create_delivery(),
            "invoice": None,
            "status": "Processing"
        }
        order["invoice"] = create_invoice(order)
        st.session_state.orders.append(order)
        st.rerun()
    else:
        st.warning("Enter an order message first.")

# ===== ORDERS DASHBOARD =====
st.markdown('<div class="section-label">📊 Orders Dashboard</div>', unsafe_allow_html=True)

if not st.session_state.orders:
    st.markdown("""
    <div class="order-card">
        <div class="empty-state">
            <div style="font-size:48px;opacity:0.3;margin-bottom:16px;">⚡</div>
            <div class="empty-title">No orders yet</div>
            <div class="empty-sub">Submit an SMS order above to get started</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for i, order in enumerate(reversed(st.session_state.orders)):
        order_num = len(st.session_state.orders) - i

        items_html = "".join([
            f'<span class="item-pill"><span class="item-qty">{it["quantity"]}×</span> {it["name"]}</span>'
            for it in order["items"]
        ])

        vendors_html = ""
        for v in order["vendors"]:
            is_best = v == order["selected"]
            row_class = "vendor-row best" if is_best else "vendor-row"
            best_tag = '<span class="best-tag">Best</span>' if is_best else ""
            vendors_html += f"""
            <div class="{row_class}">
                <span>{v['name']}</span>
                <div style="display:flex;align-items:center;gap:10px;">
                    {best_tag}<span class="vendor-price">${v['price']}</span>
                </div>
            </div>"""

        savings = max(v["price"] for v in order["vendors"]) - order["selected"]["price"]

        st.markdown(f"""
        <div class="order-card">
            <div class="order-header">
                <div>
                    <div class="order-id">Order #{order_num:03d}</div>
                    <div class="order-ts">{order['timestamp']}</div>
                </div>
                <span class="badge badge-processing">⬤ Processing</span>
            </div>
            <div class="module-grid">
                <div class="module-cell">
                    <div class="module-eyebrow"><div class="module-eyebrow-dot"></div>Ordering</div>
                    {items_html}
                </div>
                <div class="module-cell">
                    <div class="module-eyebrow"><div class="module-eyebrow-dot"></div>Vendor Quotes</div>
                    {vendors_html}
                </div>
                <div class="module-cell" style="border-right:none;">
                    <div class="module-eyebrow"><div class="module-eyebrow-dot"></div>Procurement</div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <div class="pw-icon">🏭</div>
                        <div>
                            <div class="pw-name">{order['selected']['name']}</div>
                            <div class="pw-sub">Selected · ${savings} saved vs next best</div>
                        </div>
                    </div>
                </div>
                <div class="module-cell module-cell-last-row">
                    <div class="module-eyebrow"><div class="module-eyebrow-dot"></div>Delivery</div>
                    <div class="delivery-status">{order['delivery']['status']}</div>
                    <div class="delivery-eta">ETA — {order['delivery']['eta']}</div>
                </div>
                <div class="module-cell module-cell-last-row" style="border-right:none;grid-column:2/4;">
                    <div class="module-eyebrow"><div class="module-eyebrow-dot"></div>Billing</div>
                    <div class="invoice-amount">${order['invoice']['total']}</div>
                    <div class="invoice-status">⬤ {order['invoice']['status']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
