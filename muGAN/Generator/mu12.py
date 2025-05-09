"""
    Mu12-Replace Lower-Version API
    实现 Android 应用的替换低版本的 API，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 确定要替换的 API 和其在不同 Android 版本中的变体
        3. 替换相应 Smali 文件中的 API 调用为其指定的低版本
        4. 重新打包 APK --- Apktool
        5. 对 APK 文件进行签名 --- apksigner
    可以替换的 API 有：
        1. 访问资源文件 --- Context.getDrawable(int) (API 21+)
            可以替换为 ContextCompat.getDrawable(Context, int) (兼容所有 API)
        2. 权限检查 --- Context.checkSelfPermission(String) (API 23+)
            可以替换为 ContextCompat.checkSelfPermission(Context, String)
        3. 创建通知 --- Notification.Builder(Context) (API 26+) 中使用的 NotificationChannel
            可以替换为 NotificationCompat.Builder(Context)
        4. 动画和过渡 --- ViewPropertyAnimator 库的动画方法
            可以替换为低版本的 NineOldAndroids 库或手动管理动画的开始和约束
        5. 处理位图 --- BitmapFactory.Options.inBitmap (API 11+)
            可以在较低版本中复用已存在的 Bitmap 对象进行模拟
        6. 位置服务 --- FusedLocationProviderClient (较新的 Google Play 服务) 的定位功能
            可以替换为使用 LocationManager 获取位置
        7. 文件和数据存储 --- Context.getNoBackupFilesDir() (API 21+)
            可以替换为直接使用 /data/data/<package_name>/files/ 目录进行数据存储
        8. 网络请求和连接 --- ConnectivityManager.NetworkCallback (API 21+)
            可以替换为使用广播接收器 BroadcastReceiver 监听网络变化
        9. 色彩工具 --- Color 类中的一些新方法如 Color.parse()
            可以替换为手动解析字符串
"""
import os

from Generator import set_path, mu1


def replace_lower_version_api(smali_path):
    """ 用低版本的 API 替换 Smali 文件中的 API 调用 """
    modified = False
    for root, dirs, files in os.walk(smali_path):
        for file in files:
            if file.endswith('.smali'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'Landroid/content/Context;->getDrawable(' in line:
                        lines[i] = line.replace('Landroid/content/Context;->getDrawable(',
                                                'Landroidx/core/content/res/ResourcesCompat;->getDrawable(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                    if 'Landroid/content/Context;->checkSelfPermission(' in line:
                        lines[i] = line.replace('Landroid/content/Context;->checkSelfPermission(',
                                                'Landroidx/core/content/res/ContextCompat;->checkSelfPermission(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                    if 'Landroid/app/Notification;->Builder(' in line:
                        lines[i] = line.replace('Landroid/app/Notification;->Builder(',
                                                'Landroidx/core/app/NotificationCompat;->Builder(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                if modified:
                    with open(filepath, 'w') as f:
                        f.writelines(lines)
                    return


def perturb(apk_name):
    # 配置路径
    apktool_path = set_path.apktool_path
    zipalign_path = set_path.zipalign_path
    apksigner_path = set_path.apksigner_path
    keystore = set_path.keystore
    keystore_password = set_path.keystore_password
    key_alias = set_path.key_alias

    # APK 路径
    output_folder = set_path.output_folder
    repacked_apk = set_path.repacked_apk
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reLowerAPI.apk'

    # 替换低版本的 API
    print("Replacing a lower version API...")
    replace_lower_version_api(os.path.join(output_folder, 'smali'))

    # 重打包 APK
    mu1.pack_apk(apktool_path, output_folder, repacked_apk)

    # 签名 APK
    mu1.sign_apk(zipalign_path, apksigner_path, keystore, keystore_password, key_alias, repacked_apk, final_signed_apk)

    # 删除中间文件和目录
    if os.path.exists(repacked_apk):
        os.remove(repacked_apk)
    idsig_file = final_signed_apk + '.idsig'
    if os.path.exists(idsig_file):
        os.remove(idsig_file)

    return final_signed_apk


def main():
    apk_name = '06fd5e281179fdfad8c84a4a12977a6942b989923826f91b0bb2fc0d4c9e9641.apk'
    final_apk = perturb(apk_name)
    print("final_apk: " + final_apk)


if __name__ == '__main__':
    main()
