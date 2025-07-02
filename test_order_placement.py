#!/usr/bin/env python3
"""
Test Order Placement Script
==========================

This script tests the complete Footlocker order placement flow with your captured data.
It uses the real endpoints and payload structures from your network capture.

Usage:
    python test_order_placement.py

Author: AI Assistant
Date: January 2025
"""

import sys
import json
import time
from order_placer import FootlockerOrderPlacer
import config

def test_complete_flow():
    """Test the complete order placement flow with real data"""
    
    print("🛒 Testing Footlocker Order Placement")
    print("=" * 50)
    
    # Initialize order placer
    order_placer = FootlockerOrderPlacer()
    
    # Real user information from your captured request
    user_info = {
        "firstName": "kazmi",
        "lastName": "shb", 
        "email": "domgyrgpt@gmail.com",
        "phone": "9452060458",
        "phoneCountry": "US"
    }
    
    # Real shipping address from your captured request
    shipping_address = {
        "address1": "1 Morris Rd",
        "address2": "",
        "city": "South Hill",
        "state": "VA",
        "zipCode": "23970-5627",
        "country": "US"
    }
    
    # Payment info (will use placeholder encryption)
    payment_info = config.PAYMENT_INFO
    
    print("\n📋 Test Configuration:")
    print(f"Customer: {user_info['firstName']} {user_info['lastName']}")
    print(f"Email: {user_info['email']}")
    print(f"Phone: {user_info['phone']}")
    print(f"Shipping: {shipping_address['address1']}, {shipping_address['city']}, {shipping_address['state']} {shipping_address['zipCode']}")
    print(f"Payment: Test card ending in {payment_info.get('cardNumber', 'XXXX')[-4:]}")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("- This test uses placeholder encrypted payment data")
    print("- Real orders require valid Adyen CSE encryption")
    print("- Make sure your cookies in config.py are up-to-date")
    print("- Test cards will be declined at final order placement")
    
    # Ask for confirmation
    proceed = input("\nDo you want to proceed with the test? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Test cancelled.")
        return False
    
    print("\n🚀 Starting order placement test...")
    
    try:
        # Test complete flow
        success = order_placer.complete_order_flow(user_info, shipping_address, payment_info)
        
        if success:
            print("\n✅ ORDER PLACEMENT TEST COMPLETED SUCCESSFULLY!")
            print("All steps executed without errors.")
            print("\nNote: Final order may be declined due to test payment data.")
        else:
            print("\n❌ ORDER PLACEMENT TEST FAILED!")
            print("Check the logs for error details.")
            
        return success
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        return False

