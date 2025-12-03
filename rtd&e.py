import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, SeparableConv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load FER2013 dataset
data = pd.read_csv("fer2013.csv")

# Preprocess images
pixels = data['pixels'].tolist()
faces = np.array([np.fromstring(p, dtype=int, sep=' ').reshape(48,48,1) for p in pixels], dtype='float32')
faces = faces / 255.0

# Labels
labels = to_categorical(data['emotion'], num_classes=7)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(faces, labels, test_size=0.2, random_state=42)

# Build Mini-Xception style CNN
model = Sequential()

model.add(Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(SeparableConv2D(64, (3,3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(SeparableConv2D(128, (3,3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X_train, y_train, batch_size=64, epochs=50, validation_data=(X_test, y_test), shuffle=True)

# Save model
model.save("emotion_model.h5")
print("Model saved as emotion_model.h5")