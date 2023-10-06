import turtle
import time
import random
import math
import winsound
import json


# we create the screen
win = turtle.Screen()
win.title("It's All About Rotating")




def main_menu(win : turtle):
    win.clear()
    global gaming , calculate_time_calcul
    gaming = True
    calculate_time_calcul = True
    load_best_score()
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()

    win.setup(width=800, height=700)
    win.tracer(0)
    win.bgcolor("black")

    # Draw game title (ASCII art)
    title_ascii = """
     ___ _   _          _    _ _           
    |_ _| |_( )___     / \  | | |          
     | || __|// __|   / _ \ | | |          
     | || |_  \__ \  / ___ \| | |          
    |___|\__|_|___/ /_/   \_\_|_|          
      / \  | |__   ___  _   _| |_         
     / _ \ | '_ \ / _ \| | | | __|        
    / ___ \| |_) | (_) | |_| | |_         
 _ /_/__ \_\_.__/ \___/ \__,_|\__|        
|  _ \ ___ | |_ __ _| |_(_)_ __   __ _ 
| |_) / _ \| __/ _` | __| | '_ \ / _` |
|  _ < (_) | || (_| | |_| | | | | (_| |
|_| \_\___/ \__\__,_|\__|_|_| |_|\__, |
                                 |___/   """
    text.penup()
    text.goto(30,20 )
    text.pendown()
    text.color("white")
    text.write(title_ascii, align="center", font=("Courier", 16, "normal"))

    instructions = [
        "Choose the mode that you want to play:",
        "",
        "",
        "A - Mode One: Racing Time",
        "",
        "B - Mode Two: Playing Till I Get Bored",
        "",
        "",
        "",
        "Press A or B , you can press X for exit"
    ]


    y_offset = -50
    for line in instructions:
        text.penup()
        text.goto(0, y_offset)
        text.pendown()
        text.write(line, align="center", font=("Courier", 20, "normal"))
        y_offset -= 30
    win.listen()
    win.onkeypress(explain01,"a")
    win.onkeypress(explain02,"b")
    win.onkeypress(game_end,"x")
    turtle.done()






def di_circle():
    draw = turtle.Turtle()
    draw.color("blue")
    draw.hideturtle()
    draw.speed(0)
    draw.penup() 
    draw.goto(0, -150)  
    draw.pendown()
    draw.circle(150)



def points_generator() -> turtle:
    def point_creat(x : int,y : int) -> turtle:
        point = turtle.Turtle()
        point.penup()
        point.speed(0)
        point.shape("circle")
        point.color("green")
        point.goto(x,y)
        return point
    x = random.randint(-150,150)
    y = math.sqrt(150*150 - x*x)
    y = random.choice([-y, y])
    return point_creat(x,y)


def bomb_generator(p : turtle):
    b = points_generator()
    if not (b.xcor() != p.xcor() and b.ycor() != p.ycor()) or (b.xcor() == -p.xcor() and b.ycor() == -p.ycor()) :
        b.hideturtle()
        b = bomb_generator(p)
    if math.dist((b.xcor(), b.ycor()), (p.xcor(), p.ycor())) < 70 :
        b.hideturtle()
        b = bomb_generator(p)
    if math.dist((b.xcor(), b.ycor()), (-p.xcor(), -p.ycor())) < 95:
        b.hideturtle()
        b = bomb_generator(p)
    b.color("red")
    return b




tetta = 1
def rotating(rakas):
    rakas.setheading(rakas.heading() + tetta)

tetta_2 = 1.8
def rotating_2(rakas):
    rakas.setheading(rakas.heading() + tetta_2)


def is_countable(rakas : turtle, p : turtle) -> bool :
    angle_threshold = 10  # Set an angle threshold for considering facing
    angle = rakas.towards(p)
    heading = rakas.heading()
    if heading < 0 :
        heading = 360 + heading
    return abs(angle - heading) < angle_threshold or abs(angle - heading) > 180 - angle_threshold




