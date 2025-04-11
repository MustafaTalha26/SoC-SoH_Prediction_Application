import pandas as pd
import numpy as np
import tensorflow as tf
from keras import models, layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib

# Load dataset from CSV
soh_dataset = pd.read_csv(r"../Data/soh_dataset.csv")
print("Dataset imported")

# battery_id dropped because it's a name and not a categorical value. 
# ambient_temperature dropped because only 1 unique value is not helpful.
# cycle dropped because numerical index value is not necessary.
soh_dataset.drop(columns=['battery_id', 'ambient_temperature', 'cycle'], inplace=True)
print("Columns dropped")

X = soh_dataset.drop(columns=['soh']).values  # Features
y = soh_dataset['soh'].values  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Dataset splitted")

# Use MinMaxScaler to scale the features to [0, 1]
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Dataset normalized")

# Save MinMaxScaling
joblib.dump(scaler, 'soh_minmax_scaler.pkl')

# Convert scaled data back to DataFrame for consistency with original DataFrame 
X_train_scaled = pd.DataFrame(X_train_scaled, columns=soh_dataset.drop(columns=['soh']).columns)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=soh_dataset.drop(columns=['soh']).columns)
print("Converted numpy array to Dataframe (Optional)")

# Define the neural network model
model = models.Sequential([
    layers.InputLayer(input_shape=(X_train_scaled.shape[1],)),  # Input layer with number of features
    layers.Dense(128, activation='relu'),  
    layers.Dense(64, activation='relu'),  
    layers.Dense(32, activation='relu'),  
    layers.Dense(1)  # Output layer for regression (single value)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_absolute_error')

# Train the model and capture the training history
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_data=(X_test_scaled, y_test))

# Evaluate the model on the test set
test_loss = model.evaluate(X_test_scaled, y_test)
print(f"Test loss: {test_loss}")

# Make predictions on the test set
predictions = model.predict(X_test_scaled)

# Save the weights to a file
model.save_weights('soh_weights.h5')
print("Model weights saved.")

# Print some predictions
print(f"Predictions: {predictions[:5]}")

# Plotting the loss curve
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss During Training')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig("soh_trainig.png")

# Scatter plot for actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, predictions, color='blue', alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')  # Line of perfect prediction
plt.title('Actual vs Predicted SOH')
plt.xlabel('Actual SOH')
plt.ylabel('Predicted SOH')
plt.grid(True)
plt.legend()
plt.savefig("soh_predictions.png")

# Additional analysis: Print the evaluation of the model on the test set
print(f"Test Loss: {test_loss}")