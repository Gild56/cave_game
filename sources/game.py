from direct.showbase.ShowBase import ShowBase
from sources.mapmanager import Mapmanager
from sources.hero import Hero


class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.mapmanager = Mapmanager()
        self.mapmanager = Mapmanager()
        pos_to_spawn = self.mapmanager.find_highest_empty((0, 0, 0))
        self.hero = Hero(pos_to_spawn, self.mapmanager)
