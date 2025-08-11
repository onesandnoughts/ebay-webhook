from flask import Flask, request, jsonify, Response
import json
import logging
from datetime import datetime
import os

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

@app.route('/marketplace-notifications', methods=['GET'])
def webhook_verification():
    """Handle eBay webhook verification (challenge/response)"""
    # Log all parameters to see what eBay is actually sending
    logger.info(f"GET request received with args: {dict(request.args)}")
    
    # Try different parameter names eBay might use
    challenge = (request.args.get('challenge_code') or 
                request.args.get('challenge') or 
                request.args.get('code'))
    
    if challenge:
        logger.info(f"✅ Challenge received: {challenge}")
        logger.info("Returning challenge code to eBay")
        return Response(challenge, mimetype='text/plain')
    else:
        logger.info("No challenge parameter found - returning default message")
        return "Webhook endpoint ready"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
