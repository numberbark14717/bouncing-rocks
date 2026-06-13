#pgzero
import pygame
import pgzrun
import random

WIDTH = 1024
HEIGHT = 512

#cannon
cannone = Actor('cannone',(512, 427))
hitbox_cannone = Actor("hitbox_cannone", (cannone.x + 0, cannone.y + 0))
   
#test cannon
cannone_prova = Actor("cannone_prova",(512,427))

#numbers
numero_1 = Actor("numero_1")
numero_2 = Actor("numero_2")
numero_3 = Actor("numero_3")
numero_4 = Actor("numero_4")
numero_5 = Actor("numero_5")
numero_6 = Actor("numero_6")
numero_7 = Actor("numero_7")
numero_8 = Actor("numero_8")
numero_9 = Actor("numero_9")
numero_0 = Actor("numero_0")

#rocks
#roccia_blu = Actor('roccia_blu')
#roccia_rossa = Actor("roccia_rossa")
#roccia_verde = Actor("roccia_verde")

#roccia_s = Actor("roccia_s")
#background
sfondo_caverna = pygame.image.load("images/sfondo_caverna.png")
hai_perso = Actor("hai_perso")
pausa_i = Actor("pausa")

TITLE = "Bouncing rocks" # Titolo della finestra di gioco
FPS = 70 # Numero di frame per secondo
ROCCE_TOTALI = 3
palle_cannone = []
rocce = []
cannone.x_iniziale = 512
mode = "gioco"
dueframe = 0


def inizio():
    
    global mode
    global palle_cannone
    global rocce
    global punteggio
    global danno
    global salute
    global salute_aggiuntiva
    global salute_mostrata
    global M_VU
    global M_VD
    
    hitbox_cannone.x = cannone.x_iniziale + 0
    punteggio = 0
    salute_aggiuntiva = 0
    salute_mostrata = 0
    M_VU = 2 + salute_aggiuntiva
    M_VD = 3 + salute_aggiuntiva
    danno = 1
    mode = "gioco"
    
    #Creazione rocce
    cannone.x = cannone.x_iniziale
    palle_cannone = []
    rocce = []
    for i in range(ROCCE_TOTALI):
    
        roccia = crea_roccia()
        #roccia.salute = random.randint(10, 20)
        #roccia.attack = random.randint(5, 10)
        rocce.append(roccia)

    

    palla_cannone = Actor("palla_cannone",(cannone.x, 437))
    palle_cannone.append(palla_cannone)

def crea_roccia(tipo="casuale", lato=0):
    global roccia
    global M_VU
    global M_VD
    global salute_mostrata
    
    
    salute_mostrata = (M_VU + M_VD) / 2

    
    
    if lato == 0:
        lato = random.randint(1, 2)
    altezza = random.randint(0, 160)
    
    if punteggio >= 50:
        salute = random.uniform(M_VU, M_VD)
        #print(salute, "= salute")
    else:
        salute = random.randint(2, 3)
    if tipo == "casuale":
        tipo = "roccia"
    
        rand = random.randint(1, 20)
        if rand <= 3:
            tipo = "roccia_rossa"
            
        elif rand >= 16:
            tipo = "roccia_verde_s"
            
        else:
            rand = random.randint(1, 2)
            if rand == 1:
                tipo = "roccia_s"
                

    roccia = Actor(tipo)
    roccia.tipo = tipo

    if lato == 2:
        roccia.x = random.randint(1150, 1250)
        
    elif lato == 1:
        roccia.x = random.randint(-226, -126)
        
    
# roccia.x = random.randint(24, 900)    
    roccia.y = altezza
    roccia.lato = lato
    roccia.y_partenza = altezza
    roccia.cade = 1
    roccia.cadem = roccia.cade
    roccia.salute = salute
    return roccia


