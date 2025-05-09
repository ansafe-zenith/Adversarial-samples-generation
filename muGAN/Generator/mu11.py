"""
    Mu11-Replace Similar API
    实现 Android 应用的替换相似 API，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 在 Smali 文件中寻找特定的 API 调用
        3. 随机选择一个并替换为相似功能的 API
        4. 重新打包 APK --- Apktool
        5. 对 APK 文件进行签名 --- apksigner
    可以替换的 API 有：
        1. 日志记录 --- 调试信息 Log.d()
            可替换为：错误信息 Log.e()、警告信息 Log.w()、信息 Log.i() 或 详细信息 Log.v()
        2. 数据存储 --- 轻量级的数据存储 SharedPreferences
            可替换为：Room 或 SQLite 数据库进行更复杂的数据存储
        3. 网络请求 --- HttpURLConnection
            可替换为：OkHttp 或 Retrofit 库
        4. 图片处理 --- BitmapFactory 和 Bitmap
            可替换为：Picasso 或 Glide 图像加载库
        5. UI更新 --- 直接在非 UI 线程使用 runOnUiThread() 或 Handler 更新 UI
            可替换为：使用 LiveData 和 ViewModel 配合实现响应式 UI 更新
        6. 异步处理 --- AsyncTask
            可替换为：使用 RxJava、Kotlin Coroutines 或 LiveData 配合 ViewModel 进行异步操作和数据处理
        7. 服务绑定 --- 直接使用 ServiceConnection 和 bindService()
            可替换为：使用 JobIntentService 或 WorkManager 进行后台任务的处理
"""
import os

from Generator import set_path, mu1


def replace_similar_api(smali_path):
    """ 用相似的 API 替换 Smali 文件中的 API 调用 """
    modified = False
    for root, dirs, files in os.walk(smali_path):
        for file in files:
            if file.endswith('.smali'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'Landroid/util/Log;->d(' in line:
                        lines[i] = line.replace('Landroid/util/Log;->d(', 'Landroid/util/Log;->e(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                    if 'Landroid/util/Log;->e(' in line:
                        lines[i] = line.replace('Landroid/util/Log;->e(', 'Landroid/util/Log;->w(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                    if 'Landroid/util/Log;->w(' in line:
                        lines[i] = line.replace('Landroid/util/Log;->w(', 'Landroid/util/Log;->i(')
                        modified = True
                        print(f"Replaced similar API from {line} to {lines[i]}")
                        break
                    if 'Landroid/util/Log;->i(' in line:
                        lines[i] = line.replace('Landroid/util/Log;->i(', 'Landroid/util/Log;->v(')
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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reSimilarAPI.apk'

    # 替换相似的 API
    print("Replacing a similar API...")
    replace_similar_api(os.path.join(output_folder, 'smali'))

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
