from flask import Flask, request, jsonify, Response
import json
import logging
from datetime import datetime
import os
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def health_check():
    """Simple health check endpoint"""
    return "eBay Webhook Service is running"

@app.route('/marketplace-notifications', methods=['POST'])
def handle_marketplace_notification():
    """Handle eBay marketplace account deletion notifications"""
    try:
        # Log the incoming notification
        notification_data = request.get_json()
        timestamp = datetime.now().isoformat()
        
        logger.info(f"[{timestamp}] Received marketplace deletion notification:")
        logger.info(f"Data: {json.dumps(notification_data, indent=2)}")
        
        # Since your app doesn't store user data, we just need to acknowledge receipt
        # In a real app that stores data, you'd delete the user's data here
        
        # eBay expects a 200 response to confirm we received the notification
        response_data = {
            "status": "acknowledged",
            "timestamp": timestamp,
            "message": "Notification received successfully"
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error handling notification: {str(e)}")
        # Still return 200 so eBay doesn't keep retrying
        return jsonify({"status": "error", "message": str(e)}), 200

import hashlib

@app.route('/marketplace-notifications', methods=['GET'])
def webhook_verification():
    """Handle eBay webhook verification (challenge/response)"""
    logger.info(f"GET request received with args: {dict(request.args)}")
    
    challenge_code = request.args.get('challenge_code')
    
    if challenge_code:
        # eBay verification process requires hashing challengeCode + verificationToken + endpoint
        verification_token = "my-secret-verification-token-123"
        endpoint = "https://ebay-webhook-production-afe8.up.railway.app/marketplace-notifications"
        
        # Create SHA-256 hash as required by eBay
        hash_input = challenge_code + verification_token + endpoint
        challenge_response = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        
        logger.info(f"✅ Challenge received: {challenge_code}")
        logger.info(f"Hash input: {hash_input}")
        logger.info(f"Challenge response: {challenge_response}")
        
        # Return JSON response as required by eBay
        return jsonify({"challengeResponse": challenge_response})
    else:
        logger.info("No challenge parameter found - returning default message")
        return "Webhook endpoint ready"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
