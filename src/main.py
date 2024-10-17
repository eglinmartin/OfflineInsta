"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

profile = 'Test'
starting_post = '1000'

import json
import sys
import math
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollArea, QFrame, QVBoxLayout
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt


def exit_program():
    exit()


def get_num_photos(post):
    return len(os.listdir(fr"C:\Storage\Coding/Python Apps\OfflineInsta\data\profiles\{profile}\{post}")) - 1


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


class ThumbnailArea(QFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setLayout(QVBoxLayout())


class ThumbnailImage(QPushButton):
    def __init__(self, window, post, profile_data, x, y, fpath):
        super().__init__(window)
        self.window = window
        self.post = post
        self.profile_data = profile_data
        self.resize(250, 250)
        self.move(int(x), int(y))
        self.setStyleSheet(f"border-image: url({fpath}); border: none")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.cmd)

    def cmd(self):
        self.window.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{profile}/{self.post}/{self.post} (1).jpg);" f"border : none")
        self.window.window.main_title.setText(self.profile_data['posts'][self.post]['title'])

        date = datetime.strptime(self.profile_data['posts'][self.post]['date'], "%Y-%m-%d")
        date_formatted = datetime.strftime(date, '%Y/%m/%d')
        self.window.window.main_text.setText(f"{date_formatted} - {self.profile_data['posts'][self.post]['description']}")
        self.window.window.selected_post = self.post
        self.window.window.current_photo = 1
        # self.window.window.label_photo_number.setText(f"1 / {get_num_photos(self.window.window.selected_post)}")


class MainImage(QLabel):
    def __init__(self, window, x, y):
        super().__init__(window)
        self.resize(1000, 750)
        self.move(int(x), int(y))


class ScrollButton(QPushButton):
    def __init__(self, window, direction):
        super().__init__(window)
        self.window = window
        self.direction = direction
        self.clicked.connect(self.change_photo)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.num_photos = get_num_photos(self.window.selected_post)

    def change_photo(self):
        self.num_photos = get_num_photos(self.window.selected_post)
        if self.direction == 'left':
            if self.window.current_photo > 1:
                self.window.current_photo -= 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")
                # self.window.label_photo_number.setText(f"{self.window.current_photo} / {self.num_photos}")
        elif self.direction == 'right':
            if self.window.current_photo < self.num_photos:
                self.window.current_photo += 1
                self.window.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{profile}/{self.window.selected_post}/{self.window.selected_post} ({str(self.window.current_photo)}).jpg);" f"border : none")
                # self.window.label_photo_number.setText(f"{self.window.current_photo} / {self.num_photos}")


class MainWindow(QMainWindow):
    def __init__(self, profile_data):
        super().__init__()
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)
        self.setStyleSheet('background-color: #000000;')  #TODO: Make this an option you can change
        # self.setStyleSheet('background-color: #1f261f;')  #TODO: Make this an option you can change
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.selected_post = starting_post  #TODO: Make this the most recent photo set
        self.current_photo = 1

        # Draw exit button
        self.exit_button = QPushButton(self)
        self.exit_button.resize(128, 128)
        self.exit_button.move(1792, 0)
        self.exit_button.setStyleSheet("border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/bin/ui/exit.png); border: none;")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.clicked.connect(exit_program)

        # Draw main image
        self.main_image = MainImage(self, x=870, y=50)
        self.main_image.setStyleSheet(fr"border-image: url(C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{profile}/{self.selected_post}/{self.selected_post} (1).jpg);" f"border : none")

        # Draw thumbnail section
        self.scroll = ThumbnailBox(self)
        num_rows = math.ceil((len(profile_data['posts'])) / 3)
        self.scroll.inner.setFixedHeight((260*num_rows)+(10*(num_rows-1)))
        for i, post in enumerate(reversed(profile_data['posts'])):
            self.image = ThumbnailImage(self.scroll.inner, post, profile_data, x=260*(i%3), y=260*(i//3),
                                        fpath=f"C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{profile}/{post}/{post} (0).jpg")

        # Draw main title
        self.main_title = QLabel(self)
        self.main_title.move(870, 830)  # Set the position of the label
        self.main_title.setFont(QFont("Bahnschrift", 36))
        self.main_title.setFixedWidth(850)
        self.main_title.setFixedHeight(100)
        self.main_title.setWordWrap(True)
        self.main_title.setStyleSheet("color: #FFFFFF;")
        # self.main_title.setAlignment(Qt.AlignCenter)
        self.main_title.setText(profile_data['posts'][self.selected_post]['title'])

        # Draw main text
        self.main_text = QLabel(self)
        self.main_text.move(870, 950)  # Set the position of the label
        self.main_text.setFont(QFont("Verdana", 12))
        self.main_text.setFixedWidth(800)
        self.main_text.setFixedHeight(200)
        self.main_text.setAlignment(Qt.AlignTop)
        self.main_text.setWordWrap(True)
        self.main_text.setStyleSheet("color: #ffffff;")

        self.date = datetime.strptime(profile_data['posts'][self.selected_post]['date'], "%Y-%m-%d")
        self.date_formatted = datetime.strftime(self.date, '%Y/%m/%d')
        self.main_text.setText(f"{self.date_formatted} - {profile_data['posts'][self.selected_post]['description']}")

        # Draw left button
        self.button_left = ScrollButton(self, direction='left')
        self.button_left.resize(140, 140)
        self.button_left.move(1730, 1010)
        self.button_left.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.button_left.setFont(QFont("Verdana", 40))
        self.button_left.setText(f"<")

        # Draw photo number
        # self.label_photo_number = QLabel(self)
        # self.label_photo_number.setFixedSize(150, 100)
        # self.label_photo_number.move(1320, 715)
        # self.label_photo_number.setStyleSheet("color: #ffffff;")
        # self.label_photo_number.setFont(QFont("Verdana", 24))
        # self.label_photo_number.setAlignment(Qt.AlignCenter)
        # self.label_photo_number.setText(f"1 / {get_num_photos(self.selected_post)}")

        # Draw right button
        self.button_right = ScrollButton(self, direction='right')
        self.button_right.resize(140, 140)
        self.button_right.move(1730, 850)
        self.button_right.setStyleSheet("color: #ffffff; border: none; background-color: #000000;")
        self.button_right.setFont(QFont("Verdana", 40))
        self.button_right.setText(f">")


def import_from_json(json_path):
    with open(json_path, 'r') as file:
        profile_data = json.load(file)
        return profile_data


def main():
    profile_data = import_from_json(fr"C:\Storage\Coding/Python Apps\OfflineInsta\data\profiles\{profile}\profile.json") #TODO: Soft-code filepaths!!

    app = QApplication(sys.argv)
    window = MainWindow(profile_data)
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
