import pandas as pd
import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import pickle
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import seaborn as sns

def replace_open_dates(df):
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y')
    today = datetime.date.today()
    for i in range(len(df)):
        df['Open Date'][i] = (today - df['Open Date'][i].date()).days
    return df

data_train = pd.read_csv("datasets/train.csv")
data_test = pd.read_csv("datasets/test.csv")
y_test = pd.read_csv("datasets/sampleSubmission.csv")["Prediction"]
data_train = replace_open_dates(data_train)
data_test = replace_open_dates(data_test)

for i in range(1, 38):
    column_name = f'Points{i}'
    data_train[column_name] = data_train[column_name].astype(float)
    data_test[column_name] = data_test[column_name].astype(float)

X_train = data_train[["Open Date", "City", "Type", "Points1", "Points2", "Points3", "Points5", "Points6",
                      "Points7", "Points11", "Points14", "Points21", "Points24", "Points26", "Points37"]]
y_train = data_train.revenue

X_test = data_test[["Open Date", "City", "Type", "Points1", "Points2", "Points3", "Points5", "Points6",
                      "Points7", "Points11", "Points14", "Points21", "Points24", "Points26", "Points37"]]

X_all = pd.concat([X_train, X_test])

label_encoder_city = LabelEncoder()
label_encoder_type = LabelEncoder()
X_all['City'] = label_encoder_city.fit_transform(X_all['City'])
X_all['Type'] = label_encoder_type.fit_transform(X_all['Type'])


X_train = X_all[:len(X_train)]
X_test = X_all[len(X_train):]

correlations = X_train.corrwith(data_train['revenue'])
correlations_df = pd.DataFrame({'Correlation': correlations})
correlations_df = correlations_df.sort_values(by='Correlation', ascending=False)
plt.figure(figsize=(12, 10))
sns.heatmap(correlations_df.T, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Корреляция признаков с revenue")
plt.show()

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

param_grid = {
    'n_estimators': [500, 1000, 1500],
    'max_depth': [5, 7, 9],
    'learning_rate': [0.01, 0.05, 0.1],
    'gamma': [0.0, 0.1, 0.2]
}

model = XGBRegressor(objective='reg:squarederror',
                    n_estimators=1000,
                    max_depth=7,
                    learning_rate=0.03,
                    gamma=0.1)

# grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error', cv=5)
# grid_search.fit(X_train, y_train)
#
# best_params = grid_search.best_params_
# model = XGBRegressor(objective='reg:squarederror', **best_params)

model.fit(X_train, y_train,  eval_set=[(X_train, y_train)],
          eval_metric='rmse', verbose=True, early_stopping_rounds=4)

evals_result = model.evals_result()
rmse = evals_result['validation_0']['rmse'][-1]
print(f"Корневая среднеквадратичная ошибка (RMSE): {rmse}")

with open('../restaurant_app/prediction_app/model.pkl', 'wb') as file:
    pickle.dump([model, scaler, label_encoder_city, label_encoder_type], file)

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
