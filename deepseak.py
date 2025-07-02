import requests

def footlocker_guest_checkout():
    # Start session to persist cookies
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    })
    
    # 1. ADD TO CART (Replace SKU & quantity)
    cart_url = "https://api.footlocker.com/cart/add"
    cart_data = {
        "items": [{
            "sku": "EXAMPLE_SKU",  # ⚠️ Get actual SKU from product page
            "quantity": 3,         # ⚠️ Verify quantity needed
            "price": 160.00
        }]
    }
    session.post(cart_url, json=cart_data)

    # 2. INITIATE CHECKOUT (Get cart ID)
    checkout_init_url = "https://www.footlocker.com/api/checkout/begin"
    checkout_data = {"channel": "WEB"}
    init_response = session.post(checkout_init_url, json=checkout_data)
    cart_id = init_response.json().get("cartId")  # ⚠️ Extract actual cart ID

    # 3. GUEST CHECKOUT SELECTION
    guest_url = "https://www.footlocker.com/api/checkout/guest"
    session.post(guest_url)  # No payload usually needed

    # 4. SUBMIT CONTACT INFO (From your image)
    contact_url = f"https://www.footlocker.com/api/checkout/{cart_id}/contacts"
    contact_payload = {
        "email": "customer@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "phone": "1234567890",
        "country": "US"
    }
    session.put(contact_url, json=contact_payload)

    # 5. SUBMIT SHIPPING (Address + Method)
    shipping_url = f"https://www.footlocker.com/api/checkout/{cart_id}/shipping"
    shipping_payload = {
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "US"
        },
        "method": "standard"  # Free shipping method
    }
    session.put(shipping_url, json=shipping_payload)

    # 6. PLACE ORDER (Final submit)
    order_url = f"https://www.footlocker.com/api/checkout/{cart_id}/order"
    payment_payload = {
        "cardNumber": "4111111111111111",
        "expiry": "12/2025",
        "cvv": "123",
        "cardType": "VISA"
    }
    order_response = session.post(order_url, json=payment_payload)
    
    return order_response.json()  # Returns order confirmation

# Execute
if __name__ == "__main__":
    result = footlocker_guest_checkout()
    print(result)