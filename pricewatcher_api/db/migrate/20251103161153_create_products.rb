class CreateProducts < ActiveRecord::Migration[8.0]
  def change
    create_table :products do |t|
      t.text :url, null: false
      t.text :title, null: false
      t.integer :price
      t.integer :old_price
      t.text :discount
      t.datetime :scraped_at, null: false
      t.string :image
      t.string :source

      t.timestamps
    end

    add_index :products, :url, unique: true
  end
end
