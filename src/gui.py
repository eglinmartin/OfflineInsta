from PyQt5.QtWidgets import QLabel, QPushButton, QScrollArea, QFrame, QVBoxLayout
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt


class ThumbnailArea(QFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setLayout(QVBoxLayout())


class ThumbnailBox(QScrollArea):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.resize(820, 910)
        self.move(50, 240)
        self.setStyleSheet('border: none;')
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.inner = ThumbnailArea(window)
        self.setWidget(self.inner)


class ThumbnailImage(QPushButton):
    def __init__(self, window, post, profile_name, x, y, fpath):
        super().__init__(window)
        self.window = window
        self.post = post
        self.profile_name = profile_name
        self.resize(250, 250)
        self.move(int(x), int(y))
        self.setStyleSheet(f"border-image: url({fpath}); border: none")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.cmd)

    def cmd(self):
        self.window.window.select_post(self.post.post_id)


class ScrollButton(QPushButton):
    def __init__(self, window, profile, y, direction, text):
        super().__init__(window)
        self.window = window
        self.direction = direction
        self.profile = profile
        self.clicked.connect(self.cmd)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.resize(140, 140)
        self.move(1730, y)
        self.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.setFont(QFont("Verdana", 40))
        self.setText(text)

    def cmd(self):
        self.window.change_photo(direction=self.direction)


class MenuButton(QPushButton):
    def __init__(self, window, n, text):
        super().__init__(window)
        self.resize(146, 180)
        self.move(50+((146+10)*(n-1)), 50)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.cmd)
        self.setStyleSheet("background-color: #000000; color: #ffffff")
        self.setFont(QFont("Verdana", 16))
        self.setText(text)

    def cmd(self):
        pass


class TitleText(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.move(870, 830)
        self.setFont(QFont("Bahnschrift", 36))
        self.setFixedWidth(850)
        self.setFixedHeight(100)
        self.setWordWrap(True)
        self.setStyleSheet("color: #FFFFFF;")


class DescriptionText(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.move(870, 950)
        self.setFont(QFont("Verdana", 12))
        self.setFixedWidth(800)
        self.setFixedHeight(200)
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setStyleSheet("color: #ffffff;")


class ExitButton(QPushButton):
    def __init__(self, window):
        super().__init__(window)
        self.resize(128, 128)
        self.move(1792, 0)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(window.exit_program)


class MainImage(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.resize(1000, 750)
        self.move(int(870), int(50))
