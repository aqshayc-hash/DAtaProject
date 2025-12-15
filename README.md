# Warehouse Inventory Management System

A comprehensive Python-based inventory management system for warehouse operations, featuring data management, analytics, and reporting capabilities.

## Features

### Core Functionality
- **CRUD Operations**: Complete Create, Read, Update, Delete operations for inventory items
- **Stock Management**: Track quantities, update stock levels, and manage product information
- **Search & Filter**: Search products by keyword, filter by category or supplier
- **Low Stock Alerts**: Automatic identification of items at or below reorder levels

### Analytics & Reporting
- **Stock Distribution Analysis**: Categorize items by stock levels (critical, low, normal, high)
- **Top Products**: Identify highest-value inventory items
- **Category Analysis**: Comprehensive breakdown by product category
- **Supplier Performance**: Track products and values by supplier
- **Reorder Recommendations**: Smart suggestions for restocking based on current levels

### Data Management
- **CSV Import/Export**: Load and export inventory data
- **JSON Reports**: Generate detailed reports in JSON format
- **Data Persistence**: Automatic saving of changes

## Dataset

The system includes a sample warehouse inventory dataset with 30 products across multiple categories:
- **Electronics**: Laptops, monitors, keyboards, printers, etc.
- **Furniture**: Chairs, desks, cabinets, whiteboards, etc.
- **Stationery**: Notebooks, pens, folders, staplers, etc.

Each product includes:
- Product ID
- Product Name
- Category
- Quantity in stock
- Unit Price
- Reorder Level
- Supplier
- Warehouse Location
- Last Updated Date

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone the repository:
```bash
git clone https://github.com/aqshayc-hash/DAtaProject.git
cd DAtaProject
```

2. No additional dependencies required - uses Python standard library only!

## Usage

### Command Line Interface

Run the interactive CLI:
```bash
python cli.py
```

The CLI provides a menu-driven interface with the following options:
1. View All Products
2. Search Product
3. View Product Details
4. Add New Product
5. Update Product
6. Delete Product
7. Update Stock Quantity
8. View Low Stock Items
9. View Inventory Summary
10. View by Category
11. View by Supplier
12. Analytics & Reports
13. Export Reports

### Python API

Use the inventory manager programmatically:

```python
from inventory_manager import InventoryManager

# Initialize the manager
manager = InventoryManager('data/warehouse_inventory.csv')

# View inventory summary
manager.display_summary()

# Get a specific product
product = manager.get_product('P001')
print(product)

# Update stock quantity
manager.update_quantity('P001', -5)  # Remove 5 units

# Find low stock items
low_stock = manager.get_low_stock_items()
print(f"Low stock items: {len(low_stock)}")

# Get products by category
electronics = manager.get_inventory_by_category('Electronics')

# Calculate total inventory value
total_value = manager.get_total_inventory_value()
print(f"Total inventory value: ${total_value:,.2f}")
```

### Analytics

Use the analytics module for advanced insights:

```python
from inventory_manager import InventoryManager
from analytics import InventoryAnalytics

manager = InventoryManager()
analytics = InventoryAnalytics(manager)

# Show stock distribution
analytics.show_stock_distribution()

# Show top products by value
analytics.show_top_products_by_value(10)

# Show category analysis
analytics.show_category_analysis()

# Show supplier performance
analytics.show_supplier_performance()

# Show reorder recommendations
analytics.show_reorder_recommendations()

# Export reports
analytics.export_inventory_csv('my_export.csv')
analytics.export_low_stock_json('low_stock.json')
analytics.export_category_summary_json('categories.json')
```

## Project Structure

```
DAtaProject/
├── data/
│   └── warehouse_inventory.csv    # Sample inventory dataset
├── inventory_manager.py            # Core inventory management class
├── analytics.py                    # Analytics and reporting module
├── cli.py                          # Command-line interface
├── demo.py                         # Demonstration script
├── README.md                       # This file
└── requirements.txt                # Python dependencies (empty - no external deps)
```

## Example Operations

### Adding a New Product
```python
manager.add_product({
    'product_id': 'P031',
    'product_name': 'USB Hub',
    'category': 'Electronics',
    'quantity': '100',
    'unit_price': '19.99',
    'reorder_level': '25',
    'supplier': 'TechSupply Inc',
    'warehouse_location': 'A-01-29'
})
```

### Updating Product Information
```python
manager.update_product('P001', {
    'quantity': '50',
    'unit_price': '849.99'
})
```

### Searching Products
```python
# Search by keyword
results = manager.search_products('laptop')

# Get by category
electronics = manager.get_inventory_by_category('Electronics')

# Get by supplier
tech_products = manager.get_inventory_by_supplier('TechSupply')
```

### Generating Reports
```python
# Get category summary
summary = manager.get_category_summary()
for category, stats in summary.items():
    print(f"{category}: {stats['count']} products, ${stats['total_value']:,.2f}")

# Check inventory value
total = manager.get_total_inventory_value()
print(f"Total inventory value: ${total:,.2f}")
```

## Data Format

The inventory CSV file follows this format:

```csv
product_id,product_name,category,quantity,unit_price,reorder_level,supplier,warehouse_location,last_updated
P001,Laptop Computer,Electronics,45,899.99,10,TechSupply Inc,A-01-15,2024-01-15
```

## Features in Detail

### Inventory Management
- **Add Products**: Add new items with complete details
- **Update Products**: Modify any product information
- **Delete Products**: Remove items from inventory (with confirmation)
- **Stock Updates**: Increment or decrement quantities with validation

### Analytics
- **Stock Distribution**: Categorizes stock levels as critical, low, normal, or high
- **Value Analysis**: Identifies top products by inventory value
- **Category Insights**: Breaks down inventory by category with totals
- **Supplier Tracking**: Monitors products and values per supplier
- **Reorder Intelligence**: Suggests order quantities based on reorder levels

### Reporting
- **CSV Export**: Export full inventory to CSV
- **JSON Reports**: Generate structured JSON reports
- **Low Stock Reports**: Detailed reports on items needing restock
- **Category Summaries**: Category-wise inventory breakdown

## Contributing

This is an educational project demonstrating inventory management concepts. Feel free to:
- Add new features
- Improve analytics
- Enhance the UI
- Add data visualizations
- Implement additional export formats

## License

Open source - feel free to use and modify for your needs.

## Author

DataProject - Warehouse Inventory Management System
