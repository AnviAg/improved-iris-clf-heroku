# Importing the necessary libraries.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Loading the dataset.
iris_df = pd.read_csv("iris-species.csv")

# Adding a column in the Iris DataFrame to resemble the non-numeric 'Species' column as numeric using the 'map()' function.
# Creating the numeric target column 'Label' to 'iris_df' using the 'map()' function.
iris_df['Label'] = iris_df['Species'].map({'Iris-setosa': 0, 'Iris-virginica': 1, 'Iris-versicolor': 2})


# Creating features and target DataFrames.
X = iris_df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
y = iris_df['Label']

# Splitting the dataset into train and test sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Creating an SVC model. 
svc_model = SVC(kernel='linear')
svc_model.fit(X_train, y_train)

# Creating a Logistic Regression model. 
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Creating a Random Forest Classifier model.
rfc_model = RandomForestClassifier(n_jobs = -1, n_estimators=100)
rfc_model.fit(X_train, y_train)

# Predict function to take input and predict the species
@st.cache()
def prediction(model, SepalLength, SepalWidth, PetalLength, PetalWidth):
  species = model.predict([[SepalLength, SepalWidth, PetalLength, PetalWidth]])
  species = species[0]
  if species == 0:
    return "Iris-setosa"
  elif species == 1:
    return "Iris-virginica"
  else:
    return "Iris-versicolor"

# Add title widget
st.sidebar.title("Iris Flower Species Prediction App")  

# Add 4 sliders and store the value returned by them in 4 separate variables. 
sepal_length = st.sidebar.slider("Sepal Length", float(iris_df['SepalLengthCm'].min()), float(iris_df['SepalLengthCm'].max()))
sepal_width = st.sidebar.slider("Sepal Width", float(iris_df['SepalWidthCm'].min()), float(iris_df['SepalWidthCm'].max()))
petal_length = st.sidebar.slider("Petal Length", float(iris_df['PetalLengthCm'].min()), float(iris_df['PetalLengthCm'].max()))
petal_width = st.sidebar.slider("Petal Width", float(iris_df['PetalWidthCm'].min()), float(iris_df['PetalWidthCm'].max()))

# The 'float()' function converts the 'numpy.float' values to Python float values.


# Add a select box in the sidebar with the 'Classifier' label.
# Also pass 3 options as a tuple ('Support Vector Machine', 'Logistic Regression', 'Random Forest Classifier').
# Store the current value of this slider in the 'classifier' variable.
classifier = st.sidebar.selectbox('Classifier', ('Support Vector Machine', 'Logistic Regression', 'Random Forest Classifier'))

# When the 'Predict' button is clicked, check which classifier is chosen and call the 'prediction()' function.
# Store the predicted value in the 'species_type' variable accuracy score of the model in the 'score' variable. 
# Print the values of 'species_type' and 'score' variables using the 'st.text()' function.
if st.sidebar.button("Predict"):
  if classifier == 'Support Vector Machine':
    species_type = prediction(svc_model, sepal_length, sepal_width, petal_length, petal_width)
    score = svc_model.score(X_train, y_train)
  elif classifier == 'Logistic Regression':
    species_type = prediction(lr_model, sepal_length, sepal_width, petal_length, petal_width)
    score = lr_model.score(X_train, y_train)
  else:
    species_type = prediction(rfc_model, sepal_length, sepal_width, petal_length, petal_width)
    score = rfc_model.score(X_train, y_train)

  st.write("Species predicted:", species_type)
  st.write("Accuracy score of this model is:", score)