def save_best_score():
    global best_score_1, best_score_2 , time_2 , score_mixed
    score_mixed = {"score1": best_score_1, "score2": best_score_2 , "time2": time_2}
    with open("score.json", "w") as file:
        json.dump(score_mixed, file)



def load_best_score():
    global best_score_1, best_score_2, time_2
    try:
        with open("score.json", "r") as file:
            scores = json.load(file)
            best_score_1 = scores["score1"]
            best_score_2 = scores["score2"]
            time_2 = scores["time2"]
    except FileNotFoundError:
        best_score_1, best_score_2 , time_2 = (0, 0 , 0)






score_1 = 0
def game_core_1():
    global tetta
    global score_1
    global rakas
    global bomb
    global point
    global score_bar
    tetta *= -1
    
    if is_countable(rakas,point) :
        winsound.PlaySound("powerUp.wav",winsound.SND_ASYNC)
        score_1 += 1
        score_bar.clear()
        score_bar.write(f"Score : {score_1}   Best Score : {best_score_1}", align="center", font=("Courier", 20, "normal"))
        point.hideturtle()
        point = points_generator()
        if score_1 == 5 :
            bomb = bomb_generator(point)
        if score_1 > 5 :
            bomb.hideturtle()
            bomb = bomb_generator(point)
        if -2.5 < tetta < 0:
            tetta -= 0.2
        elif 0 < tetta < 2.5 :
            tetta += 0.2
    elif score_1 > 5 and is_countable(rakas,bomb) :
        winsound.PlaySound("hitHurt.wav",winsound.SND_ASYNC)
        point.hideturtle()
        point = points_generator()
        bomb.hideturtle()
        bomb = bomb_generator(point)
        if  tetta < 0  :
            if tetta + 0.5 <= -1 :
                tetta += 0.5
            else :
                tetta = -1
        elif tetta > 0 :
            if tetta - 0.5 >= 1 :
                tetta -= 0.5
            else :
                tetta = 1
    


score_2 = 0
def game_core_2():
    global tetta_2
    global score_2
    global rakas
    global bomb
    global point
    global score_bar
    tetta_2 *= -1
    
    if is_countable(rakas,point) :
        winsound.PlaySound("powerUp.wav",winsound.SND_ASYNC)
        score_2 += 1
        score_bar.clear()
        score_bar.write(f"Score : {score_2}   Best Score : {best_score_2}\n            in : {time_2} Seconds", align="center", font=("Courier", 20, "normal"))
        point.hideturtle()
        point = points_generator()
        if score_2 == 5 :
            bomb = bomb_generator(point)
        if score_2 > 5 :
            bomb.hideturtle()
            bomb = bomb_generator(point)

    elif score_2 > 5 and is_countable(rakas,bomb) :
        winsound.PlaySound("hitHurt.wav",winsound.SND_ASYNC)
        score_2 -= 1
        score_bar.clear()
        score_bar.write(f"Score : {score_2}   Best Score : {best_score_2}\n            in : {time_2} Seconds", align="center", font=("Courier", 20, "normal"))
        point.hideturtle()
        point = points_generator()
        bomb.hideturtle()
        if score_2 > 5 :  
            bomb = bomb_generator(point)





#creating score bar
def score_bar_creator() :
    score_bar = turtle.Turtle()
    score_bar.penup()
    score_bar.goto(0,225)
    score_bar.color("white")
    score_bar.speed(0)
    score_bar.hideturtle()
    score_bar.write(f"Score : 0   Best Score : {best_score_1}", align="center", font=("Courier", 20, "normal"))
    return score_bar



def score_bar_creator_2() :
    score_bar = turtle.Turtle()
    score_bar.penup()
    score_bar.goto(0,225)
    score_bar.color("white")
    score_bar.speed(0)
    score_bar.hideturtle()
    score_bar.write(f"Score : 0   Best Score : {best_score_2}\n            in : {time_2} Seconds", align="center", font=("Courier", 20, "normal"))
    return score_bar




score_bar = None
def game_loop(rakas : turtle , win : turtle) :
    load_best_score()
    di_circle()
    global score_bar , gaming , current_time , max
    score_bar = score_bar_creator()
    while gaming:  # temporary
        win.update()
        rotating(rakas)
        time.sleep(0.004)
        if max - current_time < 0 :
            lost_menu_1()


