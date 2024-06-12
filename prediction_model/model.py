import pandas as pd
import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

def replace_open_dates(df):
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y')
    today = datetime.date.today()
    for i in range(len(df)):
        df['Open Date'][i] = (today - df['Open Date'][i].date()).days
    return df


data_train = pd.read_csv("train.csv")
data_test = pd.read_csv("test.csv")
y_test = pd.read_csv("sampleSubmission.csv")["Prediction"]
data_train = replace_open_dates(data_train)
data_test = replace_open_dates(data_test)

for i in range(1, 38):
    column_name = f'Points{i}'
    data_train[column_name] = data_train[column_name].astype(float)
    data_test[column_name] = data_test[column_name].astype(float)

X_train = data_train[["Open Date", "City", "Type", "Points1", "Points2", "Points3", "Points4", "Points5", "Points6",
                      "Points7", "Points8", "Points9", "Points10", "Points11", "Points12", "Points13", "Points14",
                      "Points15", "Points16", "Points17", "Points18", "Points19", "Points20", "Points21", "Points22",
                      "Points23", "Points24", "Points25", "Points26", "Points27", "Points28", "Points29", "Points30",
                      "Points31", "Points32", "Points33", "Points34", "Points35", "Points36", "Points37"]]
y_train = data_train.revenue

X_test = data_test[["Open Date", "City", "Type", "Points1", "Points2", "Points3", "Points4", "Points5", "Points6",
                      "Points7", "Points8", "Points9", "Points10", "Points11", "Points12", "Points13", "Points14",
                      "Points15", "Points16", "Points17", "Points18", "Points19", "Points20", "Points21", "Points22",
                      "Points23", "Points24", "Points25", "Points26", "Points27", "Points28", "Points29", "Points30",
                      "Points31", "Points32", "Points33", "Points34", "Points35", "Points36", "Points37"]]


X_all = pd.concat([X_train, X_test])

label_encoder = LabelEncoder()
X_all['City'] = label_encoder.fit_transform(X_all['City'])
X_all['Type'] = label_encoder.fit_transform(X_all['Type'])

X_all = pd.get_dummies(X_all, columns=["City", "Type"])

X_train = X_all[:len(X_train)]
X_test = X_all[len(X_train):]

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = XGBRegressor(objective='reg:squarederror',
                    n_estimators=1000,
                    max_depth=7,
                    learning_rate=0.04,
                    gamma=0.1)

model.fit(X_train, y_train,  eval_set=[(X_train, y_train)],
          eval_metric='rmse', verbose=True, early_stopping_rounds=7)

evals_result = model.evals_result()

predictions = model.predict(X_test)
predictions = predictions.astype(int)
print(predictions)

mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print(f"Среднеквадратичная ошибка (MSE): {mse}")
print(f"Средняя абсолютная ошибка (MAE): {mae}")

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.scatter(y_test, predictions)
plt.xlabel("Фактические значения")
plt.ylabel("Прогнозы")
plt.title("Сравнение фактических значений и прогнозов")

plt.tight_layout()
plt.show()
