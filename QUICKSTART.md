# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/aqshayc-hash/DAtaProject.git
cd DAtaProject
```

### Step 2: Run the Demo (Optional)
```bash
python demo.py
```
This will showcase all features of the inventory management system.

### Step 3: Use the Interactive CLI
```bash
python cli.py
```
Navigate through the menu to manage your inventory.

## Quick Examples

### Python Script Usage
```python
from inventory_manager import InventoryManager

# Load inventory
manager = InventoryManager('data/warehouse_inventory.csv')

# View summary
manager.display_summary()

# Search for products
laptops = manager.search_products('laptop')
for product in laptops:
    print(f"{product['product_name']}: ${product['unit_price']}")

# Update stock
manager.update_quantity('P001', -5)  # Remove 5 units

# Check low stock
low_stock = manager.get_low_stock_items()
print(f"Items needing restock: {len(low_stock)}")
```

### Analytics Usage
```python
from inventory_manager import InventoryManager
from analytics import InventoryAnalytics

manager = InventoryManager()
analytics = InventoryAnalytics(manager)

# Show top products
analytics.show_top_products_by_value(10)

# Export reports
analytics.export_inventory_csv('my_inventory.csv')
analytics.export_low_stock_json('reorder_list.json')
```

## Key Features

### Menu Options
- **View All Products**: Display complete inventory in table format
- **Search Product**: Find products by keyword
- **View Product Details**: Get detailed info for specific product
- **Add New Product**: Add items to inventory
- **Update Product**: Modify product information
- **Delete Product**: Remove items from inventory
- **Update Stock Quantity**: Adjust stock levels
- **View Low Stock Items**: See items at/below reorder level
- **View Inventory Summary**: Overview of entire inventory
- **View by Category**: Filter by product category
- **View by Supplier**: Filter by supplier
- **Analytics & Reports**: Advanced analytics menu
- **Export Reports**: Export data to CSV/JSON

### Analytics Features
1. **Stock Level Distribution**: Categorize items by stock status
2. **Top Products by Value**: Identify highest-value inventory
3. **Category Analysis**: Breakdown by category
4. **Supplier Performance**: Metrics per supplier
5. **Reorder Recommendations**: Smart restocking suggestions

## Common Tasks

### Adding a New Product
1. Select option 4 from main menu
2. Enter product details when prompted
3. Product is automatically saved to inventory

### Checking What Needs Reordering
1. Select option 8 from main menu
2. View all items at or below reorder level
3. Or use option 12 → 5 for detailed recommendations

### Exporting Inventory
1. Select option 13 from main menu
2. Choose export format (CSV or JSON)
3. Enter filename or use default
4. File is saved in current directory

### Searching for Products
1. Select option 2 from main menu
2. Enter keyword (searches name and category)
3. View matching results in table format

## Dataset Information

The sample dataset includes:
- **30 products** across 3 categories
- **Electronics**: 14 items (laptops, monitors, keyboards, etc.)
- **Furniture**: 8 items (chairs, desks, cabinets, etc.)
- **Stationery**: 8 items (notebooks, pens, folders, etc.)

Total inventory value: **$189,017.39**

## Tips

- The system automatically saves changes to the CSV file
- Use search functionality to quickly find products
- Check low stock items regularly to maintain inventory
- Export reports for external analysis
- Use the demo script to see all features in action

## Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## Support

For issues or questions, refer to the main README.md for detailed documentation.
