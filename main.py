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

#buttons
play = Actor("play_button")
play.pos = (WIDTH // 2, HEIGHT // 2 - 50)
play_h = Actor("play_button_h")
play_h.pos = (WIDTH // 2, HEIGHT // 2 - 50)
options = Actor("options_button")
options.pos = (WIDTH // 2, HEIGHT // 2 + 25)
options_h = Actor("options_button_h")
options_h.pos = (WIDTH // 2, HEIGHT // 2 + 25)
exit = Actor("exit_button")
exit.pos = (WIDTH // 2, HEIGHT // 2 + 175)
exit_h = Actor("exit_button_h")
exit_h.pos = (WIDTH // 2, HEIGHT // 2 + 175)

#rocks
#roccia_blu = Actor('roccia_blu')
#roccia_rossa = Actor("roccia_rossa")
#roccia_verde = Actor("roccia_verde")
#roccia_s = Actor("roccia_s")

#background
sfondo_caverna = pygame.image.load("images/sfondo_caverna.png")
hai_perso = Actor("hai_perso")
hai_perso.pos = (WIDTH // 2, HEIGHT // 2)
pausa_i = Actor("pausa")
pausa_i.pos = (WIDTH // 2, HEIGHT // 2)

TITLE = "Bouncing rocks" # Titolo della finestra di gioco
FPS = 70 # Numero di frame per secondo
ROCCE_TOTALI = 3
inizio = "menu"
palle_cannone = []
rocce = []
rocce_menu = []
cannone.x_iniziale = 512
mode = inizio
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
    velocità = random.uniform(2, 5)
    
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
    roccia.velocità = velocità
    return roccia


def crea_roccia_menu():
    tipo = "roccia"
    rand = random.randint(1, 20)
    if rand <= 3:
        tipo = "roccia_rossa"
    elif rand >= 16:
        tipo = "roccia_verde_s"
    else:
        if random.randint(1, 2) == 1:
            tipo = "roccia_s"

    r = Actor(tipo)

    lato = random.randint(1, 2)

    if lato == 1:
        r.x = random.randint(-226, -126)
    else:
        r.x = random.randint(1150, 1250)

    r.y = random.randint(0, 160)
    r.lato = lato
    r.vel = random.uniform(2, 5)

    r.y_partenza = r.y
    r.suolo = 398
    if tipo in ("roccia_s", "roccia_verde_s"):
        r.suolo = 435
    elif tipo == "roccia_rossa":
        r.suolo = 373

    r.cade = 1
    r.cadem = 1

    return r


def update_menu_rocce():
    for i in range(len(rocce_menu) - 1, -1, -1):
        r = rocce_menu[i]

        if r.lato == 1:
            r.x += r.vel
        else:
            r.x -= r.vel

        if r.cade == 1:
            animate(r, tween='accelerate', duration=2, y=r.suolo)
            r.cade = 2

        elif r.y >= r.suolo and r.cade == 2:
            r.cade = 3

        elif r.cade == 3:
            animate(r, tween='decelerate', duration=2, y=r.y_partenza)
            r.cade = 2

        elif r.y <= r.y_partenza + 1 and r.cade == 2:
            r.cade = 1

        if r.x < -300 or r.x > 1300:
            rocce_menu.pop(i)
            rocce_menu.append(crea_roccia_menu())


def draw_salute_roccia(roccia):
    valore = int(roccia.salute)
    salute_str = str(valore)

    # CENTRO ORIZZONTALE
    x = roccia.x + 8

    # CENTRO VERTICALE (numeri in mezzo alla roccia)
    y = roccia.y

    # larghezza totale del numero (20 px per cifra)
    larghezza_totale = len(salute_str) * 20
    x = x - larghezza_totale // 2

    # disegna ogni cifra
    for cifra in salute_str:
        numero = Actor("numero_" + cifra)
        numero.pos = (x, y)
        numero.draw()
        x += 20


def draw():
    global mode
    
    if mode == "menu":
        draw_menu()
        return

    elif mode == "pausa":
        pausa_i.draw()
        return


    elif mode == "sconfitta":
        hai_perso.draw()
        return # esce subito, non aggiorna nulla
    
    elif mode == "gioco":
        draw_gioco()
        return


def draw_menu():
    global mode

    screen.blit("sfondo_caverna", (0, 0))
    for r in rocce_menu:
        r.draw()
    play.draw()
    options.draw()
    exit.draw()

    if play.collidepoint(pygame.mouse.get_pos()):
        play_h.draw()
        if pygame.mouse.get_pressed()[0]:  # se il tasto sinistro del mouse è premuto
            mode = "gioco"
            inizio()
            return  # esce subito, non aggiorna nulla
    elif options.collidepoint(pygame.mouse.get_pos()):
        options_h.draw()
        return
    elif exit.collidepoint(pygame.mouse.get_pos()):
        exit_h.draw()
        if pygame.mouse.get_pressed()[0]:  # se il tasto sinistro del mouse è premuto
            raise SystemExit


def draw_gioco():
    global punteggio
    global salute
    global danno
    global salute_mostrata
    global M_VU
    global M_VD

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

    for i in range(len(rocce)):       
        rocce[i].draw()
        draw_salute_roccia(rocce[i])                   #ok
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
    global mode

    if mode == "menu":
        if len(rocce_menu) < 5:
            rocce_menu.append(crea_roccia_menu())

        update_menu_rocce()

        if keyboard.space:
            mode = "gioco"
            inizio()
            return

    elif mode == "pausa":
        return  # esce subito, non aggiorna nulla

    elif mode == "sconfitta":
        if keyboard.space:
            mode = "gioco"
            inizio()
            return  # esce subito, non aggiorna nulla    
    
    elif mode == "gioco":
        gioco()


def gioco():
    global a 
    global dueframe
    global roccia
    global M_VU
    global M_VD
    global salute_mostrata
    
    salute_mostrata = (M_VU + M_VD) / 2


    for i in range(len(rocce)):
        if roccia.cade in (1, 3):
            roccia.cadem = roccia.cade
      
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
            rocce[i].x = rocce[i].x - rocce[i].velocità
        
        elif rocce[i].lato == 1:
            rocce[i].x = rocce[i].x + rocce[i].velocità
        
    #elif roccia.x <= -300:
        
    #    rocce.pop(i)
    #    roccia = crea_roccia()
    #    rocce.append(roccia)


def collisions():
    global mode, punteggio, danno, salute, M_VU, M_VD, salute_aggiuntiva

    # Controllo collisione cannone → sconfitta
    for i in range(len(rocce) - 1, -1, -1):
        if hitbox_cannone.colliderect(rocce[i]):
            mode = "sconfitta"
            return

        # Controllo collisioni con le palle
        for j in range(len(palle_cannone) - 1, -1, -1):
            if rocce[i].colliderect(palle_cannone[j]):

                # Rimuovi la palla
                palle_cannone.pop(j)

                # Applica danno
                rocce[i].salute -= danno

                # Se la roccia è morta → uccidila SUBITO
                if rocce[i].salute < 1:
                    uccidi_roccia(i)
                    break  # interrompe il ciclo delle palle, la roccia non esiste più


def uccidi_roccia(i):
    global punteggio, danno, M_VU, M_VD, salute_aggiuntiva

    salute_aggiuntiva = random.randint(1, 2)
    M_VU += salute_aggiuntiva
    M_VD += salute_aggiuntiva

    valore = 5

    if rocce[i].tipo == "roccia_rossa":
        valore = 50

    elif rocce[i].tipo == "roccia_verde_s":
        dannop = random.randint(2, 5)
        danno += dannop

    elif rocce[i].tipo == "roccia":
        roccia_destra = crea_roccia("roccia_s", 1)
        roccia_destra.x = rocce[i].x
        roccia_destra.y = rocce[i].y

        roccia_sinistra = crea_roccia("roccia_s", 2)
        roccia_sinistra.x = rocce[i].x
        roccia_sinistra.y = rocce[i].y

        rocce.append(roccia_destra)
        rocce.append(roccia_sinistra)

    # Rimuovi la roccia
    rocce.pop(i)

    # Aggiungi punteggio
    punteggio += valore


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