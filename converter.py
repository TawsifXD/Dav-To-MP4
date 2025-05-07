import sys, os, subprocess, re, configparser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget, QMessageBox, QProgressBar, QHBoxLayout,
    QMenuBar, QAction, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

class ConverterThread(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal(str)

    def __init__(self, files, output_folder, mode):
        super().__init__()
        self.files = files
        self.output_folder = output_folder
        self.mode = mode

    def run(self):
        for i, file_path in enumerate(self.files):
            base_name = os.path.basename(file_path)
            name_no_ext = os.path.splitext(base_name)[0]

            if self.mode == "WhatsApp Optimized":
                output_path = os.path.join(self.output_folder, name_no_ext + "_cctv_footage.mp4")
                cmd = [
                    "ffmpeg", "-y", "-i", file_path,
                    "-vf", "scale='min(640,iw)':'min(480,ih)':force_original_aspect_ratio=decrease",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                    "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart",
                    output_path
                ]
            else:  # Standard MP4
                output_path = os.path.join(self.output_folder, name_no_ext + "_converted.mp4")
                cmd = [
                    "ffmpeg", "-y", "-i", file_path,
                    "-c:v", "libx264", "-crf", "20", "-preset", "fast",
                    "-c:a", "aac", "-b:a", "192k",
                    output_path
                ]

            try:
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                duration = float(result.stdout.strip())
            except:
                duration = None

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)

            for line in process.stderr:
                if "time=" in line:
                    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                    if match and duration:
                        h, m, s = map(float, match.groups())
                        current = h * 3600 + m * 60 + s
                        percent = int((current / duration) * 100)
                        self.progress.emit(percent)

            process.wait()
            self.progress.emit(100)

        self.done.emit("All files converted successfully.")

class DAVConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DAV to MP4 Converter")
        self.setFixedSize(620, 550)
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon("app_icon.ico"))

        self.files = []
        self.output_folder = os.getcwd()
        self.dark_mode = False
        self.config_file = "settings.ini"

        self.load_settings()

        # Menu bar with only About
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setCursor(Qt.PointingHandCursor)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        self.menu_bar.addAction(about_action)

        self.layout = QVBoxLayout()
        self.layout.setMenuBar(self.menu_bar)

        self.label = QLabel("🎥 Drag & Drop or Browse .dav Files")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 12px;")
        self.list_widget.setCursor(Qt.IBeamCursor)

        self.btn_browse = QPushButton("📂 Browse Files")
        self.btn_browse.clicked.connect(self.open_files)
        self.btn_browse.setCursor(Qt.PointingHandCursor)

        self.btn_output = QPushButton("📁 Output Folder")
        self.btn_output.clicked.connect(self.select_output_folder)
        self.btn_output.setCursor(Qt.PointingHandCursor)

        self.btn_convert = QPushButton("🚀 Start Conversion")
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_convert.setStyleSheet("font-weight: bold;")
        self.btn_convert.setCursor(Qt.PointingHandCursor)

        self.btn_toggle_theme = QPushButton("🌓 Toggle Theme")
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)
        self.btn_toggle_theme.setCursor(Qt.PointingHandCursor)

        self.convert_mode = QComboBox()
        self.convert_mode.addItems(["WhatsApp Optimized", "Standard MP4"])
        self.convert_mode.setToolTip("Choose conversion mode")
        self.convert_mode.setCursor(Qt.PointingHandCursor)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.btn_browse)
        top_bar.addWidget(self.btn_output)
        top_bar.addWidget(self.btn_toggle_theme)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(top_bar)
        self.layout.addWidget(self.convert_mode)
        self.layout.addWidget(self.btn_convert)
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About DAV to MP4 Converter")
        about_box.setIconPixmap(QPixmap("app_icon.ico").scaled(64, 64, Qt.KeepAspectRatio))
        about_box.setText("""
        <div style='line-height: 1.6;'>
            <h2 style='color: #2a76c6;'>DAV to MP4 Converter</h2>
            <p><b>Version:</b> 1.2.0</p>
            <p><b>Developed by:</b> Mozahid Islam</p>
            <p>This tool converts DAV video files from CCTV cameras to MP4 format.</p>
            <h3 style='color: #2a76c6;'>Features:</h3>
            <ul>
                <li>Batch conversion of multiple files</li>
                <li>WhatsApp and Standard MP4 modes</li>
                <li>Real-time progress tracking</li>
                <li>Dark/Light theme support</li>
                <li>Drag and drop interface</li>
            </ul>
            <p style='font-size: 11px; margin-top: 20px;'>© 2025 Mozahid Islam. All rights reserved.</p>
        </div>
        """)
        about_box.setStandardButtons(QMessageBox.Ok)
        about_box.exec_()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".dav") and file_path not in self.files:
                self.files.append(file_path)
                self.list_widget.addItem(file_path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected = self.list_widget.selectedItems()
            for item in selected:
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)
                self.files.pop(row)

    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select DAV Files", "", "DAV Files (*.dav)")
        for f in files:
            if f not in self.files:
                self.files.append(f)
                self.list_widget.addItem(f)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.save_settings()

    def start_conversion(self):
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add some DAV files first.")
            return
        if not os.path.exists("ffmpeg.exe") or not os.path.exists("ffprobe.exe"):
            QMessageBox.critical(self, "FFmpeg Missing", "ffmpeg.exe and ffprobe.exe must be in app folder.")
            return
        mode = self.convert_mode.currentText()
        self.thread = ConverterThread(self.files, self.output_folder, mode)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.done.connect(self.on_done)
        self.btn_convert.setEnabled(False)
        self.progress.setValue(0)
        self.thread.start()

    def on_done(self, msg):
        self.btn_convert.setEnabled(True)
        QMessageBox.information(self, "Finished", msg)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
        self.save_settings()

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #f0f0f0; font-size: 13px; }
            QPushButton { background-color: #444; border: none; padding: 8px; color: white; }
            QListWidget, QProgressBar { background-color: #333; color: white; }
            QMenuBar, QMenuBar::item, QMenu { background-color: #2b2b2b; color: #f0f0f0; }
            QMenu::item:selected, QMenuBar::item:selected { background-color: #444; }
        """)

    def set_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; color: #000; font-size: 13px; }
            QPushButton { background-color: #e0e0e0; border: none; padding: 8px; color: black; }
            QListWidget, QProgressBar { background-color: white; color: black; }
            QMenuBar, QMenuBar::item, QMenu { background-color: #f0f0f0; color: #000; }
            QMenu::item:selected, QMenuBar::item:selected { background-color: #e0e0e0; }
        """)

    def load_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            self.output_folder = config.get("Settings", "output_folder", fallback=os.getcwd())
            theme = config.get("Settings", "theme", fallback="light")
            if theme == "dark":
                self.dark_mode = True
                self.set_dark_theme()
            else:
                self.set_light_theme()
        else:
            self.set_light_theme()

    def save_settings(self):
        config = configparser.ConfigParser()
        config["Settings"] = {
            "output_folder": self.output_folder,
            "theme": "dark" if self.dark_mode else "light"
        }
        with open(self.config_file, "w") as configfile:
            config.write(configfile)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DAVConverter()
    win.show()
    sys.exit(app.exec_())
