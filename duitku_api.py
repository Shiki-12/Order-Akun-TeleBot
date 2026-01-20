import hashlib
import json
import logging
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class DuitkuAPI:
    def __init__(self):
        self.merchant_code = os.getenv("DUITKU_MERCHANT_CODE")
        self.api_key = os.getenv("DUITKU_API_KEY")
        # Base URLs
        self.sandbox_base_url = "https://sandbox.duitku.com/webapi/api/merchant"
        self.prod_base_url = "https://passport.duitku.com/webapi/api/merchant"
        
        # Determine environment (default to sandbox if not specified)
        # You can add DUITKU_ENV=production to .env to switch
        self.is_production = os.getenv("DUITKU_ENV", "sandbox").lower() == "production"
        self.base_url = self.prod_base_url if self.is_production else self.sandbox_base_url

    def _generate_signature(self, *args):
        """Generates MD5 signature from provided arguments."""
        signature_str = "".join(str(arg) for arg in args)
        return hashlib.md5(signature_str.encode('utf-8')).hexdigest()

    def create_invoice(self, order_id, amount, product_details, email, customer_name="Customer"):
        """
        Creates a transaction (Inquiry) and returns the payment URL.
        Endpoint: /v2/inquiry
        Signature: merchantCode + merchantOrderId + paymentAmount + apiKey
        """
        url = f"{self.base_url}/v2/inquiry"
        
        # Ensure amount is integer for signature if required, but usually string concatenation acts same.
        # Docs say param is integer or string, typically integer for standard JSON.
        amount = int(amount)
        
        signature = self._generate_signature(self.merchant_code, order_id, amount, self.api_key)

        data = {
            "merchantCode": self.merchant_code,
            "paymentAmount": amount,
            "paymentMethod": "VC", # Placeholder, typically prompts user or defaults if not strict
            "merchantOrderId": order_id,
            "productDetails": product_details,
            "additionalParam": "",
            "merchantUserInfo": "",
            "customerVaName": customer_name,
            "email": email,
            "phoneNumber": "08123456789",
            "itemDetails": [{
                "name": product_details,
                "price": amount,
                "quantity": 1
            }],
            "customerDetail": {
                "firstName": customer_name,
                "lastName": "",
                "email": email,
                "phoneNumber": "08123456789",
            },
            "callbackUrl": "https://example.com/callback", 
            "returnUrl": "https://example.com/return",
            "signature": signature,
            "expiryPeriod": 60 
        }

        try:
            response = requests.post(url, json=data)
            
            result = response.json()
            # result contains paymentUrl if successful
            return result
        except Exception as e:
            logging.error(f"Error creating invoice: {e}")
            return None

    def check_transaction_status(self, order_id):
        """
        Checks the status of a transaction.
        Endpoint: /transactionStatus
        Signature: merchantCode + merchantOrderId + apiKey
        """
        url = f"{self.base_url}/transactionStatus"
        signature = self._generate_signature(self.merchant_code, order_id, self.api_key)

        data = {
            "merchantCode": self.merchant_code,
            "merchantOrderId": order_id,
            "signature": signature
        }

        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            logging.error(f"Error checking status: {e}")
            return None
