import os.path

# 训练检测器的 APK 文件目录
apk_path = 'D://FeatureExtraction//dataset'
benign_apk_path = os.path.join(apk_path, 'benign')
malicious_apk_path = os.path.join(apk_path, 'malicious')

# 训练检测器的工作目录
work_path = 'D://GA-GAN//Substitute_Detector//train_substitute'
errors_log_path = os.path.join(work_path, 'apk_processing_errors.log')
features_csv_path = os.path.join(work_path, 'apk_features_with_labels.csv')

train_features_csv_path = os.path.join(work_path, 'train_features.csv')
test_features_csv_path = os.path.join(work_path, 'test_features.csv')

train_features_reduced_csv_path = os.path.join(work_path, 'train_features_reduced.csv')
test_features_reduced_csv_path = os.path.join(work_path, 'test_features_reduced.csv')

# 重训练检测器的 APK 文件目录
apk_path = 'D://GA-GAN//Reference_Detectors//dataset'
adv_benign_apk_path = os.path.join(apk_path, 'benign')
adv_malicious_apk_path = os.path.join(apk_path, 'malicious')

# 重训练检测器的工作目录
retrain_path = 'D://GA-GAN//Substitute_Detector//adv_substitute'
adv_errors_log_path = os.path.join(retrain_path, 'adv_processing_errors.log')
adv_features_csv_path = os.path.join(retrain_path, 'adv_features_with_labels.csv')

adv_train_features_csv_path = os.path.join(retrain_path, 'adv_train_features.csv')
adv_test_features_csv_path = os.path.join(retrain_path, 'adv_test_features.csv')

adv_train_features_reduced_csv_path = os.path.join(retrain_path, 'adv_train_features_reduced.csv')
adv_test_features_reduced_csv_path = os.path.join(retrain_path, 'adv_test_features_reduced.csv')

adv_train_features_feather_path = os.path.join(retrain_path, 'train_data.feather')
adv_test_features_feather_path = os.path.join(retrain_path, 'test_data.feather')

# 模型目录
model_h5_path = os.path.join(work_path, 'substitute.h5')    # SD
retrain_model_h5_path = os.path.join(retrain_path, 'retrain_substitute.h5')    # D
