import tensorflow as tf
from tensorflow.keras import layers  # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore
from tensorflow.keras.models import Sequential  # type: ignore
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


stockname = str(input("Enter the stock code: "))
ticker = yf.Ticker(stockname)
data = ticker.history(period="10y")
data.reset_index(inplace=True)

closing_prev_day = (data[-2:-1]['Close'])

def support(df1, l, n1, n2):  # n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if (df1.Low[i] > df1.Low[i-1]):
            return 0
    for i in range(l+1, l+n2+1):
        if (df1.Low[i] < df1.Low[i-1]):
            return 0
    return 1


def resistance(df1, l, n1, n2):  # n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if (df1.High[i] < df1.High[i-1]):
            return 0
    for i in range(l+1, l+n2+1):
        if (df1.High[i] > df1.High[i-1]):
            return 0
    return 1


length = len(data)
high = list(data['High'])
low = list(data['Low'])
close = list(data['Close'])
open = list(data['Open'])
bodydiff = [0] * length

highdiff = [0] * length
lowdiff = [0] * length
ratio1 = [0] * length
ratio2 = [0] * length


def isEngulfing(l):
    row = l
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row] < 0.000001:
        bodydiff[row] = 0.000001

    bodydiffmin = 0.002
    if (bodydiff[row] > bodydiffmin and bodydiff[row-1] > bodydiffmin and
        open[row-1] < close[row-1] and
        open[row] > close[row] and
            (open[row]-close[row-1]) >= -0e-5 and close[row] < open[row-1]):  # +0e-5 -5e-5
        return 1

    elif (bodydiff[row] > bodydiffmin and bodydiff[row-1] > bodydiffmin and
          open[row-1] > close[row-1] and
          open[row] < close[row] and
          (open[row]-close[row-1]) <= +0e-5 and close[row] > open[row-1]):  # -0e-5 +5e-5
        return 2
    else:
        return 0


def isStar(l):
    bodydiffmin = 0.0020
    row = l
    highdiff[row] = high[row]-max(open[row], close[row])
    lowdiff[row] = min(open[row], close[row])-low[row]
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row] < 0.000001:
        bodydiff[row] = 0.000001
    ratio1[row] = highdiff[row]/bodydiff[row]
    ratio2[row] = lowdiff[row]/bodydiff[row]

    # and open[row]>close[row]):
    if (ratio1[row] > 1 and lowdiff[row] < 0.2*highdiff[row] and bodydiff[row] > bodydiffmin):
        return 1
    # and open[row]<close[row]):
    elif (ratio2[row] > 1 and highdiff[row] < 0.2*lowdiff[row] and bodydiff[row] > bodydiffmin):
        return 2
    else:
        return 0


def closeResistance(l, levels, lim):
    if len(levels) == 0:
        return 0
    c1 = abs(data.High[l]-min(levels,
             key=lambda x: abs(x-data.High[l]))) <= lim
    c2 = abs(max(data.Open[l], data['Close'][l]) -
             min(levels, key=lambda x: abs(x-data.High[l]))) <= lim
    c3 = min(data.Open[l], data['Close'][l]) < min(
        levels, key=lambda x: abs(x-data.High[l]))
    c4 = data.Low[l] < min(levels, key=lambda x: abs(x-data.High[l]))
    if ((c1 or c2) and c3 and c4):
        return 1
    else:
        return 0


def closeSupport(l, levels, lim):
    if len(levels) == 0:
        return 0
    c1 = abs(data.Low[l]-min(levels, key=lambda x: abs(x-data.Low[l]))) <= lim
    c2 = abs(min(data.Open[l], data.Close[l]) -
             min(levels, key=lambda x: abs(x-data.Low[l]))) <= lim
    c3 = max(data.Open[l], data.Close[l]) > min(
        levels, key=lambda x: abs(x-data.Low[l]))
    c4 = data.High[l] > min(levels, key=lambda x: abs(x-data.Low[l]))
    if ((c1 or c2) and c3 and c4):
        return 1
    else:
        return 0


n1 = 2
n2 = 2
backCandles = 3
signal = [0] * length

for row in range(backCandles, len(data)-n2):
    ss = []
    rr = []
    for subrow in range(row-backCandles+n1, row+1):
        if support(data, subrow, n1, n2):
            ss.append(data.Low[subrow])
        if resistance(data, subrow, n1, n2):
            rr.append(data.High[subrow])
    #!!!! parameters
    # and df.RSI[row]<30
    if ((isEngulfing(row) == 1 or isStar(row) == 1) and closeResistance(row, rr, 150e-5)):
        signal[row] = 1
    # and df.RSI[row]>70
    elif ((isEngulfing(row) == 2 or isStar(row) == 2) and closeSupport(row, ss, 150e-5)):
        signal[row] = 2
    else:
        signal[row] = 0

data['signal'] = signal

data['RSI'] = ta.rsi(data.Close, length=15)
data['EMAF'] = ta.ema(data.Close, length=20)
data['EMAM'] = ta.ema(data.Close, length=100)
data['EMAS'] = ta.ema(data.Close, length=150)

data['TargetNextClose'] = data['Close'].shift(-1)

data.dropna(inplace=True)
data.reset_index(inplace=True)
data.drop(['Volume', 'Close', 'Date', 'Dividends',
          'Stock Splits'], axis=1, inplace=True)

data_set = pd.concat([data.iloc[:, 0:8], data.iloc[:, -1]], axis=1)
pd.set_option('display.max_columns', None)


sc = StandardScaler()
data_set_scaled = sc.fit_transform(data_set)

X = []

backcandles = 3
print(data_set_scaled.shape[0])
for j in range(7):
    X.append([])
    for i in range(backcandles, data_set_scaled.shape[0]):  # backcandles+2
        X[j].append(data_set_scaled[i-backcandles:i, j+1])

X = np.moveaxis(X, [0], [2])

X, yi = np.array(X), np.array(data_set_scaled[backcandles:, -1])
y = np.reshape(yi, (len(yi), 1))


def windowed_df_to_date_X_y(data):
    df_as_np = data.to_numpy()

    dates = df_as_np[:, 0]

    middle_matrix = df_as_np[:, 1:-1]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

    Y = df_as_np[:, -1]

    return dates, X.astype(np.float32), Y.astype(np.float32)


dates, X00, y = windowed_df_to_date_X_y(data)


q_80 = int(len(dates) * .8)
q_90 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:q_80], X[:q_80][:][:], y[:q_80]

dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

plt.plot(dates_train, y_train)
plt.plot(dates_val, y_val)
plt.plot(dates_test, y_test)

plt.legend(['Train', 'Validation', 'Test'])
# plt.show()


model = Sequential([layers.Input((backcandles, 7)),
                    layers.LSTM(64),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(1)])

model.compile(loss='mse',
              optimizer=Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])

model.fit(X_train, y_train, validation_data=(
    X_val, y_val), epochs=100, verbose=0)


# train_predictions = model.predict(X_train).flatten()
# plt.plot(dates_train, train_predictions)
# plt.plot(dates_train, y_train)
# plt.legend(['Training Predictions', 'Training Observations'])
# plt.show()


# val_predictions = model.predict(X_val).flatten()
# plt.plot(dates_val, val_predictions)
# plt.plot(dates_val, y_val)
# plt.legend(['Validation Predictions', 'Validation Observations'])
# plt.show()

closing_next_day = model.predict(X[-2:-1])
print("Opening for the next day: ", float(closing_prev_day))
print("Closing for the next day: ", float(closing_next_day))
