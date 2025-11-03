Product.create!([
  {
    title: "Samsung Galaxy S23",
    price: 450000,
    old_price: 500000,
    discount: "10%",
    source: "Jumia",
    url: "https://www.jumia.com.ng/samsung-galaxy-s23",
    scraped_at: Time.now,
    image: "https://example.com/images/s23.jpg"
  },
  {
    title: "HP Pavilion x360",
    price: 320000,
    old_price: 350000,
    discount: "8%",
    source: "Konga",
    url: "https://www.konga.com/hp-pavilion-x360",
    scraped_at: Time.now,
    image: "https://example.com/images/hp-x360.jpg"
  }
])
