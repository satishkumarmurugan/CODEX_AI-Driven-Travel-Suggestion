from flask import Flask, request, render_template, redirect
from joblib import load
import pandas as pd

app = Flask(__name__)

# Load the model and label encoders
features = ["Trip_Type", "Surroundings", "Room_Type", "Season", "Duration_Days", "Activity_To_Perform"]
loaded_model = load('ID3.joblib')
le_features = {col: load(f'{col}_encoder.joblib') for col in features}
le_labels = load('labels_encoder.joblib')

@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    # Extract form data
    trip_type = request.form.get('Trip_Type')
    Surroundings = request.form.get('Surroundings')
    room_type = request.form.get('Room_Type')
    Season = request.form.get('Season')
    Duration_Days = int(request.form.get('Duration_Days'))
    Activity_To_Perform = request.form.getlist('Activity_To_Perform') 
  

    # Encode the input data
    user_input_encoded = {
        'Trip_Type': le_features['Trip_Type'].transform([trip_type])[0],
        'Surroundings': le_features['Surroundings'].transform([Surroundings])[0],
        'Room_Type': le_features['Room_Type'].transform([room_type])[0],
        'Season': le_features['Season'].transform([Season])[0],
        'Duration_Days': Duration_Days,
        'Activity_To_Perform': le_features['Activity_To_Perform'].transform(Activity_To_Perform)[0]
    }

    # Create a DataFrame from the encoded input
    user_input_df = pd.DataFrame([user_input_encoded])

    # Make a prediction
    prediction_encoded = loaded_model.predict(user_input_df)
    prediction = le_labels.inverse_transform(prediction_encoded)

    print("Predicted Destination:", prediction[0])
    pack=prediction[0]

    pack = str(prediction[0])

    # Replace spaces in the prediction with hyphens and concatenate with the URL
    pack_small = pack.lower()
    pack_url_safe = pack_small.replace(" ", "-")

    
    # Assuming Budget is a variable containing the budget value
    url = "https://www.thomascook.in/holidays/india-tour-packages/" + pack_url_safe + "-tour-packages?holidayBudget=1,100000"

    # Redirecting to the desired URL
    return redirect(url)
    



@app.route('/')
def form():
    # Render and return the index.html template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
