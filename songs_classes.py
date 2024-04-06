from dataclasses import dataclass


@dataclass
class Song:
    artist: str
    title: str
    url: str
    index: int

    def __post_init__(self):
        self.full_title = f'{self.artist} - {self.title}'


@dataclass
class SongsHint:
    value: str
