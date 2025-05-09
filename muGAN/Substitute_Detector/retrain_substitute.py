"""
    使用生成的对抗样本重训练检测器
"""
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.models import load_model, Sequential
from tensorflow.python.keras.optimizer_v2.adam import Adam

from Substitute_Detector import set_path
# from Substitute_Detector.Metrics import Metrics

# 加载已有的检测器
print("Loading Model substitute.h5")
model = load_model(set_path.model_h5_path)


# 逐块读取并处理数据
def process_chunk(chunk):
    X = chunk.drop(columns=['label']).values
    y = chunk['label'].values
    y_categorical = to_categorical(y)
    return X, y, y_categorical


def load_and_process_data_in_chunks(file_path, chunksize=10000):
    reader = pd.read_csv(file_path, chunksize=chunksize)
    X_list, y_list, y_categorical_list = [], [], []
    for chunk in reader:
        X, y, y_categorical = process_chunk(chunk)
        X_list.append(X)
        y_list.append(y)
        y_categorical_list.append(y_categorical)
    return np.concatenate(X_list), np.concatenate(y_list), np.concatenate(y_categorical_list)


# 分块加载和处理数据
# X_train, y_train, y_train_categorical = load_and_process_data_in_chunks(set_path.adv_train_features_csv_path)
# X_test, y_test, y_test_categorical = load_and_process_data_in_chunks(set_path.adv_test_features_csv_path)


def load_data_in_chunks(file_path, chunksize=10000):
    """ 分块加载数据 """
    reader = pd.read_csv(file_path, chunksize=chunksize)
    data_list = []
    for chunk in reader:
        data_list.append(chunk)
    return pd.concat(data_list, ignore_index=True)


# 加载预处理后的训练和测试数据
# train_df = load_data_in_chunks(set_path.adv_train_features_csv_path)
# test_df = load_data_in_chunks(set_path.adv_test_features_csv_path)
# train_df = pd.read_csv(set_path.adv_train_features_csv_path)
# test_df = pd.read_csv(set_path.adv_test_features_csv_path)

# 加载预处理后的训练和测试数据
train_df = pd.read_feather(set_path.adv_train_features_feather_path)
test_df = pd.read_feather(set_path.adv_test_features_feather_path)

# 分离特征和标签
X_train = train_df.drop(columns=['label']).values
y_train = train_df['label'].values
X_test = test_df.drop(columns=['label']).values
y_test = test_df['label'].values

# 打印数据形状以进行调试
print(f'X_train shape: {X_train.shape}')
print(f'y_train shape: {y_train.shape}')
print(f'X_test shape: {X_test.shape}')
print(f'y_test shape: {y_test.shape}')

# 将标签转换为类别标签
y_train_categorical = to_categorical(y_train)
y_test_categorical = to_categorical(y_test)

# 打印独热编码后标签的形状以进行调试
print(f'y_train_categorical shape: {y_train_categorical.shape}')
print(f'y_test_categorical shape: {y_test_categorical.shape}')

# 如果现有模型输入层形状不匹配，可以构建一个新的模型
# 这里假设一个简单的模型，输入层形状与PCA降维后的特征数量匹配
input_shape = X_train.shape[1]
new_model = Sequential([
    Dense(256, activation='relu', input_shape=(input_shape,)),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dense(2, activation='softmax')
])

optimizer = Adam(learning_rate=0.001)
new_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# 使用早停法防止过拟合
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# 重新训练模型
new_model.fit(X_train, y_train_categorical, epochs=260, batch_size=32, validation_data=(X_test, y_test_categorical), callbacks=[early_stopping])

# 定义验证数据
# validation_data = (X_test, y_test_categorical)
# 重新训练模型，添加自定义回调
# model.fit(X_train, y_train_categorical, epochs=50, batch_size=32, validation_data=validation_data, callbacks=[Metrics(validation_data)])

# 评估模型
loss, accuracy = new_model.evaluate(X_test, y_test_categorical)
print(f'Test Accuracy: {accuracy:.2f}')

# 进行预测
y_predict_proba = new_model.predict(X_test)
y_predict = np.argmax(y_predict_proba, axis=1)

# 计算准确率
accuracy = accuracy_score(y_test, y_predict)

# 计算召回率
recall = recall_score(y_test, y_predict)

# 计算混淆矩阵
conf_matrix = confusion_matrix(y_test, y_predict)
tn, fp, fn, tp = conf_matrix.ravel()

# 计算假阳率
fpr = fp / (fp + tn)

print(f"Accuracy: {accuracy:.2f}")
print(f"Recall: {recall:.2f}")
print(f"False Positive Rate: {fpr:.2f}")

# 保存重新训练的模型
new_model.save(set_path.retrain_model_h5_path)
print("Model saved as 'retrain_substitute.h5'.")
