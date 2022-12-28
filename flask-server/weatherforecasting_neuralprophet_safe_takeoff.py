


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, datetime, timedelta, date
import seaborn as sns
from neuralprophet import NeuralProphet
import warnings
warnings.filterwarnings('ignore')



df = pd.read_csv("datasets/weather_data.csv")

df['time_stamp'] = pd.to_datetime(df['time_stamp'])
df.set_index('time_stamp')

df.info()

df.describe

temp_smooth = df.temperature.rolling(window=24).mean()
temp_smooth.isnull().sum()

temp = df.drop('time_stamp', axis=1)



df['date'] = df['time_stamp'].dt.date
df['year'] = df['time_stamp'].dt.year
df['month'] = df['time_stamp'].dt.month



df2 = df[['temperature','dewpoint_temperature','wind_speed','mean_sea_level_pressure','relative_humidity','surface_solar_radiation','surface_thermal_radiation','total_cloud_cover']]

print('Hello',1)

from statsmodels.tsa.seasonal import seasonal_decompose

temp_add_decomp = seasonal_decompose(df.temperature, model='multiplicative', extrapolate_trend='freq', period=365*24)



df1 = df[df['date'] >= date(2017,1,1)]
dfbefore2021 = df[df['year']<2021]


print('Hello',2)


df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'temperature']]
df.time_stamp = pd.to_datetime(df.time_stamp)

avgtemp = pd.DataFrame(df1.groupby(['date'])['temperature'].mean())
temp_add = seasonal_decompose(avgtemp['temperature'], model='additive',extrapolate_trend='freq',period=365)



yearlytemp = pd.DataFrame(dfbefore2021.groupby(['year'])['temperature'].mean())

print('Hello',3)

df.rename(columns = {'time_stamp':'ds', 'temperature':'y'}, inplace = True)


print('Hello',4)


m = NeuralProphet(changepoints_range=0.95, 
                  n_changepoints=50, 
                  trend_reg=1, 
                  weekly_seasonality=False, 
                  daily_seasonality=10, 
                  yearly_seasonality=10)

df['ds'] = pd.DatetimeIndex(df['ds'])
df.head()

df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
metrics = m.fit(df_train, freq='H', validation_df=df_val)

seasonal_components = m.predict_seasonal_components(df)
seasonal_components

metrics



future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
future.tail()

forecast = m.predict(future)

forecast

forecast_df = forecast.copy()
forecast_df.info()

df.info()



forecast_plot = m.plot(forecast)

forecast.to_csv( "temperature_prediction.csv", index=False)
print("hello")
"""# <a>Wind Speed</a>"""

df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'wind_speed']]

df.time_stamp = pd.to_datetime(df.time_stamp)

avgwindspeed = pd.DataFrame(df1.groupby(['date'])['wind_speed'].mean())
windspeed_add = seasonal_decompose(avgwindspeed['wind_speed'], model='additive',extrapolate_trend='freq',period=365)


windspeed_add.plot().suptitle('Additive Decomposition', fontsize=22)

monthlywind = pd.DataFrame(dfbefore2021.groupby(['month'])['wind_speed'].mean())
months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
monthlywind['Month']=months


df.rename(columns = {'time_stamp':'ds', 'wind_speed':'y'}, inplace = True)



m = NeuralProphet(changepoints_range=0.95, 
                  n_changepoints=50, 
                  trend_reg=1, 
                  weekly_seasonality=False, 
                  daily_seasonality=10, 
                  yearly_seasonality=10)

df['ds'] = pd.DatetimeIndex(df['ds'])
df.head()

m = NeuralProphet(changepoints_range=0.95, n_changepoints=50, trend_reg=1, weekly_seasonality=False, daily_seasonality=10)
df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
metrics = m.fit(df_train, freq='H', validation_df=df_val)

metrics



future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
forecast = m.predict(future)

forecast

m.plot_components(forecast)

forecast_plot = m.plot(forecast)

forecast.to_csv( "windspeed_prediction.csv", index=False)

"""# <a>Pressure</a>"""

df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'mean_sea_level_pressure']]
df.time_stamp = pd.to_datetime(df.time_stamp)

avgpressure = pd.DataFrame(df1.groupby(['date'])['mean_sea_level_pressure'].mean())
pressure_add = seasonal_decompose(avgpressure['mean_sea_level_pressure'], model='additive',extrapolate_trend='freq',period=365)


pressure_add.plot().suptitle('Additive Decomposition', fontsize=22)

