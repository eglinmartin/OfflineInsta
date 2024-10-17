import math
from datetime import datetime
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollArea, QFrame, QVBoxLayout
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
        self.window.window.main_image.setStyleSheet(
            fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile_name}/{self.post.post_id}/{self.post.post_id} (1).jpg);" f"border : none")

        self.window.window.main_title.setText(self.post.title)

        self.window.window.main_text.setText(
            f"{self.post.date} - {self.post.description}")
        self.window.window.selected_post = self.post.post_id
        self.window.window.current_photo = 1
        # self.window.window.label_photo_number.setText(f"1 / {get_num_photos(self.window.window.selected_post)}")



class ScrollButton(QPushButton):
    def __init__(self, window, profile, direction):
        super().__init__(window)
        self.window = window
        self.direction = direction
        self.profile = profile
        self.clicked.connect(self.change_photo)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.num_photos = self.get_num_photos()

    def get_num_photos(self):
        print(self.window.selected_post)
        for post in self.window.photosets:
            if post.post_id == self.window.selected_post:
                return len(os.listdir(fr"C:\Storage\Coding/Python Apps\OfflineInsta\data\profiles\{self.profile}\{post.post_id}")) - 1

    def change_photo(self):
        self.num_photos = self.get_num_photos()
        print(self.num_photos)
        if self.direction == 'left':
            if self.window.current_photo > 1:
                self.window.current_photo -= 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")
                # self.window.label_photo_number.setText(f"{self.window.current_photo} / {self.num_photos}")
        elif self.direction == 'right':
            if self.window.current_photo < self.num_photos:
                self.window.current_photo += 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")
                # self.window.label_photo_number.setText(f"{self.window.current_photo} / {self.num_photos}")


class MainImage(QLabel):
    def __init__(self, window, x, y):
        super().__init__(window)
        self.resize(1000, 750)
        self.move(int(x), int(y))


class MainWindow(QMainWindow):
    def __init__(self, profile_name, photosets):
        super().__init__()
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)
        self.setStyleSheet('background-color: #000000;')
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.profile_name = profile_name
        self.photosets = photosets
        self.selected_post = photosets[0].post_id
        self.current_photo = 1

        # Draw exit button
        self.exit_button = QPushButton(self)
        self.exit_button.resize(128, 128)
        self.exit_button.move(1792, 0)
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.clicked.connect(self.exit_program)

        # Draw main image
        self.main_image = MainImage(self, x=870, y=50)
        self.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile_name}/{self.selected_post}/{self.selected_post} (1).jpg);" f"border : none")

        # Draw thumbnail section
        self.scroll = ThumbnailBox(self)
        num_rows = math.ceil((len(self.photosets)) / 3)
        self.scroll.inner.setFixedHeight((260*num_rows)+(10*(num_rows-1)))
        for i, post in enumerate(reversed(self.photosets)):
            self.image = ThumbnailImage(self.scroll.inner, post, self.profile_name, x=260*(i%3), y=260*(i//3),
                                        fpath=f"C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile_name}/{post.post_id}/{post.post_id} (0).jpg")

        # Draw main title
        self.main_title = QLabel(self)
        self.main_title.move(870, 830)  # Set the position of the label
        self.main_title.setFont(QFont("Bahnschrift", 36))
        self.main_title.setFixedWidth(850)
        self.main_title.setFixedHeight(100)
        self.main_title.setWordWrap(True)
        self.main_title.setStyleSheet("color: #FFFFFF;")

        # Draw main text
        self.main_text = QLabel(self)
        self.main_text.move(870, 950)  # Set the position of the label
        self.main_text.setFont(QFont("Verdana", 12))
        self.main_text.setFixedWidth(800)
        self.main_text.setFixedHeight(200)
        self.main_text.setAlignment(Qt.AlignTop)
        self.main_text.setWordWrap(True)
        self.main_text.setStyleSheet("color: #ffffff;")

        # Draw left button
        self.button_left = ScrollButton(self, self.profile_name, direction='left')
        self.button_left.resize(140, 140)
        self.button_left.move(1730, 1010)
        self.button_left.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.button_left.setFont(QFont("Verdana", 40))
        self.button_left.setText(f"<")

        # Draw right button
        self.button_right = ScrollButton(self, self.profile_name, direction='right')
        self.button_right.resize(140, 140)
        self.button_right.move(1730, 850)
        self.button_right.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.button_right.setFont(QFont("Verdana", 40))
        self.button_right.setText(f">")

        for post in self.photosets:
            if post.post_id == self.selected_post:
                print(post.title)
                self.main_title.setText(post.title)
                self.main_text.setText(f"{post.date} - {post.description}")

    def exit_program(self):
        exit()
