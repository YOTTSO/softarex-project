import pickle
import pandas as pd
import datetime
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PredictionForm, UserForm
from .models import Prediction

with open('prediction_app/model.pkl', 'rb') as file:
    loaded_model, scaler, label_encoder_city, label_encoder_type = pickle.load(file)


def replace_open_dates(df):
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y')
    today = datetime.date.today()
    for i in range(len(df)):
        df['Open Date'][i] = (today - df['Open Date'][i].date()).days
    return df['Open Date'].values[0]


@login_required('', 'login', 'login')
def predict_revenue(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            open_date = form.cleaned_data['open_date']
            city = form.cleaned_data['city']
            type = form.cleaned_data['type']
            break_point_1 = form.cleaned_data['break_point_1']
            break_point_2 = form.cleaned_data['break_point_2']
            break_point_3 = form.cleaned_data['break_point_3']
            break_point_4 = form.cleaned_data['break_point_4']
            break_point_5 = form.cleaned_data['break_point_5']
            break_point_6 = form.cleaned_data['break_point_6']
            break_point_7 = form.cleaned_data['break_point_7']
            break_point_8 = form.cleaned_data['break_point_8']
            break_point_9 = form.cleaned_data['break_point_9']
            break_point_10 = form.cleaned_data['break_point_10']
            break_point_11 = form.cleaned_data['break_point_11']
            break_point_12 = form.cleaned_data['break_point_12']

            input_data = pd.DataFrame({
                'Open Date': [open_date],
                'City': [city],
                'Type': [type],
                'Points1': [break_point_1],
                'Points2': [break_point_2],
                'Points3': [break_point_3],
                'Points5': [break_point_4],
                'Points6': [break_point_5],
                'Points7': [break_point_6],
                'Points11': [break_point_7],
                'Points14': [break_point_8],
                'Points21': [break_point_9],
                'Points24': [break_point_10],
                'Points26': [break_point_11],
                'Points37': [break_point_12]
            }, index=[0])

            input_data['Open Date'] = replace_open_dates(input_data)
            input_data['City'] = label_encoder_city.transform(input_data['City'])
            input_data['Type'] = label_encoder_type.transform(input_data['Type'])
            data = scaler.transform(input_data)
            predictions = loaded_model.predict(data)
            predictions = predictions.astype(int)

            prediction = Prediction(
                user=request.user,
                open_date=form.cleaned_data['open_date'],
                city=form.cleaned_data['city'],
                type=form.cleaned_data['type'],
                break_point_1=form.cleaned_data['break_point_1'],
                break_point_2= form.cleaned_data['break_point_2'],
                break_point_3=form.cleaned_data['break_point_3'],
                break_point_4=form.cleaned_data['break_point_4'],
                break_point_5=form.cleaned_data['break_point_5'],
                break_point_6=form.cleaned_data['break_point_6'],
                break_point_7=form.cleaned_data['break_point_7'],
                break_point_8=form.cleaned_data['break_point_8'],
                break_point_9=form.cleaned_data['break_point_9'],
                break_point_10=form.cleaned_data['break_point_10'],
                break_point_11=form.cleaned_data['break_point_11'],
                break_point_12=form.cleaned_data['break_point_12'],
                predicted_revenue=predictions,
            )
            prediction.save()
            return render(request, 'prediction_result.html', {'prediction': predictions[0]})
    else:
        form = PredictionForm()
    return render(request, 'prediction_form.html', {'form': form})

@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'prediction_history.html', {'predictions': predictions})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('predict_revenue')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
