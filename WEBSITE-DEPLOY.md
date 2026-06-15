# Play JV Pirates in the browser (laptop / desktop only)

Keyboard controls only — best in **Chrome** on a laptop or desktop. Not optimized for phones.

---

## Option A — itch.io (easiest, free) ⭐ Recommended

### Step 1 — Build the web game (one time, or after code changes)

Open PowerShell:

```powershell
cd C:\Users\USER\latex-cv\jv-pirates-temp
py -3.12 -m pip install pygame-ce pytmx pygbag
py -3.12 -m pygbag --build --archive --disable-sound-format-error --title "The Tales of JV Pirates" --package com.hisshanzzz.jvpirates --icon favicon.png main.py
```

Output file: `build\web.zip`

### Step 2 — Create itch.io page

1. Go to https://itch.io → sign up (free)
2. **Dashboard** → **Create new project**
3. **Title:** The Tales of JV Pirates
4. **Kind of project:** HTML
5. Upload `build\web.zip`
6. Check **"This file will be played in the browser"**
7. Paste description from `itch-description.txt`
8. Set **Public** → Save

Your game URL will look like: `https://YOURNAME.itch.io/jvpirates`

---

## Option B — GitHub Pages (free, uses your GitHub repo)

After pushing this repo to GitHub, enable Pages on the `docs/` folder.

### Step 1 — Build web game (same as above)

```powershell
py -3.12 -m pygbag --build --archive --disable-sound-format-error --title "The Tales of JV Pirates" --package com.hisshanzzz.jvpirates --icon favicon.png main.py
```

### Step 2 — Copy build to docs folder

```powershell
Remove-Item -Recurse -Force docs -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path docs | Out-Null
Copy-Item -Path build\web\* -Destination docs -Recurse -Force
New-Item -ItemType File -Path docs\.nojekyll -Force
```

### Step 3 — Push to GitHub

```powershell
git add docs
git commit -m "Add browser build for GitHub Pages"
git push origin main
```

### Step 4 — Turn on GitHub Pages

1. Go to https://github.com/hisshanzzz/JVPirates
2. **Settings** → **Pages**
3. **Source:** Deploy from branch
4. **Branch:** `main` → folder **`/docs`**
5. Save

Wait 2–5 minutes. Your game will be at:

**https://hisshanzzz.github.io/JVPirates/**

---

## Controls (tell players)

| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Jump |
| X | Attack |
| Enter | Enter level (overworld) |
| P | Pause |

---

## Rebuild after any code fix

1. Run pygbag build command again
2. Re-upload `web.zip` on itch.io **OR** re-copy to `docs/` and push to GitHub

---

## What I can do vs what you do

| Task | Who |
|---|---|
| Fix code, build web.zip, write guides | Done in repo |
| Push to GitHub | Needs your git login (or approve push) |
| Create itch.io account + upload | **You** (needs your login) |
| Enable GitHub Pages in Settings | **You** (one-time, 30 seconds) |
