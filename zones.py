# -*- coding: utf-8 -*-
"""
Mouse Zones — automatisation de tâches par zones d'écran.

Chaque zone de l'écran est un rectangle. Quand vous cliquez dans une zone,
l'action associée s'exécute : ouvrir une application, taper du texte,
envoyer un raccourci clavier, ou une combinaison de tout ça.

Usage :
    python zones.py            # mode normal : écoute les clics
    python zones.py --setup    # mode repérage : affiche la position de la souris
                               # et les dimensions de l'écran pour définir les zones

Arrêt du script : arrêter le terminal (Ctrl+C) ou clic du milieu de la souris.
"""

import argparse
import json
import os
import subprocess
import sys
import time

from pynput import mouse, keyboard

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

mouse_ctl = mouse.Controller()
keyboard_ctl = keyboard.Controller()


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def zone_contains(zone, x, y):
    """Un clic compte dans la zone si le point est dans le rectangle (bords inclus)."""
    x1, y1, x2, y2 = zone["rect"]
    return x1 <= x <= x2 and y1 <= y <= y2


def run_action(action):
    """Exécute une action. Une action peut être un dict ou une liste de dicts (séquence)."""
    actions = action if isinstance(action, list) else [action]
    for step in actions:
        run_single_action(step)


def run_single_action(action):
    atype = action.get("type")

    if atype == "open":
        target = action["target"]
        if os.path.exists(target):
            os.startfile(target)
        else:
            subprocess.Popen(target, shell=True)

    elif atype == "type":
        text = action["text"]
        delay = action.get("delay", 0.05)
        for char in text:
            keyboard_ctl.type(char)
            time.sleep(delay)

    elif atype == "hotkey":
        keyboard_ctl.press(*[keyboard.KeyCode.from_char(c) if len(c) == 1 else getattr(keyboard.Key, c) for c in action["keys"]])
        keyboard_ctl.release(*[keyboard.KeyCode.from_char(c) if len(c) == 1 else getattr(keyboard.Key, c) for c in action["keys"]])

    elif atype == "click":
        pos = action.get("position")
        if pos:
            mouse_ctl.position = (pos[0], pos[1])
            time.sleep(action.get("delay", 0.1))
        mouse_ctl.click(action.get("button", "left"), action.get("count", 1))

    elif atype == "wait":
        time.sleep(action.get("seconds", 1))

    else:
        print(f"[!] Type d'action inconnu : {atype}")


def find_zone(x, y, zones):
    """Retourne la première zone contenant le point (x, y), ou None."""
    for zone in zones:
        if zone_contains(zone, x, y):
            return zone
    return None


def on_click(x, y, button, pressed, config):
    if not pressed:
        return True

    if button == mouse.Button.middle:
        print("[i] Clic du milieu : arrêt du script.")
        return False

    zone = find_zone(x, y, config["zones"])
    if zone is None:
        print(f"[-] Clic ({x}, {y}) hors de toutes les zones.")
        return True

    print(f"[+] Clic ({x}, {y}) dans la zone '{zone['name']}' -> action.")
    try:
        run_action(zone["action"])
    except Exception as e:
        print(f"[!] Erreur pendant l'action : {e}")
    return True


def setup_mode():
    """Affiche la position de la souris en continu pour aider à définir les zones."""
    print("=" * 60)
    print("MODE REPÉRAGE")
    print("Déplacez la souris aux coins de vos zones et notez les coordonnées.")
    print("Ctrl+C pour quitter.")
    print("=" * 60)
    screen_w, screen_h = mouse_ctl.position  # position initiale
    try:
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_w = user32.GetSystemMetrics(0)
        screen_h = user32.GetSystemMetrics(1)
    except Exception:
        pass
    print(f"Écran : {screen_w} x {screen_h}")
    print("-" * 60)

    last = None
    try:
        while True:
            pos = mouse_ctl.position
            if pos != last:
                last = pos
                print(f"Souris : x={pos[0]}  y={pos[1]}          ", end="\r")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n[i] Fin du mode repérage.")


def main():
    parser = argparse.ArgumentParser(description="Automatisation par zones de souris.")
    parser.add_argument("--setup", action="store_true", help="afficher la position de la souris pour définir les zones")
    args = parser.parse_args()

    if args.setup:
        setup_mode()
        return

    try:
        config = load_config()
    except FileNotFoundError:
        print(f"[!] Fichier de configuration introuvable : {CONFIG_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[!] JSON invalide dans config.json : {e}")
        sys.exit(1)

    print("=" * 60)
    print("MOUSE ZONES — écoute des clics activée")
    print(f"{len(config['zones'])} zone(s) chargée(s) :")
    for z in config["zones"]:
        print(f"  - {z['name']}  rect={z['rect']}")
    print("Clic du milieu de la souris pour arrêter. Ctrl+C dans le terminal.")
    print("=" * 60)

    with mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, config)) as listener:
        listener.join()


if __name__ == "__main__":
    main()
