"""
Globale Variablen
"""
# Speichert, welche der 5 Zeilen sichtbar sind (True = an, False = gelöscht)
ZeilenStatus = [True, True, True, True, True]

# 1 = Erstes Spiel (Solid Logo), 2 = Zweites Spiel (Hohles Logo), 3 = Ende
AktuellesLevel = 1
SpielGesperrt = False # Verhindert Eingaben während Animationen

# --- Kern-Logik ---

def ZeileLoeschen(ZeilenNummer: number, BenioetigtesLevel: number):
    global AktuellesLevel, SpielGesperrt
    
    # Eingabe nur verarbeiten, wenn wir im richtigen Level sind und keine Animation läuft
    if SpielGesperrt or AktuellesLevel != BenioetigtesLevel:
        return

    # Wenn die Zeile noch da ist, löschen
    if ZeilenStatus[ZeilenNummer] == True:
        ZeilenStatus[ZeilenNummer] = False
        
        # Sound-Feedback
        music.play_tone(Note.C5, music.beat(BeatFraction.SIXTEENTH))
        
        UpdateGraphik()
        
        # Prüfen, ob ALLE Zeilen gelöscht sind
        if not (True in ZeilenStatus):
            if AktuellesLevel == 1:
                Level1Geschafft()
            elif AktuellesLevel == 2:
                Level2Geschafft()

def UpdateGraphik():
    basic.clear_screen()
    
    if AktuellesLevel == 1:
        # LEVEL 1: Volles Logo (Linien)
        if ZeilenStatus[0]: # P0
            led.plot(0, 0); led.plot(1, 0); led.plot(2, 0)
        if ZeilenStatus[1]: # P1
            led.plot(1, 1); led.plot(2, 1); led.plot(3, 1)
        if ZeilenStatus[2]: # P2
            led.plot(2, 2); led.plot(3, 2); led.plot(4, 2)
        if ZeilenStatus[3]: # Taste A
            led.plot(1, 3); led.plot(2, 3); led.plot(3, 3)
        if ZeilenStatus[4]: # Taste B
            led.plot(0, 4); led.plot(1, 4); led.plot(2, 4)

    elif AktuellesLevel == 2:
        # LEVEL 2: Hohles Logo (Nur Punkte/Kontur)
        if ZeilenStatus[0]: # Schütteln
            led.plot(0, 0); led.plot(2, 0) # Lücke in der Mitte
        if ZeilenStatus[1]: # A+B
            led.plot(1, 1); led.plot(3, 1)
        if ZeilenStatus[2]: # Links
            led.plot(2, 2); led.plot(4, 2)
        if ZeilenStatus[3]: # Rechts
            led.plot(1, 3); led.plot(3, 3)
        if ZeilenStatus[4]: # Kopfueber
            led.plot(0, 4); led.plot(2, 4)

def Level1Geschafft():
    global SpielGesperrt, AktuellesLevel, ZeilenStatus
    SpielGesperrt = True
    
    # Gutzeichen
    basic.show_icon(IconNames.YES)
    basic.pause(2000)
    
    # Das Dollarzeichen ($)
    basic.show_leds("""
        . # # # .
        # . # . .
        . # # # .
        . . # . #
        . # # # .
        """)
    music.play_melody("E G B C5 - - - -", 300)
    
    # 5 Sekunden warten vor Runde 2
    basic.pause(5000)
    
    # Reset für Level 2
    AktuellesLevel = 2
    ZeilenStatus = [True, True, True, True, True] # Alle Zeilen wieder an
    SpielGesperrt = False
    
    # Start-Animation für Level 2
    basic.show_string("2")
    UpdateGraphik()

def Level2Geschafft():
    global SpielGesperrt, AktuellesLevel
    SpielGesperrt = True
    AktuellesLevel = 3 # Spiel vorbei
    
    # Gutzeichen
    basic.show_icon(IconNames.YES)
    basic.pause(1000)
    
    # Der POKAL (Trophy)
    basic.show_leds("""
        # # # # #
        . # # # .
        . . # . .
        . # # # .
        # # # # #
        """)
    # Große Siegesfanfare
    music.play_melody("G C5 E C5 G C5 E C5", 180)

# --- INPUTS LEVEL 1 (Pins & Buttons) ---

def on_pin_pressed_p0():
    ZeileLoeschen(0, 1) # Nur wirksam in Level 1
input.on_pin_pressed(TouchPin.P0, on_pin_pressed_p0)

def on_pin_pressed_p1():
    ZeileLoeschen(1, 1)
input.on_pin_pressed(TouchPin.P1, on_pin_pressed_p1)

def on_pin_pressed_p2():
    ZeileLoeschen(2, 1)
input.on_pin_pressed(TouchPin.P2, on_pin_pressed_p2)

def on_button_pressed_a():
    ZeileLoeschen(3, 1)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    ZeileLoeschen(4, 1)
input.on_button_pressed(Button.B, on_button_pressed_b)


# --- INPUTS LEVEL 2 (Sensoren & Gesten) ---

# 1. Zeile: Schütteln
def on_gesture_shake():
    ZeileLoeschen(0, 2) # Nur wirksam in Level 2
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# 2. Zeile: A + B gleichzeitig
def on_button_pressed_ab():
    ZeileLoeschen(1, 2)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

# 3. Zeile: Nach Links neigen
def on_gesture_tilt_left():
    ZeileLoeschen(2, 2)
input.on_gesture(Gesture.TILT_LEFT, on_gesture_tilt_left)

# 4. Zeile: Nach Rechts neigen
def on_gesture_tilt_right():
    ZeileLoeschen(3, 2)
input.on_gesture(Gesture.TILT_RIGHT, on_gesture_tilt_right)

# 5. Zeile: Logo nach unten (Kopfstand)
def on_gesture_logo_down():
    ZeileLoeschen(4, 2)
input.on_gesture(Gesture.LOGO_DOWN, on_gesture_logo_down)

# --- Start ---
UpdateGraphik()
