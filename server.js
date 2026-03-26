import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const orders = [];

// ===== Serve frontend =====
app.use(express.static(__dirname));

// ===== SMS SIMULATION =====
app.post("/sms", (req, res) => {
  const { message } = req.body;

  const items = parseItems(message);

  const order = {
    id: Date.now(),
    message,
    items,
    vendors: generateVendors(),
    status: "processing"
  };

  order.selectedVendor = pickBestVendor(order.vendors);
  order.delivery = createDelivery();
  order.invoice = createInvoice(order);

  orders.push(order);

  res.json(order);
});

// ===== GET ORDERS =====
app.get("/orders", (req, res) => {
  res.json(orders);
});

// ===== FUNCTIONS =====
function parseItems(text) {
  return text.split(",").map((line) => {
    const qty = parseInt(line.match(/\d+/)?.[0] || 1);
    return {
      name: line.replace(/\d+/g, "").trim(),
      quantity: qty
    };
  });
}

function generateVendors() {
  return [
    { name: "Vendor A", price: Math.floor(Math.random() * 300) + 100 },
    { name: "Vendor B", price: Math.floor(Math.random() * 300) + 100 },
    { name: "Vendor C", price: Math.floor(Math.random() * 300) + 100 }
  ];
}

function pickBestVendor(vendors) {
  return vendors.reduce((a, b) => (a.price < b.price ? a : b));
}

function createDelivery() {
  return {
    status: "scheduled",
    eta: "Tomorrow 9AM"
  };
}

function createInvoice(order) {
  return {
    total: order.selectedVendor.price,
    status: "unpaid"
  };
}

app.listen(3000, () => {
  console.log("Running on http://localhost:3000");
});
