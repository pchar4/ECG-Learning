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
# ~ interpreter.resize_tensor_input(outputs, [1000, 7])
interpreter.allocate_tensors()
print(interpreter.get_input_details()[0]['shape'])
print(interpreter.get_output_details()[0]['shape'])
# end of batching specific code

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(input_details[0]['index'])

# Reshape the data into batches of size 1000 x 187 x 1
batch_size = 1000
num_batches = X_test.shape[0] // batch_size
remainder = X_test.shape[0] % batch_size

batches = []
for i in range(num_batches):
    batch = X_test[i * batch_size: (i + 1) * batch_size, :, np.newaxis]
    batches.append(batch)

# If there are remaining rows, you can handle them separately
if remainder > 0:
    remaining_batch = X_test[num_batches * batch_size:, :, np.newaxis]
    # ~ batches.append(remaining_batch)

# 'batches' now contains a list of matrices of size 1000 x 187 x 1

# Make predictions
start_time = time.time() # timing start

y_pred = []
for batch in batches:
    batch = batch.astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], batch)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    y_pred.append(output_data[0])

y_pred = np.array(y_pred)
end_time = time.time() # timing end

#Convert y to one hot encoding 
ohe = OneHotEncoder(sparse_output=False)
y_train = ohe.fit_transform(y_train.reshape(-1,1))
y_val = ohe.fit_transform(y_val.reshape(-1,1))
y_test = ohe.transform(y_test.reshape(-1,1))

n_classes = 7
class_names = ['Normal','Other','LBBB','RBBB', 'PVC', 'CHF', 'MI']
# plot ROC curves for each class
# ~ for i in range(n_classes):
    # ~ fpr, tpr, thresholds = roc_curve(y_test[:, i], y_pred[:, i])
    # ~ auc = roc_auc_score(y_test[:, i], y_pred[:, i])
    # plt.plot(fpr, tpr, label=f'{class_names[i]} (AUC = {auc:.4f})')

# plot random guessing line
# plt.plot([0, 1], [0, 1], 'k--')

# plt.xlabel('False positive rate')
# plt.ylabel('True positive rate')
# plt.title('ROC curves')
# plt.legend()
# plt.show()
print(y_pred.shape)
print(y_pred)
print(y_test.shape)
print(classification_report(y_test.argmax(axis=1), y_pred.argmax(axis=1)))

elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
