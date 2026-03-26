import streamlit as st
import random
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Xpedious", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
body { background-color: #0f1117; color: white; }
.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    margin-right: 5px;
    font-size: 12px;
}
.green { background: #4CAF50; }
.blue { background: #2196F3; }
.orange { background: #ff9800; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Xpedious — Electrical Procurement Platform")

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
    return {
        "status": "Scheduled",
        "eta": "Tomorrow 9AM"
    }

def create_invoice(order):
    return {
        "total": order["selected"]["price"],
        "status": "Unpaid"
    }

# ===== SIDEBAR =====
st.sidebar.header("System Modules")
st.sidebar.markdown("""
- 📩 SMS Intake  
- 📦 Ordering  
- 🏭 Sourcing  
- 🧾 Procurement  
- 🚚 Delivery  
- 💰 Billing  
""")

# ===== INPUT =====
st.subheader("📩 SMS Ordering")

message = st.text_input("Send order (example: 3 breakers, 2 panels)")

if st.button("Process SMS Order"):
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

# ===== DASHBOARD =====
st.subheader("📊 Orders Dashboard")

for order in st.session_state.orders:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"### 🧾 Order ({order['timestamp']})")

    # ORDERING
    st.markdown("#### 📦 Ordering")
    for item in order["items"]:
        st.write(f"- {item['quantity']}x {item['name']}")

    # SOURCING
    st.markdown("#### 🏭 Sourcing (Vendor Quotes)")
    for v in order["vendors"]:
        if v == order["selected"]:
            st.markdown(f"✅ **{v['name']} — ${v['price']} (BEST)**")
        else:
            st.markdown(f"{v['name']} — ${v['price']}")

    # PROCUREMENT
    st.markdown("#### 🧾 Procurement Decision")
    st.success(f"Selected: {order['selected']['name']}")

    # DELIVERY
    st.markdown("#### 🚚 Delivery")
    st.info(f"ETA: {order['delivery']['eta']}")

    # BILLING
    st.markdown("#### 💰 Billing")
    st.warning(f"Invoice: ${order['invoice']['total']} ({order['invoice']['status']})")

    st.markdown('</div>', unsafe_allow_html=True)
