async function sendSMS() {
  const message = document.getElementById("message").value;

  await fetch("/sms", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  loadOrders();
}

async function loadOrders() {
  const res = await fetch("/orders");
  const data = await res.json();

  const container = document.getElementById("orders");
  container.innerHTML = "";

  data.forEach(order => {
    const div = document.createElement("div");
    div.className = "order";

    div.innerHTML = `
      <p><b>Items:</b> ${JSON.stringify(order.items)}</p>
      <p><b>Vendor:</b> ${order.selectedVendor.name}</p>
      <p><b>Price:</b> $${order.selectedVendor.price}</p>
      <p><b>Delivery:</b> ${order.delivery.eta}</p>
      <p><b>Invoice:</b> $${order.invoice.total}</p>
    `;

    container.appendChild(div);
  });
}

loadOrders();
