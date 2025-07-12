import streamlit as st
import pickle

# Load model and brand mapping
model = pickle.load(open('model1.pkl', 'rb'))
brand_mapping = pickle.load(open('brand_map.pkl', 'rb'))
brands = list(brand_mapping.keys())  # Use the same brand list used in training

st.title(" 🚖 Used Car Price Prediction 🚖")

# Brand selection
selected_brand = st.selectbox("Select Brand", brands)
brand_enc = brand_mapping[selected_brand]

# Year of Manufacture
year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, step=1)

# Kilometers Driven
km_driven_input = st.text_input("Kilometers Driven (e.g., 45,000)")
try:
    kmDriven_enc = int(km_driven_input.replace(',', '').strip())
except:
    kmDriven_enc = None

# Transmission
transmission = st.radio("Transmission", ['Manual', 'Automatic'], index=None)
transmission_enc = 1 if transmission == 'Manual' else 0 if transmission == 'Automatic' else None

# Owner
owner = st.radio("Owner Type", ['first', 'second'], index=None)
owner_enc = 1 if owner == 'first' else 0 if owner == 'second' else None

# Fuel Type
fuel = st.radio("Fuel Type", ['Petrol', 'Diesel'], index=None)
fuel_enc = 1 if fuel == 'Petrol' else 0 if fuel == 'Diesel' else None

# Predict Button
if st.button("Predict"):
    if None in [kmDriven_enc, transmission_enc, owner_enc, fuel_enc]:
        st.error("Please fill all fields correctly.")
    else:
        input_data = [[
            brand_enc, year, kmDriven_enc, transmission_enc, owner_enc, fuel_enc
        ]]

        try:
            prediction = model.predict(input_data)[0]

            if prediction < 0:
                st.warning("⚠️ Warning: The model predicted a negative price. Please check the inputs.")
            elif prediction < 50000:
                st.warning(f"⚠️ The predicted price ₹{int(prediction):,} seems too low. Please verify your inputs.")
            else:
                st.success(f"✅ Predicted Used Car Price: ₹{int(prediction):,}")

        except Exception as e:
            st.error(f"⚠️ Error while predicting: {e}")
