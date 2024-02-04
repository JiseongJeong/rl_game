import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
import time

#----
game_speed: float = 0.02   # 겜속도 0.01~0.02 추천


# 게임창 객체 생성 및 사이즈/ 배경색 조절 가능
screen = tr.Screen()
screen.setup(width=1200, height=600)
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0.1)

paddle = Paddle()
bricks = Bricks()
ball = Ball()


#게임 진행(iteration) 지속에 대한 flag값임, 추후 gameover 보상 값계싼에 참여시켜ㅑ볼까?
playing_game = True


screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)


# 모듈화 해줘야 더 멋있음(utils.py) : check_collision_with_walls / check_collision_with_paddle / check_collision_with_bricks
# 현재는 논리순 sudo코드 상의 순서와 계층대로만 ㄱㄱ
def check_collision_with_walls():

    # 모듈화하면서 얘네는 class variables로 바꿔주자.지금은 귀찮
	global ball, score, playing_game, ui

# 게임창 양쪽 벽에 부딛혔나?
	if ball.xcor() < -580 or ball.xcor() > 570:
		ball.bounce(x_bounce=True, y_bounce=False)
		return None

	# 게임창 윗쪽 벽에 부딛혔나?
	if ball.ycor() > 270:
		ball.bounce(x_bounce=False, y_bounce=True)
		return None

		# 게임창 바닥에 떨어졌나? 그럼 겜 오바
		# 향후 강화학습 태우기 위해 게임오버 신호값따야하는 포인트 <chkpt1>
	if ball.ycor() < -280:
		ball.reset()
		return None
		#return boolean 해서 게임오버 플레그 만들수있을듯



# 패들에 부딛혔나?
def check_collision_with_paddle():
	global ball, paddle
	# 패들/공의 x축변위
	paddle_x = paddle.xcor()
	ball_x = ball.xcor()

	# 공(중심에서)부터 패들까지의 거리가 110 이하 이고
    # 공의 y 변위가 -250 (bottom이면)   ** 공 두께 함께 고려 필수

	if ball.distance(paddle) < 110 and ball.ycor() < -250:

		# 패들 의 좌표가 중심(0) 우측일때와 좌측일때를 구분. 이부분 더 깔끔화 가능할듯 <chkpt2>
		if paddle_x > 0:
            # 패들의 좌측에 공이 맞으면 공이 좌측으로 팅겨져 나간다. 원래 이게 맞던가?
			if ball_x > paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
            # 패들의 우측에 공이 맞으면 공이 우측으로 ㅗ팅김
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# 패들 의 좌표가 중심(0) 우측일때와 좌측일때를 구분. 이부분 더 깔끔화 가능할듯
		elif paddle_x < 0:
			if ball_x < paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# 완전히 중간에 있을 떄 예외조건 일단 추가.... 혹시몰라. 동일하게 패들의 우측맞았냐 좌측 맞았냐임.
		else:
			if ball_x > paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			elif ball_x < paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
            # 단, 패들도 정확히 중간에, 공도 패들의 정확히 중간에 꽂혔을 경우에는 x축방향으로 방향전환 튕김이 없음으로 일단 정함
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

# idea : 패들 상판 마찰력이 0라고 가정하고, x축 방향 변위는 일어나지 않음연 안되나? 안되겠네 ㅇㅋㅇㅋ 그럼 유저가 결정할 수 있는게 없음

def check_collision_with_bricks():
	global ball, bricks

    # 벽돌 싹 돌면서 공과의 거리 체크...
	for brick in bricks.bricks:
        # 공과 벽돌의 거리가 40 미만일떄 = 충돌
		if ball.distance(brick) < 40:
			brick.quantity -= 1
			if brick.quantity == 0:
				brick.clear()
				brick.goto(3000, 3000)  #임시
				bricks.bricks.remove(brick)

			# 좌측 부딪
			if ball.xcor() < brick.left_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# 우측 부딪
			elif ball.xcor() > brick.right_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# 하단 부딪
			elif ball.ycor() < brick.bottom_wall:
				ball.bounce(x_bounce=False, y_bounce=True)

			# 상단 부딛
			elif ball.ycor() > brick.upper_wall:
				ball.bounce(x_bounce=False, y_bounce=True)


if __name__ == '__main__' :
	# 게임 실행 무한루프. GAME OVER시 까지
	# playing_game = True
	iteration_cnt = 0

	while playing_game:

		#디버깅 편하게 하기위해 일단 추가
		iteration_cnt += 1

		#터틀.화면새로고침기능()
		screen.update()
		#겜속도 조절가능(0.01~0.02) 적절해보임
		time.sleep(game_speed)

		#main.py 에서 정의한 3개 매쏟(check~)

		ball.move()

		# playing_game = check_collision_with_walls()
		check_collision_with_walls()

		check_collision_with_paddle()

		check_collision_with_bricks()
		# if iteration_cnt > 100:
		# 	break
	tr.mainloop()


else:
	raise exception('알 수 없는 접근')
