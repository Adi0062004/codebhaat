from flask import Flask, request, render_template  # type: ignore
import tensorflow as tf
from tensorflow.keras import models  # type: ignore
import numpy as np
import yfinance as yf

# what to do
# take the stock name as input
# check if we have a model on the stock, if not, train
# use the stockname to get the data point and predict.


app = Flask(__name__)

stockname = "AAPL"
model = models.load_model(f'models/{stockname}_model')
ticker = yf.Ticker(stockname)
data = ticker.history()


@app.route('/')
def hello_world():
    return render_template("fire.html")  # change file name


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final = [np.array(int_features)]
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)

    if output > str(0.5):
        return render_template('fire.html', pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output))
    else:
        return render_template('fire.html', pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output))


if __name__ == '__main__':
    app.run()
