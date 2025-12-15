"""
Inventory Management System
A comprehensive system for managing warehouse inventory data
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import json


class InventoryManager:
    """Main class for managing warehouse inventory operations"""
    
    def __init__(self, data_file: str = 'data/warehouse_inventory.csv'):
        """
        Initialize the inventory manager
        
        Args:
            data_file: Path to the CSV file containing inventory data
        """
        self.data_file = data_file
        self.inventory = []
        self.load_inventory()
    
    def load_inventory(self):
        """Load inventory data from CSV file"""
        if not os.path.exists(self.data_file):
            print(f"Warning: Data file '{self.data_file}' not found. Starting with empty inventory.")
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.inventory = list(reader)
            print(f"✓ Loaded {len(self.inventory)} items from inventory")
        except Exception as e:
            print(f"Error loading inventory: {e}")
            self.inventory = []
    
    def save_inventory(self):
        """Save current inventory data to CSV file"""
        if not self.inventory:
            print("Warning: No inventory data to save")
            return
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8', newline='') as file:
                fieldnames = self.inventory[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.inventory)
            print(f"✓ Saved {len(self.inventory)} items to inventory")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def add_product(self, product_data: Dict):
        """
        Add a new product to inventory
        
        Args:
            product_data: Dictionary containing product information
        """
        product_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        self.inventory.append(product_data)
        self.save_inventory()
        print(f"✓ Added product: {product_data.get('product_name', 'Unknown')}")
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """
        Get product by ID
        
        Args:
            product_id: Product ID to search for
            
        Returns:
            Product dictionary if found, None otherwise
        """
        for product in self.inventory:
            if product['product_id'] == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, updates: Dict):
        """
        Update product information
        
        Args:
            product_id: Product ID to update
            updates: Dictionary of fields to update
        """
        for product in self.inventory:
            if product['product_id'] == product_id:
                product.update(updates)
                product['last_updated'] = datetime.now().strftime('%Y-%m-%d')
                self.save_inventory()
                print(f"✓ Updated product: {product_id}")
                return True
        print(f"✗ Product not found: {product_id}")
        return False
    
    def delete_product(self, product_id: str):
        """
        Delete product from inventory
        
        Args:
            product_id: Product ID to delete
        """
        initial_len = len(self.inventory)
        self.inventory = [p for p in self.inventory if p['product_id'] != product_id]
        
        if len(self.inventory) < initial_len:
            self.save_inventory()
            print(f"✓ Deleted product: {product_id}")
            return True
        else:
            print(f"✗ Product not found: {product_id}")
            return False
    
    def update_quantity(self, product_id: str, quantity_change: int):
        """
        Update product quantity (add or remove stock)
        
        Args:
            product_id: Product ID to update
            quantity_change: Quantity to add (positive) or remove (negative)
        """
        product = self.get_product(product_id)
        if product:
            current_qty = int(product['quantity'])
            new_qty = current_qty + quantity_change
            
            if new_qty < 0:
                print(f"✗ Error: Cannot reduce quantity below 0 (current: {current_qty}, change: {quantity_change})")
                return False
            
            self.update_product(product_id, {'quantity': str(new_qty)})
            print(f"✓ Quantity updated: {current_qty} → {new_qty}")
            return True
        return False
    
    def get_low_stock_items(self) -> List[Dict]:
        """
        Get items that are at or below reorder level
        
        Returns:
            List of products with low stock
        """
        low_stock = []
        for product in self.inventory:
            if int(product['quantity']) <= int(product['reorder_level']):
                low_stock.append(product)
        return low_stock
    
    def get_inventory_by_category(self, category: str) -> List[Dict]:
        """
        Get all products in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of products in the category
        """
        return [p for p in self.inventory if p['category'].lower() == category.lower()]
    
    def get_inventory_by_supplier(self, supplier: str) -> List[Dict]:
        """
        Get all products from a specific supplier
        
        Args:
            supplier: Supplier name
            
        Returns:
            List of products from the supplier
        """
        return [p for p in self.inventory if supplier.lower() in p['supplier'].lower()]
    
    def get_total_inventory_value(self) -> float:
        """
        Calculate total inventory value
        
        Returns:
            Total value of all inventory
        """
        total = 0.0
        for product in self.inventory:
            quantity = int(product['quantity'])
            unit_price = float(product['unit_price'])
            total += quantity * unit_price
        return total
    
    def get_category_summary(self) -> Dict[str, Dict]:
        """
        Get summary statistics by category
        
        Returns:
            Dictionary with category statistics
        """
        summary = {}
        for product in self.inventory:
            category = product['category']
            if category not in summary:
                summary[category] = {
                    'count': 0,
                    'total_quantity': 0,
                    'total_value': 0.0
                }
            
            summary[category]['count'] += 1
            summary[category]['total_quantity'] += int(product['quantity'])
            summary[category]['total_value'] += int(product['quantity']) * float(product['unit_price'])
        
        return summary
    
    def search_products(self, keyword: str) -> List[Dict]:
        """
        Search products by keyword in name or category
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching products
        """
        keyword_lower = keyword.lower()
        results = []
        for product in self.inventory:
            if (keyword_lower in product['product_name'].lower() or
                keyword_lower in product['category'].lower()):
                results.append(product)
        return results
    
    def display_product(self, product: Dict):
        """Display product information in a formatted way"""
        print("\n" + "="*60)
        for key, value in product.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("="*60)
    
    def display_summary(self):
        """Display inventory summary statistics"""
        print("\n" + "="*60)
        print("INVENTORY SUMMARY")
        print("="*60)
        print(f"Total Products: {len(self.inventory)}")
        print(f"Total Inventory Value: ${self.get_total_inventory_value():,.2f}")
        
        low_stock = self.get_low_stock_items()
        print(f"Low Stock Items: {len(low_stock)}")
        
        print("\nCategory Breakdown:")
        category_summary = self.get_category_summary()
        for category, stats in category_summary.items():
            print(f"  {category}:")
            print(f"    - Products: {stats['count']}")
            print(f"    - Total Quantity: {stats['total_quantity']}")
            print(f"    - Total Value: ${stats['total_value']:,.2f}")
        print("="*60 + "\n")