def draw():
    global punteggio
    global salute
    global danno
    global salute_mostrata
    global M_VU
    global M_VD
    
    if mode == "pausa":
        pausa_i.draw()
        
        return


    elif mode == "sconfitta":
        hai_perso.draw()
        
        return
    
    # ottieni la dimensione attuale della finestra 
    w, h = screen.surface.get_size()               #ok
    # ridimensiona lo sfondo 
    sfondo_scalato = pygame.transform.scale(sfondo_caverna, (w, h))          #ok
    # disegna lo sfondo scalato 
    screen.blit(sfondo_scalato, (0, 0))           #ok

    
    #if mode == "gioco":
        
    for i in range(len(palle_cannone)):       
        palle_cannone[i].draw()                   #ok
        
    #palla_cannone.draw()           #ok
    hitbox_cannone.draw()
    cannone.draw()                 #ok
        
    #numero_1.draw()                #ok
        
    #numero_2.draw()               #ok
        
    #numero_3.draw()               #ok
        
    #numero_4.draw()                #ok
        
    #numero_5.draw()                #ok
        
    #numero_6.draw()               #ok
        
    #numero_7.draw()               #ok
    
    #numero_8.draw()               #ok
        
    #numero_9.draw()               #ok
        
    #numero_0.draw()               #ok
        
        
            
    #roccia_verde.draw()            #ok 
        
    #roccia_blu.draw()              #ok
        
    #roccia_rossa.draw()            #ok
        
        
    for i in range(len(rocce)):       
        rocce[i].draw()                   #ok
    #roccia_s.draw()                #ok
    
    screen.draw.text(str(punteggio), (20, 10), color="white")
    screen.draw.text(str(danno), (512, 10), color=(255, 198, 41))
    screen.draw.text(str(salute_mostrata), (940, 10), color= "red")

    screen.draw.text("score", (20, 472), color= "white")
    screen.draw.text("damage", (465, 472), color=(255, 198, 41))
    screen.draw.text("rock's health", (810, 472), color= "red")
    

    


def on_key_down(key):
    
    global mode
    global cadem
    global cade
    global y
    global ym
    
    if key == keys.P and mode == "gioco":
        
        mode = "pausa"  # alterna tra pausa e gioco
        
        for roccia in rocce:
            roccia.ym = roccia.y  # salva la posizione
            
            #print(roccia.cadem)
            #print(roccia.cade)
        
    elif key == keys.P and mode == "pausa":
        
        mode = "gioco"
        
        for roccia in rocce:
            roccia.y = roccia.ym  # ripristina la posizione
            roccia.cade = roccia.cadem




def update(df):
    global a
    global mode
    
    global dueframe
    global roccia
    global M_VU
    global M_VD
    global salute_mostrata
    
    salute_mostrata = (M_VU + M_VD) / 2


    for i in range(len(rocce)):
        if roccia.cade in (1, 3):
            roccia.cadem = roccia.cade
      

    
    
    if mode == "pausa":
        return  # esce subito, non aggiorna nulla
    
    
    
    
    elif mode == "gioco":
        #print(len(palle_cannone))
        if dueframe % 1 == 0:
            if len(palle_cannone) == 0:
                palla_cannone = Actor("palla_cannone",(cannone.x, 380))
                palle_cannone.append(palla_cannone)
            else:
                palla_cannone = palle_cannone[len(palle_cannone) - 1]
                if palla_cannone.y <= 285:
                    palla_cannone = Actor("palla_cannone",(cannone.x, 380))
                    palle_cannone.append(palla_cannone)
        
            for i in range(len(palle_cannone) - 1, -1, -1):
                palle_cannone[i].y = palle_cannone[i].y -8
                
                if palle_cannone[i].y <= 0:
                    palle_cannone.pop(i)
        
        dueframe += 1
    
        if keyboard.left and cannone.x > 51:
           # print("left")
            cannone.x = cannone.x - 5
            hitbox_cannone.x = hitbox_cannone.x - 5
        elif keyboard.right and cannone.x < 973:
            #print("right")
            cannone.x = cannone.x + 5
            hitbox_cannone.x = hitbox_cannone.x + 5
        
        #serve per il cannone di prova
            
        #if keyboard.left and cannone_prova.x > 51:
        #    cannone_prova.x = cannone_prova.x - 5
            
        #elif keyboard.right and cannone_prova.x < 973:
        #    cannone_prova.x = cannone_prova.x + 5
    
        #if roccia.x >= -100 or roccia.x <= 1124:
        
        #palla_cannone.y = palla_cannone.y - 5
        
        #QUESTO VALE PER IL PRIMO RMIBALZO 
        movimento()
        collisions()
        if len(rocce) < ROCCE_TOTALI:
            roccia = crea_roccia()
            rocce.append(roccia)

        for  i in range (len(rocce)):        
            if rocce[i].lato == 2:
                rocce[i].x = rocce[i].x - 3
            
            elif rocce[i].lato == 1:
               rocce[i].x = rocce[i].x + 3    
    elif mode == "sconfitta":
        if keyboard.space:
            mode = "gioco"
            inizio()
            
        
    #elif roccia.x <= -300:
        
    #    rocce.pop(i)
    #    roccia = crea_roccia()
    #    rocce.append(roccia)
        
