export default function ProductCard({ product }) {
    return (
        <div className="backdrop-blur-md bg-white/30 border border-white/20 rounded-xl shadow-lg overflow-hidden hover:shadow-xl hover:border-green-400 transition">
            {/* Product Image */}
            <img
                src={product.image}
                alt={product.title}
                className="w-full h-48 object-cover"
            />

            {/* Product Info */}
            <div className="p-4">
                <h2 className="text-lg font-bold text-white border-b-2 border-green-400 inline-block">
                    {product.title}
                </h2>

                <p className="text-xl font-semibold text-green-300 mt-2">
                    ₦{product.price}
                </p>

                <span
                    className={`inline-block px-2 py-1 text-sm rounded ${product.source === "jumia"
                            ? "bg-orange-500/70 text-white"
                            : "bg-pink-500/70 text-white"
                        }`}
                >
                    {product.source}
                </span>

                <a
                    href={product.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block mt-3 text-green-200 hover:text-green-400 underline"
                >
                    View product
                </a>
            </div>
        </div>
    );
}
