from actions.driven.inmemory.server import InMemoryServer
from actions.driving.music_player import DomainMusicPlayer
from actions.model.album import Album


def test_music_player_should_acknowledge_album_playing_with_artist_and_title():
    server = InMemoryServer()

    music_player = DomainMusicPlayer(server)

    assert music_player.play(Album(artist="The Beatles", title="Abbey Road")) == ("Ok, je vais faire comme si on "
                                                                                  "écoutait Abbey Road de The Beatles")
