import turtle, json, time, random , math

display = turtle.Screen()
display.screensize(500, 500)

user_keypresses = {
    'Up':0,
    'Down':0,
    'Left':0,
    'Right':0,
    'QUIT':0
}

user_ordered_keypresses = []

triangle_measures = {
    's1':None,
    's2':None,
    'hypo':None,
    'angle':None
}

user = turtle.Turtle()
user.shape('circle')
user.pensize(3)

nav_turtle = turtle.Turtle()
nav_turtle.penup()
nav_turtle.speed(0)
nav_turtle.goto(300, 300)

nav_text = turtle.Turtle()
nav_text.hideturtle()
nav_text.penup()
nav_text.speed(0)
nav_text.goto(280, 270)
nav_text.write('Heading') 


def forward():
    user.forward(10)
    user_keypresses['Up'] += 1
    user_ordered_keypresses.append('up arrow')

def backward():
    user.backward(10)
    user_keypresses['Down'] += 1
    user_ordered_keypresses.append('down arrow')

def left():
    user.left(10)
    nav_turtle.left(10)
    user_keypresses['Left'] += 1
    user_ordered_keypresses.append('left arrow')

def right():
    user.right(10)
    nav_turtle.right(10)
    user_keypresses['Right'] += 1
    user_ordered_keypresses.append('right arrow')

def get_turtle_pos(turtle):
    return turtle.pos()

def gen_ran_point():
    point = [random.randint(-75, 75) -250, random.randint(-75, 75) + 250]
    return point

def calculate():
    display.reset()
    user.shape('circle')
    user.pensize(3)

    nav_turtle.penup()
    nav_turtle.speed(0)
    nav_turtle.goto(300, 300)

    nav_text.hideturtle()
    nav_text.penup()
    nav_text.speed(0)
    nav_text.goto(280, 270)
    nav_text.write('Heading') 
    
    
    random_point = gen_ran_point()
    
    line_turtle = turtle.Turtle()
    line_turtle.speed(5)
    line_turtle.hideturtle()
    line_turtle.penup()
    line_turtle.goto(-250, 250)	
    line_turtle.pendown()
    line_turtle.goto(random_point[0], 250)
    line_turtle.goto(random_point[0], random_point[1])
    line_turtle.goto(-250, 250)

    triangle_measures['s1'] = abs(random_point[0] + 250)
    triangle_measures['s2'] = abs(random_point[1] - 250)
    triangle_measures['hypo'] = math.sqrt((triangle_measures['s1'] ** 2) + (triangle_measures['s2'] ** 2))

    print(math.degrees(math.atan(triangle_measures['s2'] / triangle_measures['s1'])))   

def terminate():
    global running
    running = False
    turtle.bye()

running = True
start_time= time.time()
while running:

    turtle.onkey(forward, 'Up')
    turtle.onkey(left, 'Left')
    turtle.onkey(backward, 'Down')
    turtle.onkey(right, 'Right')
    turtle.onkey(terminate, 'q')
    turtle.onkey(calculate, 'c')
    turtle.listen()

    if time.time() - start_time > 2:
        start_time = time.time()
        print('User Position: ', get_turtle_pos(user))
    
    display.update()

file = open('user_keypresses.json', 'w')
json.dump(user_keypresses, file, indent = 4)
file.close()

print('Keypress Order: ', user_ordered_keypresses)
print('User pressed', len(user_ordered_keypresses), 'keys')

