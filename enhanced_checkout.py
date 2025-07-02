#!/usr/bin/env python3
"""
Enhanced Footlocker Checkout Script with Cookie Management
==========================================================

This enhanced version uses browser cookies and session data
for more reliable checkout automation.

Usage:
1. Update config.py with your current browser cookies
2. Run this script to perform checkout
3. Monitor the logs for progress

"""

import requests
import json
import time
import random
import logging
from typing import Dict, List, Optional
from urllib.parse import quote, unquote
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('footlocker_enhanced.log'),
        logging.StreamHandler()
    ]
)

class EnhancedFootlockerCheckout:
    """Enhanced Footlocker checkout with real browser session cookies"""
    
    def __init__(self, use_config_cookies=True):
        self.session = requests.Session()
        self.base_url = "https://www.footlocker.com"
        self.api_base = "https://www.footlocker.com/zgw"
        self.cart_id = None
        self.guest_id = None
        
        # Load cookies from config if requested
        if use_config_cookies:
            self._load_config_cookies()
        
        self._setup_session()
        
    def _load_config_cookies(self):
        """Load cookies from config file"""
        try:
            # Set cookies from config
            cookie_data = {
                'ZGWID': config.ZGWID,
                'JSESSIONID': config.JSESSIONID,
                'AMCV_40A3741F578E26BA7F000101%40AdobeOrg': config.AMCV_40A3741F578E26BA7F000101_40AdobeOrg,
                'ConstructorioID_client_id': config.ConstructorioID_client_id,
                'ConstructorioID_session': config.ConstructorioID_session,
                'ConstructorioID_session_id': config.ConstructorioID_session_id,
                '_ga': config._ga,
                '_cs_id': config._cs_id,
                '__attentive_id': config.__attentive_id,
                '__attentive_dv': config.__attentive_dv,
                'at_check': 'true',
                's_cc': 'true',
                'termsofuse_consentv2': 'true',
                'bluecoreNV': 'true'
            }
            
            for name, value in cookie_data.items():
                self.session.cookies.set(name, value, domain='.footlocker.com')
                
            logging.info("Loaded cookies from config")
            
        except Exception as e:
            logging.warning(f"Could not load config cookies: {str(e)}")
    
    def _setup_session(self):
        """Setup session with headers from config"""
        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': getattr(config, 'USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://www.footlocker.com/',
            'origin': 'https://www.footlocker.com'
        })

    def _get_tracking_headers(self) -> Dict[str, str]:
        """Generate realistic tracking headers"""
        timestamp = str(int(time.time() * 1000))
        trace_id = ''.join([random.choice('0123456789abcdef') for _ in range(32)])
        span_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
        request_id = f'{"".join([random.choice("0123456789abcdef") for _ in range(8)])}-56d8-11f0-af56-{"".join([random.choice("0123456789abcdef") for _ in range(12)])}'
        
        return {
            'newrelic': json.dumps({
                "v": [0, 1],
                "d": {
                    "ty": "Browser",
                    "ac": "2684125", 
                    "ap": "655559411",
                    "id": span_id,
                    "tr": trace_id,
                    "ti": int(timestamp),
                    "tk": "3671077"
                }
            }),
            'traceparent': f'00-{trace_id}-{span_id}-01',
            'tracestate': f'3671077@nr=0-1-2684125-655559411-{span_id}----{timestamp}',
            'x-fl-request-id': request_id,
            'x-kpsdk-v': 'j-1.1.0',
            'priority': 'u=1, i'
        }

    def check_product_availability(self, sku: str) -> Optional[Dict]:
        """Check if product is available and get details"""
        try:
            logging.info(f"Checking availability for SKU: {sku}")
            
            url = f"{self.api_base}/product-core/v1/pdp/sku/{sku}"
            headers = self._get_tracking_headers()
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                product_data = response.json()
                logging.info(f"Product available: {product_data.get('name', 'Unknown')}")
                
                # Check if product has sizes available
                sizes = product_data.get('variantOptions', {}).get('size', [])
                available_sizes = [size['id'] for size in sizes if size.get('stock', 0) > 0]
                
                product_data['available_sizes'] = available_sizes
                return product_data
            else:
                logging.error(f"Product not available: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error checking product availability: {str(e)}")
            return None

    def add_to_cart_real(self, sku: str, size: str, quantity: int = 1) -> Dict:
        """Add product to cart using real Footlocker API"""
        try:
            logging.info(f"Adding to cart: {sku} size {size}")
            
            # Use the cart API endpoint from your captured requests
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/add"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'x-api-simulation': 'undefined'
            })
            
            # Payload structure based on Footlocker's API
            payload = {
                "productCode": sku,
                "quantity": quantity,
                "size": size,
                "fulfillmentType": "JC"  # Just Classic
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                cart_data = response.json()
                self.cart_id = cart_data.get('cartId')
                logging.info(f"Added to cart successfully! Cart ID: {self.cart_id}")
                return cart_data
            else:
                logging.error(f"Failed to add to cart: {response.status_code}")
                logging.error(f"Response: {response.text}")
                return {}
                
        except Exception as e:
            logging.error(f"Error adding to cart: {str(e)}")
            return {}

    def get_cart_status(self) -> Optional[Dict]:
        """Get current cart status - using your captured endpoint"""
        try:
            logging.info("Getting cart status...")
            
            # This is the exact endpoint from your captured requests
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/getUpdatedCart"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'accept-language': 'undefined',
                'x-api-lang': 'en-US',
                'x-api-simulation': 'undefined',
                'referer': 'https://www.footlocker.com/checkout'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                
                # Update cart ID and guest ID from response
                self.cart_id = cart_data.get('cartId')
                user_info = cart_data.get('user', {})
                self.guest_id = user_info.get('id')
                
                logging.info(f"Cart Status - Items: {cart_data.get('totalUnitCount', 0)}, Total: {cart_data.get('totalPriceWithTax', {}).get('formattedValue', 'N/A')}")
                logging.info(f"Guest ID: {self.guest_id}")
                
                return cart_data
            else:
                logging.error(f"Failed to get cart status: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting cart status: {str(e)}")
            return None

    def set_shipping_address(self, shipping_info: Dict) -> bool:
        """Set shipping address for checkout"""
        try:
            logging.info("Setting shipping address...")
            
            # Shipping address endpoint
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/setShippingAddress"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'referer': 'https://www.footlocker.com/checkout'
            })
            
            # Format shipping address for Footlocker API
            address_payload = {
                "shippingAddress": {
                    "firstName": shipping_info["firstName"],
                    "lastName": shipping_info["lastName"],
                    "line1": shipping_info["address1"],
                    "line2": shipping_info.get("address2", ""),
                    "town": shipping_info["city"],
                    "region": {"isocode": shipping_info["state"]},
                    "postalCode": shipping_info["zipCode"],
                    "country": {"isocode": shipping_info["country"]},
                    "phone": shipping_info["phone"],
                    "email": shipping_info["email"]
                }
            }
            
            response = self.session.post(url, headers=headers, json=address_payload)
            
            if response.status_code == 200:
                logging.info("Shipping address set successfully")
                return True
            else:
                logging.error(f"Failed to set shipping address: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error setting shipping address: {str(e)}")
            return False

    def quick_add_and_checkout(self, product_key: str, size: str) -> bool:
        """Quick method to add product and start checkout"""
        try:
            # Get product info from config
            if product_key not in config.PRODUCTS:
                logging.error(f"Product key '{product_key}' not found in config")
                return False
            
            product_info = config.PRODUCTS[product_key]
            sku = product_info["sku"]
            
            logging.info(f"=== Quick Checkout for {product_info['name']} ===")
            
            # Step 1: Check product availability
            product_data = self.check_product_availability(sku)
            if not product_data:
                logging.error("Product not available")
                return False
            
            # Step 2: Add to cart
            cart_result = self.add_to_cart_real(sku, size)
            if not cart_result:
                logging.error("Failed to add to cart")
                return False
            
            # Step 3: Get updated cart (this triggers guest checkout)
            cart_status = self.get_cart_status()
            if not cart_status:
                logging.error("Failed to get cart status")
                return False
            
            # Step 4: Set shipping address
            if not self.set_shipping_address(config.SHIPPING_INFO):
                logging.error("Failed to set shipping address")
                return False
            
            logging.info("=== Ready for payment - Manual completion required ===")
            logging.info("Cart prepared successfully. Complete payment manually in browser.")
            
            return True
            
        except Exception as e:
            logging.error(f"Error in quick checkout: {str(e)}")
            return False

    def print_cart_summary(self):
        """Print a summary of the current cart"""
        cart = self.get_cart_status()
        if cart:
            print("\n" + "="*50)
            print("CART SUMMARY")
            print("="*50)
            print(f"Cart ID: {cart.get('cartId', 'N/A')}")
            print(f"Guest ID: {cart.get('user', {}).get('id', 'N/A')}")
            print(f"Total Items: {cart.get('totalUnitCount', 0)}")
            print(f"Subtotal: {cart.get('subTotal', {}).get('formattedValue', 'N/A')}")
            print(f"Total: {cart.get('totalPriceWithTax', {}).get('formattedValue', 'N/A')}")
            
            print("\nITEMS:")
            for item in cart.get('cartItems', []):
                print(f"- {item.get('name', 'Unknown')} (Size: {item.get('size', 'N/A')})")
                print(f"  SKU: {item.get('sku', 'N/A')} | Price: {item.get('priceData', {}).get('formattedValue', 'N/A')}")
            
            print("="*50)