def game_loop_2(rakas : turtle , win : turtle) :
    load_best_score()
    di_circle()
    global score_bar , gaming , current_time
    score_bar = score_bar_creator_2()
    while gaming:  # temporary
        win.update()
        rotating_2(rakas)
        time.sleep(0.004)







calculate_time_calcul = True
def the_time_1(x = 0,y = -260 , t = 1) :
    global timer , current_time , calculate_time_calcul , max
    max = 60 #related to this mode
    timer = turtle.Turtle()
    timer.penup()
    timer.goto(x,y)
    timer.color("white")
    timer.speed(0)
    timer.hideturtle()
    current_time = -1


    def time_printer():
        global current_time
        global timer
        timer.clear()
        timer.write(f"time : {max - current_time}", align="center", font=("Courier", 20, "normal"))#related
    time_printer()
    def time_calcule() :
        global timer
        global current_time ,calculate_time_calcul
        current_time += t

        time_printer()
        if calculate_time_calcul :
            win.ontimer(lambda: time_calcule(), 1000)
        else : 
            timer.clear()
    time_calcule()

def the_time_2(x = 0,y = -260 , t = 1) :
    global timer , current_time , calculate_time_calcul , max
    timer = turtle.Turtle()
    timer.penup()
    timer.goto(x,y)
    timer.color("white")
    timer.speed(0)
    timer.hideturtle()
    current_time = -1


    def time_printer():
        global current_time
        global timer
        timer.clear()
        timer.write(f"time : {current_time}", align="center", font=("Courier", 20, "normal"))
    time_printer()
    def time_calcule() :
        global timer
        global current_time ,calculate_time_calcul
        current_time += t

        time_printer()
        if calculate_time_calcul :
            win.ontimer(lambda: time_calcule(), 1000)
        else : 
            timer.clear()
    time_calcule()





def lost_menu_1():
    global score_1 , win ,calculate_time_calcul , gaming , best_score_1,tetta

    tetta = 1

    temp = score_1
    if score_1 > best_score_1 :
        best_score_1 = score_1
    save_best_score()
    score_1 = 0


    calculate_time_calcul = False
    gaming = False
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()

    win.clear()
    win.setup(width=800, height=450)
    win.tracer(0)
    win.bgcolor("black")

    # Draw game title (ASCII art)
    title_ascii = """
  ____                         ___                 
 / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __ 
| |  _ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__|
| |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |   
 \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|   """
    text.penup()
    text.goto(5,105 )
    text.pendown()
    text.color("white")
    text.write(title_ascii, align="center", font=("Courier", 16, "normal"))

    instructions = [
        f"Your Score is : {temp}",
        "",
        "",
        "",
        "",
        "",
        "Press X to Save and exit",
        "",
        "Press M to go back to menu"
    ]


    y_offset = -20
    for line in instructions:
        text.penup()
        text.goto(0, y_offset)
        text.pendown()
        text.write(line, align="center", font=("Courier", 20, "normal"))
        y_offset -= 20
    win.listen()
    win.onkeypress(lambda: main_menu(win),"m")
    win.onkeypress(game_end,"x")
    turtle.done()




def lost_menu_2():
    global score_2 , win ,calculate_time_calcul , gaming , best_score_2 ,current_time,time_2

    temp = score_2
    temp2 = current_time
    if score_2 > best_score_2 :
        best_score_2 = score_2
        time_2 = current_time
        
    save_best_score()
    score_2 = 0
    current_time = -1

    calculate_time_calcul = False
    gaming = False
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()

    win.clear()
    win.setup(width=800, height=450)
    win.tracer(0)
    win.bgcolor("black")

    # Draw game title (ASCII art)
    title_ascii = """
  ____                         ___                 
 / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __ 
| |  _ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__|
| |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |   
 \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|   """
    text.penup()
    text.goto(5,105 )
    text.pendown()
    text.color("white")
    text.write(title_ascii, align="center", font=("Courier", 16, "normal"))

    instructions = [
        f"Your Score is : {temp} in The Time Of : {temp2} Seconds",
        "",
        "",
        "",
        "",
        "",
        "Press X to Save and exit",
        "",
        "Press M to go back to menu"
    ]


    y_offset = -20
    for line in instructions:
        text.penup()
        text.goto(0, y_offset)
        text.pendown()
        text.write(line, align="center", font=("Courier", 20, "normal"))
        y_offset -= 20
    win.listen()
    win.onkeypress(lambda: main_menu(win),"m")
    win.onkeypress(game_end,"x")
    turtle.done()










