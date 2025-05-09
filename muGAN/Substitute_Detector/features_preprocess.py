"""
    数据加载和预处理：
        1. 加载提取的特征数据
        2. 进行必要的预处理
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

from Substitute_Detector import set_path

# 加载 CSV 文件
df = pd.read_csv(set_path.features_csv_path)

# 分离特征和标签
X = df.drop(columns=['apk_path', 'label'])
y = df['label']

# 确保所有特征列的值都是字符串，并处理 NaN 值
X['permissions'] = X['permissions'].fillna('').astype(str)
X['api_calls'] = X['api_calls'].fillna('').astype(str)
X['intent_filters'] = X['intent_filters'].fillna('').astype(str)

# 将多标签特征转换为独热编码
mlb = MultiLabelBinarizer()
X_permissions = mlb.fit_transform(X['permissions'].str.split())
X_api_calls = mlb.fit_transform(X['api_calls'].str.split())
X_intent_filters = mlb.fit_transform(X['intent_filters'].str.split())

# 合并所有特征
X_combined = pd.concat([pd.DataFrame(X_permissions), pd.DataFrame(X_api_calls), pd.DataFrame(X_intent_filters)], axis=1)

# 标准化特征数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# 将标签转换为二进制形式
y_binary = (y == 'malware').astype(int)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_binary, test_size=0.2, random_state=42)

# 保存处理后的特征和标签
train_df = pd.DataFrame(X_train)
train_df['label'] = y_train.values
test_df = pd.DataFrame(X_test)
test_df['label'] = y_test.values

train_df.to_csv(set_path.train_features_csv_path, index=False)
test_df.to_csv(set_path.test_features_csv_path, index=False)

print("Data preparation complete. Processed data saved in 'train_features.csv' and 'test_features.csv'.")
