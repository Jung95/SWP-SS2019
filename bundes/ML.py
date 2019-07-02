import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

column_names = ['Datum','Heim','Gast','Tore Heim','Tore Gast']
raw_dataset = pd.read_csv('2017.csv', names = column_names)

dataset = raw_dataset.copy()
