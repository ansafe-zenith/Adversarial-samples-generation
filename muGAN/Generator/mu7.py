"""
    Mu7-Reorder Code
    实现 Android 应用的代码重排序，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 遍历 smali 文件
        3. 随机选择一个 Smali 文件
        4. 选择并重新排序其中的一部分代码
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机修改一个 Smali 文件中的两个方法
"""
import os
import random

from Generator import set_path, mu1


def collect_smali_files(smali_folder):
    """ 收集所有 Smali 文件的路径 """
    smali_files = []
    for root, dirs, files in os.walk(smali_folder):
        for file in files:
            if file.endswith('.smali'):
                smali_files.append(os.path.join(root, file))
    return smali_files


def reorder_smali(smali_files):
    """ 随机选择并重排序 Smali 文件中的方法 """
    if not smali_files:
        return

    # 尝试找到一个包含至少两个方法的 Smali 文件
    while smali_files:
        # 随机选择一个 Smali 文件
        selected_smali = random.choice(smali_files)
        smali_files.remove(selected_smali)
        print("selected_res: " + selected_smali)

        with open(selected_smali, 'r') as file:
            lines = file.readlines()

        method_start_indices = [i for i, line in enumerate(lines) if line.startswith('.method')]
        method_end_indices = [i for i, line in enumerate(lines) if line.startswith('.end method')]

        if len(method_start_indices) > 1:
            # 随机选择两个方法交换
            m1, m2 = random.sample(list(zip(method_start_indices, method_end_indices)), 2)
            method1_lines = lines[m1[0]:m1[1]+1]
            method2_lines = lines[m2[0]:m2[1]+1]
            print("method1_lines: " + method1_lines.__str__())
            print("method2_lines: " + method2_lines.__str__())

            # 删除原有方法位置的内容
            del lines[m1[0]:m1[1]+1]
            # 修改第二个方法的位置
            m2_adj_start = m2[0] - len(method1_lines)
            m2_adj_end = m2_adj_start + (m2[1] - m2[0])
            del lines[m2_adj_start:m2_adj_end+1]

            # 计算新的插入点
            if m1[0] < m2[0]:
                new_m2_start = m1[0]
                new_m1_start = m2_adj_start
            else:
                new_m1_start = m2_adj_start
                new_m2_start = m1[0]

            # 插入新位置
            lines[new_m1_start:new_m1_start] = method2_lines
            lines[new_m2_start:new_m2_start] = method1_lines

            # 写回修改后的 Smali 文件
            with open(selected_smali, 'w') as file:
                file.writelines(lines)

            print(f"Reordered code in {selected_smali}")
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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reorder.apk'

    # 收集所有类的标识符
    print("Collecting smali files...")
    smali_files = collect_smali_files(os.path.join(output_folder, 'smali'))

    # 代码重排序
    print("Reordering a random smali file...")
    reorder_smali(smali_files)

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
