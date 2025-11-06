import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="backdrop-blur-md bg-white/20 border-b border-white/30 fixed top-0 left-0 w-full z-50">
            <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
                {/* Logo / Brand */}
                <Link to="/" className="text-2xl font-bold text-green-700">
                    PriceWatcher
                </Link>

                {/* Navigation Links */}
                <div className="flex gap-6">
                    <Link
                        to="/products"
                        className="text-white hover:text-green-300 transition"
                    >
                        Products
                    </Link>
                    <Link
                        to="/compare"
                        className="text-white hover:text-green-300 transition"
                    >
                        Compare
                    </Link>
                </div>
            </div>
        </nav>
    );
}
