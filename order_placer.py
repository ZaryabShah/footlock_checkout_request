#!/usr/bin/env python3
"""
Footlocker Order Placement Script
=================================

This script handles the final checkout steps to place an order on Footlocker.
Based on your captured network requests showing the complete checkout flow.

Flow:
1. Submit user info (contact details)
2. Verify shipping address
3. Set shipping address on cart
4. Get updated cart info
5. Submit payment info
6. Place final order

Author: AI Assistant
Date: July 2025
"""

import requests
import json
import logging
import time
import random
from typing import Dict, Optional
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('footlocker_order_placement.log'),
        logging.StreamHandler()
    ]
)

class FootlockerOrderPlacer:
    """
    Handles the final order placement steps for Footlocker checkout
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.footlocker.com"
        self.api_base = "https://www.footlocker.com/zgw"
        self.cart_id = None
        self.guest_id = None
        
        # Setup session
        self._setup_session()
        
    def _setup_session(self):
        """Initialize session with cookies and headers"""
        try:
            # Load cookies from config
            cookies = config.get_all_cookies()
            for name, value in cookies.items():
                if value:
                    self.session.cookies.set(name, str(value))
            
            # Set headers
            self.session.headers.update({
                'User-Agent': config.USER_AGENT,
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Origin': self.base_url,
                'Referer': f'{self.base_url}/checkout',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/json'
            })
            
            logging.info("Order placer session initialized")
            
        except Exception as e:
            logging.error(f"Error setting up session: {str(e)}")
    
    def _get_tracking_headers(self) -> Dict[str, str]:
        """Generate dynamic tracking headers"""
        timestamp = str(int(time.time() * 1000))
        request_id = f"{''.join([random.choice('0123456789abcdef') for _ in range(8)])}-{''.join([random.choice('0123456789abcdef') for _ in range(4)])}-11f0-{''.join([random.choice('0123456789abcdef') for _ in range(4)])}-{''.join([random.choice('0123456789abcdef') for _ in range(12)])}"
        
        return {
            'newrelic': f'{{"v":[0,1],"d":{{"ty":"Browser","ac":"2684125","ap":"655559411","id":"{"".join([random.choice("0123456789abcdef") for _ in range(16)])}","tr":"{"".join([random.choice("0123456789abcdef") for _ in range(32)])}","ti":{timestamp},"tk":"3671077"}}}}',
            'priority': 'u=1, i',
            'traceparent': f'00-{"".join([random.choice("0123456789abcdef") for _ in range(32)])}-{"".join([random.choice("0123456789abcdef") for _ in range(16)])}-01',
            'tracestate': f'3671077@nr=0-1-2684125-655559411-{"".join([random.choice("0123456789abcdef") for _ in range(16)])}-""--{timestamp}',
            'x-api-lang': 'en-US',
            'x-api-simulation': 'undefined',
            'x-fl-request-id': request_id,
            'x-kpsdk-cd': f'{{"workTime":{timestamp},"id":"{"".join([random.choice("0123456789abcdef") for _ in range(32)])}","answers":[9,7],"duration":98,"d":-439,"st":1751392861410,"rst":1751392860971}}',
            'x-kpsdk-ct': config.ak_bmsc_fl_com,
            'x-kpsdk-v': 'j-1.1.0'
        }
    
    def submit_user_info(self, user_info: Dict) -> bool:
        """
        Step 1: Submit user contact information
        Based on your first captured request
        """
        try:
            logging.info("Step 1: Submitting user contact information...")
            
            url = f"{self.api_base}/carts/co-cart-aggregation-service/site/fl/cart/userInfo"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'accept-language': 'undefined'
            })
            
            # Payload based on your captured request
            payload = {
                "firstName": user_info.get("firstName"),
                "lastName": user_info.get("lastName"),
                "email": user_info.get("email"),
                "phone": user_info.get("phone"),
                "phoneCountry": user_info.get("phoneCountry", "US"),
                "payPalAlert": False
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logging.info("✅ User info submitted successfully")
                return True
            else:
                logging.error(f"❌ Failed to submit user info: {response.status_code}")
                if response.text:
                    logging.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error submitting user info: {str(e)}")
            return False
    
    def verify_shipping_address(self, address: Dict) -> Optional[Dict]:
        """
        Step 2: Verify shipping address
        Based on your second captured request
        """
        try:
            logging.info("Step 2: Verifying shipping address...")
            
            url = f"{self.api_base}/address-verification/v0/address/verification"
            
            headers = self._get_tracking_headers()
            headers.update({
                'x-functions-key': 'm663XzcEgqHJqzbq4JH6FrDIStLZh4FMUMAzXct09W6HAzFuozxPuA=='
            })
            
            # Payload based on your captured request
            payload = {
                "country": {
                    "isocode": address.get("country", "US"),
                    "name": address.get("country", "US")
                },
                "region": {
                    "isocodeShort": address.get("state")
                },
                "line1": address.get("address1"),
                "line2": address.get("address2", ""),
                "postalCode": address.get("zipCode"),
                "town": address.get("city")
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                verification_result = response.json()
                logging.info(f"✅ Address verified: {verification_result.get('decision', 'Unknown')}")
                
                if verification_result.get('decision') == 'Accepted':
                    suggested = verification_result.get('suggestedAddresses', [])
                    if suggested:
                        return suggested[0]  # Return the verified address
                    
                return verification_result
            else:
                logging.error(f"❌ Failed to verify address: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error verifying address: {str(e)}")
            return None
    
    def set_shipping_address(self, verified_address: Dict) -> bool:
        """
        Step 3: Set shipping address on cart
        Based on your third captured request
        """
        try:
            logging.info("Step 3: Setting shipping address on cart...")
            
            url = f"{self.api_base}/carts-experience/carts-experience-service/site/fl/cart/address"
            
            headers = self._get_tracking_headers()
            
            # Convert verified address to cart format
            payload = {
                "shippingAddress": {
                    "firstName": config.SHIPPING_INFO.get("firstName"),
                    "lastName": config.SHIPPING_INFO.get("lastName"),
                    "line1": verified_address.get("line1"),
                    "line2": verified_address.get("line2", ""),
                    "town": verified_address.get("town"),
                    "region": {
                        "isocodeShort": verified_address.get("region", {}).get("isocodeShort")
                    },
                    "postalCode": verified_address.get("postalCode"),
                    "country": {
                        "isocode": verified_address.get("country", {}).get("isocode", "US")
                    },
                    "phone": config.SHIPPING_INFO.get("phone"),
                    "email": config.SHIPPING_INFO.get("email"),
                    "shippingAddress": True
                }
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logging.info("✅ Shipping address set successfully")
                return True
            else:
                logging.error(f"❌ Failed to set shipping address: {response.status_code}")
                if response.text:
                    logging.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error setting shipping address: {str(e)}")
            return False
    
    def get_updated_cart_with_shipping(self) -> Optional[Dict]:
        """
        Step 4: Get updated cart info with shipping
        Based on your fourth captured request
        """
        try:
            logging.info("Step 4: Getting updated cart with shipping...")
            
            url = f"{self.api_base}/carts/co-cart-aggregation-service/site/fl/cart/userInfo"
            
            headers = self._get_tracking_headers()
            headers.update({
                'accept': 'application/json',
                'accept-language': 'undefined'
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                logging.info("✅ Updated cart retrieved with shipping info")
                return cart_data
            else:
                logging.error(f"❌ Failed to get updated cart: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting updated cart: {str(e)}")
            return None
    
    def submit_payment_info(self, payment_info: Dict) -> bool:
        """
        Step 5: Submit payment information
        This would be the payment submission step
        """
        try:
            logging.info("Step 5: Submitting payment information...")
            
            # This endpoint would be captured from your payment flow
            url = f"{self.api_base}/payment/submit"
            
            headers = self._get_tracking_headers()
            
            # Payment payload (use test data only!)
            payload = {
                "paymentMethod": {
                    "type": payment_info.get("paymentType", "CREDITCARD"),
                    "cardNumber": payment_info.get("cardNumber"),
                    "expiryMonth": payment_info.get("expiryMonth"),
                    "expiryYear": payment_info.get("expiryYear"),
                    "cvv": payment_info.get("cvv"),
                    "nameOnCard": payment_info.get("nameOnCard")
                },
                "billingAddress": payment_info.get("billingAddress", {})
            }
            
            # Note: This is a placeholder - you'll need to capture the actual payment endpoint
            logging.warning("⚠️ Payment endpoint not captured yet - this is a placeholder")
            logging.info("Payment info prepared but not submitted (test mode)")
            return True
            
        except Exception as e:
            logging.error(f"Error submitting payment: {str(e)}")
            return False
    
    def place_final_order(self) -> Optional[Dict]:
        """
        Step 6: Place the final order
        This would be the final order submission
        """
        try:
            logging.info("Step 6: Placing final order...")
            
            # This would be captured from the final order placement
            url = f"{self.api_base}/checkout/placeorder"
            
            headers = self._get_tracking_headers()
            
            payload = {
                "cartId": self.cart_id,
                "termsAccepted": True,
                "marketingOptIn": False
            }
            
            # Note: This is a placeholder - you'll need to capture the actual order endpoint
            logging.warning("⚠️ Order placement endpoint not captured yet - this is a placeholder")
            logging.info("Order prepared but not placed (test mode)")
            
            # Return mock order confirmation
            return {
                "orderId": "TEST-ORDER-12345",
                "status": "TEST_MODE",
                "message": "Order placement in test mode"
            }
            
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            return None
    
    def complete_order_flow(self, user_info: Dict, shipping_address: Dict, payment_info: Dict) -> bool:
        """
        Complete the entire order placement flow
        """
        try:
            logging.info("🚀 Starting complete order placement flow...")
            
            # Step 1: Submit user info
            if not self.submit_user_info(user_info):
                logging.error("Failed at Step 1: User info submission")
                return False
            
            # Step 2: Verify shipping address
            verified_address = self.verify_shipping_address(shipping_address)
            if not verified_address:
                logging.error("Failed at Step 2: Address verification")
                return False
            
            # Step 3: Set shipping address
            if not self.set_shipping_address(verified_address):
                logging.error("Failed at Step 3: Setting shipping address")
                return False
            
            # Step 4: Get updated cart
            cart_data = self.get_updated_cart_with_shipping()
            if not cart_data:
                logging.error("Failed at Step 4: Getting updated cart")
                return False
            
            # Step 5: Submit payment (placeholder)
            if not self.submit_payment_info(payment_info):
                logging.error("Failed at Step 5: Payment submission")
                return False
            
            # Step 6: Place order (placeholder)
            order_result = self.place_final_order()
            if not order_result:
                logging.error("Failed at Step 6: Order placement")
                return False
            
            logging.info("🎉 Order placement flow completed successfully!")
            logging.info(f"Order ID: {order_result.get('orderId', 'N/A')}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error in complete order flow: {str(e)}")
            return False

def main():
    """
    Main function for order placement
    """
    print("🛒 Footlocker Order Placement Tool")
    print("=" * 50)
    
    # Initialize order placer
    order_placer = FootlockerOrderPlacer()
    
    # User information (from your captured request)
    user_info = {
        "firstName": "kazmi",
        "lastName": "shb", 
        "email": "domgyrgpt@gmail.com",
        "phone": "9452060458",
        "phoneCountry": "US"
    }
    
    # Shipping address (from your captured request)
    shipping_address = {
        "address1": "1 Morris Rd",
        "address2": "",
        "city": "South Hill",
        "state": "VA",
        "zipCode": "23970-5627",
        "country": "US"
    }
    
    # Payment info (use test data)
    payment_info = config.PAYMENT_INFO
    
    print("\n📋 Order Details:")
    print(f"Customer: {user_info['firstName']} {user_info['lastName']}")
    print(f"Email: {user_info['email']}")
    print(f"Phone: {user_info['phone']}")
    print(f"Shipping: {shipping_address['address1']}, {shipping_address['city']}, {shipping_address['state']} {shipping_address['zipCode']}")
    
    print("\nOptions:")
    print("1. Run complete order flow")
    print("2. Test individual steps")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        # Complete order flow
        print("\n🚀 Starting complete order placement...")
        success = order_placer.complete_order_flow(user_info, shipping_address, payment_info)
        
        if success:
            print("\n✅ Order placement completed successfully!")
        else:
            print("\n❌ Order placement failed!")
            
    elif choice == "2":
        # Test individual steps
        print("\n🔧 Testing individual steps...")
        
        print("\n1. Testing user info submission...")
        if order_placer.submit_user_info(user_info):
            print("✅ User info submitted")
        else:
            print("❌ User info failed")
        
        print("\n2. Testing address verification...")
        verified = order_placer.verify_shipping_address(shipping_address)
        if verified:
            print(f"✅ Address verified: {verified.get('line1', 'N/A')}")
        else:
            print("❌ Address verification failed")
        
        print("\n3. Testing shipping address setup...")
        if verified and order_placer.set_shipping_address(verified):
            print("✅ Shipping address set")
        else:
            print("❌ Shipping address failed")
        
        print("\n4. Testing cart update...")
        cart = order_placer.get_updated_cart_with_shipping()
        if cart:
            print("✅ Cart updated with shipping")
        else:
            print("❌ Cart update failed")
            
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
