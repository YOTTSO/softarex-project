import json
import datetime
import pandas as pd
from confluent_kafka import Consumer, Producer
import pickle, os

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')

conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'model_group',
    'auto.offset.reset': 'earliest'
}

with open('./model.pkl', 'rb') as file:
    loaded_model, scaler, label_encoder_city, label_encoder_type = pickle.load(file)


def replace_open_dates(df):
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y')
    today = datetime.date.today()
    for i in range(len(df)):
        df['Open Date'][i] = (today - df['Open Date'][i].date()).days
    return df['Open Date'].values[0]


consumer = Consumer(conf)
producer = Producer(conf)
consumer.subscribe(['input_topic'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    df_json = json.loads(msg.value().decode('utf-8'))
    input_df = pd.read_json(df_json, orient='records')

    input_df['Open Date'] = replace_open_dates(input_df)
    input_df['City'] = label_encoder_city.transform(input_df['City'])
    input_df['Type'] = label_encoder_type.transform(input_df['Type'])
    data = scaler.transform(input_df)
    predictions = loaded_model.predict(data)
    predictions = predictions.astype(int)
    producer.produce('output_topic', str(predictions[0]).encode('utf-8'))
    producer.flush()
