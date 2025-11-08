import { useState, useEffect } from "react";
import ProductCard from "../components/ProductCard";

export default function ComparisonPage() {
    const [query, setQuery] = useState("");
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const [pageComparisons, setPageComparisons] = useState(1);
    const [pageSingles, setPageSingles] = useState(1);
    const [perPage] = useState(20);

    async function fetchComparisons(q, pComp = 1, pSing = 1) {
        setError(null);
        setLoading(true);
        try {
            const res = await fetch(
                `/api/v1/comparisons?q=${encodeURIComponent(q)}&page=${pComp}&per_page=${perPage}`
            );
            if (!res.ok) throw new Error("Failed to fetch comparisons");
            const json = await res.json();
            setData(json);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleSearch(e) {
        e.preventDefault();
        setPageComparisons(1);
        setPageSingles(1);
        if (query.trim()) {
            fetchComparisons(query, 1, 1);
        }
    }

    useEffect(() => {
        if (query.trim()) {
            fetchComparisons(query, pageComparisons, pageSingles);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [pageComparisons, pageSingles]);

    return (
        <div className="bg-gradient-to-br from-green-700 via-white to-green-700 min-h-screen p-8">
            <h1 className="text-4xl font-extrabold text-white text-shadow mb-6">
                Compare Products
            </h1>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="flex gap-2 mb-6">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search product..."
                    className="flex-1 px-3 py-2 rounded-lg backdrop-blur-md bg-white/40 border border-white/20 text-white placeholder-green-200 focus:outline-none focus:border-green-400"
                />
                <button
                    type="submit"
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition font-semibold"
                >
                    Compare
                </button>
            </form>

            {error && <p className="text-red-500 font-semibold">{error}</p>}

            {loading && (
                <div className="flex justify-center items-center h-32">
                    <div className="w-12 h-12 border-4 border-green-300 border-t-transparent rounded-full animate-spin"></div>
                </div>
            )}

            {/* Grouped Comparisons */}
            {!loading && data?.comparisons?.length > 0 && (
                <div className="space-y-6">
                    {data.comparisons.map((c, idx) => (
                        <div
                            key={idx}
                            className="backdrop-blur-md bg-white/40 border border-white/20 rounded-xl shadow-lg p-4 hover:border-green-400 transition"
                        >
                            <h3 className="text-2xl font-extrabold text-white text-shadow mb-4">
                                {c.brand?.toUpperCase()} {c.series} {c.model?.toUpperCase()}
                            </h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <h4 className="text-green-700 font-extrabold text-shadow mb-2">
                                        Jumia Variants
                                    </h4>
                                    <div className="flex flex-wrap gap-10">
                                        {c.jumia.map((p) => (
                                            <ProductCard key={p.id} product={p} />
                                        ))}
                                    </div>
                                </div>
                                <div>
                                    <h4 className="text-green-700 font-extrabold text-shadow mb-2">
                                        Konga Variants
                                    </h4>
                                    <div className="flex flex-wrap gap-10">
                                        {c.konga.map((p) => (
                                            <ProductCard key={p.id} product={p} />
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Pagination Controls for Comparisons */}
                    <div className="flex justify-center gap-4 mt-6">
                        <button
                            disabled={pageComparisons <= 1}
                            onClick={() => setPageComparisons(pageComparisons - 1)}
                            className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 font-semibold"
                        >
                            Previous
                        </button>
                        <span className="text-white font-semibold">
                            Page {pageComparisons} of {data.meta.total_pages_comparisons}
                        </span>
                        <button
                            disabled={pageComparisons >= data.meta.total_pages_comparisons}
                            onClick={() => setPageComparisons(pageComparisons + 1)}
                            className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 font-semibold"
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}

            {/* Singles */}
            {!loading && data?.singles?.length > 0 && (
                <div className="space-y-6 mt-8">
                    <h2 className="text-2xl font-extrabold text-white text-shadow">
                        Available Products
                    </h2>
                    <div className="flex flex-wrap gap-10">
                        {data.singles.map((p) => (
                            <ProductCard key={p.id} product={p} />
                        ))}
                    </div>

                    {/* Pagination Controls for Singles */}
                    <div className="flex justify-center gap-4 mt-6">
                        <button
                            disabled={pageSingles <= 1}
                            onClick={() => setPageSingles(pageSingles - 1)}
                            className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 font-semibold"
                        >
                            Previous
                        </button>
                        <span className="text-white font-semibold">
                            Page {pageSingles} of {data.meta.total_pages_singles}
                        </span>
                        <button
                            disabled={pageSingles >= data.meta.total_pages_singles}
                            onClick={() => setPageSingles(pageSingles + 1)}
                            className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 font-semibold"
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}

            {!loading &&
                data &&
                data.comparisons?.length === 0 &&
                data.singles?.length === 0 && (
                    <p className="text-green-100 font-semibold text-shadow">
                        No products found.
                    </p>
                )}
        </div>
    );
}
