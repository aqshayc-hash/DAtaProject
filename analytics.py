"""
Analytics Module for Inventory Management System
Provides advanced analytics and reporting capabilities
"""

import json
import csv
from collections import defaultdict
from typing import Dict, List


class InventoryAnalytics:
    """Analytics and reporting for inventory data"""
    
    def __init__(self, manager):
        """
        Initialize analytics with inventory manager
        
        Args:
            manager: InventoryManager instance
        """
        self.manager = manager
    
    def show_stock_distribution(self):
        """Display stock level distribution"""
        print("\n" + "="*60)
        print("STOCK LEVEL DISTRIBUTION")
        print("="*60)
        
        # Categorize stock levels
        critical = []  # 0-25% of reorder level
        low = []       # 25-100% of reorder level
        normal = []    # 100-200% of reorder level
        high = []      # > 200% of reorder level
        
        for product in self.manager.inventory:
            qty = int(product['quantity'])
            reorder = int(product['reorder_level'])
            
            if qty == 0:
                critical.append(product)
            elif qty <= reorder * 0.25:
                critical.append(product)
            elif qty <= reorder:
                low.append(product)
            elif qty <= reorder * 2:
                normal.append(product)
            else:
                high.append(product)
        
        print(f"Critical (≤25% of reorder): {len(critical)} products")
        print(f"Low (25-100% of reorder):   {len(low)} products")
        print(f"Normal (100-200% reorder):  {len(normal)} products")
        print(f"High (>200% of reorder):    {len(high)} products")
        
        if critical:
            print(f"\n⚠ CRITICAL STOCK ITEMS:")
            for p in critical:
                print(f"  - {p['product_id']}: {p['product_name']} (Qty: {p['quantity']}, Reorder: {p['reorder_level']})")
        
        print("="*60 + "\n")
    
    def show_top_products_by_value(self, top_n: int = 10):
        """
        Display top products by inventory value
        
        Args:
            top_n: Number of top products to show
        """
        print("\n" + "="*60)
        print(f"TOP {top_n} PRODUCTS BY INVENTORY VALUE")
        print("="*60)
        
        # Calculate value for each product
        products_with_value = []
        for product in self.manager.inventory:
            qty = int(product['quantity'])
            price = float(product['unit_price'])
            value = qty * price
            products_with_value.append((product, value))
        
        # Sort by value descending
        products_with_value.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n{'Rank':<6} {'Product ID':<10} {'Product Name':<30} {'Quantity':<10} {'Value':<15}")
        print("-"*75)
        
        for i, (product, value) in enumerate(products_with_value[:top_n], 1):
            print(f"{i:<6} {product['product_id']:<10} {product['product_name']:<30} "
                  f"{product['quantity']:<10} ${value:>12,.2f}")
        
        print("="*60 + "\n")
    
    def show_category_analysis(self):
        """Display detailed category analysis"""
        print("\n" + "="*60)
        print("CATEGORY ANALYSIS")
        print("="*60)
        
        summary = self.manager.get_category_summary()
        
        # Sort by total value descending
        sorted_categories = sorted(summary.items(), 
                                  key=lambda x: x[1]['total_value'], 
                                  reverse=True)
        
        total_value = sum(cat['total_value'] for cat in summary.values())
        
        print(f"\n{'Category':<20} {'Products':<10} {'Quantity':<12} {'Value':<15} {'% of Total':<12}")
        print("-"*75)
        
        for category, stats in sorted_categories:
            percentage = (stats['total_value'] / total_value * 100) if total_value > 0 else 0
            print(f"{category:<20} {stats['count']:<10} {stats['total_quantity']:<12} "
                  f"${stats['total_value']:>12,.2f} {percentage:>10.1f}%")
        
        print("-"*75)
        print(f"{'TOTAL':<20} {len(self.manager.inventory):<10} "
              f"{sum(int(p['quantity']) for p in self.manager.inventory):<12} "
              f"${total_value:>12,.2f} {100.0:>10.1f}%")
        print("="*60 + "\n")
    
    def show_supplier_performance(self):
        """Display supplier performance metrics"""
        print("\n" + "="*60)
        print("SUPPLIER PERFORMANCE")
        print("="*60)
        
        supplier_data = defaultdict(lambda: {
            'products': 0,
            'total_quantity': 0,
            'total_value': 0.0,
            'low_stock_items': 0
        })
        
        for product in self.manager.inventory:
            supplier = product['supplier']
            qty = int(product['quantity'])
            value = qty * float(product['unit_price'])
            
            supplier_data[supplier]['products'] += 1
            supplier_data[supplier]['total_quantity'] += qty
            supplier_data[supplier]['total_value'] += value
            
            if qty <= int(product['reorder_level']):
                supplier_data[supplier]['low_stock_items'] += 1
        
        # Sort by total value descending
        sorted_suppliers = sorted(supplier_data.items(), 
                                 key=lambda x: x[1]['total_value'], 
                                 reverse=True)
        
        print(f"\n{'Supplier':<25} {'Products':<10} {'Quantity':<12} {'Value':<15} {'Low Stock':<12}")
        print("-"*80)
        
        for supplier, data in sorted_suppliers:
            print(f"{supplier:<25} {data['products']:<10} {data['total_quantity']:<12} "
                  f"${data['total_value']:>12,.2f} {data['low_stock_items']:<12}")
        
        print("="*60 + "\n")
    
    def show_reorder_recommendations(self):
        """Display reorder recommendations"""
        print("\n" + "="*60)
        print("REORDER RECOMMENDATIONS")
        print("="*60)
        
        low_stock = self.manager.get_low_stock_items()
        
        if not low_stock:
            print("\n✓ All products are adequately stocked!")
            print("="*60 + "\n")
            return
        
        print(f"\n{len(low_stock)} products need reordering:\n")
        
        # Group by supplier
        by_supplier = defaultdict(list)
        for product in low_stock:
            by_supplier[product['supplier']].append(product)
        
        for supplier, products in sorted(by_supplier.items()):
            print(f"\n📦 {supplier}:")
            print("-"*60)
            
            for product in products:
                qty = int(product['quantity'])
                reorder = int(product['reorder_level'])
                shortage = reorder * 2 - qty  # Recommend restocking to 2x reorder level
                
                print(f"  {product['product_id']}: {product['product_name']}")
                print(f"    Current: {qty} | Reorder Level: {reorder} | Recommended Order: {shortage} units")
        
        print("\n" + "="*60 + "\n")
    
    def export_inventory_csv(self, filename: str = "inventory_export.csv"):
        """
        Export full inventory to CSV
        
        Args:
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                if self.manager.inventory:
                    fieldnames = self.manager.inventory[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.manager.inventory)
            print(f"✓ Inventory exported to '{filename}'")
        except Exception as e:
            print(f"✗ Error exporting inventory: {e}")
    
    def export_low_stock_json(self, filename: str = "low_stock_report.json"):
        """
        Export low stock items to JSON
        
        Args:
            filename: Output filename
        """
        try:
            low_stock = self.manager.get_low_stock_items()
            report = {
                'generated_at': __import__('datetime').datetime.now().isoformat(),
                'total_low_stock_items': len(low_stock),
                'items': low_stock
            }
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2)
            
            print(f"✓ Low stock report exported to '{filename}'")
        except Exception as e:
            print(f"✗ Error exporting low stock report: {e}")
    
    def export_category_summary_json(self, filename: str = "category_summary.json"):
        """
        Export category summary to JSON
        
        Args:
            filename: Output filename
        """
        try:
            summary = self.manager.get_category_summary()
            report = {
                'generated_at': __import__('datetime').datetime.now().isoformat(),
                'total_categories': len(summary),
                'categories': summary
            }
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2)
            
            print(f"✓ Category summary exported to '{filename}'")
        except Exception as e:
            print(f"✗ Error exporting category summary: {e}")
