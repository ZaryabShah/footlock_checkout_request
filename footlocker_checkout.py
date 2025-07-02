#!/usr/bin/env python3
"""
Footlocker Checkout Automation Script
=====================================

This script automates the checkout process for Footlocker products.
Based on captured network requests from browser developer tools.

Features:
- Product search and availability check
- Add to cart functionality
- Guest checkout process
- Session management
- Complete order placement

Author: AI Assistant
Date: July 2025
"""

import requests
import json
import urllib.parse
import time
import random
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('footlocker_checkout.log'),
        logging.StreamHandler()
    ]
)

class FootlockerCheckout:
    """
    Footlocker checkout automation class
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.footlocker.com"
        self.api_base = "https://www.footlocker.com/zgw"
        self.cart_id = None
        self.guest_id = None
        self.zgw_id = None
        
        # Setup session with default headers
        self._setup_session()
        
    def _setup_session(self):
        """Setup session with required headers and user agent"""
        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
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
        """Generate tracking headers for requests"""
        timestamp = str(int(time.time() * 1000))
        return {
            'newrelic': f'{{"v":[0,1],"d":{{"ty":"Browser","ac":"2684125","ap":"655559411","id":"{"".join([random.choice("0123456789abcdef") for _ in range(16)])}","tr":"{"".join([random.choice("0123456789abcdef") for _ in range(32)])}","ti":{timestamp},"tk":"3671077"}}}}',
            'traceparent': f'00-{"".join([random.choice("0123456789abcdef") for _ in range(32)])}-{"".join([random.choice("0123456789abcdef") for _ in range(16)])}-01',
            'x-fl-request-id': f'{"".join([random.choice("0123456789abcdef") for _ in range(8)])}-{"".join([random.choice("0123456789abcdef") for _ in range(4)])}-11f0-{"".join([random.choice("0123456789abcdef") for _ in range(4)])}-{"".join([random.choice("0123456789abcdef") for _ in range(12)])}'
        }

    def initialize_session(self) -> bool:
        """Initialize session by visiting homepage and setting up cookies"""
        try:
            logging.info("Initializing Footlocker session...")
            
            # Visit homepage to get initial cookies
            response = self.session.get(self.base_url)
            
            if response.status_code == 200:
                logging.info("Successfully initialized session")
                return True
            else:
                logging.error(f"Failed to initialize session: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error initializing session: {str(e)}")
            return False

    def get_product_details(self, sku: str) -> Optional[Dict]:
        """
        Get product details by SKU
        
        Args:
            sku (str): Product SKU (e.g., 'H7980100')
            
        Returns:
            Dict: Product details or None if failed
        """
        try:
            logging.info(f"Fetching product details for SKU: {sku}")
            
            url = f"{self.api_base}/product-core/v1/pdp/sku/{sku}"
            headers = self._get_tracking_headers()
            headers.update({
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                product_data = response.json()
                logging.info(f"Successfully retrieved product: {product_data.get('name', 'Unknown')}")
                return product_data
            else:
                logging.error(f"Failed to get product details: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting product details: {str(e)}")
            return None

    def add_to_cart(self, sku: str, size: str, quantity: int = 1) -> bool:
        """
        Add product to cart
        
        Args:
            sku (str): Product SKU
            size (str): Product size (e.g., '04.5')
            quantity (int): Quantity to add
            
        Returns:
            bool: Success status
        """
        try:
            logging.info(f"Adding to cart: SKU={sku}, Size={size}, Qty={quantity}")
            
            # First get product details to ensure it exists
            product = self.get_product_details(sku)
            if not product:
                logging.error("Failed to get product details before adding to cart")
                return False
            
            # Add to cart endpoint
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/add"
            
            headers = self._get_tracking_headers()
            headers.update({
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            # Prepare add to cart payload
            payload = {
                "sku": sku,
                "size": size,
                "quantity": quantity,
                "fulfillmentType": "JC",  # Just Classic fulfillment
                "selectedSizeGroup": "",
                "selectedSizeValue": ""
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                cart_data = response.json()
                self.cart_id = cart_data.get('cartId')
                logging.info(f"Successfully added to cart. Cart ID: {self.cart_id}")
                return True
            else:
                logging.error(f"Failed to add to cart: {response.status_code}")
                if response.text:
                    logging.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error adding to cart: {str(e)}")
            return False

    def get_updated_cart(self) -> Optional[Dict]:
        """
        Get updated cart information
        
        Returns:
            Dict: Cart data or None if failed
        """
        try:
            logging.info("Getting updated cart information...")
            
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/getUpdatedCart"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                self.cart_id = cart_data.get('cartId')
                logging.info(f"Cart updated. Items: {cart_data.get('totalUnitCount', 0)}, Total: {cart_data.get('totalPriceWithTax', {}).get('formattedValue', 'N/A')}")
                return cart_data
            else:
                logging.error(f"Failed to get updated cart: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting updated cart: {str(e)}")
            return None

    def checkout_as_guest(self) -> bool:
        """
        Initiate checkout as guest
        
        Returns:
            bool: Success status
        """
        try:
            logging.info("Starting guest checkout process...")
            
            # Get updated cart first
            cart_data = self.get_updated_cart()
            if not cart_data:
                logging.error("Cannot proceed with checkout - no cart data")
                return False
            
            # Continue as guest - this was captured in your requests
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/getUpdatedCart"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'referer': 'https://www.footlocker.com/checkout',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                checkout_data = response.json()
                logging.info("Successfully initiated guest checkout")
                
                # Extract guest user info
                user_info = checkout_data.get('user', {})
                self.guest_id = user_info.get('id')
                logging.info(f"Guest ID: {self.guest_id}")
                
                return True
            else:
                logging.error(f"Failed to initiate guest checkout: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error in guest checkout: {str(e)}")
            return False

    def submit_shipping_info(self, shipping_info: Dict) -> bool:
        """
        Submit shipping information
        
        Args:
            shipping_info (Dict): Shipping details
            
        Returns:
            bool: Success status
        """
        try:
            logging.info("Submitting shipping information...")
            
            # This would be the shipping info submission endpoint
            # Based on typical e-commerce patterns
            url = f"{self.api_base}/checkout/shipping"
            
            headers = self._get_tracking_headers()
            headers.update({
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            response = self.session.post(url, headers=headers, json=shipping_info)
            
            if response.status_code == 200:
                logging.info("Successfully submitted shipping information")
                return True
            else:
                logging.error(f"Failed to submit shipping info: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error submitting shipping info: {str(e)}")
            return False

    def submit_payment_info(self, payment_info: Dict) -> bool:
        """
        Submit payment information
        
        Args:
            payment_info (Dict): Payment details
            
        Returns:
            bool: Success status
        """
        try:
            logging.info("Submitting payment information...")
            
            # Payment submission endpoint
            url = f"{self.api_base}/checkout/payment"
            
            headers = self._get_tracking_headers()
            headers.update({
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            response = self.session.post(url, headers=headers, json=payment_info)
            
            if response.status_code == 200:
                logging.info("Successfully submitted payment information")
                return True
            else:
                logging.error(f"Failed to submit payment info: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error submitting payment info: {str(e)}")
            return False

    def place_order(self) -> Optional[Dict]:
        """
        Place the final order
        
        Returns:
            Dict: Order confirmation or None if failed
        """
        try:
            logging.info("Placing final order...")
            
            # Order placement endpoint
            url = f"{self.api_base}/checkout/placeorder"
            
            headers = self._get_tracking_headers()
            headers.update({
                'content-type': 'application/json',
                'x-api-lang': 'en-US',
                'x-kpsdk-v': 'j-1.1.0'
            })
            
            # Basic order placement payload
            payload = {
                "cartId": self.cart_id,
                "guestId": self.guest_id
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                order_data = response.json()
                logging.info(f"Order placed successfully! Order ID: {order_data.get('orderId', 'N/A')}")
                return order_data
            else:
                logging.error(f"Failed to place order: {response.status_code}")
                if response.text:
                    logging.error(f"Response: {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            return None

    def complete_checkout_flow(self, sku: str, size: str, shipping_info: Dict, payment_info: Dict) -> bool:
        """
        Complete the entire checkout flow
        
        Args:
            sku (str): Product SKU
            size (str): Product size
            shipping_info (Dict): Shipping information
            payment_info (Dict): Payment information
            
        Returns:
            bool: Success status
        """
        try:
            logging.info("=== Starting Complete Checkout Flow ===")
            
            # Step 1: Initialize session
            if not self.initialize_session():
                return False
            
            # Step 2: Add product to cart
            if not self.add_to_cart(sku, size):
                return False
            
            # Step 3: Start guest checkout
            if not self.checkout_as_guest():
                return False
            
            # Step 4: Submit shipping info
            if not self.submit_shipping_info(shipping_info):
                return False
            
            # Step 5: Submit payment info
            if not self.submit_payment_info(payment_info):
                return False
            
            # Step 6: Place order
            order_result = self.place_order()
            if order_result:
                logging.info("=== Checkout Flow Completed Successfully ===")
                return True
            else:
                logging.error("=== Checkout Flow Failed ===")
                return False
                
        except Exception as e:
            logging.error(f"Error in complete checkout flow: {str(e)}")
            return False

def main():
    """
    Main function demonstrating usage
    """
    # Initialize checkout instance
    checkout = FootlockerCheckout()
    
    # Example product information (Jordan Air Jordan 5 Retro OG from your captured requests)
    sku = "H7980100"
    size = "04.5"
    
    # Example shipping information
    shipping_info = {
        "firstName": "John",
        "lastName": "Doe",
        "address1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zipCode": "10001",
        "country": "US",
        "phone": "555-123-4567",
        "email": "john.doe@example.com"
    }
    
    # Example payment information (use test data only!)
    payment_info = {
        "paymentType": "CREDITCARD",
        "cardNumber": "4111111111111111",  # Test card number
        "expiryMonth": "12",
        "expiryYear": "2025",
        "cvv": "123",
        "nameOnCard": "John Doe"
    }
    
    print("=== Footlocker Checkout Automation ===")
    print(f"Product SKU: {sku}")
    print(f"Size: {size}")
    print("=" * 40)
    
    # Option 1: Complete checkout flow
    print("\n1. Run complete checkout flow")
    print("2. Test individual steps")
    print("3. Just add to cart and view")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Complete checkout flow
        success = checkout.complete_checkout_flow(sku, size, shipping_info, payment_info)
        if success:
            print("\n✅ Checkout completed successfully!")
        else:
            print("\n❌ Checkout failed!")
            
    elif choice == "2":
        # Test individual steps
        print("\nTesting individual steps...")
        
        # Initialize session
        if checkout.initialize_session():
            print("✅ Session initialized")
        else:
            print("❌ Session initialization failed")
            return
        
        # Get product details
        product = checkout.get_product_details(sku)
        if product:
            print(f"✅ Product found: {product.get('name', 'Unknown')}")
        else:
            print("❌ Product not found")
            return
        
        # Add to cart
        if checkout.add_to_cart(sku, size):
            print("✅ Added to cart")
        else:
            print("❌ Failed to add to cart")
            return
        
        # Get cart info
        cart = checkout.get_updated_cart()
        if cart:
            print(f"✅ Cart retrieved: {cart.get('totalUnitCount', 0)} items")
        else:
            print("❌ Failed to get cart")
            
    elif choice == "3":
        # Just add to cart and view
        print("\nAdding product to cart...")
        
        checkout.initialize_session()
        if checkout.add_to_cart(sku, size):
            cart = checkout.get_updated_cart()
            if cart:
                print(f"\n✅ Product added to cart!")
                print(f"Cart ID: {cart.get('cartId')}")
                print(f"Items: {cart.get('totalUnitCount', 0)}")
                print(f"Total: {cart.get('totalPriceWithTax', {}).get('formattedValue', 'N/A')}")
                
                # Print cart items
                for item in cart.get('cartItems', []):
                    print(f"- {item.get('name')} ({item.get('size')}) - {item.get('priceData', {}).get('formattedValue', 'N/A')}")
            else:
                print("❌ Failed to retrieve cart")
        else:
            print("❌ Failed to add to cart")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
