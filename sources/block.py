class Block:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.model = None
        self.texture = None
        self.color = None
        self.position = None

    def set_model(self, model_path):
        self.model = model_path

    def set_texture(self, texture_path):
        self.texture = texture_path

    def set_color(self, color):
        self.color = color

    def set_position(self, position):
        self.position = position

    def create(self, node):
        self.model = loader.loadModel(self.model)
        texture = loader.loadTexture(self.texture)
        self.model.setTexture(texture)
        # model.setColor(self.color or (0, 0, 0))
        self.model.setPos(self.position)

        self.model.reparentTo(node)
