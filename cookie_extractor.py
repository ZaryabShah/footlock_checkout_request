#!/usr/bin/env python3
"""
Cookie Extractor Tool for Footlocker
Helps extract cookies from cURL commands
"""

import re
import json

def extract_cookies_from_curl(curl_command: str) -> dict:
    """
    Extract cookies from a cURL command string
    
    Args:
        curl_command (str): The cURL command copied from browser
        
    Returns:
        dict: Dictionary of cookie name-value pairs
    """
    cookies = {}
    
    # Find the -b or --cookie parameter
    cookie_pattern = r'-b\s+["\']([^"\']+)["\']'
    match = re.search(cookie_pattern, curl_command)
    
    if match:
        cookie_string = match.group(1)
        
        # Split cookies by semicolon and parse
        cookie_pairs = cookie_string.split(';')
        
        for pair in cookie_pairs:
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name.strip()] = value.strip()
    
    return cookies

def format_for_config(cookies: dict) -> str:
    """
    Format cookies for config.py file
    
    Args:
        cookies (dict): Dictionary of cookies
        
    Returns:
        str: Formatted string for config.py
    """
    output = []
    
    # Important cookies that we need
    important_cookies = [
        'ZGWID', 'JSESSIONID', 'AMCV_40A3741F578E26BA7F000101%40AdobeOrg',
        'ConstructorioID_client_id', '_ga', '_cs_id', '__attentive_id',
        'ak_bmsc_fl_com', 'affinity'
    ]
    
    output.append("# Updated cookies from browser")
    output.append("# Copy these values to your config.py file\n")
    
    for cookie_name in important_cookies:
        if cookie_name in cookies:
            # Convert cookie name to valid Python variable name
            var_name = cookie_name.replace('%40', '_40').replace('-', '_')
            output.append(f'{var_name} = "{cookies[cookie_name]}"')
        else:
            print(f"Warning: {cookie_name} not found in cookies")
    
    # Add any other cookies we found
    output.append("\n# Additional cookies found:")
    for name, value in cookies.items():
        if name not in important_cookies:
            var_name = name.replace('%40', '_40').replace('-', '_').replace('.', '_')
            output.append(f'# {var_name} = "{value}"')
    
    return '\n'.join(output)

def main():
    """Main function for cookie extraction"""
    print("🍪 Footlocker Cookie Extractor")
    print("=" * 40)
    print("This tool helps you extract cookies from cURL commands")
    print("\nTo get a cURL command:")
    print("1. Open Chrome DevTools (F12)")
    print("2. Go to Network tab")
    print("3. Visit footlocker.com and add something to cart")
    print("4. Find any request to footlocker.com")
    print("5. Right-click → Copy → Copy as cURL")
    print("6. Paste it below")
    print("\n" + "=" * 40)
    
    while True:
        try:
            print("\nPaste your cURL command here (or 'quit' to exit):")
            curl_input = input().strip()
            
            if curl_input.lower() == 'quit':
                break
                
            if not curl_input.startswith('curl'):
                print("❌ Please paste a valid cURL command starting with 'curl'")
                continue
            
            # Extract cookies
            cookies = extract_cookies_from_curl(curl_input)
            
            if not cookies:
                print("❌ No cookies found in the cURL command")
                continue
            
            print(f"\n✅ Found {len(cookies)} cookies!")
            
            # Format for config
            config_output = format_for_config(cookies)
            
            print("\n" + "=" * 50)
            print("COPY THE FOLLOWING TO YOUR config.py FILE:")
            print("=" * 50)
            print(config_output)
            print("=" * 50)
            
            # Save to file
            with open('extracted_cookies.txt', 'w') as f:
                f.write(config_output)
            
            print(f"\n💾 Cookies also saved to: extracted_cookies.txt")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
