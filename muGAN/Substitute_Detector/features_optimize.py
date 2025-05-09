"""
    结合使用特征选择方法和降维技术来优化特征集：
        基于随机森林的特征重要性
            工作原理：
                1. 用有抽样放回的方法 (bootstrap) 从样本集中选取n个样本作为一个训练集。
                2. 用抽样得到的样本集生成一棵决策树，在生成的每一个结点：
                    随机不重复地选择d个特征；
                    利用这d个特征分别对样本集进行划分，找到最佳的划分特征（可用基尼系数、增益率或者信息增益判别）。
                3. 重复以上两个步骤共 k 次，k 即为随机森林中决策树的个数。
        主成分分析 PCA
            基本思想：是用较少的变量来代替原来较多的变量，并反映原来多个变量的大部分信息。
            应用场景：是一种数据降维方法，在数据分析、机器学习等方面具有广泛应用。
"""
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

from Substitute_Detector import set_path

# 加载 CSV 数据并预处理
# 加载 CSV 文件
df = pd.read_csv(set_path.features_csv_path)

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
X_combined = pd.concat([pd.DataFrame(X_permissions), pd.DataFrame(X_api_calls), pd.DataFrame(X_intent_filters)], axis=1)

# 标准化特征数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# 将标签转换为二进制形式
y_binary = (y == 'malware').astype(int)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_binary, test_size=0.2, random_state=42)


# 特征选择和降维
# 特征选择：基于随机森林的特征重要性
selector = RandomForestClassifier(n_estimators=100, random_state=42)
selector.fit(X_train, y_train)

# 获取特征重要性
importance = selector.feature_importances_

# 选择重要性最高的 50 个特征
indices = importance.argsort()[-50:]

# 选择这些特征
X_train_selected = X_train[:, indices]
X_test_selected = X_test[:, indices]

# 特征降维：主成分分析 (PCA)
pca = PCA(n_components=10)  # 选择合适的主成分数量
X_train_reduced = pca.fit_transform(X_train_selected)
X_test_reduced = pca.transform(X_test_selected)

# 保存处理后的特征和标签
train_df = pd.DataFrame(X_train_reduced)
train_df['label'] = y_train.values
test_df = pd.DataFrame(X_test_reduced)
test_df['label'] = y_test.values

train_df.to_csv(set_path.train_features_reduced_csv_path, index=False)
test_df.to_csv(set_path.test_features_reduced_csv_path, index=False)

print("Feature selection and dimensionality reduction complete. "
      "Processed data saved in 'train_features_reduced.csv' and 'test_features_reduced.csv'.")

"""
    结合使用特征选择方法和降维技术来优化特征集：
        数据集的特征数量过多或者选择特征的方法计算复杂度过高导致程序无法停止运行
        递归特征消除 RFE
            基本思想：在不断迭代中递归地删除特征，直到达到预设的特征数量为止。
            应用场景：是一种特征选择方法，可用于回归和分类问题。
            工作原理：
                1. 使用所有特征训练一个模型，并计算每个特征的权重或系数；
                2. 排序这些特征的权重或系数，并删除权重或系数最小的特征；
                3. 重复以上两个步骤，直至特征数量达到预设的值。
            实现方法：
                from sklearn.feature_selection import RFE
                    通过递归地移除特征并重新训练模型来评估每个特征的重要性。
                    在每次迭代中，它都会移除最不重要的特征，并重新训练模型。
                    这个过程会一直持续到达到指定的特征数量或没有更多的特征可以移除为止。
                from sklearn.feature_selection import RFECV
                    使用交叉验证来评估特征的重要性。
                    在每次迭代中，它都会使用交叉验证来评估模型的性能，并选择最佳的特征数量。
                    这个过程会一直持续到找到最佳的特征数量为止。
            不使用的原因：数据集的特征数量过多或者选择特征的方法计算复杂度过高导致程序无法停止运行
"""
# 初步特征选择：使用方差阈值筛选
# selector_variance = VarianceThreshold(threshold=(.8 * (1 - .8)))
# X_train_var = selector_variance.fit_transform(X_train)
# X_test_var = selector_variance.transform(X_test)
# 特征选择：递归特征消除 (RFE)
# estimator = LogisticRegression(max_iter=1000, random_state=42)
# selector = RFE(estimator, n_features_to_select=50, step=1)
# selector = selector.fit(X_train_var, y_train)
# 变换训练集和测试集
# X_train_selected = selector.transform(X_train)
# X_test_selected = selector.transform(X_test)
