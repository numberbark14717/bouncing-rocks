import pygame
import random
import math


pygame.init()
pygame.mixer.init()

WIDTH = 1024
HEIGHT = 512
FPS = 70
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing rocks")
font = pygame.font.Font(None, 36)
animazioni = []
eventi_programmati = []
keyboard = pygame.key.get_pressed()
RECORD_PATH = "assets/record.txt"

class Sprite:
    def __init__(self, image, center=None):
        self.image = image
        self.rect = image.get_rect()
        if center is not None:
            self.rect.center = center

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        self.rect.centerx = round(value)

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        self.rect.centery = round(value)

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value

    @property
    def center(self):
        return self.rect.center

    @property
    def width(self):
        return self.rect.width

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def topleft(self):
        return self.rect.topleft

    @property
    def topright(self):
        return self.rect.topright

    @property
    def midleft(self):
        return self.rect.midleft

    @property
    def midright(self):
        return self.rect.midright

    @property
    def midtop(self):
        return self.rect.midtop

    @property
    def midbottom(self):
        return self.rect.midbottom

    def get_rect(self, **kwargs):
        return self.image.get_rect(**kwargs)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def draw(self):
        screen.blit(self.image, self.rect)


def sprite_from_file(path, center=None):
    return Sprite(pygame.image.load(path).convert_alpha(), center)


class Suoni:
    def __init__(self):
        self.suono_palla_contro_roccia = pygame.mixer.Sound("sounds/suono_palla_contro_roccia.ogg")
        self.suono_pressione_pulsante = pygame.mixer.Sound("sounds/suono_pressione_pulsante.ogg")
        self.suono_rottura_roccia = pygame.mixer.Sound("sounds/suono_rottura_roccia.ogg")
        self.suono_schianto_roccia = pygame.mixer.Sound("sounds/suono_schianto_roccia.ogg")
        self.suono_snap_scroller = pygame.mixer.Sound("sounds/suono_snap_scroller.ogg")
        self.suono_sparo = pygame.mixer.Sound("sounds/suono_sparo.ogg")


sounds = Suoni()


def testo(stringa, posizione, color="white", fontsize=36, midtop=None):
    superficie = pygame.font.Font(None, fontsize).render(stringa, True, pygame.Color(color))
    rettangolo = superficie.get_rect()
    if midtop is not None:
        rettangolo.midtop = midtop
    else:
        rettangolo.topleft = posizione
    screen.blit(superficie, rettangolo)


def animate(sprite, tween="linear", duration=1, **target):
    animazioni[:] = [a for a in animazioni if a["sprite"] is not sprite]
    animazioni.append({
        "sprite": sprite,
        "target": target,
        "start": {nome: getattr(sprite, nome) for nome in target},
        "elapsed": 0.0,
        "duration": max(float(duration), 1 / FPS),
        "tween": tween,
    })


def aggiorna_animazioni(dt):
    for animazione in animazioni[:]:
        animazione["elapsed"] += dt
        percentuale = min(animazione["elapsed"] / animazione["duration"], 1.0)
        if animazione["tween"] == "accelerate":
            percentuale *= percentuale
        elif animazione["tween"] == "decelerate":
            percentuale = 1 - (1 - percentuale) ** 2
        for nome, valore in animazione["target"].items():
            iniziale = animazione["start"][nome]
            setattr(animazione["sprite"], nome, iniziale + (valore - iniziale) * percentuale)
        if percentuale >= 1.0:
            animazioni.remove(animazione)


def programma_unica(funzione, ritardo):
    eventi_programmati[:] = [evento for evento in eventi_programmati if evento[0] is not funzione]
    eventi_programmati.append([funzione, float(ritardo)])


def aggiorna_eventi_programmati(dt):
    for evento in eventi_programmati[:]:
        evento[1] -= dt
        if evento[1] <= 0:
            eventi_programmati.remove(evento)
            evento[0]()

