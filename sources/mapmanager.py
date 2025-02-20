import pickle
from random import randint

from sources.registry import Registry
from panda3d.core import *


class Mapmanager:
    def __init__(self):
        self.land = None
        self.registry = Registry()

        self.cubeMap = loader.loadCubeMap(
            'resources/textures/skybox/skybox_#.jpg')

        self.skybox = loader.loadModel('resources/models/blocks/block.egg')

        self.skybox.setScale(10000)
        self.skybox.setBin('background', 0)
        self.skybox.setTwoSided(True)

        self.skybox.setTexGen(
            TextureStage.getDefault(),TexGenAttrib.MWorldPosition)
        self.skybox.setTexProjector(
            TextureStage.getDefault(), render, self.skybox)
        self.skybox.setTexture(self.cubeMap)

        self.skybox.reparentTo(render)

        self.start_new_world()

    def start_new_world(self):
        self.land = render.attachNewNode("Land")

        import sources.generate_world

        with open("start_world.txt", "r") as file:
            for y, row in enumerate(file.readlines(), start=0):
                for x, symbol in enumerate(row.split(" "), start=0):
                    for z in range(int(symbol)):

                        block_choosen = 2

                        if z == 0:
                            block_choosen = 3

                        if z == 1:
                            num = randint(1, 5)
                            if num == 1:
                                block_choosen = 2
                            else:
                                block_choosen = 3

                        if z == 2:
                            num = randint(1, 5)
                            if num == 1:
                                block_choosen = 3
                            else:
                                block_choosen = 2

                        if z == int(symbol) - 1:
                            block_choosen = 0

                        if int(symbol) - 4 <= z < int(symbol) - 1:
                            block_choosen = 1

                        self.set_block(
                            block=self.registry.get_block_by_id(block_choosen),
                            position=(x, y, z)
                        )

    # "(0, 0, 0)" != "(0.0, 0.0, 0.0)"

    def set_block(self, block, position):
        block.set_position(position)
        block.create(self.land)
        block.model.setTag("pos", str((int(position[0]), int(position[1]), int(position[2]))))
        block.model.setTag("id", str(block.id))

    def remove_block(self, position):
        blocks = self.find_blocks(position)
        for block in blocks:
            block.removeNode()

    def build_block(self, block, position):
        x, y, z = position

        new_block_position = self.find_highest_empty(position)
        if new_block_position[2] <= z + 1:
            self.set_block(block, new_block_position)

    def destroy_block(self, position):
        x, y, z = self.find_highest_empty(position)
        z -= 1

        self.remove_block((x, y, z))

    def is_empty(self, pos):
        blocks = self.find_blocks(pos)
        return False if blocks else True

    def find_blocks(self, pos):
        x, y, z = int(pos[0]), int(pos[1]), int(pos[2])
        return self.land.findAllMatches("=pos=" + str((x, y, z)))

    def find_highest_empty(self, pos):
        x, y, z = int(pos[0]), int(pos[1]), 0

        while not self.is_empty((x, y, z)):
            z += 1

        return (x, y, z)

    def clear_map(self):
        self.land.removeNode()
        self.land = render.attachNewNode("Land")

    def load_map(self):
        self.clear_map()

        with open("saved_map.dat", "rb") as file:
            blocks_count = pickle.load(file)

            for i in range(blocks_count):
                block_info = pickle.load(file)

                id = block_info[0]
                pos = block_info[1]

                self.set_block(self.registry.get_block_by_id(id), pos)

    def save_map(self):
        blocks = self.land.getChildren()

        with open("saved_map.dat", "wb") as file:
            pickle.dump(len(blocks), file)

            for block in blocks:
                pos = block.getPos()
                pos = (int(pos[0]), int(pos[1]), int(pos[2]))
                id = int(block.getTag("id"))
                pickle.dump((id, pos), file)
