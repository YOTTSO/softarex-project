import pickle
import pandas as pd
import datetime
import tkinter as tk
with open('restaurant_app/prediction_app/model.pkl', 'rb') as file:
    loaded_model, scaler, label_encoder_city, label_encoder_type = pickle.load(file)

def replace_open_dates(df):
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y')
    today = datetime.date.today()
    for i in range(len(df)):
        df['Open Date'][i] = (today - df['Open Date'][i].date()).days
    return df['Open Date'].values[0]

def make_prediction():
    data = pd.DataFrame({
        'Open Date': ['06/16/2001'],
        'City': ['Ankara'],
        'Type': ['Food Casual'],
        'Points1': [2],
        'Points2': [3],
        'Points3': [0],
        'Points5': [0],
        'Points6': [0],
        'Points7': [0],
        'Points11': [2],
        'Points14': [0],
        'Points21': [0],
        'Points24': [0],
        'Points26': [0],
        'Points37': [0]
    }, index=[0])

    data['Open Date'] = replace_open_dates(data)
    data['City'] = label_encoder_city.transform(data['City'])
    data['Type'] = label_encoder_type.transform(data['Type'])
    data = scaler.transform(data)
    predictions = loaded_model.predict(data)
    predictions = predictions.astype(int)
    print(predictions)

root = tk.Tk()
root.title("Приложение для предсказаний")

predict_button = tk.Button(root, text="Сделать предсказание", command=make_prediction)
predict_button.pack()

root.mainloop()