#cannon
cannone = sprite_from_file("images/cannone.png", (512, 427))
cannone_r = cannone.rect
hitbox_cannone = sprite_from_file("images/hitbox_cannone.png", (512, 427))
hitbox_cannone_r = hitbox_cannone.rect

#numbers
numero_1 = sprite_from_file("images/numero_1.png")
numero_1_r = numero_1.get_rect()
numero_2 = sprite_from_file("images/numero_2.png")
numero_2_r = numero_2.get_rect()
numero_3 = sprite_from_file("images/numero_3.png")
numero_3_r = numero_3.get_rect()
numero_4 = sprite_from_file("images/numero_4.png")
numero_4_r = numero_4.get_rect()
numero_5 = sprite_from_file("images/numero_5.png")
numero_5_r = numero_5.get_rect()
numero_6 = sprite_from_file("images/numero_6.png")
numero_6_r = numero_6.get_rect()
numero_7 = sprite_from_file("images/numero_7.png")
numero_7_r = numero_7.get_rect()
numero_8 = sprite_from_file("images/numero_8.png")
numero_8_r = numero_8.get_rect()
numero_9 = sprite_from_file("images/numero_9.png")
numero_9_r = numero_9.get_rect()
numero_0 = sprite_from_file("images/numero_0.png")
numero_0_r = numero_0.get_rect()
numero_più = sprite_from_file("images/numero_più.png")
numero_più_r = numero_più.get_rect()

