#!/usr/bin/env python
"""
Demo script for Warehouse Inventory Management System
Demonstrates key features and capabilities
"""

from inventory_manager import InventoryManager
from analytics import InventoryAnalytics
import time


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def pause():
    """Pause for demo effect"""
    time.sleep(1)


def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "WAREHOUSE INVENTORY MANAGEMENT SYSTEM" + " "*16 + "║")
    print("║" + " "*26 + "DEMO SCRIPT" + " "*31 + "║")
    print("╚" + "="*68 + "╝")
    
    # Initialize system
    print_header("1. INITIALIZING SYSTEM")
    manager = InventoryManager('data/warehouse_inventory.csv')
    analytics = InventoryAnalytics(manager)
    pause()
    
    # Display inventory summary
    print_header("2. INVENTORY OVERVIEW")
    manager.display_summary()
    pause()
    
    # Show stock distribution
    print_header("3. STOCK LEVEL DISTRIBUTION")
    analytics.show_stock_distribution()
    pause()
    
    # Show top products
    print_header("4. TOP 5 PRODUCTS BY VALUE")
    analytics.show_top_products_by_value(5)
    pause()
    
    # Show category analysis
    print_header("5. CATEGORY ANALYSIS")
    analytics.show_category_analysis()
    pause()
    
    # Show supplier performance
    print_header("6. SUPPLIER PERFORMANCE")
    analytics.show_supplier_performance()
    pause()
    
    # Demo search functionality
    print_header("7. PRODUCT SEARCH DEMO")
    print("Searching for 'laptop'...")
    results = manager.search_products('laptop')
    for product in results:
        print(f"\n  Found: {product['product_name']} ({product['product_id']})")
        print(f"  Category: {product['category']}, Price: ${product['unit_price']}, Qty: {product['quantity']}")
    pause()
    
    # Demo quantity update
    print_header("8. STOCK QUANTITY UPDATE DEMO")
    print("Simulating sale: Removing 5 units from Laptop Computer (P001)...")
    original_qty = manager.get_product('P001')['quantity']
    manager.update_quantity('P001', -5)
    new_qty = manager.get_product('P001')['quantity']
    print(f"  Previous quantity: {original_qty}")
    print(f"  New quantity: {new_qty}")
    
    # Restore original quantity
    print("\nRestoring original quantity...")
    manager.update_quantity('P001', 5)
    pause()
    
    # Show products by category
    print_header("9. VIEW BY CATEGORY - ELECTRONICS")
    electronics = manager.get_inventory_by_category('Electronics')
    print(f"Found {len(electronics)} electronics products:\n")
    for i, product in enumerate(electronics[:5], 1):
        print(f"  {i}. {product['product_name']} - Qty: {product['quantity']}, Price: ${product['unit_price']}")
    if len(electronics) > 5:
        print(f"  ... and {len(electronics) - 5} more")
    pause()
    
    # Show reorder recommendations
    print_header("10. REORDER RECOMMENDATIONS")
    # Temporarily reduce stock to demonstrate low stock alerts
    print("Simulating low stock scenarios for demo...")
    manager.update_quantity('P010', -10)  # Reduce Printer stock
    manager.update_quantity('P017', -7)   # Reduce Paper Shredder stock
    
    analytics.show_reorder_recommendations()
    
    # Restore stock
    print("Restoring stock levels...")
    manager.update_quantity('P010', 10)
    manager.update_quantity('P017', 7)
    pause()
    
    # Export demo
    print_header("11. DATA EXPORT CAPABILITIES")
    print("Exporting reports to /tmp/demo_* files...")
    analytics.export_inventory_csv('/tmp/demo_inventory.csv')
    analytics.export_low_stock_json('/tmp/demo_low_stock.json')
    analytics.export_category_summary_json('/tmp/demo_categories.json')
    print("\n✓ Reports exported successfully!")
    pause()
    
    # Summary
    print_header("12. DEMO COMPLETE")
    print("Key Features Demonstrated:")
    print("  ✓ Inventory loading and management")
    print("  ✓ Comprehensive analytics and reporting")
    print("  ✓ Stock distribution analysis")
    print("  ✓ Product search and filtering")
    print("  ✓ Real-time quantity updates")
    print("  ✓ Category and supplier views")
    print("  ✓ Reorder recommendations")
    print("  ✓ Data export (CSV/JSON)")
    print("\nFor interactive usage, run: python cli.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
