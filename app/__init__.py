from flask import Flask, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.decomposition import PCA
from sklearn import preprocessing
# import tensorflow as tf
import seaborn as sns



np.random.seed(5)
sns.set_style('darkgrid')


app = Flask(__name__,
            static_url_path='', 
            # static_folder='app/static',
            # template_folder='app/templates'
            )


from app import views
# # Saeed Shamsi sh4msi@gmail.com
