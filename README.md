# The Tales of JV Pirates

A pirate-themed 2D adventure game built with **Python** and **Pygame** during **CraftQuest** at the **American Center Colombo** (AJAX program).

![Game intro](graphics/backgrounds/Game_Intro.jpg)

## About

Our team **Typhoons** created this as our first dive into 2D game development — level design, sprites, collisions, game loops, and teamwork under a deadline.

| | |
|---|---|
| **Program** | CraftQuest 2D Game Development — American Center Colombo |
| **Mentor** | Liyanage Kalana Perera |
| **Coordinator** | Janitha Alendra Arachchige |
| **Team org** | [TyphoonsLK](https://github.com/TyphoonsLK) |
| **Original repo** | [TyphoonsLK/JVPirates](https://github.com/TyphoonsLK/JVPirates) |

## Team Typhoons

Mohamed Jaufer Mohamed Hisshan, Shenali Madurapperuma, Sahan Jayamal, Thiyagarajah Madusheshan, Pasan Wanigasuriya

## Run locally (Windows)

**Requirements:** [Python 3.12](https://www.python.org/downloads/) (recommended). Python 3.14 may fail to install or run Pygame; use 3.12 if you hit errors.

1. **Clone the repo**

```powershell
git clone https://github.com/hisshanzzz/JVPirates.git
cd JVPirates
```

2. **Install dependencies**

```powershell
py -3.12 -m pip install -r requirements.txt
```

3. **Run the game** from the **project root** (not inside `code/`)

```powershell
py -3.12 code/main.py
```

Or double-click **`PLAY.bat`** on Windows.

## Play in browser (itch.io / web)

The game can run in Chrome via **pygbag** (WebAssembly).

**Rebuild the itch.io upload:**

```powershell
py -3.12 -m pip install -r requirements-web.txt
py -3.12 -m pygbag --build --archive --disable-sound-format-error --title "The Tales of JV Pirates" --package com.hisshanzzz.jvpirates --icon favicon.png main.py
```

Upload `build/web.zip` to itch.io — see **ITCHIO-UPLOAD.md** for step-by-step instructions.

**Browser controls:** keyboard on desktop; on-screen touch buttons on phone/tablet.

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Jump |
| X | Attack (deflect enemies) |
| Enter | Enter level / confirm |
| P | Pause |

## Combat

Press **X** (or the **ATK** touch button in the browser) while facing an enemy to deflect it. Attacks do not destroy most hazards.

| Enemy / hazard | Attackable? | Effect when hit |
|---|---|---|
| **Tooth** (walking enemy) | Yes | Reverses direction |
| **Perl** (shell projectile) | Yes | Deflected back |
| **Shell** (shooter) | No | Shoots perls; attack the projectiles |
| **Saw** (moving / static) | No | Avoid only |
| **Floor spike** | No | Avoid only |
| **Spike ball** (orbiting) | No | Avoid only |
| **Moving hazards** (non-platform) | No | Avoid only |

## What we learned

- Pygame fundamentals (sprites, groups, game loop)
- Level design with Tiled maps (`.tmx` files)
- Team collaboration — communication, time management, debugging together

## Note

This copy on [hisshanzzz/JVPirates](https://github.com/hisshanzzz/JVPirates) is forked from the team organization repo for portfolio purposes. Full credit to Team Typhoons and American Center Colombo.
