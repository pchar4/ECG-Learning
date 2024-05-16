import time

import numpy as np 
from keras.models import Model, load_model
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

model = load_model('./interence_model.h5')

start_time = time.time()
y_pred = model.predict(X_test, batch_size=1)
end_time = time.time()

#Convert y to one hot encoding 
ohe = OneHotEncoder(sparse_output=False)
y_train = ohe.fit_transform(y_train.reshape(-1,1))
y_val = ohe.fit_transform(y_val.reshape(-1,1))
y_test = ohe.transform(y_test.reshape(-1,1))

n_classes = 7
class_names = ['Normal','Other','LBBB','RBBB', 'PVC', 'CHF', 'MI']
# plot ROC curves for each class
for i in range(n_classes):
    fpr, tpr, thresholds = roc_curve(y_test[:, i], y_pred[:, i])
    auc = roc_auc_score(y_test[:, i], y_pred[:, i])
    plt.plot(fpr, tpr, label=f'{class_names[i]} (AUC = {auc:.4f})')

# plot random guessing line
plt.plot([0, 1], [0, 1], 'k--')

plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curves')
plt.legend()
# plt.show()

print(classification_report(y_test.argmax(axis=1), y_pred.argmax(axis=1)))

elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
