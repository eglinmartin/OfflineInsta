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
from PyQt5.QtWidgets import QApplication
from datetime import datetime

from gui import MainWindow


class PhotoSet:
    def __init__(self, post_id, post):
        self.post_id = post_id
        self.title = post['title']
        self.people = post['people'].split(', ')
        self.date = datetime.strptime(post['date'], '%Y-%m-%d')
        self.description = post['description']


def import_from_json(json_path):
    with open(json_path, 'r') as file:
        profile_data = json.load(file)

        photosets = [PhotoSet(post_id, profile_data['posts'][post_id]) for post_id in profile_data['posts']]
        photosets = sorted(photosets, key=lambda photoset: photoset.date)

        return photosets


def main():
    profile_name = 'Test'
    photosets = import_from_json(fr"C:\Storage\Coding\Python Apps\OfflineInsta\data\profiles\{profile_name}\profile.json")

    app = QApplication(sys.argv)
    window = MainWindow(profile_name, photosets)
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
