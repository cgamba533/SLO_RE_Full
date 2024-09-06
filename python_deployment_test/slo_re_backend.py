from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load('model.pkl')  # Ensure this is the correct model

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Create DataFrame with the correct columns and data in the right order
        df = pd.DataFrame([[data['Lot Size'], data['List Price'], data['Baths'], 
                            data['Structure Type'], data['Beds'], data['Square Footage'], 
                            data['HOA Fee'], data['Stories'], data['Attached Garage'], 
                            data['New Construction']]], 
                            columns=['Lot Size', 'List Price', 'Baths', 'Structure Type', 
                                     'Beds', 'Square Footage', 'HOA Fee', 'Stories', 
                                     'Attached Garage', 'New Construction'])
        
        # Ensure correct data types
        df = df.astype({
            'Lot Size': float,
            'List Price': float,
            'Baths': float,
            'Structure Type': str,
            'Beds': int,
            'Square Footage': int,
            'HOA Fee': float,
            'Stories': int,
            'Attached Garage': str,  # Adjusted to string for OneHotEncoder
            'New Construction': int  # Already 0 or 1, so kept as int
        })
        
        # Make prediction
        prediction = model.predict(df)[0]  # Get the first (and only) element
        class_probabilities = model.predict_proba(df)[0]  # Probabilities for all classes
        
        # Assuming the model was trained on a set of labels like ['fast', 'average', 'slow']
        labels = model.classes_  # Get the class labels from the model
        probabilities = {label: prob for label, prob in zip(labels, class_probabilities)}  # Map labels to probabilities
        
        # Print for debugging
        print(f"Prediction: {prediction}")
        print(f"Probabilities: {probabilities}")

        # Return prediction and probabilities in the desired format
        return jsonify({
            'prediction': str(prediction),  # Ensure prediction is a string
            'probabilities': probabilities  # Return the probabilities mapped to labels
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
