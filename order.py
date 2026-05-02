# order_service.py
from flask import Flask, jsonify
import requests
import pybreaker

app = Flask(__name__)

# Define the circuit breaker
breaker = pybreaker.CircuitBreaker(
    fail_max=3,              # Open circuit after 3 consecutive failures
    reset_timeout=10         # Try again after 10 seconds
)

PAYMENT_URL = "http://localhost:5001/pay"

# Function to call the payment service
@breaker
def call_payment_service():
    response = requests.get(PAYMENT_URL, timeout=2)
    response.raise_for_status()
    return response.json()

@app.route("/order")
def place_order():
    try:
        result = call_payment_service()
        return jsonify({
            "status": "success",
            "payment_response": result
        }), 200
    except pybreaker.CircuitBreakerError:
        # Circuit breaker open
        return jsonify({
            "status": "error",
            "message": "⚠️ Payment Service unavailable (circuit open). Please try later."
        }), 503
    except Exception as e:
        # Other errors like timeout or HTTP error
        return jsonify({
            "status": "error",
            "message": f"Payment failed: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