def main():
    """Main function with enhanced options"""
    print("🚀 Enhanced Footlocker Checkout Tool")
    print("="*40)
    
    # Initialize checkout with config cookies
    checkout = EnhancedFootlockerCheckout(use_config_cookies=True)
    
    # Show available products from config
    print("\nAvailable Products:")
    for key, product in config.PRODUCTS.items():
        print(f"{key}: {product['name']} (${product['price']}) - SKU: {product['sku']}")
        print(f"    Sizes: {', '.join(product['available_sizes'])}")
    
    print("\nOptions:")
    print("1. Quick add to cart and start checkout")
    print("2. Check product availability")
    print("3. View current cart")
    print("4. Manual step-by-step")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        product_key = input("Enter product key: ").strip()
        size = input("Enter size: ").strip()
        
        success = checkout.quick_add_and_checkout(product_key, size)
        if success:
            checkout.print_cart_summary()
            print("\n✅ Product added and ready for checkout!")
            print("🌐 Complete the payment in your browser at: https://www.footlocker.com/checkout")
        else:
            print("\n❌ Checkout failed!")
    
    elif choice == "2":
        sku = input("Enter SKU to check: ").strip()
        product = checkout.check_product_availability(sku)
        if product:
            print(f"\n✅ Product available: {product.get('name', 'Unknown')}")
            print(f"Available sizes: {product.get('available_sizes', [])}")
        else:
            print("\n❌ Product not available")
    
    elif choice == "3":
        checkout.print_cart_summary()
    
    elif choice == "4":
        print("\nManual step-by-step mode")
        print("Use the class methods to perform individual actions:")
        print("- checkout.check_product_availability(sku)")
        print("- checkout.add_to_cart_real(sku, size)")
        print("- checkout.get_cart_status()")
        print("- checkout.set_shipping_address(shipping_info)")
        
        # Start interactive mode
        import code
        code.interact(local=locals())
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