monthlypressure = pd.DataFrame(dfbefore2021.groupby(['month'])['mean_sea_level_pressure'].mean())
months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
monthlypressure['Month']=months

df.rename(columns = {'time_stamp':'ds', 'mean_sea_level_pressure':'y'}, inplace = True)

df['ds'] = pd.DatetimeIndex(df['ds'])
df.head()





m = NeuralProphet(changepoints_range=0.95, 
                  n_changepoints=50, 
                  trend_reg=1, 
                  weekly_seasonality=False, 
                  daily_seasonality=10, 
                  yearly_seasonality=10)

df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
metrics = m.fit(df_train, freq='H', validation_df=df_val)

metrics

fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(metrics["MAE"], '-o', label="Training Loss")  
ax.plot(metrics["MAE_val"], '-r', label="Validation Loss")
ax.legend(loc='center right', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.set_xlabel("Epoch", fontsize=28)
ax.set_ylabel("Loss", fontsize=28)
ax.set_title("Model Loss (MAE)", fontsize=28)

future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
forecast = m.predict(future)

forecast


forecast_plot = m.plot(forecast)

forecast.to_csv( "pressure_prediction.csv", index=False)

"""# <a>Total Cloud Cover</a>"""

df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'total_cloud_cover']]
df.time_stamp = pd.to_datetime(df.time_stamp)

avgcloud = pd.DataFrame(df1.groupby(['date'])['total_cloud_cover'].mean())
cloud_add = seasonal_decompose(avgcloud['total_cloud_cover'], model='additive',extrapolate_trend='freq',period=365)


cloud_add.plot().suptitle('Additive Decomposition', fontsize=22)

monthlycloud = pd.DataFrame(dfbefore2021.groupby(['month'])['total_cloud_cover'].mean())
months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
monthlycloud['Month']=months


df.rename(columns = {'time_stamp':'ds', 'total_cloud_cover':'y'}, inplace = True)

df['ds'] = pd.DatetimeIndex(df['ds'])
df.head()



m = NeuralProphet(changepoints_range=0.95, 
                  n_changepoints=50, 
                  trend_reg=1, 
                  weekly_seasonality=False, 
                  daily_seasonality=10, 
                  yearly_seasonality=10)

df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
metrics = m.fit(df_train, freq='H', validation_df=df_val)

metrics



future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
forecast = m.predict(future)

forecast


forecast_plot = m.plot(forecast)

forecast.to_csv( "cloudcover_prediction.csv", index=False)

temp= pd.read_csv('temperature_prediction.csv')
cloudcover= pd.read_csv('cloudcover_prediction.csv')
pressure= pd.read_csv('pressure_prediction.csv')
wind= pd.read_csv('windspeed_prediction.csv')

new= temp["ds"].str.split(" ", n = 1, expand = True)
temp['datestamp'] = pd.to_datetime(temp['ds'])
temp['date'] = new[0]
temp['time'] = new[1]
temp['hour'] = temp['datestamp'].dt.hour

new= cloudcover["ds"].str.split(" ", n = 1, expand = True)
cloudcover['datestamp'] = pd.to_datetime(cloudcover['ds'])
cloudcover['date'] = new[0]
cloudcover['time'] = new[1]
cloudcover['hour'] = cloudcover['datestamp'].dt.hour
cloudcover['date'] = new[0]
cloudcover['time'] = new[1]

new= wind["ds"].str.split(" ", n = 1, expand = True)
wind['datestamp'] = pd.to_datetime(wind['ds'])
wind['date'] = new[0]
wind['time'] = new[1]
wind['hour'] = wind['datestamp'].dt.hour
wind['date'] = new[0]
wind['time'] = new[1]

new= pressure["ds"].str.split(" ", n = 1, expand = True)
pressure['datestamp'] = pd.to_datetime(pressure['ds'])
pressure['date'] = new[0]
pressure['time'] = new[1]
pressure['hour'] = pressure['datestamp'].dt.hour
pressure['date'] = new[0]
pressure['date'] = new[1]

final =pd.DataFrame()

final['datestamp'] = temp['datestamp'].astype(str)
final['date'] = temp['date']
final['time'] = temp['time']
final['hour'] = temp['hour']
final['temperature'] = temp['yhat1']
final['windspeed'] = wind['yhat1']
final['pressure'] = pressure['yhat1']
final['cloudcover'] = cloudcover['yhat1']

final.to_csv('allpredicted2.csv',index=False)

