from turtle import *
from lettres import *
import time

up()
speed(100)
setup(1450,850,0,0)
ht()
"""
goto(-500,-10)
down()
goto(5000,-10)
up()
goto(-500,30)
down()
goto(500,30)
up()
goto(-500,20)
down()
goto(500,20)
up()
"""

def un(vx,vy,multi=40):
    multi=multi/40
    goto(vx+10*multi,vy)
    down()
    goto(vx+10*multi,vy+40*multi)
    goto(vx,vy+20*multi)
    up()
    return 10*multi+5

def deux(vx,vy,multi=40):
    multi=multi/40
    goto(vx+20*multi,vy)
    down()
    setheading(0)
    backward(int(20*multi))
    setheading(40)
    goto(vx+int(16*multi),vy+int(22*multi))
    circle(int(10*multi),270)
    up()
    return 20*multi+5

def trois(vx,vy,multi=40):
    multi=multi/40
    goto(vx+10*multi,vy+20*multi)
    setheading(0)
    down()
    circle(10*multi,270)
    up()
    goto(vx,vy+10*multi)
    setheading(270)
    down()
    circle(10*multi,270)
    up()
    return 20*multi+5

def quatre(vx,vy,multi=40):
    multi=multi/40
    goto(vx+15*multi,vy)
    down()
    goto(vx+15*multi,vy+20*multi)
    up()
    goto(vx+15*multi,vy+40*multi)
    down()
    goto(vx,vy+10*multi)
    goto(vx+20*multi,vy+10*multi)
    up()
    return 20*multi+5
    
def cinq(vx,vy,multi=40):
    multi=multi/40
    goto(vx+int(18*multi),vy+int(40*multi))
    setheading(180)
    down()
    forward(int(18*multi))
    left(90)
    forward(int(15*multi))
    up()
    goto(vx,vy)
    down()
    setheading(339)
    circle(13.5*multi,220)
    up()
    return 20*multi+5
    
    
def six(vx,vy,multi=40):
    multi=multi/40
    goto(vx,vy+int(10*multi))
    down()
    setheading(270)
    circle(int(10*multi))
    backward(int(20*multi))
    circle(int(10*multi),-145)
    up()
    return 20*multi+5
    
def sept(vx,vy,multi=40):
    multi=multi/40
    goto(vx,vy+int(40*multi))
    down()
    goto(vx+int(20*multi),vy+int(40*multi))
    goto(vx,vy)
    up()
    return 20*multi+5

def huit(vx,vy,multi=40):
    multi=multi/40
    setheading(90)
    for vi in range (10,31,20):
        goto(vx+20*multi,vy+vi*multi)
        down()
        circle(10*multi)
        up()
    return 20*multi+5

def neuf(vx,vy,multi=40):
    multi=multi/40
    goto(vx+int(20*multi),vy+int(30*multi))
    setheading(90)
    down()
    circle(int(10*multi))
    goto(vx+int(20*multi),vy+int(10*multi))
    circle(int(10*multi),-150)
    up()
    return 20*multi+5

def zero(vx,vy,multi=40):
    multi=multi/40
    goto(vx+20*multi,vy+30*multi)
    setheading(90)
    down()
    circle(10*multi,180)
    goto(vx,vy+10*multi)
    circle(10*multi,180)
    goto(vx+20*multi,vy+30*multi)
    up()
    return 20*multi+5
    #Tracer un trait en diagonale afin de le distinquer de O / 0

def degré(vx,vy,multi=40):
    multi=multi/40
    goto(vx+5*multi,vy+multi*30)
    down()
    circle(5*multi)
    up()
    return 10*multi+5
    
def tiret(vx,vy,taille=40):
    goto(vx,vy+20*taille/40)
    down()
    goto(vx+20*taille/40,vy+20*taille/40)
    up()
    return 20*taille/40+5

def copyrights(vx,vy,taille=40):
    setheading(0)
    multi=taille/30
    vx+=10
    goto(vx,vy)
    down()
    circle(10*multi)
    up()
    goto(vx+4*multi,vy+12*multi)
    down()
    setheading(90)
    circle(4*multi,180)
    goto(vx-4*multi,vy+7*multi)
    circle(4*multi,180)
    up()
    return 20*multi+5

def apostrophe(vx,vy,multi=40):
    multi/=40
    goto(vx+5*multi,vy+40*multi)
    down()
    goto(vx,vy+25*multi)
    up()
    return 6

def barre_oblique(vx=0,vy=0,multi=40):
    multi/=40
    goto(vx,vy)
    down()
    goto(vx+15*multi,vy+40*multi)
    up()
    return 20*multi+5

def point(vx=0, vy=0, multi=40):
    goto(vx,vy)
    down()
    dot(2)
    up()
    return 10*multi/40
    
def deux_points(vx=0,vy=0, multi=40):
    point(vx,vy)
    point(vx,vy+20*multi/40)
    return 5*multi/40

def taille_phrase(phrase="", multi=40):
    taille=0.0
    caractères_fins={"1":10, "°":10, "'":1, ".":10, ":":5,"c":17, "i":1, "j":5, "k":10, "l":1, "r":10, "s":10, "t":15, "v":10, "w":10, "x":10,"z":10}
    for element in phrase:
        if element==" ":
            taille+=10*multi/40
        else:
            try:
                taille+=caractères_fins[element]*multi/40+5
            except KeyError:
                taille+=20*multi/40+5
    return taille 
# Penser à faire varier la taille du bordel quand j'aurais du temps à perdre.    
# Penser à faire la même avec des minuscules. Ça peut être long, je sais

def écriture(vx=0,vy=0,phrase="",multi=40, centrage=False, changeur_de_multi=()):
    caractères_spéciaux={"0":"zero", "1":"un", "2":"deux", "3":"trois", "4":"quatre", "5":"cinq", "6":"six", "7":"sept", "8":"huit", "9":"neuf", "°":"degré", "C":"C", "-":"tiret", "©":"copyrights", "'":"apostrophe", "/":"barre_oblique", ".":"point", ":":"deux_points"}
    if centrage==False:
        x_mod=vx-taille_phrase(phrase)/2
        #x_mod=vx-int(((len(phrase)+2)*(20*multi/40)+(len(phrase)+2)*5)/2) # Centrage des chiffres
    else:
        x_mod=vx
    for vi in range(len(phrase)):
        if len(changeur_de_multi)!=0 and changeur_de_multi[0]==vi:
            multi=changeur_de_multi[1]
        setheading(0)
        if phrase[vi] in "1234567890-°©/'./:":
            x_mod+=globals()[caractères_spéciaux[phrase[vi]]](x_mod,vy,multi)
        elif phrase[vi]!=" " and phrase[vi] not in "}?,;+=)!({":
            x_mod+=globals()[phrase[vi]](x_mod,vy,multi)
        else:
            x_mod+=10*(multi/40)
            

"""
écriture(0,50,"abcdefghijklmnopqrstuvwxyz".upper(),30)
écriture(0,0,"abcdefghijklmnopqrstuvwxyz",30)
écriture(0,-60,"1234567890-°©'/.:",30)
écriture(0,0,"L'anglais : c'est de la merde.", 30)
time.sleep(15)
"""
