"""
    预处理重训练需要的数据，并保存预处理后的训练和测试数据
"""
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

from Substitute_Detector import set_path

# 加载原始训练数据
df = pd.read_csv(set_path.features_csv_path)

# 加载对抗样本特征
adv_df = pd.read_csv(set_path.adv_features_csv_path)

# 合并对抗样本和原始数据
df = pd.concat([df, adv_df], ignore_index=True)

# 分离特征和标签
X = df.drop(columns=['apk_path', 'label'])
y = df['label']

# 确保所有特征列的值都是字符串，并处理NaN值
X['permissions'] = X['permissions'].fillna('').astype(str)
X['api_calls'] = X['api_calls'].fillna('').astype(str)
X['intent_filters'] = X['intent_filters'].fillna('').astype(str)

# 将多标签特征转换为独热编码
mlb = MultiLabelBinarizer()
X_permissions = mlb.fit_transform(X['permissions'].str.split())
X_api_calls = mlb.fit_transform(X['api_calls'].str.split())
X_intent_filters = mlb.fit_transform(X['intent_filters'].str.split())

# 合并所有特征
X_combined = np.hstack((X_permissions, X_api_calls, X_intent_filters))

# 标准化特征数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# 使用方差阈值选择特征，去除低方差特征
selector = VarianceThreshold(threshold=0.01)  # 设置阈值，去除低方差特征
X_selected = selector.fit_transform(X_scaled)

# 使用PCA降维，将特征数量减少到模型期望的大小
pca = PCA(n_components=648)  # 模型期望的特征数量为412150
X_reduced = pca.fit_transform(X_selected)

# 将标签转换为二进制形式
y_binary = (y == 'malware').astype(int)
# 确保没有异常值
print(f"Unique values in y_binary: {np.unique(y_binary)}")

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_reduced, y_binary, test_size=0.2, random_state=42)

# 保存预处理后的数据
# train_df = pd.DataFrame(X_train)
# train_df['label'] = y_train
# test_df = pd.DataFrame(X_test)
# test_df['label'] = y_test
# train_df.to_csv(set_path.adv_train_features_csv_path, index=False)
# test_df.to_csv(set_path.adv_test_features_csv_path, index=False)

# 检查和清理标签数据，确保其只包含有效值
valid_labels = [0, 1]
y_train = np.where(np.isin(y_train, valid_labels), y_train, 0)
y_test = np.where(np.isin(y_test, valid_labels), y_test, 0)
print(f"Unique values in cleaned y_train: {np.unique(y_train)}")
print(f"Unique values in cleaned y_test: {np.unique(y_test)}")

# 将数据转换为 DataFrame，并确保列名是字符串
train_df = pd.DataFrame(X_train, columns=[str(i) for i in range(X_train.shape[1])])
train_df['label'] = y_train
test_df = pd.DataFrame(X_test, columns=[str(i) for i in range(X_test.shape[1])])
test_df['label'] = y_test

# 使用 feather 格式存储数据
train_df.reset_index(drop=True).to_feather(set_path.adv_train_features_feather_path)
test_df.reset_index(drop=True).to_feather(set_path.adv_test_features_feather_path)

# train_df.to_feather(set_path.adv_train_features_feather_path)
# test_df.to_feather(set_path.adv_test_features_feather_path)

# 将标签转换为类别标签
y_train_categorical = to_categorical(y_train)
y_test_categorical = to_categorical(y_test)
print(f"Shape of y_train_categorical: {y_train_categorical.shape}")
print(f"Shape of y_test_categorical: {y_test_categorical.shape}")
