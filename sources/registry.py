import json

from sources.block import Block


class Registry:
    def __init__(self):

        self.blocks = {}

        with open("blocks.json", "r", encoding="UTF-8") as file:
            self.blocks = json.load(file)

    def get_block_by_id(self, id):
        block_info = self.blocks.get(str(id), None)

        if block_info is not None:
            block = Block(block_info.get("name", "Undefined"))
            block.set_model(block_info.get("model", "resources/models/blocks/block.egg"))
            block.set_texture(block_info.get("texture", "resources/textures/blocks/block.png"))
            block.id = id

            return block

        return None
