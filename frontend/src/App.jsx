import { useEffect, useState } from 'react'

function App() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    fetch('/api/v1/products')
      .then(res => res.json())
      .then(setProducts)
      .catch(err => console.error("API error:", err))
  }, [])

  if (!products.length) return <p>Loading...</p>

  return (
    <div style={{ padding: "2rem" }}>
      <h1>PriceWatcher Frontend</h1>

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Source</th>
            <th>Title</th>
            <th>Price (₦)</th>
            <th>Discount</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <tr key={p.id}>
              <td>{p.source}</td>
              <td>{p.title}</td>
              <td>{p.price?.toLocaleString()}</td>
              <td>{p.discount || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App