def collisions():
    global mode
    global punteggio
    global danno
    global salute
    global M_VU
    global M_VD
    global salute_aggiuntiva

    #print(danno, "= danno")
    
    for i in range(len(rocce) -1, -1, -1):
        if hitbox_cannone.colliderect(rocce[i]):
            mode = "sconfitta"
        for j in range(len(palle_cannone) - 1, -1, -1):
            if rocce[i].colliderect(palle_cannone[j]):
                
                palle_cannone.pop(j)
                
                rocce[i].salute = rocce[i].salute - danno
                
        if rocce[i].salute <= 0:
            salute_aggiuntiva = random.randint(1, 2)
            M_VU = M_VU + salute_aggiuntiva
            M_VD = M_VD + salute_aggiuntiva
            #print("M_VU =", M_VU, "M_VD =", M_VD)
            valore = 5
            
            if rocce[i].tipo == "roccia_rossa":
                valore = 50
                
            elif rocce[i].tipo == "roccia_verde_s":
                #valore = 150
                dannop = random.randint(2, 5)
                danno = danno + dannop
                
            elif rocce[i].tipo == "roccia":
                
                roccia_destra = crea_roccia("roccia_s", 1)
                roccia_destra.x = rocce[i].x
                roccia_destra.y = rocce[i].y
                
                roccia_sinistra = crea_roccia("roccia_s", 2)
                roccia_sinistra.x = rocce[i].x
                roccia_sinistra.y = rocce[i].y
                
                rocce.append(roccia_destra)
                rocce.append(roccia_sinistra)
                
            rocce.pop(i)
            punteggio = punteggio + valore
            
            #roccia = crea_roccia()
            #rocce.append(roccia)
            
            
            


        

#def on_mouse_down(button):
    
inizio()

def movimento():
    global suolo
    global cadem
    global cade
    
    for i in range(len(rocce) -1, -1, -1):
        roccia = rocce[i]
        
        #make the decision of wich height the ground is for each rock
        roccia.suolo = 373
        if roccia.tipo == "roccia_s" or roccia.tipo == "roccia_verde_s":
            roccia.suolo = 435
            
        elif roccia.tipo == "roccia":
            roccia.suolo = 398
        
        
        if roccia.cade == 1:
            #print("giu", roccia.y)
            animate(roccia, tween='accelerate', duration=2, y = roccia.suolo)
            #roccia.y += 5
            roccia.cade = 2
            
        elif roccia.y >= roccia.suolo and roccia.cade == 2:
            roccia.cade = 3
            roccia.cadem = 3
            
        elif roccia.cade == 3:
            #print("su", roccia.y)
            animate(roccia, tween='decelerate', duration=2, y = roccia.y_partenza)
            #roccia.y -= 5
            roccia.cade = 2
            
        elif roccia.y <= roccia.y_partenza + 1 and roccia.cade == 2:
            roccia.cade = 1
            roccia.cadem = 1
            
        if roccia.x >= 1300 or roccia.x <= -300:
            
            rocce.pop(i)
            roccia = crea_roccia()
            rocce.append(roccia)
pgzrun.go()                    