import streamlit as st
import random
import time

st.title("Xpedious Procurement System")

# ====== SESSION STORAGE ======
if "orders" not in st.session_state:
    st.session_state.orders = []

# ====== FUNCTIONS ======
def parse_items(text):
    items = []
    lines = text.split(",")

    for line in lines:
        qty = "".join([c for c in line if c.isdigit()])
        qty = int(qty) if qty else 1

        name = "".join([c for c in line if not c.isdigit()]).strip()

        items.append({
            "name": name,
            "quantity": qty
        })

    return items

def generate_vendors():
    return [
        {"name": "Vendor A", "price": random.randint(100, 400)},
        {"name": "Vendor B", "price": random.randint(100, 400)},
        {"name": "Vendor C", "price": random.randint(100, 400)},
    ]

def pick_best_vendor(vendors):
    return min(vendors, key=lambda x: x["price"])

def create_delivery():
    return {
        "status": "scheduled",
        "eta": "Tomorrow 9AM"
    }

def create_invoice(order):
    return {
        "total": order["selected_vendor"]["price"],
        "status": "unpaid"
    }

# ====== INPUT ======
message = st.text_input("Enter SMS Order (example: 3 breakers, 2 panels)")

if st.button("Process Order"):
    if message:
        items = parse_items(message)
        vendors = generate_vendors()
        selected = pick_best_vendor(vendors)

        order = {
            "items": items,
            "vendors": vendors,
            "selected_vendor": selected,
            "delivery": create_delivery(),
            "invoice": None
        }

        order["invoice"] = create_invoice(order)

        st.session_state.orders.append(order)

# ====== DISPLAY ======
st.subheader("Orders")

for i, order in enumerate(st.session_state.orders):
    with st.expander(f"Order {i+1}"):

        st.write("**Items:**", order["items"])

        st.write("**Vendor Quotes:**")
        for v in order["vendors"]:
            st.write(f"{v['name']}: ${v['price']}")

        st.write("**Selected Vendor:**", order["selected_vendor"]["name"])

        st.write("**Delivery ETA:**", order["delivery"]["eta"])

        st.write("**Invoice Total:** $", order["invoice"]["total"])
