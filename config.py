# Footlocker Session Configuration
# Copy these values from your browser's developer tools

# Main cookies (from your captured requests)
ZGWID = "eyJhbGciOiJIUzUxMiJ9.eyJndWVzdElkIjoiNzI3MDBjYzQtZTU0Yi00YzY3LWFmZjAtNzg3MjkwMzkwYjU5IiwiaWF0IjoxNzUxMzkyODYzLCJleHAiOjE3ODI5Mjg4NjN9.Stn6drhKgHOmk3nUSNVk3CmtDTnP1aaVsZgkv-mAeeeOzyU8JLqdiWVf0ih_AApIqB91Ae8vjLJhfChfoU2Scg"
JSESSIONID = "9164b9cb-8329-417a-be00-ce81712c81d7"

# Adobe Marketing Cloud cookies
AMCV_40A3741F578E26BA7F000101_40AdobeOrg = "179643557%7CMCIDTS%7C20271%7CMCMID%7C75815063124236325170672623285627760182%7CMCAAMLH-1751997657%7C3%7CMCAAMB-1751997657%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1751400057s%7CNONE%7CvVersion%7C5.5.0"

# Constructor.io cookies
ConstructorioID_client_id = "6da697d4-eb87-4a38-88a9-3d3ed8349f26"
ConstructorioID_session = "{'sessionId':1%2C'lastTime':1751392866644}"
ConstructorioID_session_id = "1"

# Other tracking cookies
_ga = "GA1.1.1284347224.1751392866"
_cs_id = "5b6b067c-15c4-aec2-cc69-03f713e667bf.1751392866.2.1751414016.1751413523.1750451311.1785556866194.1.x"

# Attentive cookies
__attentive_id = "f17dd50c362249df893c13d61700de7a"
__attentive_dv = "1"

# Additional cookies from your captured requests
at_check = "true"
AMCVS_40A3741F578E26BA7F000101_40AdobeOrg = "1"
s_pr_tbe65 = "1751392859985"
s_cc = "true"
_crbx = "4PiUDH9FS4WukLpOvrO4FQ"
_cs_c = "0"
BVBRANDID = "7a13390f-2788-4eee-a5eb-e7e2112c84fd"
BVImplmain_site = "8001"
_gcl_au = "1.1.534519834.1751392867"
bluecoreNV = "true"
IR_gbd = "footlocker.com"
__attentive_cco = "1751392872826"
IR_PI = "60730a94-56a5-11f0-81d4-d9f03ed1929c%7C1751392871230"
termsofuse_consentv2 = "true"
styliticsWidgetSession = "8d779680-6654-4179-950f-9996b35d38d7"
rskxRunCookie = "0"
rCookie = "ol01sjvnigevtk6b65lehmcku4d8v"
affinity = "77553cf37f6b410f"
ak_bmsc_fl_com = "0crWWT42ZZJrWrJm0d1AlHuZ9zhvanN7AHGkKcyPvWqJhKXWU8etGwodKFUmkVe2YiNp4v3BABFd2SbvJ7epV04o0WSLCMmOTOuk8tVq5sPHEVANXgBbbXHN0QvoxW2laffvh9XeFZ7clJSkirYKoBIm8r3kQbPwrAbSU4ibtrF"

# Important: Update these values from your fresh browser session for best results
# To get fresh cookies:
# 1. Open Chrome DevTools (F12)
# 2. Go to Application > Storage > Cookies > https://www.footlocker.com
# 3. Copy the values for the important cookies listed above

# User Agent from your session
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

# Product information that you want to purchase
PRODUCTS = {
    "jordan_5_retro": {
        "sku": "H7980100",
        "name": "Jordan Air Jordan 5 Retro OG - Boys' Grade School",
        "available_sizes": ["03.5", "04.0", "04.5", "05.0", "05.5", "06.0"],
        "price": 160.00
    },
    "other_product": {
        "sku": "S001AS9",
        "name": "Sample Product",
        "available_sizes": ["08.0", "09.0", "10.0"],
        "price": 120.00
    }
}

# Shipping information template
SHIPPING_INFO = {
    "firstName": "John",
    "lastName": "Doe", 
    "address1": "123 Main Street",
    "address2": "",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "US",
    "phone": "555-123-4567",
    "email": "john.doe@example.com"
}

# Payment information template (DO NOT PUT REAL CARD INFO HERE)
PAYMENT_INFO = {
    "paymentType": "CREDITCARD",
    "cardNumber": "4111111111111111",  # Test Visa card
    "expiryMonth": "12",
    "expiryYear": "2025", 
    "cvv": "123",
    "nameOnCard": "John Doe",
    "billingAddress": {
        "firstName": "John",
        "lastName": "Doe",
        "address1": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "zipCode": "10001",
        "country": "US"
    }
}

def get_all_cookies():
    """
    Get all cookies as a dictionary for requests
    """
    return {
        'at_check': at_check,
        'AMCVS_40A3741F578E26BA7F000101%40AdobeOrg': AMCVS_40A3741F578E26BA7F000101_40AdobeOrg,
        'AMCV_40A3741F578E26BA7F000101%40AdobeOrg': AMCV_40A3741F578E26BA7F000101_40AdobeOrg,
        'ConstructorioID_client_id': ConstructorioID_client_id,
        's_pr_tbe65': s_pr_tbe65,
        's_cc': s_cc,
        'ZGWID': ZGWID,
        '_crbx': _crbx,
        '_ga': _ga,
        '_cs_c': _cs_c,
        'BVBRANDID': BVBRANDID,
        'ConstructorioID_session': ConstructorioID_session,
        'ConstructorioID_session_id': ConstructorioID_session_id,
        'BVImplmain_site': BVImplmain_site,
        '_gcl_au': _gcl_au,
        'bluecoreNV': bluecoreNV,
        'IR_gbd': IR_gbd,
        '__attentive_id': __attentive_id,
        '__attentive_cco': __attentive_cco,
        'IR_PI': IR_PI,
        'termsofuse_consentv2': termsofuse_consentv2,
        '__attentive_dv': __attentive_dv,
        'styliticsWidgetSession': styliticsWidgetSession,
        'rskxRunCookie': rskxRunCookie,
        'rCookie': rCookie,
        'JSESSIONID': JSESSIONID,
        '_cs_id': _cs_id,
        'affinity': affinity,
        'ak_bmsc_fl_com': ak_bmsc_fl_com
    }

def get_fresh_session_info():
    """
    Instructions for getting fresh session data
    """
    return """
    🔄 TO GET FRESH COOKIES:
    
    1. Open Chrome and go to https://www.footlocker.com/
    2. Open Developer Tools (F12)
    3. Go to Network tab
    4. Add any product to cart
    5. Look for requests to footlocker.com
    6. Right-click on any request → Copy → Copy as cURL
    7. Extract the cookies from the cURL command
    8. Update the values in config.py
    
    ⚠️  IMPORTANT: Cookies expire! Update them regularly for best results.
    """

# Instructions for updating cookies
COOKIE_UPDATE_INSTRUCTIONS = get_fresh_session_info()
