import streamlit as st
import requests

# API Endpoints
SEGMENTATION_API_URL = "http://127.0.0.1:5000/segment"  # Update if deployed elsewhere
PURCHASE_PROB_API_URL = "http://127.0.0.1:5000/purchase-probability"  # Update if deployed elsewhere

st.title("Customer Insights Dashboard 📊")

# Navigation
option = st.sidebar.radio("Select Action", ["Customer Segmentation", "Purchase Probability"])

# ---------------------- CUSTOMER SEGMENTATION ----------------------
if option == "Customer Segmentation":
    st.header("Customer Segmentation 📌")

    # User Inputs
    age = st.number_input("Age", min_value=18, max_value=100, value=25)
    purchase_amount = st.number_input("Purchase Amount (USD)", min_value=20, value=50)

    # Button to Predict
    if st.button("Predict Segment"):
        data = {
            "Age": age,
            "Purchase Amount (USD)": purchase_amount
        }
        
        response = requests.post(SEGMENTATION_API_URL, json=data)
        
        if response.status_code == 200:
            st.success(f"Predicted Customer Segment: {response.json()['Customer Segment']}")
        else:
            st.error("Error in prediction. Check API.")

# ---------------------- PURCHASE PROBABILITY ----------------------
elif option == "Purchase Probability":
    st.header("Purchase Probability Prediction 🎯")

    # User Inputs
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    prev_purchases = st.number_input("Previous Purchases", min_value=1, value=5)
    purchase_amount = st.number_input("Purchase Amount (USD)", min_value=20, value=100)
    review_rating = st.slider("Review Rating", min_value=1.0, max_value=5.0, step=0.1, value=4.0)

    # Button to Predict
    if st.button("Predict Probability"):
        data = {
            "Age": age,
            "Previous Purchases": prev_purchases,
            "Purchase Amount (USD)": purchase_amount,
            "Review Rating": review_rating
        }
        
        response = requests.post(PURCHASE_PROB_API_URL, json=data)
        
        if response.status_code == 200:
            st.success(f"Purchase Probability: {response.json()['Purchase Probability']}")
        else:
            st.error("Error in prediction. Check API.")

