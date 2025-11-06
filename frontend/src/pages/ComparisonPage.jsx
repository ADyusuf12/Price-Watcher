import { useState } from "react";

export default function ComparisonPage() {
    const [query, setQuery] = useState("");
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    async function handleSearch(e) {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            const res = await fetch(`/api/v1/comparisons?q=${encodeURIComponent(query)}`);
            if (!res.ok) throw new Error("Failed to fetch comparisons");
            const json = await res.json();
            setData(json);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="bg-gradient-to-br from-green-700 via-white to-green-700 min-h-screen p-8">
            <h1 className="text-3xl font-bold text-white mb-6">Compare Products</h1>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="flex gap-2 mb-6">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search product..."
                    className="flex-1 px-3 py-2 rounded-lg backdrop-blur-md bg-white/30 border border-white/20 text-white placeholder-green-200 focus:outline-none focus:border-green-400"
                />
                <button
                    type="submit"
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
                >
                    Compare
                </button>
            </form>

            {error && <p className="text-red-500">{error}</p>}

            {loading && (
                <div className="flex justify-center items-center h-32">
                    <div className="w-12 h-12 border-4 border-green-300 border-t-transparent rounded-full animate-spin"></div>
                </div>
            )}

            {!loading && data?.comparisons?.length > 0 && (
                <div className="space-y-6">
                    {data.comparisons.map((c, idx) => (
                        <div
                            key={idx}
                            className="grid grid-cols-3 gap-4 backdrop-blur-md bg-white/30 border border-white/20 rounded-xl shadow-lg p-4 hover:border-green-400 transition"
                        >
                            {/* Jumia */}
                            <div className="bg-orange-500/30 p-3 rounded-lg">
                                <h2 className="font-semibold text-orange-200">{c.jumia.title}</h2>
                                <p className="text-lg text-white">₦{c.jumia.price}</p>
                                {c.jumia.discount && (
                                    <p className="text-sm text-orange-100">Discount: {c.jumia.discount}%</p>
                                )}
                            </div>

                            {/* Konga */}
                            <div className="bg-pink-500/30 p-3 rounded-lg">
                                <h2 className="font-semibold text-pink-200">{c.konga.title}</h2>
                                <p className="text-lg text-white">₦{c.konga.price}</p>
                                {c.konga.discount && (
                                    <p className="text-sm text-pink-100">Discount: {c.konga.discount}%</p>
                                )}
                            </div>

                            {/* Difference */}
                            <div className="flex items-center justify-center">
                                <p className="text-green-200 font-semibold">
                                    Difference: ₦{c.price_difference}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {!loading && data && data.comparisons?.length === 0 && (
                <p className="text-green-100">No comparisons found.</p>
            )}
        </div>
    );
}
