import os

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
        self.clicked.connect(self.change_photo)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.num_photos = self.get_num_photos()

        self.resize(140, 140)
        self.move(1730, y)
        self.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.setFont(QFont("Verdana", 40))
        self.setText(text)

    def get_num_photos(self):
        for post in self.window.photosets:
            if post.post_id == self.window.selected_post:
                return len(os.listdir(fr"C:\Storage\Coding/Python Apps\OfflineInsta\data\profiles\{self.profile}\{post.post_id}")) - 1

    def change_photo(self):
        self.num_photos = self.get_num_photos()
        if self.direction == 'left':
            if self.window.current_photo > 1:
                self.window.current_photo -= 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")
        elif self.direction == 'right':
            if self.window.current_photo < self.num_photos:
                self.window.current_photo += 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")


class TitleText(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.move(870, 830)  # Set the position of the label
        self.setFont(QFont("Bahnschrift", 36))
        self.setFixedWidth(850)
        self.setFixedHeight(100)
        self.setWordWrap(True)
        self.setStyleSheet("color: #FFFFFF;")


class DescriptionText(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.move(870, 950)  # Set the position of the label
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
