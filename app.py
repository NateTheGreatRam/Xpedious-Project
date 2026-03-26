import streamlit as st
import random

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Xpedious", layout="wide")

# ====== CUSTOM CSS ======
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    color: #4CAF50;
}

.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.vendor {
    padding: 8px;
    border-radius: 8px;
    margin-bottom: 5px;
}

.best {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

.bad {
    background-color: #2a2d36;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Xpedious Procurement System")

# ====== STATE ======
if "orders" not in st.session_state:
    st.session_state.orders = []

# ====== FUNCTIONS ======
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
        {"name": "Vendor A", "price": random.randint(100, 400)},
        {"name": "Vendor B", "price": random.randint(100, 400)},
        {"name": "Vendor C", "price": random.randint(100, 400)},
    ]

def pick_best(vendors):
    return min(vendors, key=lambda x: x["price"])

def create_delivery():
    return {"eta": "Tomorrow 9AM"}

def create_invoice(order):
    return {"total": order["selected"]["price"]}

# ====== INPUT ======
col1, col2 = st.columns([3,1])

with col1:
    message = st.text_input("Enter Order (e.g. 3 breakers, 2 panels)")

with col2:
    if st.button("Create Order"):
        if message:
            items = parse_items(message)
            vendors = generate_vendors()
            best = pick_best(vendors)

            order = {
                "items": items,
                "vendors": vendors,
                "selected": best,
                "delivery": create_delivery(),
                "invoice": None
            }

            order["invoice"] = create_invoice(order)
            st.session_state.orders.append(order)

# ====== DISPLAY ======
st.subheader("Orders")

for order in st.session_state.orders:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📦 Items")
    for item in order["items"]:
        st.write(f"- {item['quantity']}x {item['name']}")

    st.markdown("### 🏭 Vendor Quotes")
    for v in order["vendors"]:
        if v == order["selected"]:
            st.markdown(
                f'<div class="vendor best">{v["name"]} - ${v["price"]} ✅ BEST</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="vendor bad">{v["name"]} - ${v["price"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown(f"### 🚚 Delivery: {order['delivery']['eta']}")
    st.markdown(f"### 💰 Invoice: ${order['invoice']['total']}")

    st.markdown('</div>', unsafe_allow_html=True)
