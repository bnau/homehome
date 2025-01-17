import os.path
from typing import List

import json

from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.model.metadata import Album


class InMemoryMetadataRetriever(MetadataRetriever):

    def get_albums(self) -> List[Album]:
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/albums.json") as f:
            d = json.load(f)
            albums = []
            for album in d['result']['albums_loop']:
                albums.append(Album(
                    album_id=album['id'],
                    title=album['album'],
                    artist=album['artist']
                ))
            return albums