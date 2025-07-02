#!/usr/bin/env python3
"""
Improved Footlocker Checkout Bot
Enhanced with better error handling and authentication
"""

import requests
import json
import logging
import time
import random
from typing import Dict, Optional, List
from urllib.parse import urlencode
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('footlocker_improved.log'),
        logging.StreamHandler()
    ]
)

class ImprovedFootlockerCheckout:
    def __init__(self):
        self.session = requests.Session()
        self.api_base = "https://www.footlocker.com/zgw"
        self.base_url = "https://www.footlocker.com"
        self.cart_id = None
        self.guest_id = None
        
        # Set up session with proper headers
        self._setup_session()
        
    def _setup_session(self):
        """Initialize session with headers and cookies"""
        try:
            # Load cookies from config
            cookies = config.get_all_cookies()
            for name, value in cookies.items():
                if value:  # Only set non-empty cookies
                    self.session.cookies.set(name, str(value))
            
            # Set default headers
            self.session.headers.update({
                'User-Agent': config.USER_AGENT,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            })
            
            logging.info("Session initialized with cookies and headers")
            
        except Exception as e:
            logging.error(f"Error setting up session: {str(e)}")
            
    def _get_tracking_headers(self) -> Dict[str, str]:
        """Get tracking headers for requests"""
        return {
            'newrelic': f'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI2ODQxMjUiLCJhcCI6IjY1NTU1OTQxMSIsImlkIjoiMmVlYzJjZDRhNTAzNzE2NSIsInRyIjoiYWEzNmVmOTQ3NzIxNTZjMTE4YTNlODFlZWQ1ZjljOTUiLCJ0aSI6MTc1MTQxNDAyMzEyNCwidGsiOiIzNjcxMDc3In19',
            'priority': 'u=1, i',
            'referer': f'{self.base_url}/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'traceparent': '00-aa36ef94772156c118a3e81eed5f9c95-2eec2cd4a5037165-01',
            'tracestate': '3671077@nr=0-1-2684125-655559411-2eec2cd4a5037165----1751414023124',
            'x-kpsdk-ct': config.ak_bmsc_fl_com,
            'x-kpsdk-v': 'j-1.1.0'
        }
    
    def initialize_session(self) -> bool:
        """Initialize session by visiting homepage"""
        try:
            logging.info("Initializing session...")
            
            # Visit homepage to establish session
            response = self.session.get(self.base_url)
            
            if response.status_code == 200:
                logging.info("Session initialized successfully")
                return True
            else:
                logging.error(f"Failed to initialize session: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error initializing session: {str(e)}")
            return False
    
    def check_product_availability(self, sku: str) -> Optional[Dict]:
        """Check if product is available and get details"""
        try:
            logging.info(f"Checking availability for SKU: {sku}")
            
            # Use the exact endpoint from your captured requests
            url = f"{self.api_base}/product-core/v1/pdp/sku/{sku}"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': '*/*',
                'x-api-lang': 'en-US'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                product_data = response.json()
                logging.info(f"Product found: {product_data.get('name', 'Unknown')}")
                return product_data
            elif response.status_code == 403:
                logging.error("Access denied - cookies may be expired")
                print("\n🚨 AUTHENTICATION ERROR:")
                print(config.COOKIE_UPDATE_INSTRUCTIONS)
                return None
            else:
                logging.error(f"Product not available: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error checking product availability: {str(e)}")
            return None
    
    def get_fresh_cookies_interactive(self):
        """Interactive method to get fresh cookies"""
        print("\n🍪 COOKIE UPDATE REQUIRED")
        print("=" * 50)
        print(config.COOKIE_UPDATE_INSTRUCTIONS)
        print("\nAfter getting fresh cookies:")
        print("1. Update the values in config.py")
        print("2. Restart this program")
        print("\nPress Enter to continue or Ctrl+C to exit...")
        input()
    
    def test_connection(self) -> bool:
        """Test if connection is working"""
        try:
            logging.info("Testing connection...")
            
            # Try to access a simple endpoint
            url = f"{self.base_url}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                logging.info("✅ Connection test successful")
                return True
            else:
                logging.error(f"❌ Connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Connection test error: {str(e)}")
            return False
    
    def add_to_cart_v2(self, sku: str, size: str, quantity: int = 1) -> bool:
        """Improved add to cart with better error handling"""
        try:
            logging.info(f"Adding to cart: SKU={sku}, Size={size}, Qty={quantity}")
            
            # First check if product is available
            product = self.check_product_availability(sku)
            if not product:
                return False
            
            # Use the captured add to cart endpoint
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/add"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'origin': self.base_url,
                'referer': f'{self.base_url}/product/{sku}.html'
            })
            
            # Build payload based on captured requests
            payload = {
                "productCode": sku,
                "quantity": quantity,
                "size": size,
                "productType": "NORMAL"
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                cart_data = response.json()
                self.cart_id = cart_data.get('cartId')
                logging.info(f"✅ Successfully added to cart. Cart ID: {self.cart_id}")
                return True
            elif response.status_code == 403:
                logging.error("❌ Access denied - authentication required")
                self.get_fresh_cookies_interactive()
                return False
            else:
                logging.error(f"❌ Failed to add to cart: {response.status_code}")
                if response.text:
                    logging.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error adding to cart: {str(e)}")
            return False
    
    def get_cart_info(self) -> Optional[Dict]:
        """Get current cart information"""
        try:
            logging.info("Getting cart information...")
            
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/getUpdatedCart"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'x-api-lang': 'en-US'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                logging.info("✅ Cart information retrieved")
                return cart_data
            else:
                logging.error(f"❌ Failed to get cart info: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting cart info: {str(e)}")
            return None
    
    def display_cart_summary(self, cart_data: Dict):
        """Display cart summary in a nice format"""
        if not cart_data:
            print("❌ No cart data available")
            return
            
        print("\n🛒 CART SUMMARY")
        print("=" * 40)
        print(f"Cart ID: {cart_data.get('cartId', 'N/A')}")
        print(f"Total Items: {cart_data.get('totalUnitCount', 0)}")
        print(f"Subtotal: {cart_data.get('totalPrice', {}).get('formattedValue', 'N/A')}")
        print(f"Total (with tax): {cart_data.get('totalPriceWithTax', {}).get('formattedValue', 'N/A')}")
        
        items = cart_data.get('cartItems', [])
        if items:
            print("\nITEMS:")
            for i, item in enumerate(items, 1):
                name = item.get('name', 'Unknown Product')
                size = item.get('size', 'N/A')
                qty = item.get('quantity', 1)
                price = item.get('priceData', {}).get('formattedValue', 'N/A')
                print(f"{i}. {name}")
                print(f"   Size: {size} | Qty: {qty} | Price: {price}")
        
        print("=" * 40)

def main():
    """Main function with improved UI"""
    print("🚀 Improved Footlocker Checkout Tool")
    print("=" * 50)
    
    checkout = ImprovedFootlockerCheckout()
    
    # Test connection first
    if not checkout.test_connection():
        print("❌ Connection failed. Check your internet connection.")
        return
    
    # Display available products
    print("\nAvailable Products:")
    for key, product in config.PRODUCTS.items():
        print(f"{key}: {product['name']} (${product['price']}) - SKU: {product['sku']}")
        print(f"    Sizes: {', '.join(product['available_sizes'])}")
    
    print("\nOptions:")
    print("1. Test product availability")
    print("2. Add product to cart")
    print("3. View current cart")
    print("4. Update cookies guide")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                # Test product availability
                sku = input("Enter SKU to check: ").strip()
                product = checkout.check_product_availability(sku)
                if product:
                    print(f"✅ Product available: {product.get('name', 'Unknown')}")
                    print(f"Price: {product.get('price', {}).get('formattedValue', 'N/A')}")
                else:
                    print("❌ Product not available or authentication required")
                    
            elif choice == "2":
                # Add to cart
                sku = input("Enter SKU: ").strip()
                size = input("Enter size: ").strip()
                
                if checkout.add_to_cart_v2(sku, size):
                    print("✅ Product added to cart!")
                    
                    # Show cart summary
                    cart = checkout.get_cart_info()
                    if cart:
                        checkout.display_cart_summary(cart)
                else:
                    print("❌ Failed to add product to cart")
                    
            elif choice == "3":
                # View cart
                cart = checkout.get_cart_info()
                if cart:
                    checkout.display_cart_summary(cart)
                else:
                    print("❌ Could not retrieve cart information")
                    
            elif choice == "4":
                # Cookie update guide
                checkout.get_fresh_cookies_interactive()
                
            elif choice == "5":
                # Exit
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