def game_end():
    global score_1,best_score_2,best_score_1,score_2
    if score_1 > best_score_1 :
        best_score_1 = score_1
    if score_2 > best_score_2 :
        best_score_2 = score_2
    save_best_score()
    turtle.bye()




def run_1():
    global win
    win.setup(width=500, height=600)
    win.clear()
    win.tracer(0)
    win.bgcolor("black")
    global rakas
    rakas = turtle.Turtle()
    rakas.penup()
    rakas.color("white")
    rakas.shape("square")
    rakas.shapesize(stretch_wid=1, stretch_len=10.5)
    rakas.speed(0)
    win.listen()
    win.onkeypress(game_core_1, "space")
    win.onkeypress(lost_menu_1, "x")

    the_time_1()

    global point 
    point = points_generator()
    global bomb
    bomb = None
    game_loop(rakas,win)



def run_2():
    global win
    win.setup(width=500, height=600)
    win.clear()
    win.tracer(0)
    win.bgcolor("black")
    global rakas
    rakas = turtle.Turtle()
    rakas.penup()
    rakas.color("white")
    rakas.shape("square")
    rakas.shapesize(stretch_wid=1, stretch_len=10.5)
    rakas.speed(0)
    win.listen()
    win.onkeypress(game_core_2, "space")
    win.onkeypress(lost_menu_2, "x")

    the_time_2()

    global point 
    point = points_generator()
    global bomb
    bomb = None
    game_loop_2(rakas,win)







def explain01():
    global win
    win.clear()
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()

    win.setup(width=1000, height=500)
    win.tracer(0)
    win.bgcolor("black")

    text.color("white")
    instructions = [
        "In this mode the objective is to collect as much points as you can",
        "",
        "",
        "The points will spawn in green , ",
        "",
        "Press the space bar whenever you face it to collect it ",
        "",
        "collecting points will increase your speed.",
        "",
        " but watch out ,",
        "",
        "some bombs will spawn in red",
        "",
        "and if you hit them you will lose a part of your speed",
        "",
        "",
        "",
        "",
        "You can press X in mid game whenever you want to exit ",
        "",
        "Press enter to continue"
    ]


    y_offset = 215
    for line in instructions:
        text.penup()
        text.goto(0, y_offset)
        text.pendown()
        text.write(line, align="center", font=("Courier", 17, "normal"))
        y_offset -= 22
    win.listen()
    win.onkeypress(run_1,"Return")
    turtle.done()




def explain02():
    global win
    win.clear()
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()

    win.setup(width=1000, height=500)
    win.tracer(0)
    win.bgcolor("black")

    text.color("white")
    instructions = [
        "In this mode the objective is to collect the green points",
        "",
        "",
        "The points will spawn randomly around you",
        "",
        "Press the space bar whenever you face it to collect it ",
        "",
        "Collecting points will increase your score.",
        "",
        " But watch out ,",
        "",
        "Some bombs will spawn in red",
        "",
        "and if you hit them youre score will dicrease.",
        "",
        "",
        "",
        "",
        "You can press X in mid game whenever you want to exit ",
        "",
        "Press enter to continue"
    ]


    y_offset = 215
    for line in instructions:
        text.penup()
        text.goto(0, y_offset)
        text.pendown()
        text.write(line, align="center", font=("Courier", 17, "normal"))
        y_offset -= 22
    win.listen()
    win.onkeypress(run_2,"Return")
    turtle.done()








main_menu(win)



