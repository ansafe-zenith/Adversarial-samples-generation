"""
    训练一个拟合 VirusTotal 检测能力的 Android 恶意软件检测器：
        1. 数据收集 --- 恶意样本 (Drebin 数据集) + 良性样本 (Google Play 收集的 benign)
        2. 数据预处理
            静态分析 --- 提取 APK 文件的静态特征 (permissions、API calls、Intent-filters)
            特征提取 --- 将提取的特征转换为适合机器学习模型的格式 (二元向量)
        3. 特征选择 --- 选择最具代表性的特征，减少维度 (主成分分析 PCA、递归特征消除 RFE)
        4. 模型训练
            选择模型 --- 以神经网络 NN 作为机器学习模型
            模型训练 --- 使用良性 + 恶意样本训练模型，确保训练数据集的平衡
            超参数调优 --- 使用交叉验证和网络搜索等技术优化模型的超参数
        5. 模型评估
            性能评估 --- 使用测试集评估模型性能，主要指标包括准确率、精确率、召回率、F1-score、ROC 曲线和 AUC 值等
            定期更新 --- 定期收集新的恶意软件样本，更新模型
"""
import pandas as pd
from keras.utils import to_categorical
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.models import Sequential

from Substitute_Detector import set_path
"""
    神经网路模型训练和评估 --- 使用优化后的特征进行训练：
        1. 加载处理后的特征和标签
        2. 将标签转换为类别标签
        3. 使用 Keras 构建神经网络模型，包括输入层、隐藏层和输出层
        4. 编译模型，使用 Adam 优化器和交叉熵损失函数
        5. 训练模型，并使用测试数据评估模型的准确性
"""

# 加载处理后的特征和标签
train_df = pd.read_csv(set_path.train_features_reduced_csv_path)
test_df = pd.read_csv(set_path.test_features_reduced_csv_path)

# 分离特征和标签
X_train_reduced = train_df.drop(columns=['label']).values
y_train = train_df['label'].values
X_test_reduced = test_df.drop(columns=['label']).values
y_test = test_df['label'].values

# 将标签转换为类别标签
y_train_categorical = to_categorical(y_train)
y_test_categorical = to_categorical(y_test)

# 构建神经网络模型
model = Sequential([
    Dense(256, input_dim=X_train_reduced.shape[1], activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(2, activation='softmax')  # 二分类问题的输出层
])

# 编译模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 训练模型
model.fit(X_train_reduced, y_train_categorical, epochs=50, batch_size=32,
          validation_data=(X_test_reduced, y_test_categorical))

# 评估模型
loss, accuracy = model.evaluate(X_test_reduced, y_test_categorical)
print(f'Test Accuracy: {accuracy:.2f}')
