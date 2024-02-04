from turtle import Turtle
import random


#색깔 엄청 많음 turtle 공식문서 참조
COLOR_LIST = ['light blue', 'royal blue',
              'light steel blue', 'steel blue',
              'light cyan', 'light sky blue',
              'violet', 'salmon', 'tomato',
              'sandy brown', 'purple', 'deep pink',
              'medium sea green', 'khaki']
# 몇번떄려야 깨지는 벽돌이니? 이 기능은 강화학습때 꺼야할수도있다.
weights = [1, 2, 1, 1, 3, 2, 1, 4, 1, 3,
           1, 1, 1, 4, 1, 3, 2, 2, 1, 2,
           1, 2, 1, 2, 1]

#각 벽돌에 대한 커스텀
class Brick(Turtle):
    def __init__(self, x_cor, y_cor):
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=3)
        self.color(random.choice(COLOR_LIST))
        self.goto(x=x_cor, y=y_cor)

        self.quantity = random.choice(weights)

        # 각 벽돌객체의 경계 좌표 설정해줌
        self.left_wall = self.xcor() - 30
        self.right_wall = self.xcor() + 30
        self.upper_wall = self.ycor() + 15
        self.bottom_wall = self.ycor() - 15



# 벽돌 그룹 정의
class Bricks:
    gap = 32
    def __init__(self):
        self.y_start = 0
        self.y_end = 240
        self.bricks = []
        self.create_all_lanes()

# 내가 정한 간격으로 배치 가능 사각형 배열 말고는.. 어려웡.. 나중에!
    # 위에 cls.gap = 32로 했음

    # 아래아래 create_lane에서 x축방향 쭉 이은 벽돌들을 y방향 appending!
    def create_all_lanes(self):
        for i in range(self.y_start, self.y_end, Bricks.gap):
            self.create_lane(i)

    def create_lane(self, y_cor):
        for i in range(-570, 570, 63):
            brick = Brick(i, y_cor)
            self.bricks.append(brick)
