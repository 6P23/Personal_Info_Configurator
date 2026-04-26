# Personal Info Configurator

### 📝 Description
This is a batch update tool specifically designed for **EuroScope** `.prf` configuration files. It enables Air Traffic Controllers (ATCs) to quickly and securely synchronize personal information (Name, CID, Password, etc.) across multiple sector profiles, eliminating the tedious process of manually entering account credentials every time you go online.

### ✨ Key Features
- **Batch Synchronization**: One-click recursive scanning of all `.prf` files within the selected directory and its subdirectories.
- **Smart Deduplication**: Utilizes a "Clean First, Append Later" logic to ensure no duplicate configuration entries are created within the files.
- **Full Compatibility**: Adheres to EuroScope standards by enforcing `GBK` encoding for all read/write operations, preventing text corruption or "mojibake."

### 🚀 Quick Start
1. **System Requirements**: Windows 10/11, Python 3.9 or higher.
2. **Install Dependencies**:
   ```bash
   pip install PySide6 Pillow
   ```
3. **Run Application**:
   ```bash
   python Personal_Info_Configurator.py
   ```

### 🛠 Built With
- **Python 3.9+** - Core programming language.
- **PySide6** - GUI framework (Qt for Python) for a modern interface.
- **Pillow** - Image processing for icon conversion and bundling.
- **PyInstaller** - Tool for creating the standalone Windows executable.

### ⚠️ Notes
- **Backup Recommendation**: It is highly recommended to back up your sector data before performing large-scale batch modifications.

### 🤝 Contributing
Since this is my first project on GitHub, suggestions and improvements are more than welcome! If you'd like to contribute:
1. **Fork** the repository.
2. Create a new **Branch** for your feature or bug fix.
3. Submit a **Pull Request**, and I’ll review it as soon as possible.
4. You can also open an **Issue** to report bugs or suggest new features.

### ⚖️ License & Copyright
Copyright (c) 2026 **InkWh1te**

This project is licensed under the **MIT License**.
You are free to use, copy, modify, and distribute this software provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.

---

# 个人信息配置器

### 📝 项目简介
这是一款专为 **EuroScope** 模拟飞行管制软件设计的 `.prf` 配置文件批量更新工具。它可以帮助管制员快速、安全地同步多个扇区文件中的个人信息（姓名、CID、密码等），彻底告别每次上线输入账户密码的繁琐过程。

### ✨ 核心功能
- **批量同步**：一键递归扫描选定目录及其子目录下所有的 `.prf` 文件。
- **智能去重**：采用“先清理、后追加”的逻辑，确保配置文件内不会产生重复的条目。
- **完美兼容**：针对 EuroScope 规范，强制使用 `GBK` 编码进行读写，防止字符乱码。

### 🚀 快速开始
1. **环境要求**：Windows 10/11，Python 3.9 及以上版本。
2. **安装依赖**：
   ```bash
   pip install PySide6 Pillow
   ```
3. **运行程序**：
   ```bash
   python Personal_Info_Configurator.py
   ```

### 🛠 技术栈
- **Python 3.9+** - 核心编程语言。
- **PySide6** - 用于构建现代化界面的 GUI 框架。
- **Pillow** - 图像处理库，支持图标转换。
- **PyInstaller** - 用于生成 Windows 独立可执行程序 (.exe)。

### ⚠️ 注意事项
- **备份建议**：在进行大规模批量修改前，强烈建议先对扇区数据进行备份。

### 🤝 参与贡献
这是我的第一个 GitHub 项目，非常欢迎大家提出改进建议！如果你想参与贡献：
1. **Fork** 本仓库到你的账号下。
2. 为你的新功能或 Bug 修复创建一个新的 **Branch (分支)**。
3. 提交 **Pull Request (拉取请求)**，我会尽快查看。
4. 你也可以通过提交 **Issue** 来报告程序漏洞或反馈新功能建议。

### ⚖️ 版权与许可证
版权所有 (c) 2026 **InkWh1te**

本项目采用 **MIT 许可证** 开源。你可以自由地使用、复制、修改和分发本软件，但必须在副本中保留上述版权声明。本软件按“原样”提供，作者不承担任何由此产生的责任。
