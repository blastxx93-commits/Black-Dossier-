"""Visual themes for the edit engine (render_aus.py, subtitles.py, thumbnail_aus.py).

An episode picks one with "theme" in episode.json (aus_kit: A.THEME = "retro60" in the build script).
Each theme changes: accent colours (cards, rank numbers, wipes, buttons), the studio background behind graphics,
the headline/body fonts, the colour grade of the whole video and the burned-in subtitle style.
"clasico" is the original look and the default, so older episodes render exactly as before.

Fonts: Inter (engine/fonts, OFL) plus Bebas Neue, Anton, Abril Fatface, Archivo Black (Google Fonts, OFL).
"""

THEMES = {
    # the original look: yellow + red on a dark studio, Inter Black
    "clasico": {
        "accent": (255, 212, 0), "accent2": (225, 12, 6), "accent2_dark": (150, 8, 4),
        "white": (245, 245, 242), "grey": (165, 165, 170),
        "bg": (12, 12, 15), "hairline": (24, 24, 28), "glows": ((255, 190, 0), (210, 10, 5)),
        "impact": "InterDisplay-Black.otf", "body": "Inter-SemiBold.otf",
        "grade": {"contrast": 1.06, "saturation": 1.08, "gamma": 1.0, "grain": 2},
        "tone": "",
        "sub_font": "Inter SemiBold", "sub_colour": "&H0000E6FF", "sub_outline": "&H00000000", "sub_size": 44,
    },
    # 60s nostalgia: warm orange + teal, tall condensed headlines, warm faded film
    "retro60": {
        "accent": (255, 176, 59), "accent2": (0, 150, 150), "accent2_dark": (0, 95, 95),
        "white": (248, 240, 225), "grey": (190, 175, 155),
        "bg": (24, 19, 15), "hairline": (44, 36, 29), "glows": ((255, 150, 40), (0, 140, 140)),
        "impact": "BebasNeue-Regular.ttf", "body": "Inter-SemiBold.otf",
        "grade": {"contrast": 1.0, "saturation": 0.82, "gamma": 1.05, "grain": 8},
        "tone": "colorbalance=rs=0.08:gs=0.03:bs=-0.09:rm=0.06:gm=0.02:bm=-0.07:rh=0.04:bh=-0.05",
        "sub_font": "Inter SemiBold", "sub_colour": "&H00E1F0F8", "sub_outline": "&H00102030", "sub_size": 44,
    },
    # luxury / records: gold + deep red on black, serif display headlines, rich contrast, slightly desaturated
    "noir_oro": {
        "accent": (212, 175, 55), "accent2": (160, 22, 34), "accent2_dark": (100, 12, 20),
        "white": (242, 236, 220), "grey": (170, 160, 140),
        "bg": (8, 8, 10), "hairline": (30, 26, 18), "glows": ((212, 160, 40), (140, 15, 25)),
        "impact": "AbrilFatface-Regular.ttf", "body": "Inter-SemiBold.otf",
        "grade": {"contrast": 1.14, "saturation": 0.68, "gamma": 0.96, "grain": 6},
        "tone": "colorbalance=rh=0.07:gh=0.04:bh=-0.05:bs=0.02",
        "sub_font": "Inter SemiBold", "sub_colour": "&H00A0DCF0", "sub_outline": "&H00000000", "sub_size": 44,
    },
    # magazine: cyan + magenta, heavy condensed headlines, punchy colour
    "revista": {
        "accent": (0, 200, 255), "accent2": (255, 40, 120), "accent2_dark": (170, 20, 80),
        "white": (245, 248, 252), "grey": (160, 170, 185),
        "bg": (10, 14, 24), "hairline": (24, 30, 46), "glows": ((0, 170, 255), (255, 30, 110)),
        "impact": "Anton-Regular.ttf", "body": "Inter-SemiBold.otf",
        "grade": {"contrast": 1.08, "saturation": 1.15, "gamma": 1.0, "grain": 2},
        "tone": "",
        "sub_font": "Inter SemiBold", "sub_colour": "&H00FFFFFF", "sub_outline": "&H00401000", "sub_size": 44,
    },
    # old newspaper: black + white + red, near-monochrome archive grade
    "periodico": {
        "accent": (240, 236, 225), "accent2": (200, 20, 20), "accent2_dark": (130, 10, 10),
        "white": (240, 236, 225), "grey": (150, 150, 150),
        "bg": (16, 16, 16), "hairline": (34, 34, 34), "glows": ((180, 180, 180), (190, 20, 20)),
        "impact": "ArchivoBlack-Regular.ttf", "body": "Inter-SemiBold.otf",
        "grade": {"contrast": 1.12, "saturation": 0.35, "gamma": 1.0, "grain": 9},
        "tone": "",
        "sub_font": "Inter SemiBold", "sub_colour": "&H00FFFFFF", "sub_outline": "&H00000000", "sub_size": 44,
    },
}


def get(name):
    return THEMES.get(name or "clasico", THEMES["clasico"])
