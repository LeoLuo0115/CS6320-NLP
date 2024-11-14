import matplotlib.pyplot as plt

# Updated log data
epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
training_accuracy = [
    0.534625, 0.581875, 0.618125, 0.647125, 0.65775,
    0.6945, 0.718875, 0.741, 0.767625, 0.781625
]
validation_accuracy = [
    0.54375, 0.58375, 0.59375, 0.54, 0.5975,
    0.60375, 0.54625, 0.56625, 0.6175, 0.61875
]

# Plotting the learning curve
plt.figure(figsize=(10, 6))
plt.plot(epochs, training_accuracy, label='Training Accuracy')
plt.plot(epochs, validation_accuracy, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Learning Curve')
plt.legend()
plt.savefig('ffnn_learning_curve.png', dpi=300, bbox_inches='tight')
plt.show()
