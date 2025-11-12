/**
 * Globale Variablen
 */
function UpdateGraphik () {
    basic.clearScreen()
    if (AktuellesLevel == 1) {
        // LEVEL 1: Volles Logo (Linien)
        if (ZeilenStatus[0]) {
            // P0
            led.plot(0, 0)
            led.plot(1, 0)
            led.plot(2, 0)
        }
        if (ZeilenStatus[1]) {
            // P1
            led.plot(1, 1)
            led.plot(2, 1)
            led.plot(3, 1)
        }
        if (ZeilenStatus[2]) {
            // P2
            led.plot(2, 2)
            led.plot(3, 2)
            led.plot(4, 2)
        }
        if (ZeilenStatus[3]) {
            // Taste A
            led.plot(1, 3)
            led.plot(2, 3)
            led.plot(3, 3)
        }
        if (ZeilenStatus[4]) {
            // Taste B
            led.plot(0, 4)
            led.plot(1, 4)
            led.plot(2, 4)
        }
    } else if (AktuellesLevel == 2) {
        // LEVEL 2: Hohles Logo (Nur Punkte/Kontur)
        if (ZeilenStatus[0]) {
            // Schütteln
            led.plot(0, 0)
            led.plot(2, 0)
        }
        // Lücke in der Mitte
        if (ZeilenStatus[1]) {
            // A+B
            led.plot(1, 1)
            led.plot(3, 1)
        }
        if (ZeilenStatus[2]) {
            // Links
            led.plot(2, 2)
            led.plot(4, 2)
        }
        if (ZeilenStatus[3]) {
            // Rechts
            led.plot(1, 3)
            led.plot(3, 3)
        }
        if (ZeilenStatus[4]) {
            // Kopfueber
            led.plot(0, 4)
            led.plot(2, 4)
        }
    }
}
// --- INPUTS LEVEL 1 (Pins & Buttons) ---
// Nur wirksam in Level 1
input.onPinPressed(TouchPin.P0, function () {
    ZeileLoeschen(0, 1)
})
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    ZeileLoeschen(4, 2)
})
input.onSound(DetectedSound.Loud, function () {
    ZeileLoeschen(0, 2)
})
input.onButtonPressed(Button.A, function () {
    ZeileLoeschen(3, 1)
})
function Level1Geschafft () {
    SpielGesperrt = true
    // Gutzeichen
    basic.showIcon(IconNames.Yes)
    basic.pause(2000)
    // Das Dollarzeichen ($)
    basic.showLeds(`
        . # # # .
        # . # . .
        . # # # .
        . . # . #
        . # # # .
        `)
    music.playMelody("E G B C5 - - - - ", 300)
    // 5 Sekunden warten vor Runde 2
    basic.pause(5000)
    // Reset für Level 2
    AktuellesLevel = 2
    ZeilenStatus = [
    true,
    true,
    true,
    true,
    true
    ]
    // Alle Zeilen wieder an
    SpielGesperrt = false
    // Start-Animation für Level 2
    basic.showString("2")
    UpdateGraphik()
}
// Verhindert Eingaben während Animationen
// --- Kern-Logik ---
function ZeileLoeschen (ZeilenNummer: number, BenioetigtesLevel: number) {
    // Eingabe nur verarbeiten, wenn wir im richtigen Level sind und keine Animation läuft
    if (SpielGesperrt || AktuellesLevel != BenioetigtesLevel) {
        return
    }
    // Wenn die Zeile noch da ist, löschen
    if (ZeilenStatus[ZeilenNummer] == true) {
        ZeilenStatus[ZeilenNummer] = false
        // Sound-Feedback
        music.playTone(523, music.beat(BeatFraction.Sixteenth))
        UpdateGraphik()
        // Prüfen, ob ALLE Zeilen gelöscht sind
        if (!(ZeilenStatus.indexOf(true) >= 0)) {
            if (AktuellesLevel == 1) {
                Level1Geschafft()
            } else if (AktuellesLevel == 2) {
                Level2Geschafft()
            }
        }
    }
}
input.onPinPressed(TouchPin.P2, function () {
    ZeileLoeschen(2, 1)
})
input.onGesture(Gesture.Shake, function () {
    ZeileLoeschen(1, 2)
})
function Level2Geschafft () {
    SpielGesperrt = true
    AktuellesLevel = 3
    // Spiel vorbei
    // Gutzeichen
    basic.showIcon(IconNames.Yes)
    basic.pause(1000)
    // Der POKAL (Trophy)
    basic.showLeds(`
        # # # # #
        . # # # .
        . . # . .
        . # # # .
        # # # # #
        `)
    // Große Siegesfanfare
    music.playMelody("G C5 E C5 G C5 E C5 ", 180)
}
input.onButtonPressed(Button.B, function () {
    ZeileLoeschen(4, 1)
})
input.onPinPressed(TouchPin.P1, function () {
    ZeileLoeschen(1, 1)
})
let SpielGesperrt = false
let AktuellesLevel = 0
let ZeilenStatus: boolean[] = []
// Speichert, welche der 5 Zeilen sichtbar sind (True = an, False = gelöscht)
ZeilenStatus = [
true,
true,
true,
true,
true
]
// 1 = Erstes Spiel (Solid Logo), 2 = Zweites Spiel (Hohles Logo), 3 = Ende
AktuellesLevel = 1
// --- Start ---
UpdateGraphik()
basic.forever(function () {
    if (input.compassHeading() < 10) {
        ZeileLoeschen(2, 2)
    }
})
basic.forever(function () {
    if (input.lightLevel() < 10) {
        ZeileLoeschen(2, 2)
    }
})
