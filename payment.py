# payment_service.py
from flask import Flask, jsonify
import random, time

app = Flask(__name__)

@app.route("/pay")
def pay():
    # Randomly fail or delay to simulate an unstable service
    if random.random() < 0.5:  # 50% failure rate
        return jsonify({"error": "Payment Service Failed!"}), 500
    time.sleep(random.uniform(0.1, 0.5))  # random delay
    return jsonify({"message": "Payment processed successfully"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
