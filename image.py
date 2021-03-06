"""
SJSU CS 218 Fall 2019 TEAM 4

Class to present Image data and conveniently pass it to front-end.
"""


class Image:
    def __init__(self, image_id, username="default user", description="Default description", tags=list(), privacy=True):
        self.image_id = image_id
        self.image_src = "/images/" + image_id + ".jpg"
        self.username = username
        self.description = description
        self.tags = tags
        self.privacy = privacy
