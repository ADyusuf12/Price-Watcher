import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProductsPage from "./pages/ProductsPage";
import ComparisonPage from "./pages/ComparisonPage";

export default function App() {
  return (
    <>
      <Navbar />
      <div className="pt-20"></div>
      <Routes>
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/compare" element={<ComparisonPage />} />
      </Routes>
    </>
  );
}