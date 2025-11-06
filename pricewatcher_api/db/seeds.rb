# db/seeds.rb

def create_product(attrs)
  Product.find_or_create_by!(title: attrs[:title], source: attrs[:source]) do |p|
    p.price      = attrs[:price]
    p.old_price  = attrs[:old_price]
    p.discount   = attrs[:discount]
    p.url        = attrs[:url]
    p.scraped_at = attrs[:scraped_at]
    p.image      = attrs[:image]
  end
end

products = [
  {
    title: "Samsung Galaxy S23",
    price: 450000,
    old_price: 500000,
    discount: "10%",
    source: "jumia",
    url: "https://www.jumia.com.ng/samsung-galaxy-s23",
    scraped_at: Time.now,
    image: "https://example.com/images/s23.jpg"
  },
  {
    title: "Samsung Galaxy S23",
    price: 460000,
    old_price: 490000,
    discount: "6%",
    source: "konga",
    url: "https://www.konga.com/samsung-galaxy-s23",
    scraped_at: Time.now,
    image: "https://example.com/images/s23-konga.jpg"
  },
  {
    title: "HP Pavilion x360",
    price: 320000,
    old_price: 350000,
    discount: "8%",
    source: "konga",
    url: "https://www.konga.com/hp-pavilion-x360",
    scraped_at: Time.now,
    image: "https://example.com/images/hp-x360.jpg"
  },
  {
    title: "HP Pavilion x360",
    price: 310000,
    old_price: 340000,
    discount: "9%",
    source: "jumia",
    url: "https://www.jumia.com.ng/hp-pavilion-x360",
    scraped_at: Time.now,
    image: "https://example.com/images/hp-x360-jumia.jpg"
  },
  {
    title: "Tecno Camon 20 Pro",
    price: 150000,
    old_price: 170000,
    discount: "12%",
    source: "jumia",
    url: "https://www.jumia.com.ng/tecno-camon-20-pro",
    scraped_at: Time.now,
    image: "https://example.com/images/tecno-camon20.jpg"
  },
  {
    title: "Tecno Camon 20 Pro",
    price: 155000,
    old_price: 165000,
    discount: "6%",
    source: "konga",
    url: "https://www.konga.com/tecno-camon-20-pro",
    scraped_at: Time.now,
    image: "https://example.com/images/tecno-camon20-konga.jpg"
  },
  {
    title: "Infinix Note 30",
    price: 130000,
    old_price: 145000,
    discount: "10%",
    source: "jumia",
    url: "https://www.jumia.com.ng/infinix-note-30",
    scraped_at: Time.now,
    image: "https://example.com/images/infinix-note30.jpg"
  },
  {
    title: "Infinix Note 30",
    price: 128000,
    old_price: 140000,
    discount: "8%",
    source: "konga",
    url: "https://www.konga.com/infinix-note-30",
    scraped_at: Time.now,
    image: "https://example.com/images/infinix-note30-konga.jpg"
  },
  {
    title: "Dell Inspiron 15",
    price: 400000,
    old_price: 420000,
    discount: "5%",
    source: "jumia",
    url: "https://www.jumia.com.ng/dell-inspiron-15",
    scraped_at: Time.now,
    image: "https://example.com/images/dell-inspiron15.jpg"
  },
  {
    title: "Dell Inspiron 15",
    price: 390000,
    old_price: 410000,
    discount: "4%",
    source: "konga",
    url: "https://www.konga.com/dell-inspiron-15",
    scraped_at: Time.now,
    image: "https://example.com/images/dell-inspiron15-konga.jpg"
  }
]

products.each { |attrs| create_product(attrs) }
