"""
    自动回调类来计算并输出评估指标 --- 准确率、召回率和假阳率
"""
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix
from tensorflow.python.keras.callbacks import Callback


class Metrics(Callback):
    def __init__(self, validation_data):
        super(Metrics, self).__init__()
        self.validation_data = validation_data

    def on_epoch_end(self, epoch, logs=None):
        # 获取验证数据
        val_predict = np.argmax(self.model.predict(self.validation_data[0]), axis=1)
        val_targ = np.argmax(self.validation_data[1], axis=1)

        # 计算准确率
        accuracy = accuracy_score(val_targ, val_predict)

        # 计算召回率
        # 计算召回率
        recall = recall_score(val_targ, val_predict)

        # 计算混淆矩阵
        conf_matrix = confusion_matrix(val_targ, val_predict)
        tn, fp, fn, tp = conf_matrix.ravel()

        # 计算假阳率
        fpr = fp / (fp + tn)

        print(f' - val_accuracy: {accuracy:.4f} - val_recall: {recall:.4f} - val_fpr: {fpr:.4f}')