def test_individual_steps():
    """Test each step individually for debugging"""
    
    print("🔧 Testing Individual Steps")
    print("=" * 50)
    
    # Initialize order placer
    order_placer = FootlockerOrderPlacer()
    
    # Test data
    user_info = {
        "firstName": "kazmi",
        "lastName": "shb", 
        "email": "domgyrgpt@gmail.com",
        "phone": "9452060458",
        "phoneCountry": "US"
    }
    
    shipping_address = {
        "address1": "1 Morris Rd",
        "address2": "",
        "city": "South Hill",
        "state": "VA",
        "zipCode": "23970-5627",
        "country": "US"
    }
    
    payment_info = config.PAYMENT_INFO
    
    results = {}
    
    # Step 1: User Info
    print("\n1️⃣ Testing user info submission...")
    try:
        result = order_placer.submit_user_info(user_info)
        results['user_info'] = result
        if result:
            print("✅ User info submitted successfully")
        else:
            print("❌ User info submission failed")
    except Exception as e:
        print(f"❌ User info error: {str(e)}")
        results['user_info'] = False
    
    time.sleep(1)  # Rate limiting
    
    # Step 2: Address Verification
    print("\n2️⃣ Testing address verification...")
    try:
        verified = order_placer.verify_shipping_address(shipping_address)
        results['address_verification'] = verified is not None
        if verified:
            print(f"✅ Address verified: {verified.get('line1', 'N/A')}")
            results['verified_address'] = verified
        else:
            print("❌ Address verification failed")
    except Exception as e:
        print(f"❌ Address verification error: {str(e)}")
        results['address_verification'] = False
        verified = None
    
    time.sleep(1)  # Rate limiting
    
    # Step 3: Set Shipping Address
    if verified:
        print("\n3️⃣ Testing shipping address setup...")
        try:
            result = order_placer.set_shipping_address(verified)
            results['shipping_address'] = result
            if result:
                print("✅ Shipping address set successfully")
            else:
                print("❌ Shipping address setup failed")
        except Exception as e:
            print(f"❌ Shipping address error: {str(e)}")
            results['shipping_address'] = False
    else:
        print("\n3️⃣ Skipping shipping address (verification failed)")
        results['shipping_address'] = False
    
    time.sleep(1)  # Rate limiting
    
    # Step 4: Get Updated Cart
    print("\n4️⃣ Testing cart update...")
    try:
        cart = order_placer.get_updated_cart_with_shipping()
        results['cart_update'] = cart is not None
        if cart:
            print("✅ Cart updated with shipping info")
        else:
            print("❌ Cart update failed")
    except Exception as e:
        print(f"❌ Cart update error: {str(e)}")
        results['cart_update'] = False
    
    # Step 5: Payment Preparation
    print("\n5️⃣ Testing payment preparation...")
    try:
        payment_data = order_placer.submit_payment_info(payment_info)
        results['payment_prep'] = payment_data is not None
        if payment_data:
            print("✅ Payment data prepared (test encryption)")
        else:
            print("❌ Payment preparation failed")
    except Exception as e:
        print(f"❌ Payment preparation error: {str(e)}")
        results['payment_prep'] = False
        payment_data = None
    
    # Step 6: Final Order (only if all previous steps passed)
    if all([results.get('user_info'), results.get('address_verification'), 
            results.get('shipping_address'), results.get('cart_update'), results.get('payment_prep')]):
        
        print("\n6️⃣ Testing final order placement...")
        print("⚠️  This will attempt to place a real order (will likely fail with test data)")
        
        proceed = input("Proceed with final order test? (y/n): ").strip().lower()
        if proceed == 'y':
            try:
                order_result = order_placer.place_final_order(payment_data)
                results['final_order'] = order_result is not None
                if order_result:
                    print("✅ Order placement API call succeeded")
                    print(f"Order ID: {order_result.get('orderId', 'N/A')}")
                else:
                    print("❌ Order placement failed (expected with test data)")
            except Exception as e:
                print(f"❌ Final order error: {str(e)}")
                results['final_order'] = False
        else:
            print("Skipping final order test")
            results['final_order'] = 'skipped'
    else:
        print("\n6️⃣ Skipping final order (previous steps failed)")
        results['final_order'] = 'skipped'
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    for step, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL" if result is not False else "⏭️  SKIP"
        print(f"{step.replace('_', ' ').title()}: {status}")
    
    return results

def main():
    """Main test runner"""
    
    print("🧪 Footlocker Order Placement Test Suite")
    print("=" * 50)
    
    print("\nTest Options:")
    print("1. Run complete order flow test")
    print("2. Test individual steps (debugging)")
    print("3. Check configuration")
    print("4. Exit")
    
    choice = input("\nSelect test option (1-4): ").strip()
    
    if choice == "1":
        test_complete_flow()
        
    elif choice == "2":
        test_individual_steps()
        
    elif choice == "3":
        print("\n⚙️  Configuration Check:")
        print("=" * 30)
        
        # Check cookies
        cookies = config.get_all_cookies()
        active_cookies = {k: v for k, v in cookies.items() if v}
        print(f"Active cookies: {len(active_cookies)}")
        
        # Check config
        print(f"User Agent: {config.USER_AGENT[:50]}...")
        print(f"Shipping configured: {'firstName' in config.SHIPPING_INFO}")
        print(f"Payment configured: {'cardNumber' in config.PAYMENT_INFO}")
        
        print("\n⚠️  Remember to update cookies in config.py before testing!")
        
    elif choice == "4":
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
