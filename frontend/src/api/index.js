// src/api/index.js

const API_BASE = "/api/v1"; // relative path, works with your Docker setup

// Fetch all products
export async function fetchProducts() {
    const res = await fetch(`${API_BASE}/products`);
    if (!res.ok) throw new Error("Failed to fetch products");
    return res.json();
}

// Fetch a single product by ID
export async function fetchProduct(id) {
    const res = await fetch(`${API_BASE}/products/${id}`);
    if (!res.ok) throw new Error("Failed to fetch product");
    return res.json();
}
