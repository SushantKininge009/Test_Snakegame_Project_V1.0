import turtle
import time
import random

delay = 0.1

# Score
score = 0
high_score = 0

# Screen setup
wn = turtle.Screen()
wn.title("Infinite Snake Game")
wn.bgcolor("#2E8B57")  # A darker, 'SeaGreen' background
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off screen updates for smoother animation

# Snake head
head = turtle.Turtle()
head.speed(0)  # Animation speed, not movement speed
head.shape("square")
head.color("#00008B")  # DarkBlue
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle") # You can try "triangle" or "classic" (arrow)
food.color("yellow")
food.penup()
food.goto(0, 100)

segments = []

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Arial", 22, "bold"))

# Game Over Pen
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.shape("square")
game_over_pen.color("white")
game_over_pen.penup()
game_over_pen.hideturtle()


# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def touch_control(x, y):
    """Change direction based on tap location."""
    # Get center of the screen
    center_x, center_y = 0, 0
    # Divide screen into 4 regions
    if abs(x) > abs(y):
        if x > 0:
            go_right()
        else:
            go_left()
    else:
        if y > 0:
            go_up()
        else:
            go_down()

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def show_game_over():
    """Displays the Game Over message."""
    game_over_pen.goto(0,0) # Centered
    game_over_pen.write("GAME OVER!", align="center", font=("Arial", 30, "bold"))
    wn.update() # Ensure message is shown immediately
    time.sleep(2) # Pause for 2 seconds
    game_over_pen.clear() # Clear the message

def reset_game():
    """Resets the game state after game over."""
    global score, delay, segments # Declare as global to modify them
    
    time.sleep(0.5) # Brief pause before full reset
    head.goto(0, 0)
    head.direction = "stop"

    # Hide the segments
    for segment in segments:
        segment.goto(1000, 1000)  # Move them off-screen

    segments.clear()
    score = 0
    delay = 0.1  # Reset delay

    # Update the score display
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 22, "bold"))
    
    # Move food to a new random spot
    x = random.randint(-280, 280)
    y = random.randint(-280, 280)
    food.goto(x,y)


# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
# For W, A, S, D controls as well
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Touch controls
wn.onscreenclick(touch_control)


# Main game loop
while True:
    wn.update()

    # Wall wrap-around logic
    if head.xcor() > 290:
        head.setx(-290)
    elif head.xcor() < -290:
        head.setx(290)
    
    if head.ycor() > 290:
        head.sety(-290)
    elif head.ycor() < -290:
        head.sety(290)

    # Check for collision with food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#ADD8E6")  # LightBlue for segments
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay to make game faster
        delay -= 0.001
        if delay < 0.03: # Set a minimum delay
            delay = 0.03

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 22, "bold"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move() # Move the snake head

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            show_game_over()
            reset_game()
            # No need to break, reset_game handles clearing segments

    time.sleep(delay)

wn.mainloop()
