# Velocitone REAPER Toolbar Icons

A Python build system that generates custom toolbar and track icons for [REAPER](https://www.reaper.fm/) from modular SVG building blocks ("legos"). It composites background shapes with tool/instrument glyphs, applies per-state color theming, renders multi-state sprite sheets for toolbar icons and single-frame images for track icons, exports PNGs at multiple resolutions, and optionally copies the results straight into your REAPER Data directory.

Ideal for workflows like track tagging/filtering or controlling external MIDI devices (e.g., MidiFighter Twister).

---

## How It Works

The generator uses a **lego** system — small, self-contained 100×100 SVG files that are combined at build time:

1. **Background legos** (`assets/svg/legos/backgrounds/`) define the icon shape (circle, filter badge, tags badge, tiki variants, etc.). They use placeholder fill/stroke colors (`rgb(11,11,11)` for fill, `rgb(111,111,111)` for stroke).
2. **Tool legos** (`assets/svg/legos/tools/`) define the foreground glyph (guitar, midi, amp, numbers 1–9, etc.). They use a placeholder fill color (`rgb(222,222,222)`).
3. **Wrapper** (`assets/svg/legos/wrapper/`) provides the SVG `header.svg` (300×100 viewBox for toolbar sprites, enabling three icon states side-by-side) and `footer.svg`.

At generation time the script:

- Strips the XML/DOCTYPE/svg-open preamble and closing tag from each lego via `get_core()`.
- Wraps each extracted SVG fragment in a `<g transform="...">` that scales and positions it within a 300×100 canvas (toolbar) or 100×100 canvas (track).
- Replaces the placeholder RGB colors with the actual theme colors defined in `config/config.json` for each state (**off**, **over**, **on**, **track**).
- Writes composite SVG files, then converts them to PNG with CairoSVG at three toolbar scales and one track scale, cropping track icons to 64×64.

### Toolbar Icon States (300×100 sprite)

REAPER toolbar icons pack three states side by side in a single image:

| Pixel range | State | Description |
|---|---|---|
| 0–99 | **OFF** | Default / inactive |
| 100–199 | **OVER** | Mouse hover |
| 200–299 | **ON** | Active / toggled on |

### Track Icons (64×64 single frame)

Track icons use a separate **track** color state and are rendered as a single 100×100 SVG, converted to PNG, then cropped to 64×64.

---

## Features

- **Modular SVG composition** — mix and match any background with any tool glyph.
- **Automatic multi-state rendering** — OFF / OVER / ON states in a single sprite for toolbar icons.
- **Multiple PNG sizes** — exports at 3 scales for toolbar icons and 64×64 for track icons.
- **Theme-driven color system** — all colors configured via JSON; swap entire themes without touching SVGs.
- **Extensive color palette** — 140+ named colors available out of the box, plus custom "tiki" brand colors.
- **Auto-copy to REAPER** — optionally deploys icons directly to your REAPER Data directory.

---

## Requirements

- **macOS** (primary development/testing platform) or **Windows 10/11**
- **Python 3.10+** (Homebrew recommended on macOS)
- **REAPER** (for icon installation)

> **Note:** This script was written and tested on macOS. It uses only cross-platform Python APIs (`os.path`, `shutil`, etc.) so the code itself runs on Windows without modification — you just need to install the Cairo system library and update `reaperDataDir` in the config.

---

## Dependencies

| Package | Purpose |
|---|---|
| [CairoSVG](https://cairosvg.org/) | SVG → PNG rasterization |
| [Pillow](https://python-pillow.org/) | PNG cropping (track icons) |

### System Libraries — macOS (Homebrew)

```sh
brew install python cairo pango gdk-pixbuf libffi
```

### System Libraries — Windows

CairoSVG requires the Cairo DLL to be available on your system. The easiest options:

1. **GTK3 Runtime** — Download and install the [GTK3 runtime for Windows](https://github.com/nickvdp/gtk3-windows). This bundles Cairo and adds it to your PATH.
2. **MSYS2** — Install [MSYS2](https://www.msys2.org/), then: `pacman -S mingw-w64-x86_64-cairo`
3. **Conda** — `conda install -c conda-forge cairo`

Pillow installs cleanly on Windows via pip with no extra steps.

---

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/velocitone-reaper-toolbar-icons.git
cd velocitone-reaper-toolbar-icons
```

### 2. Create and activate a virtual environment

> **Important (macOS):** You must use **Homebrew Python**, not the macOS system Python. The system Python (`/usr/bin/python3`, typically 3.9.x) cannot find Homebrew-installed libraries like Cairo, and you'll get `OSError: no library called "cairo-2" was found` at runtime. Verify with:
> ```sh
> /opt/homebrew/bin/python3 --version   # Should show 3.10+
> ```
> If you don't have it yet: `brew install python`

**macOS / Linux:**
```sh
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```sh
pip install -r requirements.txt
```

---

## Configuration

All settings live in **`config/config.json`**. Key fields:

| Key | Description | Default |
|---|---|---|
| `themeName` | Prefix for all output filenames | `"velocitone_"` |
| `legoDir` | Subfolder under `assets/svg/` containing the lego SVGs | `"legos/"` |
| `copyFiles` | If `true`, finished PNGs are copied to your REAPER Data dir | `false` |
| `reaperDataDir` | Path to your REAPER Data directory (`~` is expanded at runtime) | `"~/Library/Application Support/REAPER/Data/"` |

> **Windows users:** Update `reaperDataDir` to your Windows REAPER path, typically:
> ```json
> "reaperDataDir": "~/AppData/Roaming/REAPER/Data/"
> ```
| `colors` | Named color palette (140+ entries) mapping names → `rgb(...)` values | *(see file)* |
| `themecolor` | Maps each icon element (background fill/stroke, icon fill) to a named color for each state (off, over, on, track) | *(see file)* |

### Default Theme Colors

| Element | OFF | OVER | ON | TRACK |
|---|---|---|---|---|
| Background fill | tiki offblack | dim grey | black | black |
| Background stroke | dark olive green | gold | lime green | steel blue |
| Icon fill | dim grey | white | white | white |

To change the theme, edit the `themecolor` section and point each state at any color name from the `colors` palette.

---

## Usage

### Run the generator

```sh
python toolbar.py
```

This is the primary entry point. It:

1. Loads `config/config.json`.
2. Ensures all output directories exist.
3. Composites every background × tool combination into SVGs.
4. Converts all SVGs to PNGs at multiple scales.
5. If `copyFiles` is `true`, copies PNGs to REAPER.

> **Note:** `copyFiles` is `false` by default so you can do a test run first and inspect the `output/` directory. When you're happy with the results, set `"copyFiles": true` in `config/config.json` and re-run to deploy icons to your REAPER Data directory.

---

## Output Files & Paths

All generated files are written under an `output/` directory (git-ignored) at the project root:

```
output/
├── svg/
│   ├── toolbar/                        # Composite 300×100 SVGs (3-state sprites)
│   │   ├── velocitone_circle.svg
│   │   ├── velocitone_circle_guitar.svg
│   │   ├── velocitone_filter_midi.svg
│   │   └── ...
│   └── track/                          # Single-frame 100×100 SVGs
│       ├── velocitone_circle.svg
│       ├── velocitone_circle_guitar.svg
│       └── ...
├── png/
│   ├── toolbar_icons/                  # ~30px tall (scale 0.3)  — REAPER default size
│   │   ├── velocitone_circle_guitar.png
│   │   ├── 150/                        # ~45px tall (scale 0.45) — 150% HiDPI
│   │   │   └── velocitone_circle_guitar.png
│   │   └── 200/                        # ~60px tall (scale 0.6)  — 200% Retina
│   │       └── velocitone_circle_guitar.png
│   └── track_icons/
│       └── Custom/                     # 64×64 track icons
│           └── velocitone_circle_guitar.png
```

### Naming convention

```
{themeName}{background}_{tool}.png
```

Example: `velocitone_circle_guitar.png` = "velocitone_" theme + "circle" background + "guitar" tool.

Background-only icons (no tool overlay) omit the tool suffix: `velocitone_circle.png`.

### REAPER copy destinations

When `copyFiles` is `true`, PNGs are copied to:

| Source | Destination |
|---|---|
| `output/png/toolbar_icons/*.png` | `{reaperDataDir}/toolbar_icons/` |
| `output/png/toolbar_icons/150/*.png` | `{reaperDataDir}/toolbar_icons/150/` |
| `output/png/toolbar_icons/200/*.png` | `{reaperDataDir}/toolbar_icons/200/` |
| `output/png/track_icons/Custom/*.png` | `{reaperDataDir}/track_icons/Custom/` |

Default REAPER Data directory on macOS:
```
/Users/chris/Library/Application Support/REAPER/Data/
```

---

## Included SVG Legos

### Backgrounds (6)

`circle` · `filter` · `tags` · `tiki_green` · `tiki_red` · `tiki_yellow`

### Tools (25)

`1` · `2` · `3` · `4` · `5` · `6` · `7` · `8` · `9` · `amp` · `audio` · `bass` · `buss` · `custom` · `folder` · `fx` · `guitar` · `midi` · `mixer` · `output` · `section` · `stem` · `tape` · `vst` · `vu`

### Total icons generated

**6 backgrounds × (25 tools + 1 background-only) = 156 icon sets**, each producing:
- 1 toolbar SVG (300×100, 3-state)
- 1 track SVG (100×100, single-state)
- 3 toolbar PNGs (default, 150%, 200%)
- 1 track PNG (64×64)

**= 780 total output files** (156 SVG toolbar + 156 SVG track + 156×3 PNG toolbar + 156 PNG track)

---

## Project Structure

```
.
├── toolbar.py                          # Primary entry point
├── main.py                             # Alternate entry point (delegates to helpers/)
├── requirements.txt                    # Python dependencies (cairosvg, pillow)
├── config/
│   └── config.json                     # All configuration: theme, colors, paths
├── helpers/
│   ├── icon_generator.py               # Orchestrates SVG composition & PNG export
│   ├── svg_utils.py                    # SVG string manipulation (get_core, wrap_svg, color replacement)
│   └── file_utils.py                   # Directory creation & PNG copy utilities
├── assets/
│   ├── css/
│   │   └── colors.css                  # CSS reference for the full color palette
│   └── svg/
│       └── legos/
│           ├── wrapper/
│           │   ├── header.svg          # SVG document open (300×100 viewBox)
│           │   └── footer.svg          # SVG document close
│           ├── backgrounds/            # Background shape SVGs (circle, filter, tags, tiki_*)
│           └── tools/                  # Tool/glyph SVGs (guitar, midi, amp, 1–9, etc.)
├── mocks/                              # Example/reference output for visual QA
│   ├── png/
│   │   ├── toolbar_icons/
│   │   │   ├── 150/
│   │   │   └── 200/
│   │   └── track_icons/
│   │       └── Custom/
│   └── svg/
│       ├── toolbar/
│       └── track/
└── .gitignore
```

---

## Adding New Icons

### New background

1. Create a 100×100 SVG in `assets/svg/legos/backgrounds/`.
2. Use `rgb(11,11,11)` for fills you want themed and `rgb(111,111,111)` for strokes.
3. Run `python toolbar.py` — it will automatically combine with all existing tools.

### New tool

1. Create a 100×100 SVG in `assets/svg/legos/tools/`.
2. Use `rgb(222,222,222)` for fills you want themed.
3. Run `python toolbar.py` — it will automatically combine with all existing backgrounds.

---

## Troubleshooting

### Cairo Library Not Found

**macOS** — If you see `OSError: no library called "cairo-2" was found`, ensure Cairo is installed via Homebrew and you are using the Homebrew Python:

```sh
which python3        # Should show /opt/homebrew/bin/python3 or similar
brew install cairo
```

Activate your virtual environment before installing dependencies and running the script.

**Windows** — The same error means the Cairo DLL is not on your system PATH. See the [System Libraries — Windows](#system-libraries--windows) section above for installation options. After installing, you may need to restart your terminal or reboot for PATH changes to take effect.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Credits

Created by Chris Lundeen for the Velocitone REAPER workflow.