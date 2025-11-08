# app/queries/product_comparison_query.rb
class ProductComparisonQuery
  def initialize(query:, page: 1, per_page: 20)
    @query = query
    @page = page.to_i
    @per_page = per_page.to_i
  end

  def call
    products = Product.where("title ILIKE ?", "%#{@query}%")
    grouped  = products.group_by(&:source)

    comparisons, singles = build_matches(grouped)

    {
      query: @query,
      comparisons: paginate(comparisons),
      singles: paginate(singles),
      meta: {
        total_comparisons: comparisons.size,
        total_singles: singles.size,
        page: @page,
        per_page: @per_page,
        total_pages_comparisons: (comparisons.size.to_f / @per_page).ceil,
        total_pages_singles: (singles.size.to_f / @per_page).ceil
      }
    }
  end

  private

  # General parser: extracts brand, series, model, specs from title dynamically
  def parse_specs(title)
    normalized = title.downcase.gsub(/[^a-z0-9\s\."]/, " ").squeeze(" ").strip
    tokens = normalized.split(" ")

    {
      brand: tokens[0], # assume first word is brand
      series: tokens[1], # often second word is series
      model: tokens.find { |t| t.match?(/[a-z]?\d{2,}/) }, # e.g. a06, 15, spark20
      ram: normalized[/\d+gb ram/, 0],
      storage: normalized[/\d+gb (rom|storage)/, 0],
      screen: normalized[/\d+(\.\d+)?"/, 0],
      color: normalized[/\b(black|blue|gold|green|white|red)\b/, 0]
    }
  end

  def build_matches(grouped)
    comparisons = []
    singles = []

    jumia_products = grouped["jumia"] || []
    konga_products = grouped["konga"] || []

    # Group products by brand+series+model
    jumia_map = jumia_products.group_by do |p|
      specs = parse_specs(p.title)
      [specs[:brand], specs[:series], specs[:model]]
    end
    konga_map = konga_products.group_by do |p|
      specs = parse_specs(p.title)
      [specs[:brand], specs[:series], specs[:model]]
    end

    common_keys = jumia_map.keys & konga_map.keys

    # Build grouped comparisons
    common_keys.each do |key|
      comparisons << {
        brand: key[0],
        series: key[1],
        model: key[2],
        jumia: jumia_map[key].map { |p| product_hash(p) },
        konga: konga_map[key].map { |p| product_hash(p) }
      }
    end

    # Singles = models that don’t overlap
    (jumia_map.keys - common_keys).each do |k|
      jumia_map[k].each { |p| singles << product_hash(p) }
    end
    (konga_map.keys - common_keys).each do |k|
      konga_map[k].each { |p| singles << product_hash(p) }
    end

    [comparisons, singles]
  end

  def product_hash(p)
    {
      id: p.id,
      title: p.title,
      url: p.url,
      price: p.price,
      discount: p.discount,
      image: p.image,
      source: p.source
    }
  end

  def paginate(array)
    array.slice((@page - 1) * @per_page, @per_page) || []
  end
end
