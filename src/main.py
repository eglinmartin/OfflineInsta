"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import math

profile = 'Test'
starting_post = '1000'

import json
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollArea, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
import gui


class PhotoSet:
    def __init__(self, post_id, post):
        self.post_id = post_id
        self.title = post['title']
        self.people = post['people'].split(', ')
        self.date = datetime.strptime(post['date'], '%Y-%m-%d')
        self.description = post['description']


class MainWindow(QMainWindow):
    def __init__(self, profile_name):
        super().__init__()
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)
        self.setStyleSheet('background-color: #000000;')
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.profile_name = profile_name
        self.photosets = self.import_from_json(fr"C:/Storage\Coding\Python Apps\OfflineInsta\data\profiles\{profile_name}\profile.json")
        self.current_photo = 1
        self.selected_post = self.photosets[len(self.photosets)-1].post_id

        self.exit_button = gui.ExitButton(self)
        self.main_image = gui.MainImage(self)
        self.title_text = gui.TitleText(self)
        self.description_text = gui.DescriptionText(self)
        self.button_left = gui.ScrollButton(self, self.profile_name, y=1010, direction='left', text='<')
        self.button_right = gui.ScrollButton(self, self.profile_name, y=850, direction='right', text='>')

        # Draw thumbnail section
        self.scroll = gui.ThumbnailBox(self)
        num_rows = math.ceil((len(self.photosets)) / 3)
        self.scroll.inner.setFixedHeight((260*num_rows)+(10*(num_rows-1)))
        for i, post in enumerate(reversed(self.photosets)):
            self.image = gui.ThumbnailImage(self.scroll.inner, post, self.profile_name, x=260*(i%3), y=260*(i//3),
                                        fpath=f"C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles/{self.profile_name}/{post.post_id}/{post.post_id} (0).jpg")
        self.select_post(self.selected_post)

    def import_from_json(self, json_path):
        with open(json_path, 'r') as file:
            profile_data = json.load(file)
            photosets = [PhotoSet(post_id, profile_data['posts'][post_id]) for post_id in profile_data['posts']]
            photosets = sorted(photosets, key=lambda photoset: photoset.date)
        return photosets

    def select_post(self, post_id):
        self.current_photo = 1
        base_path = "C:/Storage/Coding/Python Apps/OfflineInsta/data/profiles"

        for post in self.photosets:
            if post.post_id == post_id:
                self.title_text.setText(post.title.upper())
                self.description_text.setText(post.description)

        self.main_image.setStyleSheet(
            fr"border-image: url({base_path}/{self.profile_name}/{post_id}/{post_id} (1).jpg);" f"border : none")

        self.selected_post = post_id

    def exit_program(self):
        exit()


def main():
    profile_name = 'Test'

    app = QApplication(sys.argv)
    window = MainWindow(profile_name)
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
