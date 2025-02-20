from sources.registry import Registry


KEY_SWITCH_CAMERA = 'c'
KEY_SWITCH_GAMEMODE = "v"
KEY_SWITCH_BLOCK = "x"

KEY_PLACE_BLOCK = "mouse3"
KEY_DESTROY_BLOCK = "mouse1"

KEY_FORWARD = "w"
KEY_LEFT = "a"
KEY_BACK = "s"
KEY_RIGHT = "d"

KEY_UP = "r"
KEY_DOWN = "f"

KEY_TURN_LEFT = "q"
KEY_TURN_RIGHT = "e"

KEY_TURN_UP = "b"
KEY_TURN_DOWN = "n"

KEY_SAVE_MAP = "o"
KEY_LOAD_MAP = "p"


class Hero:
    def __init__(self, position, land):

        self.registry = Registry()

        self.land = land
        self.camera_mode = 0
        self.gamemode = 0
        self.block = 1

        self.hero = loader.loadModel("smiley")
        self.hero.setColor(1, 0.35, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(position)
        self.hero.reparentTo(render)

        self.enable_first_person_camera()
        self.enable_controls()

    def enable_first_person_camera(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.setR(0)
        base.camera.setP(0)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 2)
        self.camera_mode = 0

    def enable_third_person_camera(self):
        base.enableMouse()
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        self.camera_mode = 1

    def switch_camera(self):
        # 1. Звичайна реалізація
        if self.camera_mode == 1:
            self.enable_first_person_camera()
        else:
            self.enable_third_person_camera()

        # 2. Тернарний умовний оператор
        # self.enable_first_person_camera()
        # if self.camera_mode == 1 else self.enable_third_person_camera()

    def switch_gamemode(self):
        if self.gamemode == 0:
            self.gamemode = 1
        else:
            self.gamemode = 0

    def switch_block(self):
        self.block = (self.block + 1) % len(self.registry.blocks)

    def check_direction(self, angle):

        if angle <= 20 and angle >= 0:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def get_forward_coordinates(self, angle):

        pos = self.hero.getPos()
        x, y, z = int(pos[0]), int(pos[1]), int(pos[2])

        shift_x, shift_y = self.check_direction(angle)
        x += shift_x
        y += shift_y

        return (x, y, z)

    def just_move(self, angle):
        pos = self.get_forward_coordinates(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.get_forward_coordinates(angle)
        if self.land.is_empty(pos):
            pos = self.land.find_highest_empty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.is_empty(pos):
                self.hero.setPos(pos)

    def move_to(self, angle):
        if self.gamemode == 0:
            self.try_move(angle)
        else:
            self.just_move(angle)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def go_forward(self):
        angle = (self.hero.getH() + 0) % 360
        self.move_to(angle)

    def go_left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def go_right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def go_back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def go_up(self):
        if self.gamemode == 1:
            self.hero.setZ(self.hero.getZ() + 1)

    def go_down(self):
        if self.gamemode == 1:
            self.hero.setZ(self.hero.getZ() + -1)

    def turn_down(self):
        self.hero.setP(self.hero.getP() + 1)

    def turn_up(self):
        self.hero.setP(self.hero.getP() + -1)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.get_forward_coordinates(angle)
        if self.gamemode == 1:
            self.land.set_block(
                block=self.registry.get_block_by_id(self.block),
                position=pos
            )
        else:
            self.land.build_block(
                block=self.registry.get_block_by_id(self.block),
                position=pos
            )

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.get_forward_coordinates(angle)
        if self.gamemode == 1:
            self.land.remove_block(pos)
        else:
            self.land.destroy_block(pos)

    def enable_controls(self):
        base.accept(KEY_SWITCH_CAMERA, self.switch_camera)
        base.accept(KEY_SWITCH_GAMEMODE, self.switch_gamemode)
        base.accept(KEY_SWITCH_BLOCK, self.switch_block)

        base.accept(KEY_PLACE_BLOCK, self.build)
        base.accept(KEY_DESTROY_BLOCK, self.destroy)

        base.accept(KEY_TURN_LEFT, self.turn_left)
        base.accept(KEY_TURN_RIGHT, self.turn_right)

        base.accept(KEY_TURN_LEFT + "-repeat", self.turn_left)
        base.accept(KEY_TURN_RIGHT + "-repeat", self.turn_right)

        base.accept(KEY_FORWARD, self.go_forward)
        base.accept(KEY_LEFT, self.go_left)
        base.accept(KEY_RIGHT, self.go_right)
        base.accept(KEY_BACK, self.go_back)

        base.accept(KEY_FORWARD + "-repeat", self.go_forward)
        base.accept(KEY_LEFT + "-repeat", self.go_left)
        base.accept(KEY_RIGHT + "-repeat", self.go_right)
        base.accept(KEY_BACK + "-repeat", self.go_back)

        base.accept(KEY_SWITCH_GAMEMODE, self.switch_gamemode)

        base.accept(KEY_LOAD_MAP, self.land.load_map)
        base.accept(KEY_SAVE_MAP, self.land.save_map)

        base.accept(KEY_UP, self.go_up)
        base.accept(KEY_DOWN, self.go_down)

        base.accept(KEY_TURN_UP, self.turn_up)
        base.accept(KEY_TURN_DOWN, self.turn_down)
