import { formatCurrency } from "../utils";

export default function ProductCard({ product }) {
    return (
        <div className="group backdrop-blur-md bg-white/40 border w-[340px] cursor-pointer border-white/20 rounded-xl shadow-lg overflow-hidden hover:shadow-xl hover:border-green-400 transition">
            {/* Product Image */}
            <img
                src={product.image}
                alt={product.title}
                className="w-full h-48 object-cover"
            />

            {/* Product Info */}
            <div className="p-4">
                {/* Animated scrolling title */}
                <div className="relative overflow-hidden">
                    <h2 className="text-lg font-bold text-green-700 text-shadow border-b-2 border-green-400 whitespace-nowrap transition-transform duration-[8000ms] ease-linear group-hover:translate-x-[-100%]">
                        {product.title}
                    </h2>
                </div>

                <p className="text-2xl font-bold text-green-500 text-shadow mt-2">
                    {formatCurrency(product.price)}
                </p>

                <span
                    className={`inline-block px-2 py-1 text-sm font-semibold uppercase tracking-wide rounded ${product.source === "jumia"
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
                    className="block mt-3 text-green-500 hover:text-green-300 no-underline font-medium"
                >
                    View product
                </a>
            </div>
        </div>
    );
}
