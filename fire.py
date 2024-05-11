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

# write code to load data as per
# request and train the model

# model.save(f'models/{stockname}_model')
