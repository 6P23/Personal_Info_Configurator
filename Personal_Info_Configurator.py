import os
import sys
import glob
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QWidget, QPushButton,
                               QLineEdit, QLabel, QMainWindow, QHBoxLayout,
                               QTextEdit, QFileDialog, QMessageBox, QGridLayout,
                               QFrame, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette

# 定义版本号
VERSION = "v1.1.0"  # 升级了小版本号


class PRFConfiguratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # 预定义实例属性
        self.dir_input = QLineEdit()
        self.inputs = {}
        self.tovatsim_checkbox = QCheckBox("自动连接至 VATSIM (connect to VATSIM)")
        self.execute_btn = QPushButton("🚀 立即开始批量更新")
        self.result_display = QTextEdit()

        # 配置项映射
        self.CONFIG_MAPPING = {
            "realname": "LastSession\trealname",
            "certificate": "LastSession\tcertificate",
            "rating": "LastSession\trating",
            "password": "LastSession\tpassword",
            "tovatsim": "LastSession\ttovatsim"
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Personal Info Configurator {VERSION}")
        self.setGeometry(100, 100, 800, 800)  # 稍微调高了窗口高度

        self.apply_dark_theme()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # --- 标题栏 ---
        title_container = QHBoxLayout()
        title_label = QLabel("个人信息配置器")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00a2ff; margin-bottom: 5px;")

        ver_label = QLabel(VERSION)
        ver_label.setFont(QFont("Consolas", 10))
        ver_label.setStyleSheet("color: #666; margin-top: 10px; margin-left: 10px;")

        title_container.addWidget(title_label)
        title_container.addWidget(ver_label)
        title_container.addStretch()
        main_layout.addLayout(title_container)

        # --- 目录选择区 ---
        dir_group = QFrame()
        dir_group.setStyleSheet("QFrame { background-color: #2d2d2d; border-radius: 8px; }")
        dir_h_layout = QHBoxLayout(dir_group)

        self.dir_input.setPlaceholderText("请选择扇区根目录...")
        self.dir_input.setStyleSheet("background: transparent; border: none; color: white; padding: 8px;")

        browse_btn = QPushButton("浏览目录")
        browse_btn.setFixedWidth(100)
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet("""
            QPushButton { background-color: #444; border-radius: 4px; padding: 5px; }
            QPushButton:hover { background-color: #555; }
        """)
        browse_btn.clicked.connect(self.browse_directory)

        dir_h_layout.addWidget(QLabel("📂"))
        dir_h_layout.addWidget(self.dir_input)
        dir_h_layout.addWidget(browse_btn)
        main_layout.addWidget(dir_group)

        # --- 输入表单区 ---
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px; padding: 15px;")
        input_group = QGridLayout(form_frame)
        input_group.setVerticalSpacing(12)

        fields = [
            ("姓名", "realname", "Real Name (例如: Zhang San)"),
            ("CID", "certificate", "CID (例如: 1234)"),
            ("密码", "password", "Your Network Password"),
            ("等级", "rating", "(OBS-'0' S1-'1' S2-'2' S3-'3' C1-'4' C2-'5' C3-'6' I1-'7' I2-'8' I3-'9')"),
        ]

        for i, (label_text, key, placeholder) in enumerate(fields):
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Microsoft YaHei", -1, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #bbb;")

            edit = QLineEdit()
            edit.setPlaceholderText(placeholder)
            edit.setStyleSheet("""
                QLineEdit { 
                    background-color: #3d3d3d; border: 1px solid #444; 
                    border-radius: 4px; color: white; padding: 8px; 
                }
                QLineEdit:focus { border: 1px solid #00a2ff; }
            """)

            input_group.addWidget(lbl, i, 0)

            # 针对密码框的特殊处理
            if key == "password":
                edit.setEchoMode(QLineEdit.EchoMode.Password)

                # 创建一个水平布局来放置密码框和切换按钮
                pwd_layout = QHBoxLayout()
                pwd_layout.setContentsMargins(0, 0, 0, 0)
                pwd_layout.addWidget(edit)

                self.show_pwd_cb = QCheckBox("显示")
                self.show_pwd_cb.setStyleSheet("color: #888; font-size: 11px;")
                self.show_pwd_cb.stateChanged.connect(self.toggle_password_visibility)
                pwd_layout.addWidget(self.show_pwd_cb)

                input_group.addLayout(pwd_layout, i, 1)
            else:
                input_group.addWidget(edit, i, 1)

            self.inputs[key] = edit

        # --- tovatsim 勾选框 ---
        self.tovatsim_checkbox.setChecked(True)
        self.tovatsim_checkbox.setStyleSheet("""
            QCheckBox { color: #bbb; font-weight: bold; padding: 5px; }
            QCheckBox::indicator { width: 18px; height: 18px; }
        """)
        input_group.addWidget(self.tovatsim_checkbox, len(fields), 1)

        main_layout.addWidget(form_frame)

        # --- 执行按钮 ---
        self.execute_btn.setFixedHeight(50)
        self.execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.execute_btn.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        self.execute_btn.setStyleSheet("""
            QPushButton { background-color: #0078d4; color: white; border-radius: 6px; }
            QPushButton:hover { background-color: #0086f0; }
            QPushButton:pressed { background-color: #005a9e; }
        """)
        self.execute_btn.clicked.connect(self.start_processing)
        main_layout.addWidget(self.execute_btn)

        # --- 日志输出区 ---
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("""
            QTextEdit { 
                background-color: #1a1a1a; border: 1px solid #333; 
                border-radius: 6px; color: #d4d4d4; font-family: 'Consolas';
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.result_display)

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(37, 37, 38))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        self.setPalette(palette)

    def toggle_password_visibility(self, state):
        """切换密码可见性"""
        if state == Qt.CheckState.Checked.value:
            self.inputs["password"].setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.inputs["password"].setEchoMode(QLineEdit.EchoMode.Password)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择 PRF 所在目录")
        if directory:
            self.dir_input.setText(directory)

    def start_processing(self):
        target_dir = self.dir_input.text().strip()
        if not target_dir or not os.path.isdir(target_dir):
            QMessageBox.warning(self, "错误", "请先选择有效的根目录！")
            return

        self.result_display.clear()
        self.result_display.append(f"<span style='color: #888;'>Core Version: {VERSION}</span>")
        self.result_display.append("<span style='color: #00a2ff;'>[INFO] 正在扫描 .prf 文件...</span>")

        prf_files = glob.glob(os.path.join(target_dir, '**', '*.prf'), recursive=True)

        if not prf_files:
            self.result_display.append("<span style='color: #e51400;'>[WARN] 未找到配置文件。</span>")
            return

        success_count = 0
        for file_path in prf_files:
            try:
                self.process_single_file(file_path)
                self.result_display.append(f"<span style='color: #4ec9b0;'>[PASS]</span> {os.path.basename(file_path)}")
                success_count += 1
            except Exception as e:
                self.result_display.append(
                    f"<span style='color: #f44747;'>[FAIL]</span> {os.path.basename(file_path)}: {str(e)}")

        self.result_display.append(f"<br><b style='color: white;'>处理完成！成功同步: {success_count} 个文件</b>")

    def process_single_file(self, file_path):
        lines = []
        if os.path.exists(file_path):
            # 增加对 GBK 的鲁棒性处理
            with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
                lines = f.readlines()

        prefixes = self.CONFIG_MAPPING.values()
        new_lines = [line for line in lines if not any(line.startswith(p) for p in prefixes)]

        for key, prefix in self.CONFIG_MAPPING.items():
            if key == "tovatsim":
                val = "1" if self.tovatsim_checkbox.isChecked() else "0"
            else:
                val = self.inputs[key].text().strip()

            if val or key == "tovatsim":
                new_lines.append(f"{prefix}\t{val}\n")

        with open(file_path, 'w', encoding='gbk') as f:
            f.writelines(new_lines)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PRFConfiguratorGUI()
    window.show()
    sys.exit(app.exec())