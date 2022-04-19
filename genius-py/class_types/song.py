import json
from filecmp import cmp

from class_types.base import BaseEntity
from class_types.artist import Artist


class Song(BaseEntity):
    """A song from Genius"""

    def __init__(self, client, json_dict, lyrics=""):
        body = json_dict
        super().__init__(body["id"])
        self.body = body
        self._client = client
        self.artist = body["primary_artist"]["name"]
        self.lyrics = lyrics
        self.primary_artist = Artist(client, body["primary_artist"])

        self.api_path = body["api_path"]
        self.full_title = body["full_title"]
        self.path = body["path"]
        self.title = body["title"]
        self.url = body["url"]

    def to_dict(self):
        body = self.body.copy()
        body["artist"] = self.artist
        body["lyrics"] = self.lyrics
        return body

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data, indent=2, ensure_ascii=True)

    def __str__(self):
        lyr = self.lyrics[:100]
        if len(self.lyrics) > 100:
            lyr += "…"
        lyr.replace('\n', '\n    ')
        return f"{self.title} by {self.artist}:\n    {lyr}"

    def __cmp__(self, other):
        return (cmp(self.title, other.title)
            and cmp(self.artist, other.artist)
            and cmp(self.lyrics, other.lyrics))
