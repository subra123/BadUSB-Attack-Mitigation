import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import QProcess

class DuckHuntGUI(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("DuckHunt Monitor")
        self.setGeometry(100, 100, 600, 400)
        self.process = None

        # Create widgets
        self.statusLabel = QLabel("Status: OFF", self)
        self.toggleButton = QPushButton("Turn ON", self)
        self.logText = QTextEdit(self)
        self.logText.setReadOnly(True)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.toggleButton)
        layout.addWidget(self.logText)
        self.setLayout(layout)

        # Connect the button to toggle the mode
        self.toggleButton.clicked.connect(self.toggle_mode)

    def toggle_mode(self):
        if self.process is None:
            self.start_duckhunt()
        else:
            self.stop_duckhunt()

    def start_duckhunt(self):
        # Update these paths as necessary
        exe_path = "/home/subramanian/BadUSB-Attack-Mitigation/builds/duckhunt.0.9.exe"


        self.process = QProcess(self)
        self.process.setProgram(exe_path)
        # You can pass any required command line arguments via setArguments([])
        self.process.setArguments([])

        # Connect process signals for real-time logging
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.started.connect(lambda: self.log("DuckHunt process started."))
        self.process.finished.connect(lambda exitCode, exitStatus: self.log(f"DuckHunt process terminated with exit code {exitCode}"))

        # Start the process (runs as a daemon)
        self.process.start()

        # Update GUI state
        self.statusLabel.setText("Status: ON")
        self.toggleButton.setText("Turn OFF")

    def stop_duckhunt(self):
        if self.process:
            self.process.kill()  # Terminates the running process
            self.log("DuckHunt process terminated manually.")
            self.process = None

        # Update GUI state
        self.statusLabel.setText("Status: OFF")
        self.toggleButton.setText("Turn ON")

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.log(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.log(data)

    def log(self, message):
        self.logText.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DuckHuntGUI()
    window.show()
    sys.exit(app.exec_())
