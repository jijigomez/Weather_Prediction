
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def reg(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Create a new user with a hashed password
        user = User.objects.create(username=username, email=email, password=make_password(password))
        return redirect('log')  # Redirect to the login page

    return render(request, 'reg.html')
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import redirect

def log(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect
            login(request, user)
            return redirect('index')  # Replace 'home' with your target view name
        else:
            return render(request, 'log.html', {'error': 'Invalid username or password'})

    return render(request, 'log.html')


def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def cont(request):
    template = loader.get_template('cont.html')
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import joblib

# Load the model, scaler, and label encoder at the start
MODEL_PATH = "app8/ml_models/weather_model.pkl"
SCALER_PATH = "app8/ml_models/scaler.pkl"
ENCODER_PATH = "app8/ml_models/label_encoder.pkl"

# Load components
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoder = joblib.load(ENCODER_PATH)

from django.shortcuts import render
import pandas as pd
# from .models import model, scaler, label_encoder  # Ensure the model, scaler, and label encoder are correctly imported

def predict_weather(request):
    if request.method == "POST":
        # Extract data from the POST request
        try:
            precipitation = float(request.POST.get('precipitation', 0))
            temp_max = float(request.POST.get('temp_max', 0))
            temp_min = float(request.POST.get('temp_min', 0))
            wind = float(request.POST.get('wind', 0))
        except ValueError:
            # Handle invalid inputs
            return render(request, "predict.html", {
                "error": "Invalid input. Please enter numeric values for all fields."
            })
        
        # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            'precipitation': [precipitation],
            'temp_max': [temp_max],
            'temp_min': [temp_min],
            'wind': [wind]
        })
        
        # Scale the input data (ensure you have the correct scaler object)
        scaled_data = scaler.transform(input_data)
        
        # Predict the encoded label
        predicted_label_encoded = model.predict(scaled_data)
        
        # Decode to the original weather category
        predicted_label = label_encoder.inverse_transform(predicted_label_encoded)[0]
        
       
        
        # Render the template with the prediction results and dynamic background
        return render(request, "predict.html", {
            "prediction": predicted_label,
            
            "input_data": {
                "precipitation": precipitation,
                "temp_max": temp_max,
                "temp_min": temp_min,
                "wind": wind
            }
        })
    
    # Render the prediction form if GET request
    return render(request, "predict.html")
