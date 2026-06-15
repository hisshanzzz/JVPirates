# Upload JV Pirates to itch.io

Everything is already built. You just need to create the itch.io page and upload two files.

## Files ready for upload

| File | Use on itch.io |
|---|---|
| `build/web.zip` | **Play in browser** (HTML game) |
| `dist/JVPirates-Windows.zip` | **Download** version (Windows, needs Python) |

---

## Step 1 — Create itch.io account

1. Go to https://itch.io and sign up (free)
2. Click your profile → **Dashboard** → **Create new project**

---

## Step 2 — Fill in project details

Copy from `itch-description.txt` or use this:

- **Title:** The Tales of JV Pirates
- **Project URL:** `jvpirates` (or `tales-of-jv-pirates`)
- **Classification:** Games
- **Kind of project:** HTML
- **This file will be played in the browser:** ✅ checked
- **Price:** Free (or pay what you want)

**Short description:**
> Pirate-themed 2D adventure built with Python + Pygame during CraftQuest at American Center Colombo. Team Typhoons.

**Tags:** pygame, 2d, adventure, pirate, student-project, browser

---

## Step 3 — Upload browser version

1. Under **Uploads**, click **Upload files**
2. Upload **`build/web.zip`**
3. itch.io will detect it as an HTML game
4. Make sure **"Embed in page"** / **"Play in browser"** is enabled

---

## Step 4 — Upload Windows download (optional but recommended)

1. Click **Add new file**
2. Upload **`dist/JVPirates-Windows.zip`**
3. Label it: `Windows (Python required)`
4. Check **"This file will be played in the browser"** only for web.zip — NOT for the Windows zip

---

## Step 5 — Cover image

Use one of these as your itch.io cover (upload in project settings):
- `graphics/backgrounds/Game_Intro.jpg`
- `graphics/backgrounds/logo.png`

---

## Step 6 — Publish

1. Set visibility to **Public** or **Restricted** (link-only)
2. Click **Save & view page**
3. Test the **Run game** button in Chrome

---

## Controls (add to page description)

**Keyboard (desktop browser):**
| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Jump |
| X | Attack |
| Enter | Select level / confirm |
| P | Pause |

**Touch (phone/tablet):** Use the on-screen buttons.

---

## Rebuild browser version later

If you change the game code, rebuild from the project folder:

```powershell
cd C:\Users\USER\latex-cv\jv-pirates-temp
py -3.12 -m pygbag --build --archive --disable-sound-format-error --title "The Tales of JV Pirates" --package com.hisshanzzz.jvpirates --icon favicon.png main.py
```

New `build/web.zip` → re-upload on itch.io.

---

## Links to add on the page

- GitHub: https://github.com/hisshanzzz/JVPirates
- Team repo: https://github.com/TyphoonsLK/JVPirates
