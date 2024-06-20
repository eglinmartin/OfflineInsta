"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt


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
        self.window.main_image.setStyleSheet(fr"border-image: url(D:/Coding/Python/OfflineInsta/data/profiles/EchoRope/photos/{self.post}/01.jpg);" f"border : none")
        self.window.main_title.setText(self.profile_data['posts'][self.post]['title'])
        self.window.main_text.setText(self.profile_data['posts'][self.post]['text'])


class MainImage(QLabel):
    def __init__(self, window, x, y):
        super().__init__(window)
        self.resize(850, 600)
        self.move(int(x), int(y))


class MainWindow(QMainWindow):
    def __init__(self, profile_data):
        super().__init__()
        self.setWindowTitle(profile_data['username'])
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        self.setStyleSheet('background-color: #282828;')
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Draw profile name
        self.profile_name = QLabel(profile_data['username'], self)
        self.profile_name.move(372, 97)  # Set the position of the label
        self.profile_name.setFont(QFont("Verdana", 64))
        self.profile_name.adjustSize()
        self.profile_name.setStyleSheet("color: #00FFFF;")

        # Draw profile picture
        self.profile_picture = QLabel(self)
        self.profile_picture.resize(220, 220)
        self.profile_picture.move(100, 100)
        self.profile_picture.setStyleSheet(fr"border-image : url(D:/Coding/Python/OfflineInsta/bin/ui/profile_border_temp.png);" f"border : none")

        # Draw profile bio
        self.profile_bio = QLabel(f"{profile_data['role']}\n{profile_data['city']}, {profile_data['country']}", self)
        self.profile_bio.move(375, 210)  # Set the position of the label
        self.profile_bio.setFont(QFont("Verdana", 32))
        self.profile_bio.adjustSize()
        self.profile_bio.setStyleSheet("color: #205252;")

        # # Draw thumbnail images
        for i, post in enumerate(reversed(profile_data['posts'])):
            self.image = ThumbnailImage(self, post, profile_data, x=100+(260*(i%3)), y=400+(260*(i//3)),
                                        fpath=f"D:/Coding/Python/OfflineInsta/data/profiles/EchoRope/photos/{post}/_thumb.jpg")

        # Draw main image
        self.main_image = MainImage(self, x=970, y=100)

        # Draw main title
        self.main_title = QLabel(self)
        self.main_title.move(970, 700)  # Set the position of the label
        self.main_title.setFont(QFont("Verdana", 24))
        self.main_title.setFixedWidth(850)
        self.main_title.setFixedHeight(100)
        self.main_title.setAlignment(Qt.AlignVCenter)
        self.main_title.setWordWrap(True)
        self.main_title.setStyleSheet("color: #00FFFF;")

        # Draw main text
        self.main_text = QLabel(self)
        self.main_text.move(970, 800)  # Set the position of the label
        self.main_text.setFont(QFont("Verdana", 16))
        self.main_text.setFixedWidth(850)
        self.main_text.setFixedHeight(400)
        self.main_text.setAlignment(Qt.AlignTop)
        self.main_text.setWordWrap(True)
        self.main_text.setStyleSheet("color: #ffffff;")



def import_from_json(json_path):
    with open(json_path, 'r') as file:
        profile_data = json.load(file)
        return profile_data


def main():
    profile_data = import_from_json(r"D:\Coding\Python\OfflineInsta\data\profiles\EchoRope\profile.json")

    app = QApplication(sys.argv)
    window = MainWindow(profile_data)
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()