# app/controllers/api/v1/comparisons_controller.rb
module Api
  module V1
    class ComparisonsController < ApplicationController
      def index
        query = params[:q]
        return render json: { error: "Missing query" }, status: :bad_request unless query

        products = Product.where("title ILIKE ?", "%#{query}%")
        grouped  = products.group_by(&:source)

        # Build side-by-side comparisons if both sources exist
        comparisons = []
        if grouped["jumia"] && grouped["konga"]
          grouped["jumia"].each do |jumia_product|
            grouped["konga"].each do |konga_product|
              next unless jumia_product.price && konga_product.price

              comparisons << {
                jumia: {
                  id: jumia_product.id,
                  title: jumia_product.title,
                  price: jumia_product.price,
                  discount: jumia_product.discount
                },
                konga: {
                  id: konga_product.id,
                  title: konga_product.title,
                  price: konga_product.price,
                  discount: konga_product.discount
                },
                price_difference: (jumia_product.price - konga_product.price)
              }
            end
          end
        end

        render json: {
          query: query,
          results: grouped.transform_values { |arr| arr.map { |p| { id: p.id, title: p.title, price: p.price, discount: p.discount } } },
          comparisons: comparisons
        }
      end
    end
  end
end
