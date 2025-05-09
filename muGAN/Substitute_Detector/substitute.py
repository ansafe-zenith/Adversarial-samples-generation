"""
    神经网络模型训练和评估 --- 直接使用提取的特征进行训练：
        1. 加载处理后的特征和标签
        2. 将标签转换为类别标签
        3. 使用 Keras 构建神经网络模型，包括输入层、隐藏层和输出层
        4. 编译模型，使用 Adam 优化器和交叉熵损失函数
        5. 训练模型，并使用测试数据评估模型的准确性
"""
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.models import Sequential

from Substitute_Detector import set_path
from Substitute_Detector.Metrics import Metrics

# from Substitute_Detector.Metrics import Metrics

# 加载处理后的特征和标签
print("Loading train datasets")
train_df = pd.read_csv(set_path.train_features_csv_path)
print("Loading test datasets")
test_df = pd.read_csv(set_path.test_features_csv_path)

# 分离特征和标签
X_train = train_df.drop(columns=['label']).values
y_train = train_df['label'].values
X_test = test_df.drop(columns=['label']).values
y_test = test_df['label'].values

# 将标签转换为类别标签
y_train_categorical = to_categorical(y_train)
y_test_categorical = to_categorical(y_test)

# 构建神经网络模型
model = Sequential([
    Dense(256, input_dim=X_train.shape[1], activation='relu'),  # 输入层和第一层隐藏层
    Dropout(0.5),
    Dense(128, activation='relu'),  # 第二层隐藏层
    Dropout(0.5),
    Dense(2, activation='softmax')  # 二分类问题的输出层
])

# 编译模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # 训练模型
# model.fit(X_train, y_train_categorical, epochs=50, batch_size=32, validation_data=(X_test, y_test_categorical))

# # 定义验证数据
validation_data = (X_test, y_test_categorical)
#
# # 训练模型，添加自定义回调
model.fit(X_train, y_train_categorical, epochs=50, batch_size=32, validation_data=validation_data, callbacks=[Metrics(validation_data)])

# 评估模型
loss, accu = model.evaluate(X_test, y_test_categorical)
print(f'Test Accuracy: {accu:.2f}')

# 进行预测
y_predict_proba = model.predict(X_test)
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

# 保存模型
model.save(set_path.model_h5_path)
print("Model saved as 'trained_model.h5'.")
