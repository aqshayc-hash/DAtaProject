"""
CLI Interface for Inventory Management System
Interactive command-line interface for managing warehouse inventory
"""

import sys
from inventory_manager import InventoryManager
from analytics import InventoryAnalytics


def print_menu():
    """Display main menu options"""
    print("\n" + "="*60)
    print("WAREHOUSE INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("1.  View All Products")
    print("2.  Search Product")
    print("3.  View Product Details")
    print("4.  Add New Product")
    print("5.  Update Product")
    print("6.  Delete Product")
    print("7.  Update Stock Quantity")
    print("8.  View Low Stock Items")
    print("9.  View Inventory Summary")
    print("10. View by Category")
    print("11. View by Supplier")
    print("12. Analytics & Reports")
    print("13. Export Reports")
    print("0.  Exit")
    print("="*60)


def print_analytics_menu():
    """Display analytics menu options"""
    print("\n" + "="*60)
    print("ANALYTICS & REPORTS")
    print("="*60)
    print("1. Stock Level Distribution")
    print("2. Top Products by Value")
    print("3. Category Analysis")
    print("4. Supplier Performance")
    print("5. Reorder Recommendations")
    print("0. Back to Main Menu")
    print("="*60)


def display_products_table(products):
    """Display products in a formatted table"""
    if not products:
        print("\nNo products found.")
        return
    
    print("\n" + "-"*140)
    print(f"{'ID':<8} {'Name':<25} {'Category':<15} {'Qty':<6} {'Price':<10} {'Reorder':<8} {'Location':<12} {'Supplier':<20}")
    print("-"*140)
    
    for product in products:
        print(f"{product['product_id']:<8} "
              f"{product['product_name']:<25} "
              f"{product['category']:<15} "
              f"{product['quantity']:<6} "
              f"${float(product['unit_price']):<9.2f} "
              f"{product['reorder_level']:<8} "
              f"{product['warehouse_location']:<12} "
              f"{product['supplier']:<20}")
    
    print("-"*140)
    print(f"Total: {len(products)} products\n")


def handle_view_all(manager):
    """Handle view all products"""
    display_products_table(manager.inventory)


def handle_search(manager):
    """Handle product search"""
    keyword = input("Enter search keyword: ").strip()
    if keyword:
        results = manager.search_products(keyword)
        print(f"\nFound {len(results)} products matching '{keyword}':")
        display_products_table(results)


def handle_view_details(manager):
    """Handle view product details"""
    product_id = input("Enter Product ID: ").strip()
    product = manager.get_product(product_id)
    if product:
        manager.display_product(product)
    else:
        print(f"✗ Product '{product_id}' not found.")


def handle_add_product(manager):
    """Handle add new product"""
    print("\nAdd New Product")
    print("-"*60)
    
    try:
        product_data = {
            'product_id': input("Product ID: ").strip(),
            'product_name': input("Product Name: ").strip(),
            'category': input("Category: ").strip(),
            'quantity': input("Quantity: ").strip(),
            'unit_price': input("Unit Price: ").strip(),
            'reorder_level': input("Reorder Level: ").strip(),
            'supplier': input("Supplier: ").strip(),
            'warehouse_location': input("Warehouse Location: ").strip(),
        }
        
        # Validate required fields
        if not all(product_data.values()):
            print("✗ Error: All fields are required.")
            return
        
        # Check if product ID already exists
        if manager.get_product(product_data['product_id']):
            print(f"✗ Error: Product ID '{product_data['product_id']}' already exists.")
            return
        
        manager.add_product(product_data)
    except Exception as e:
        print(f"✗ Error adding product: {e}")


def handle_update_product(manager):
    """Handle update product"""
    product_id = input("Enter Product ID to update: ").strip()
    product = manager.get_product(product_id)
    
    if not product:
        print(f"✗ Product '{product_id}' not found.")
        return
    
    print("\nCurrent Product Details:")
    manager.display_product(product)
    
    print("\nEnter new values (press Enter to keep current value):")
    updates = {}
    
    fields = ['product_name', 'category', 'quantity', 'unit_price', 
              'reorder_level', 'supplier', 'warehouse_location']
    
    for field in fields:
        value = input(f"{field.replace('_', ' ').title()} [{product[field]}]: ").strip()
        if value:
            updates[field] = value
    
    if updates:
        manager.update_product(product_id, updates)
    else:
        print("No updates made.")


def handle_delete_product(manager):
    """Handle delete product"""
    product_id = input("Enter Product ID to delete: ").strip()
    product = manager.get_product(product_id)
    
    if not product:
        print(f"✗ Product '{product_id}' not found.")
        return
    
    manager.display_product(product)
    confirm = input("\nAre you sure you want to delete this product? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        manager.delete_product(product_id)
    else:
        print("Deletion cancelled.")


def handle_update_quantity(manager):
    """Handle update stock quantity"""
    product_id = input("Enter Product ID: ").strip()
    product = manager.get_product(product_id)
    
    if not product:
        print(f"✗ Product '{product_id}' not found.")
        return
    
    print(f"\nCurrent quantity: {product['quantity']}")
    print("Enter quantity change (positive to add, negative to remove):")
    
    try:
        change = int(input("Quantity change: ").strip())
        manager.update_quantity(product_id, change)
    except ValueError:
        print("✗ Error: Please enter a valid integer.")


def handle_low_stock(manager):
    """Handle view low stock items"""
    low_stock = manager.get_low_stock_items()
    print(f"\n⚠ Low Stock Items (at or below reorder level): {len(low_stock)}")
    display_products_table(low_stock)


def handle_view_by_category(manager):
    """Handle view by category"""
    # Get unique categories
    categories = set(p['category'] for p in manager.inventory)
    print("\nAvailable Categories:")
    for cat in sorted(categories):
        print(f"  - {cat}")
    
    category = input("\nEnter category name: ").strip()
    products = manager.get_inventory_by_category(category)
    print(f"\nProducts in '{category}' category:")
    display_products_table(products)


def handle_view_by_supplier(manager):
    """Handle view by supplier"""
    # Get unique suppliers
    suppliers = set(p['supplier'] for p in manager.inventory)
    print("\nAvailable Suppliers:")
    for sup in sorted(suppliers):
        print(f"  - {sup}")
    
    supplier = input("\nEnter supplier name: ").strip()
    products = manager.get_inventory_by_supplier(supplier)
    print(f"\nProducts from '{supplier}':")
    display_products_table(products)


def handle_analytics(manager):
    """Handle analytics menu"""
    analytics = InventoryAnalytics(manager)
    
    while True:
        print_analytics_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            analytics.show_stock_distribution()
        elif choice == '2':
            analytics.show_top_products_by_value()
        elif choice == '3':
            analytics.show_category_analysis()
        elif choice == '4':
            analytics.show_supplier_performance()
        elif choice == '5':
            analytics.show_reorder_recommendations()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def handle_export(manager):
    """Handle export reports"""
    analytics = InventoryAnalytics(manager)
    
    print("\n" + "="*60)
    print("EXPORT REPORTS")
    print("="*60)
    print("1. Export Full Inventory (CSV)")
    print("2. Export Low Stock Report (JSON)")
    print("3. Export Category Summary (JSON)")
    print("0. Cancel")
    print("="*60)
    
    choice = input("\nSelect export option: ").strip()
    
    if choice == '1':
        filename = input("Enter filename (default: inventory_export.csv): ").strip()
        if not filename:
            filename = "inventory_export.csv"
        analytics.export_inventory_csv(filename)
    elif choice == '2':
        filename = input("Enter filename (default: low_stock_report.json): ").strip()
        if not filename:
            filename = "low_stock_report.json"
        analytics.export_low_stock_json(filename)
    elif choice == '3':
        filename = input("Enter filename (default: category_summary.json): ").strip()
        if not filename:
            filename = "category_summary.json"
        analytics.export_category_summary_json(filename)


def main():
    """Main CLI loop"""
    print("\nInitializing Inventory Management System...")
    manager = InventoryManager()
    
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '0':
            print("\nThank you for using the Inventory Management System!")
            sys.exit(0)
        elif choice == '1':
            handle_view_all(manager)
        elif choice == '2':
            handle_search(manager)
        elif choice == '3':
            handle_view_details(manager)
        elif choice == '4':
            handle_add_product(manager)
        elif choice == '5':
            handle_update_product(manager)
        elif choice == '6':
            handle_delete_product(manager)
        elif choice == '7':
            handle_update_quantity(manager)
        elif choice == '8':
            handle_low_stock(manager)
        elif choice == '9':
            manager.display_summary()
        elif choice == '10':
            handle_view_by_category(manager)
        elif choice == '11':
            handle_view_by_supplier(manager)
        elif choice == '12':
            handle_analytics(manager)
        elif choice == '13':
            handle_export(manager)
        else:
            print("✗ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
