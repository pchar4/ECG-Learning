import time

import numpy as np 
import tflite_runtime.interpreter as tflite
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_curve, roc_auc_score



#load the numpy arrays from disk
X_train = np.load('./X_train.npy')
X_val = np.load('./X_val.npy')
X_test = np.load('./X_test.npy')
y_train = np.load('./y_train.npy')
y_val = np.load('./y_val.npy')
y_test = np.load('./y_test.npy')


# Load TFLite model
interpreter = tflite.Interpreter(model_path='inference_optimized.tflite')
inputs = interpreter.get_input_details()[0]['index']
outputs = interpreter.get_output_details()[0]['index']

# this code gets us our batching (hopefully)
interpreter.resize_tensor_input(inputs, [1000, 187, 1])
interpreter.resize_tensor_input(outputs, [1000, 7])
interpreter.allocate_tensors()
print(interpreter.get_input_details()[0]['shape'])
print(interpreter.get_output_details()[0]['shape'])
# end of batching specific code

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(input_details[0]['index'])

# Perform batched inference with a batch size of 1000
batch_size = 1000
num_samples = X_test.shape[0]
num_batches = num_samples // batch_size
remainder = num_samples % batch_size

print(X_test.shape)

# ~ # Make predictions
# ~ start_time = time.time() # timing start

# ~ y_pred = []
# ~ for x in X_test:
    # ~ x = np.expand_dims(x, axis=(0, 2)).astype(np.float32)
    # ~ interpreter.set_tensor(input_details[0]['index'], x)
    # ~ interpreter.invoke()
    # ~ output_data = interpreter.get_tensor(output_details[0]['index'])
    # ~ y_pred.append(output_data[0])

# ~ y_pred = np.array(y_pred)
# ~ end_time = time.time() # timing end

# ~ #Convert y to one hot encoding 
# ~ ohe = OneHotEncoder(sparse_output=False)
# ~ y_train = ohe.fit_transform(y_train.reshape(-1,1))
# ~ y_val = ohe.fit_transform(y_val.reshape(-1,1))
# ~ y_test = ohe.transform(y_test.reshape(-1,1))

# ~ n_classes = 7
# ~ class_names = ['Normal','Other','LBBB','RBBB', 'PVC', 'CHF', 'MI']
# ~ # plot ROC curves for each class
# ~ for i in range(n_classes):
    # ~ fpr, tpr, thresholds = roc_curve(y_test[:, i], y_pred[:, i])
    # ~ auc = roc_auc_score(y_test[:, i], y_pred[:, i])
    # ~ # plt.plot(fpr, tpr, label=f'{class_names[i]} (AUC = {auc:.4f})')

# ~ # plot random guessing line
# ~ # plt.plot([0, 1], [0, 1], 'k--')

# ~ # plt.xlabel('False positive rate')
# ~ # plt.ylabel('True positive rate')
# ~ # plt.title('ROC curves')
# ~ # plt.legend()
# ~ # plt.show()

# ~ print(classification_report(y_test.argmax(axis=1), y_pred.argmax(axis=1)))

# ~ elapsed_time = end_time - start_time
# ~ print("Elapsed time: ", elapsed_time)
