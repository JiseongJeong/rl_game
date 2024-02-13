from turtle import Turtle


#일종의 속도임 1iter당 몇 tic?
MOVE_DIST = 5


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('white')
        self.penup()
        self.x_move_dist = MOVE_DIST
        self.y_move_dist = MOVE_DIST
        self.reset()

    def move(self):
        new_y = self.ycor() + self.y_move_dist
        new_x = self.xcor() + self.x_move_dist
        self.goto(x=new_x, y=new_y)

    def bounce(self, x_bounce, y_bounce):
        if x_bounce:
            # x방향 방향전환
            self.x_move_dist *= -1

        if y_bounce:
            # y출방향 전환
            self.y_move_dist *= -1

    def reset(self):
        # 초기 시작점과 그 방향, 거리(사실상 속도)
        # randomize해주면 좋을듯.
        self.goto(x=0, y=-240)
        self.y_move_dist = 10