#buttons
# PLAY
play = sprite_from_file("images/play_button.png", (WIDTH // 2, HEIGHT // 2 - 50))
play_r = play.rect
play_h = sprite_from_file("images/play_button_h.png", (WIDTH // 2, HEIGHT // 2 - 50))
play_h_r = play_h.rect
play_p = sprite_from_file("images/play_button_p.png", (WIDTH // 2, HEIGHT // 2 - 50))
play_p_r = play_p.rect
# OPTIONS
options = sprite_from_file("images/options_button.png", (WIDTH // 2, HEIGHT // 2 + 25))
options_r = options.rect
options_h = sprite_from_file("images/options_button_h.png", (WIDTH // 2, HEIGHT // 2 + 25))
options_h_r = options_h.rect
options_p = sprite_from_file("images/options_button_p.png", (WIDTH // 2, HEIGHT // 2 + 25))
options_p_r = options_p.rect
# EXIT
exit = sprite_from_file("images/exit_button.png", (WIDTH // 2, HEIGHT // 2 + 175))
exit_r = exit.rect
exit_h = sprite_from_file("images/exit_button_h.png", (WIDTH // 2, HEIGHT // 2 + 175))
exit_h_r = exit_h.rect
exit_p = sprite_from_file("images/exit_button_p.png", (WIDTH // 2, HEIGHT // 2 + 175))
exit_p_r = exit_p.rect

play_state = "normale"
options_state = "normale"
exit_state = "normale"

#volumes
volume_impostato = 0
volume_generale = 1.0
trascinando = False
bordo_sx = 512 - 181

tacche = [
    bordo_sx + 31,
    bordo_sx + 61,
    bordo_sx + 91,
    bordo_sx + 121,
    bordo_sx + 151,
    bordo_sx + 181,
    bordo_sx + 211,
    bordo_sx + 241,
    bordo_sx + 271,
    bordo_sx + 301,
    bordo_sx + 331
]


indice = 10 #100%
indice_calcoli = indice
volume = 1.0
volume_calcoli = volume
volume_t = sprite_from_file("images/volume.png", (WIDTH // 2, HEIGHT // 2 - 50))
volume_t_r = volume_t.rect
scroll_bar = sprite_from_file("images/scroll_bar.png", (WIDTH // 2, HEIGHT // 2 + 10))
scroll_bar_r = scroll_bar.rect
scroller = sprite_from_file("images/scroller.png", (tacche[indice], HEIGHT // 2 + 10))
scroller_r = scroller.rect

#animations

animazioni_morte = []

#background
sfondo_caverna = pygame.image.load("images/sfondo_caverna.png").convert()
hai_perso = sprite_from_file("images/hai_perso.png", (WIDTH // 2, HEIGHT // 2))
hai_perso_r = hai_perso.get_rect(center=(WIDTH // 2, HEIGHT // 2))
pausa_i = sprite_from_file("images/pausa.png", (WIDTH // 2, HEIGHT // 2))
pausa_i_r = pausa_i.get_rect(center=(WIDTH // 2, HEIGHT // 2))

#variabili iniziali
TITLE = "Bouncing rocks"
ROCCE_TOTALI = 3
inizio = "menu"
palle_cannone = []
rocce = []
rocce_menu = []
cannone_x_iniziale = 512
mode = inizio
dueframe = 0
attivato = False
maggiore = False
timer_color = 0


def carica_record():
    global record_precedente1, record_precedente2, record_precedente3
    try:
        with open(RECORD_PATH, "r") as f:
            linee = f.read().splitlines()
            record_precedente1 = int(linee[0])
            record_precedente2 = int(linee[1])
            record_precedente3 = int(linee[2])
    except:
        record_precedente1 = 0
        record_precedente2 = 0
        record_precedente3 = 0


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
    global maggiore
    global timer_color
    
    hitbox_cannone_r.x = cannone_x_iniziale + 0
    punteggio = 0
    salute_aggiuntiva = 0
    salute_mostrata = 0
    M_VU = 2 + salute_aggiuntiva
    M_VD = 3 + salute_aggiuntiva
    danno = 1
    mode = "gioco"
    animazioni_morte.clear()
    maggiore = False
    timer_color = 0
    carica_record()

    #Creazione rocce
    cannone_r.x = cannone_x_iniziale
    palle_cannone = []
    rocce = []
    for i in range(ROCCE_TOTALI):
    
        roccia = crea_roccia()
        #roccia.salute = random.randint(10, 20)
        #roccia.attack = random.randint(5, 10)
        rocce.append(roccia)


    palla_cannone = sprite_from_file("images/palla_cannone.png", (cannone_r.centerx, 437))
    palla_cannone_r = palla_cannone.rect
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
    velocità = random.uniform(1.7, 2.8) #velocità rocce gioco
    
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
                

    roccia_tipo = tipo

    if lato == 2:
        roccia_x = random.randint(1150, 1250)
        
    elif lato == 1:
        roccia_x = random.randint(-226, -126)
        
    
    # roccia.x = random.randint(24, 900)    
    roccia_y = altezza
    roccia_lato = lato
    roccia_y_partenza = altezza
    roccia_cade = 1
    roccia_cadem = roccia_cade
    roccia_salute = salute
    roccia_velocità = velocità
    roccia = sprite_from_file("images/" + roccia_tipo + ".png", (roccia_x, roccia_y))
    roccia.x = roccia_x
    roccia.y = roccia_y
    roccia.tipo = roccia_tipo
    roccia.lato = roccia_lato
    roccia.y_partenza = roccia_y_partenza
    roccia.cade = roccia_cade
    roccia.cadem = roccia_cadem
    roccia.salute = roccia_salute
    roccia.velocità = roccia_velocità
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

    r = sprite_from_file("images/" + tipo + ".png")

    lato = random.randint(1, 2)

    if lato == 1:
        r.x = random.randint(-226, -126)
    else:
        r.x = random.randint(1150, 1250)

    r.y = random.randint(0, 160)
    r.lato = lato
    r.vel = random.uniform(0.8, 1.6)    #velocità rocce menu

    r.tipo = tipo

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

        variazione_y = fisica(r)
        if variazione_y is not None:
            r.y += variazione_y

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
        numero = sprite_from_file("images/numero_" + cifra + ".png")
        numero.pos = (x, y)
        numero.draw()
        x += 20


def crea_animazione_morte(roccia, punteggio_aggiunto):

    valore_agg = int(punteggio_aggiunto)
    valore_agg_str = str(valore_agg)

    x_an = roccia.x + 8
    y_an = roccia.y

    larghezza_totale_an = len(valore_agg_str) * 20
    x_an = x_an - larghezza_totale_an // 2
    
    animazione = {
        "x_an": x_an,
        "y_an": y_an,
        "timer": 120,
        "valore_agg_str": valore_agg_str
    }

    animazioni_morte.append(animazione)


def draw():
    global mode
    
    if mode == "menu":
        draw_menu()
        return

    elif mode == "pausa":
        screen.blit(screenshot_pausa, (0, 0))
        pausa_i.draw()
        return

    elif mode == "impostazioni":
        draw_imp()
        return

    elif mode == "sconfitta":
        draw_sconfitta()
        return # esce subito, non aggiorna nulla
    
    elif mode == "gioco":
        draw_gioco()
        return


def on_mouse_down(pos):
    global mode
    global trascinando
    global play_state
    global options_state
    global exit_state
    if mode == "menu" and attivato == False:
        if play.collidepoint(pos):
            play_state = "premuto"
            sounds.suono_pressione_pulsante.play()
        elif options.collidepoint(pos):
            options_state = "premuto"
            sounds.suono_pressione_pulsante.play()
        elif exit.collidepoint(pos):
            exit_state = "premuto"
            sounds.suono_pressione_pulsante.play()

    elif mode == "impostazioni":
        if scroll_bar.collidepoint(pos):
            trascinando = True
        elif exit.collidepoint(pos):
            exit_state = "premuto"
            sounds.suono_pressione_pulsante.play()

    elif mode == "sconfitta":
        if exit.collidepoint(pos):
            exit_state = "premuto"
            sounds.suono_pressione_pulsante.play()


def on_mouse_up(pos):
    global mode
    global attivato
    global trascinando
    global volume_calcoli
    global indice
    global indice_calcoli
    global distanza
    global play_state
    global options_state
    global exit_state
    if mode == "menu" and attivato == False:
        if play.collidepoint(pos):
            play_state = "normale"
            programma_unica(pulsante_play, 0.5)
            #risposta_pulsante(play)
            attivato = True
        elif exit.collidepoint(pos):
            exit_state = "normale"
            programma_unica(pulsante_exit, 0.5)
            attivato = True
            #risposta_pulsante(exit)
        elif options.collidepoint(pos):
            options_state = "normale"
            programma_unica(pulsante_options, 0.5)
            attivato = True
    
    elif mode == "impostazioni":
        if not trascinando:
            if exit.collidepoint(pos):
                exit_state = "normale"
                programma_unica(pulsante_exit, 0.5)
                attivato = True
        else:
            # abbiamo finito di trascinare: snap alla tacca più vicina
            trascinando = False

            x = scroller.center[0]

            # trova la tacca più vicina
            migliore_tacca = tacche[0]
            migliore_dist = abs(x - tacche[0])
            migliore_indice = 0

            for i in range(1, len(tacche)):
                d = abs(x - tacche[i])
                if d < migliore_dist:
                    migliore_dist = d
                    migliore_tacca = tacche[i]
                    migliore_indice = i

            # snap
            animate(scroller, tween='decelerate', duration=0.2, x=migliore_tacca)
            indice = migliore_indice
            setter_volume()
            sounds.suono_snap_scroller.play()

    elif mode == "sconfitta":
        if exit.collidepoint(pos):
            exit_state = "normale"
            programma_unica(pulsante_exit, 0.5)
            attivato = True


def on_mouse_move():
    global mode
    global indice
    global trascinando
    global attivato
    global tacche
    global play_state
    global options_state
    global exit_state

    if mode == "menu" and attivato == False:
        if play.collidepoint(pygame.mouse.get_pos()):
            play_state = "hover"
        else:
            play_state = "normale"

        if options.collidepoint(pygame.mouse.get_pos()):
            options_state = "hover"
        else:
            options_state = "normale"

        if exit.collidepoint(pygame.mouse.get_pos()):
            exit_state = "hover"
        else:
            exit_state = "normale"
    
    elif mode == "impostazioni":
        mx, my = pygame.mouse.get_pos()

        if trascinando:
            # limiti reali: bordo barra tenendo conto della metà dello scroller
            lim_sx = scroll_bar.left + scroller.width // 2
            lim_dx = scroll_bar.right - scroller.width // 2

            if mx <= lim_sx:
                scroller.x = tacche[0]
                indice = 0
            elif mx >= lim_dx:
                scroller.x = tacche[10]
                indice = 10
            else:
                scroller.x = mx

        if exit.collidepoint((mx, my)):
            exit_state = "hover"
        else:
            exit_state = "normale"

    elif mode == "sconfitta":
        if exit.collidepoint(pygame.mouse.get_pos()):
            exit_state = "hover"
        else:
            exit_state = "normale"


def setter_volume():
    global volume
    global indice
    global play_state
    global options_state
    global exit_state

    volume = indice / 10
    sounds.suono_palla_contro_roccia.set_volume(volume)
    sounds.suono_pressione_pulsante.set_volume(volume)
    sounds.suono_rottura_roccia.set_volume(volume)
    sounds.suono_schianto_roccia.set_volume(volume)
    sounds.suono_snap_scroller.set_volume(volume)
    sounds.suono_sparo.set_volume(volume)


def draw_menu():
    global mode

    screen.blit(sfondo_caverna, (0, 0))
    for r in rocce_menu:
        r.draw()
    if play_state == "normale":
        play.draw()
    elif play_state == "hover":
        play_h.draw()
    elif play_state == "premuto":
        play_p.draw()
    if options_state == "normale":
        options.draw()
    elif options_state == "hover":
        options_h.draw()
    elif options_state == "premuto":
        options_p.draw()
    if exit_state == "normale":
        exit.draw()
    elif exit_state == "hover":
        exit_h.draw()
    elif exit_state == "premuto":
        exit_p.draw()


def draw_imp():
    global mode

    screen.blit(sfondo_caverna, (0, 0))
    for r in rocce_menu:
        r.draw()
    if exit_state == "normale":
        exit.draw()
    elif exit_state == "hover":
        exit_h.draw()
    elif exit_state == "premuto":
        exit_p.draw()
    volume_t.draw()
    scroll_bar.draw()
    scroller.draw()


def draw_sconfitta():
    global mode
    global record_precedente1
    global record_precedente2
    global record_precedente3
    global maggiore
    global play_state
    global options_state
    global exit_state

    screen.blit(screenshot_morte, (0, 0))
    hai_perso.draw()
    testo(str(record_precedente1), (0, 0), color="gold", fontsize=50, midtop=(WIDTH//2, 35))
    testo(str(record_precedente2), (0, 0), color="gray", fontsize=45, midtop=(WIDTH//2, 75))
    testo(str(record_precedente3), (0, 0), color="brown", fontsize=30, midtop=(WIDTH//2, 110))
    if exit_state == "normale":
        exit.draw()
    elif exit_state == "hover":
        exit_h.draw()
    elif exit_state == "premuto":
        exit_p.draw()
    
    if maggiore:
        draw_new_record()


def draw_new_record():
    global timer_color

    # ciclo dei colori arcobaleno
    colori = [
        (255,0,0),
        (255,127,0),
        (255,255,0),
        (0,255,0),
        (0,0,255),
        (75,0,130),
        (148,0,211)
    ]

    color = colori[timer_color // 10 % len(colori)]

    # prendi l'immagine originale
    img = pygame.image.load("images/new_record.png").convert_alpha()

    # crea una copia colorata
    img_colorata = img.copy()
    img_colorata.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    # disegna
    x = WIDTH//2 - img_colorata.get_width()//2
    y = 170 - img_colorata.get_height()//2
    screen.blit(img_colorata, (x, y))

    timer_color += 1


def geometria_analitica(x1, x2, y1, y2):
    radice = (x2 - x1) ** 2 + (y2 - y1) ** 2
    distanza = math.sqrt(radice)
    return distanza


def valore_indice():
    global tacche
    global scroller
    global indice

    if scroller.center[0] == tacche[0]:
        indice = 0
    elif scroller.center[0] == tacche[1]:
        indice = 1
    elif scroller.center[0] == tacche[2]:
        indice = 2
    elif scroller.center[0] == tacche[3]:
        indice = 3
    elif scroller.center[0] == tacche[4]:
        indice = 4
    elif scroller.center[0] == tacche[5]:
        indice = 5
    elif scroller.center[0] == tacche[6]:
        indice = 6
    elif scroller.center[0] == tacche[7]:
        indice = 7
    elif scroller.center[0] == tacche[8]:
        indice = 8
    elif scroller.center[0] == tacche[9]:
        indice = 9
    elif scroller.center[0] == tacche[10]:
        indice = 10
    return indice


def pulsante_play():
    risposta_pulsante(play)


def pulsante_exit():
    risposta_pulsante(exit)


def pulsante_options():
    risposta_pulsante(options)


def risposta_pulsante(pulsante):
    global mode
    global attivato

    if pulsante is play:
        mode = "gioco"
        attivato = False
        inizio()
        return  # esce subito, non aggiorna nulla
    elif pulsante is exit:
        if mode == "menu":
            raise SystemExit
        elif mode == "impostazioni":
            mode = "menu"
            attivato = False
            return  # esce subito, non aggiorna nulla
        elif mode == "sconfitta":
            mode = "menu"
            attivato = False
    elif pulsante is options:
        mode = "impostazioni"
        attivato = False
        return  # esce subito, non aggiorna nulla


def draw_gioco():
    global punteggio
    global salute
    global danno
    global salute_mostrata
    global M_VU
    global M_VD
    global maggiore

    # ottieni la dimensione attuale della finestra 
    w, h = screen.get_size()
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
        roccia = rocce[i]
        rocce[i].draw()
        draw_salute_roccia(rocce[i])                   #ok
    #roccia_s.draw()                #ok
    
    testo(str(punteggio), (20, 10), color="white")
    testo(str(danno), (0, 0), midtop=(WIDTH//2, 10), color=(255, 198, 41))
    testo(str(salute_mostrata), (940, 10), color="red")

    testo("score", (20, 480), color="white")
    testo("damage", (0, 0), midtop=(WIDTH//2, 480), color=(255, 198, 41))
    testo("future rock's health", (810, 480), color="red")

    for animazione in animazioni_morte:
        x_t = animazione["x_an"]
        y_t = animazione["y_an"]
        numero_più.pos = (x_t, y_t)
        numero_più.draw()
        x_t += 20
        x_tn = x_t

        for cifra_an in animazione["valore_agg_str"]:
            numero_an = sprite_from_file("images/numero_" + cifra_an + ".png")
            numero_an.pos = (x_tn, y_t)
            numero_an.draw()
            x_tn += 20


def salva_record():
    with open(RECORD_PATH, "w") as f:
        f.write(str(record_precedente1) + "\n")
        f.write(str(record_precedente2) + "\n")
        f.write(str(record_precedente3) + "\n")


def gestione_punteggi_migliori(record):
    global record_precedente1, record_precedente2, record_precedente3, maggiore

    if record > record_precedente1:
        record_precedente3 = record_precedente2
        record_precedente2 = record_precedente1
        record_precedente1 = record
        maggiore = True

    elif record > record_precedente2:
        record_precedente3 = record_precedente2
        record_precedente2 = record
        maggiore = True

    elif record > record_precedente3:
        record_precedente3 = record
        maggiore = True

    salva_record()


def on_key_down(key):
    
    global mode
    global cadem
    global cade
    global y
    global ym
    global screenshot_pausa
    
    if key == pygame.K_p and mode == "gioco":
        screenshot_pausa = screen.copy()
        mode = "pausa"  # alterna tra pausa e gioco
        
        for roccia in rocce:
            roccia.ym = roccia.y  # salva la posizione
            
            #print(roccia.cadem)
            #print(roccia.cade)
        
    elif key == pygame.K_p and mode == "pausa":
        
        mode = "gioco"
        
        for roccia in rocce:
            roccia.y = roccia.ym  # ripristina la posizione
            roccia.cade = roccia.cadem


def update(df):
    global mode, keyboard

    keyboard = pygame.key.get_pressed()
    aggiorna_eventi_programmati(df)
    aggiorna_animazioni(df)

    if mode == "menu" or mode == "impostazioni":
        if len(rocce_menu) < 5:
            rocce_menu.append(crea_roccia_menu())

        update_menu_rocce()

        if keyboard[pygame.K_SPACE]:
            mode = "gioco"
            inizio()
            return

    elif mode == "pausa":
        return  # esce subito, non aggiorna nulla

    elif mode == "sconfitta":
        if keyboard[pygame.K_SPACE]:
            mode = "gioco"
            inizio()
            return  # esce subito, non aggiorna nulla    
    
    elif mode == "gioco":
        gioco()
        gestione_animazioni()


def gestione_animazioni():
    for j in range(len(animazioni_morte) - 1, -1, -1):
        animazione = animazioni_morte[j]
        animazione["timer"] -= 1
        animazione["y_an"] -= 0.5
        if animazione["timer"] <= 0:
            animazioni_morte.pop(j)


def gioco():
    global a 
    global dueframe
    global roccia
    global M_VU
    global M_VD
    global salute_mostrata
    
    salute_mostrata = (M_VU + M_VD) / 2


    for i in range(len(rocce)):
        roccia = rocce[i]
        if roccia.cade in (1, 3):
            roccia.cadem = roccia.cade
      
    #print(len(palle_cannone))
    if dueframe % 1 == 0:
        if len(palle_cannone) == 0:
            palla_cannone = sprite_from_file("images/palla_cannone.png", (cannone.x, 380))
            sounds.suono_sparo.play()
            palle_cannone.append(palla_cannone)
        else:
            palla_cannone = palle_cannone[len(palle_cannone) - 1]
            if palla_cannone.y <= 285:
                palla_cannone = sprite_from_file("images/palla_cannone.png", (cannone.x, 380))
                sounds.suono_sparo.play()
                palle_cannone.append(palla_cannone)
    
        for i in range(len(palle_cannone) - 1, -1, -1):
            palle_cannone[i].y = palle_cannone[i].y -8
            
            if palle_cannone[i].y <= 0:
                palle_cannone.pop(i)
    
    dueframe += 1

    if keyboard[pygame.K_LEFT] and cannone.x > 51:
        # print("left")
        cannone.x = cannone.x - 5
        hitbox_cannone.x = hitbox_cannone.x - 5
    elif keyboard[pygame.K_RIGHT] and cannone.x < 973:
        #print("right")
        cannone.x = cannone.x + 5
        hitbox_cannone.x = hitbox_cannone.x + 5

    hitbox_cannone.pos = cannone.pos
    
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
    global mode, punteggio, danno, salute, M_VU, M_VD, salute_aggiuntiva, screenshot_morte

    punti_cannone = [
        hitbox_cannone.topleft,
        hitbox_cannone.topright,
        hitbox_cannone.midleft,
        hitbox_cannone.midright
    ]

    # Controllo collisione cannone → sconfitta
    for i in range(len(rocce)-1, -1, -1):

        roccia = rocce[i]
        if roccia.tipo ==  "roccia_s" or roccia.tipo == "roccia_verde_s":
            raggio = 35
        elif roccia.tipo == "roccia":
            raggio = 70
        else:
            raggio = 105

        rx = rocce[i].x
        ry = rocce[i].y
        for (cx, cy) in punti_cannone:
            if geometria_analitica(rx, cx, ry, cy) <= raggio:
                screenshot_morte = screen.copy()
                mode = "sconfitta"
                gestione_punteggi_migliori(punteggio)
                return

        # Controllo collisioni con le palle
        for j in range(len(palle_cannone) - 1, -1, -1):

            p = palle_cannone[j]

            punti_palla = [
                p.midtop,
                p.midbottom,
                p.midleft,
                p.midright
            ]

            colpita = False

            for (px, py) in punti_palla:
                if geometria_analitica(rx, px, ry, py) <= raggio:
                    colpita = True
                    break

            if colpita:
                palle_cannone.pop(j)
                sounds.suono_palla_contro_roccia.play()
                rocce[i].salute -= danno

                if rocce[i].salute < 1:
                    uccidi_roccia(i)
                    sounds.suono_rottura_roccia.play()
                break


def uccidi_roccia(i):
    global punteggio
    global danno
    global M_VU
    global M_VD
    global salute_aggiuntiva

    salute_aggiuntiva = random.randint(1, 2)
    M_VU += salute_aggiuntiva
    M_VD += salute_aggiuntiva

    valore = 5

    if rocce[i].tipo == "roccia_rossa":
        valored = random.randint(-1, 3) * 10
        valore = valored + 50

    elif rocce[i].tipo == "roccia_verde_s":
        dannop = random.randint(2, 5)
        danno += dannop
        valore = 0

    elif rocce[i].tipo == "roccia":
        roccia_destra = crea_roccia("roccia_s", 1)
        roccia_destra.x = rocce[i].x
        roccia_destra.y = rocce[i].y

        roccia_sinistra = crea_roccia("roccia_s", 2)
        roccia_sinistra.x = rocce[i].x
        roccia_sinistra.y = rocce[i].y

        rocce.append(roccia_destra)
        rocce.append(roccia_sinistra)

        valore = 10

    # Prima di rimuovere la roccia, dici alla funzione quale roccia vuole l'animazione
    crea_animazione_morte(rocce[i], valore)

    # Rimuovi la roccia
    rocce.pop(i)

    # Aggiungi punteggio
    punteggio += valore


def fisica(roccia):
    # inizializza la velocità verticale se non esiste
    if not hasattr(roccia, "vy"):
        roccia.vy = 0

    # gravità
    gravità = 0.09
    roccia.vy += gravità

    # calcolo del suolo in base al tipo
    if roccia.tipo in ("roccia_s", "roccia_verde_s"):
        suolo = 435
    elif roccia.tipo == "roccia_rossa":
        suolo = 373
    else:
        suolo = 398

    # movimento verticale proposto
    delta_y = roccia.vy

    # se superiamo il suolo → rimbalzo
    if roccia.y + delta_y >= suolo:
        # blocca la roccia sul suolo
        roccia.y = suolo
        # inverti la velocità e riducila
        roccia.vy *= -0.999
        return 0  # niente movimento oltre il suolo

    return delta_y


def movimento():
    for i in range(len(rocce) -1, -1, -1):
        roccia = rocce[i]

        variazione_y = fisica(roccia)
        if variazione_y is not None:
            roccia.y += variazione_y
            
        if roccia.x >= 1300 or roccia.x <= -300:
            
            rocce.pop(i)
            roccia = crea_roccia()
            rocce.append(roccia)


carica_record()


def main():
    clock = pygame.time.Clock()
    attivo = True

    while attivo:
        dt = clock.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                attivo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_down(evento.pos)
            elif evento.type == pygame.MOUSEBUTTONUP:
                on_mouse_up(evento.pos)
            elif evento.type == pygame.MOUSEMOTION:
                on_mouse_move()
            elif evento.type == pygame.KEYDOWN:
                on_key_down(evento.key)

        update(dt)
        screen.fill((0, 0, 0))
        draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

