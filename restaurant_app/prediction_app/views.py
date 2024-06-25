import json
import pickle
from time import sleep

import pandas as pd
import datetime
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PredictionForm, UserForm
from .models import Prediction
from confluent_kafka import Producer, Consumer


conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'django_group',
    'auto.offset.reset': 'earliest'
}

def wait_for_kafka():
    while True:
        try:
            producer = Producer(conf)
            producer.purge()
            print("Kafka готова!")
            break
        except Exception as e:
            print(f"Ошибка подключения к Kafka: {e}")
            sleep(5)

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
            })

            wait_for_kafka()
            input_json = input_data.to_json(orient='records')
            producer = Producer(conf)
            producer.produce('input_topic', json.dumps(input_json).encode('utf-8'))
            producer.flush()

            consumer = Consumer(conf)
            consumer.subscribe(['output_topic'])
            msg = consumer.poll(200.0)
            if msg is None:
                predictions = 69
            else:
                response = json.loads(msg.value().decode('utf-8'))
                predictions = int(msg.value().decode('utf-8'))
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
            return render(request, 'prediction_result.html', {'prediction': prediction})
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
