from flask import Flask, request, jsonify, make_response
import pandas as pd
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the segmentation model and scaler
seg_model_and_scaler = joblib.load("models/customer_segmentation_with_scaler.pkl")
segmentation_model = seg_model_and_scaler["model"]
segmentation_scaler = seg_model_and_scaler["scaler"]

prob_model_and_scaler = joblib.load("models/purchase_probability_with_scaler.pkl")
purchase_prob_model = prob_model_and_scaler["model"]
purchase_prob_scaler = prob_model_and_scaler["scaler"]

@app.route("/")
def home():
    return "Welcome to the Customer Segmentation API!"

# Route 1: Customer Segmentation (Clustering)
@app.route("/segment", methods=["POST"])
def segment_customer():
    try:
        # Get JSON data
        data = request.json
        
        # Validate the input
        required_features = ["Age", "Purchase Amount (USD)"]
        
        # Check for missing features
        for feature in required_features:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: {feature}"}), 400
        
        # Convert input data to a DataFrame
        input_df = pd.DataFrame([data])
        
        # Select only required features
        input_df = input_df[required_features]
        
        # Scale the input data using the same scaler used in training
        input_scaled = segmentation_scaler.transform(input_df)
        
        # Predict customer segment
        cluster_label = segmentation_model.predict(input_scaled)[0]
        
        return jsonify({"Customer Segment": int(cluster_label)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route 2: Purchase Probability Prediction (Classification)
@app.route("/purchase-probability", methods=["POST"])
def predict_purchase_probability():
    try:
        # Get JSON data
        data = request.json
        
        # Validate input
        required_features = ["Age", "Previous Purchases", "Purchase Amount (USD)", "Review Rating"]
        
        # Check for missing features
        for feature in required_features:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: {feature}"}), 400
        
        # Convert input to DataFrame
        input_df = pd.DataFrame([data])
        
        # Select only required features
        input_df = input_df[required_features]
        
        # Scale numerical columns
        numerical_columns = ["Age", "Previous Purchases", "Purchase Amount (USD)", "Review Rating"]
        input_df[numerical_columns] = purchase_prob_scaler.transform(input_df[numerical_columns])
        
        # Predict purchase probability
        purchase_prob = purchase_prob_model.predict(input_df)[0]

        return jsonify({"Purchase Probability": int(purchase_prob)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
