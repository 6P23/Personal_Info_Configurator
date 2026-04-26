import PyInstaller.__main__
import os

# ==================== 自动化配置中心 ====================
# 1. 排除列表：运行打包时，脚本会忽略这些文件
EXCLUDE_FILES = ["EXE.py", "build.py", "setup.py", "build_master.py"]

# 2. 默认输出名称：如果不填，将自动使用主脚本的名字
APP_DISPLAY_NAME = ""

# 3. 版本号
VERSION = "1.0.0"

# 4. 模式配置
ONE_FILE = True  # True: 单个EXE | False: 文件夹
GUI_MODE = True  # True: 隐藏黑窗口 | False: 显示黑窗口


# ========================================================

def find_main_script():
    """自动寻找当前目录下最像主程序的 .py 文件"""
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    targets = [f for f in py_files if f not in EXCLUDE_FILES]

    if not targets:
        return None

    # 优先找名字里带 'main' 或 'GUI' 的
    for t in targets:
        if "main" in t.lower() or "gui" in t.lower():
            return t
    return targets[0]


def build():
    main_script = find_main_script()

    if not main_script:
        print("❌ 错误：未发现可打包的 Python 脚本！")
        return

    # 确定生成的最终文件名
    raw_name = os.path.splitext(main_script)[0]
    base_name = APP_DISPLAY_NAME if APP_DISPLAY_NAME else raw_name
    final_name = f"{base_name}_{VERSION}"

    # 组装基础参数
    params = [
        main_script,
        '--clean',
        f'--name={final_name}',
        '--onefile' if ONE_FILE else '--onedir',
    ]

    if GUI_MODE:
        params.append('--noconsole')

    # --- 自动搜索图标逻辑 ---
    icons = [f for f in os.listdir('.') if f.endswith('.ico')]
    if icons:
        params.append(f'--icon={icons[0]}')
        print(f"🎨 已检测并应用图标: {icons[0]}")
    else:
        # 如果没有图标，直接跳过，不添加 --icon 参数
        print("ℹ️ 未检测到 .ico 文件，将使用系统默认图标。")

    print(f"🚀 打包引擎启动...")
    print(f"🎯 识别到主程序: {main_script}")
    print(f"📦 产出文件名: {final_name}.exe")
    print("-" * 35)

    try:
        PyInstaller.__main__.run(params)
        print("-" * 35)
        print(f"✅ 任务成功完成！")
        print(f"📂 请查看 dist 文件夹下的 {final_name}.exe")
    except Exception as e:
        print(f"❌ 运行失败: {e}")


if __name__ == "__main__":
    build()