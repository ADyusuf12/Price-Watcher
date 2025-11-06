import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";

export default function ProductsPage() {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchProducts() {
            try {
                const res = await fetch("/api/v1/products");
                if (!res.ok) throw new Error("Failed to fetch products");
                const json = await res.json();
                setProducts(json);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchProducts();
    }, []);

    return (
        <div className="bg-gradient-to-br from-green-700 via-white to-green-700 min-h-screen p-8">
            <h1 className="text-3xl font-bold text-white mb-6">Latest Products</h1>

            {loading && (
                <div className="flex justify-center items-center h-64">
                    <div className="w-12 h-12 border-4 border-green-300 border-t-transparent rounded-full animate-spin"></div>
                </div>
            )}

            {error && <p className="text-red-500">{error}</p>}

            {!loading && !error && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {products.map((p) => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                </div>
            )}
        </div>
    );
}
