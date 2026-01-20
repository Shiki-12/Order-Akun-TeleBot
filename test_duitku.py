from duitku_api import DuitkuAPI
import os
import logging

# Configure logging to show all details
logging.basicConfig(level=logging.DEBUG)

def test_create_invoice():
    print("--- Testing Duitku API: Create Invoice ---")
    
    # Check credentials
    m_code = os.getenv("DUITKU_MERCHANT_CODE")
    api_key = os.getenv("DUITKU_API_KEY")
    print(f"Merchant Code: {m_code}")
    print(f"API Key: {api_key[:5]}...{api_key[-5:] if api_key and len(api_key)>10 else 'invalid'}")
    
    if not m_code or not api_key:
        print("ERROR: Missing credentials in .env")
        return

    dui = DuitkuAPI()
    
    # Test Data
    order_id = "TEST-INV-001"
    amount = 10000
    product_details = "Test Product"
    email = "test@example.com"
    
    print(f"Attempting to create invoice for {order_id} with amount {amount}")
    
    try:
        resp = dui.create_invoice(order_id, amount, product_details, email)
        print("\n--- API Response ---")
        print(resp)
        print("--------------------")
        
        if resp and 'paymentUrl' in resp:
            print(f"SUCCESS! Payment URL: {resp['paymentUrl']}")
        else:
            print("FAILED: No paymentUrl in response.")
            if resp:
                print(f"Status Code: {resp.get('statusCode')}")
                print(f"Message: {resp.get('statusMessage')}")
                
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_create_invoice()
