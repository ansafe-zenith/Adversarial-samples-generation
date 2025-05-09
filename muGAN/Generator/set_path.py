"""
    设置执行命令所需的环境和 APK 路径
"""

# 环境路径
apktool_path = 'D://apktool//apktool.jar'
zipalign_path = 'D://Android//SDK//build-tools//33.0.0//zipalign.exe'
apksigner_path = 'D://Android//SDK//build-tools//33.0.0//apksigner.bat'
keystore = 'D://apktool//key_apk.keystore'
keystore_password = '123456'
key_alias = 'key_apk'

# APK 路径
apk_file = 'D://GA-GAN//Drebin'
# apk_file = 'D://GA-GAN//Generator//Datasets'
output_folder = 'unpack'
repacked_apk = 'repack.apk'
# print(f"Trying to open APK file at {original_apk}")

# 数据集路径
dataset_folder = 'D://GA-GAN//Generator//Datasets'

# 存储路径
samples_file = 'D://GA-GAN//Generator//Samples'

# Normal 级别的权限
normal_permissions = [
        "android.permission.ACCESS_LOCATION_EXTRA_COMMANDS",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.ACCESS_NOTIFICATION_POLICY",
        "android.permission.ACCESS_WIFI_STATE",
        "android.permission.BLUETOOTH",
        "android.permission.BLUETOOTH_ADMIN",
        "android.permission.BROADCAST_STICKY",
        "android.permission.CHANGE_NETWORK_STATE",
        "android.permission.CHANGE_WIFI_MULTICAST_STATE",
        "android.permission.CHANGE_WIFI_STATE",
        "android.permission.DISABLE_KEYGUARD",
        "android.permission.EXPAND_STATUS_BAR",
        "android.permission.GET_PACKAGE_SIZE",
        "android.permission.INTERNET",
        "android.permission.KILL_BACKGROUND_PROCESSES",
        "android.permission.MODIFY_AUDIO_SETTINGS",
        "android.permission.NFC",
        "android.permission.READ_SYNC_SETTINGS",
        "android.permission.READ_SYNC_STATS",
        "android.permission.RECEIVE_BOOT_COMPLETED",
        "android.permission.REORDER_TASKS",
        "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
        "android.permission.SET_ALARM",
        "android.permission.SET_TIME_ZONE",
        "android.permission.SET_WALLPAPER",
        "android.permission.SET_WALLPAPER_HINTS",
        "android.permission.TRANSMIT_IR",
        "android.permission.USE_FINGERPRINT",
        "android.permission.VIBRATE",
        "android.permission.WAKE_LOCK",
        "android.permission.WRITE_SYNC_SETTINGS"
    ]
