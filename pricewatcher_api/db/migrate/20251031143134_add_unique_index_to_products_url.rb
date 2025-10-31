class AddUniqueIndexToProductsUrl < ActiveRecord::Migration[8.0]
  def change
    add_index :products, :url, unique: true
  end
end
