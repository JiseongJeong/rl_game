class States():
    ball_pos_x: float = 0.0
    ball_pos_y: float = 0.0
    prev_ball_pos_x: float = 0.0
    prev_ball_pos_y: float = 0.0
    paddle_pos_x: float = 0.0
    bricks_left_count: float = 0
    total_bricks_hp: float = 0.0

    @classmethod
    def initializing(cls):
        cls.ball_pos_x: float = 0.0
        cls.ball_pos_y: float = 0.0
        cls.prev_ball_pos_x: float = 0.0
        cls.prev_ball_pos_y: float = 0.0
        cls.paddle_pos_x: float = 0.0
        cls.bricks_left_count: int = 0
        cls.total_bricks_hp: int = 0
    @classmethod
    def get_ball_direction(cls) -> tuple:
        __ball_displacement_x = cls.prev_ball_pos_x - cls.ball_pos_x
        __ball_displacement_y = cls.prev_ball_pos_y - cls.ball_pos_y
        _ball_pos_x_norm = __ball_displacement_x / (__ball_displacement_y^2 + __ball_displacement_x^2)^(1/2)
        _ball_pos_y_norm = __ball_displacement_y / (__ball_displacement_y^2 + __ball_displacement_x^2)^(1/2)
        return _ball_pos_x_norm, _ball_pos_y_norm

