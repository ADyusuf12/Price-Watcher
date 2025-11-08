module Api
  module V1
    class ComparisonsController < ApplicationController
      def index
        query = params[:q]
        page  = params[:page] || 1
        per_page = params[:per_page] || 20

        return render json: { error: "Missing query" }, status: :bad_request unless query

        result = ProductComparisonQuery.new(query: query, page: page, per_page: per_page).call
        render json: result
      end
    end
  end
end
