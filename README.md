# Mouse Zones

Automatisation de tâches sous Windows déclenchée par des clics de souris, selon la **zone de l'écran** où vous cliquez.

## Installation

1. Installez [Python](https://www.python.org/downloads/) (cochez "Add Python to PATH" à l'installation).
2. Ouvrez un terminal dans ce dossier et lancez :

```
pip install -r requirements.txt
```

## Utilisation

### 1. Définir vos zones (mode repérage)

```
python zones.py --setup
```

Déplacez la souris aux coins de chaque zone et notez les coordonnées affichées (x, y). Chaque zone est un rectangle `[x_gauche, y_haut, x_droite, y_bas]`.

### 2. Configurer les zones et leurs actions

Ouvrez `config.json`. Chaque zone a un `name`, un `rect` et une `action`.

Le paramètre facultatif `"verbose"` (défaut : `true`) contrôle l'affichage des clics hors zones : mettez `"verbose": false` pour un log silencieux qui ne montre que les actions déclenchées.

Types d'actions disponibles (une action peut être un objet **ou une liste** d'objets pour enchaîner plusieurs étapes) :

| Type | Description | Exemple |
|------|-------------|---------|
| `open` | Ouvre une application ou un fichier | `{"type": "open", "target": "notepad.exe"}` |
| `type` | Tape du texte | `{"type": "type", "text": "Bonjour", "delay": 0.05}` |
| `hotkey` | Raccourci clavier | `{"type": "hotkey", "keys": ["ctrl", "s"]}` |
| `click` | Simule un clic de souris | `{"type": "click", "position": [960, 540], "count": 2}` |
| `wait` | Attendre (secondes) | `{"type": "wait", "seconds": 0.5}` |

Touches valides pour `hotkey` : `ctrl`, `alt`, `shift`, `cmd`, `enter`, `esc`, `tab`, `space`, `backspace`, `delete`, `up`, `down`, `left`, `right`, `f1`…`f12`, ou un caractère simple comme `"a"`.

### 3. Lancer l'automatisation

```
python zones.py
```

Ou plus simplement : **double-cliquez sur `lancer.bat`** — il installe `pynput` au premier lancement si nécessaire, puis démarre le script et garde la fenêtre ouverte.

### La fenêtre se ferme immédiatement ?

Si vous lancez `zones.py` par double-clic et que la fenêtre se referme aussitôt, c'est qu'une erreur s'est produite (le plus souvent `pynput` non installé). Le script affiche maintenant le message d'erreur et attend que vous appuyiez sur Entrée. Utilisez `lancer.bat` ou lancez depuis un terminal pour voir le message.

- Chaque clic dans une zone déclenche l'action associée.
- **Clic du milieu** de la souris ou **Ctrl+C** dans le terminal pour arrêter.

## Conseils

- Évitez de placer des zones sur des boutons que vous utilisez normalement : tous les clics dans la zone sont interceptés.
- Ajustez les `rect` à votre résolution d'écran (les exemples supposent 2560×1440).
- Pour un lancement rapide, créez un raccourci Windows vers `pythonw zones.py` (sans fenêtre terminal).
