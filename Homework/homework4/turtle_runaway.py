# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import math
import random
import time
import tkinter as tk
import turtle

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, duration_seconds=60):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.duration_seconds = duration_seconds
        self.started_at = 0.0
        self.elapsed_seconds = 0.0
        self.is_running = False

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.started_at = time.monotonic()
        self.elapsed_seconds = 0.0
        self.is_running = True
        self._draw_status()
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if not self.is_running:
            return

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        self.elapsed_seconds = min(time.monotonic() - self.started_at, self.duration_seconds)
        if self.is_catched():
            self._finish('Caught! Game over.')
            return
        if self.elapsed_seconds >= self.duration_seconds:
            self._finish('Time is up! You escaped.')
            return

        self._draw_status()

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def _draw_status(self, message=''):
        remaining = math.ceil(max(0, self.duration_seconds - self.elapsed_seconds))
        score = int(self.elapsed_seconds)
        self.drawer.clear()
        self.drawer.goto(-320, 310)
        self.drawer.write(
            f'Time left: {remaining:02d}s   Score: {score}',
            align='left',
            font=('Arial', 14, 'bold'),
        )
        if message:
            self.drawer.goto(0, 0)
            self.drawer.write(message, align='center', font=('Arial', 22, 'bold'))

    def _finish(self, message):
        self.is_running = False
        self._draw_status(f'{message}  Final score: {int(self.elapsed_seconds)}')

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, _opp_pos, _opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, _opp_pos, _opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)


class ChaseMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=6, step_turn=12):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        lead_distance = min(
            self.step_move * 4,
            math.hypot(opp_pos[0] - self.xcor(), opp_pos[1] - self.ycor()) / 2,
        )
        target_pos = (
            opp_pos[0] + math.cos(math.radians(opp_heading)) * lead_distance,
            opp_pos[1] + math.sin(math.radians(opp_heading)) * lead_distance,
        )
        target_heading = self.towards(target_pos)
        heading_error = (target_heading - self.heading() + 180) % 360 - 180

        if heading_error > 0:
            self.left(min(heading_error, self.step_turn))
        elif heading_error < 0:
            self.right(min(-heading_error, self.step_turn))
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title('Turtle Runaway')
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    runner = ManualMover(screen)
    chaser = ChaseMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
