"""WCAG rules and palette specifications, mirrored from a11yviz (R)."""

wcag_rules = {
    "version": "0.1.7",
    "wcag_version": "2.1",
    "contrast": {
        "AA":  {"text": 4.5, "nontext": 3.0},
        "AAA": {"text": 7.0, "nontext": 3.0},
    },
    "font_size": {
        "AA":  {"body": 12, "title": 12, "legend": 12, "axis_text": 10},
        "AAA": {"body": 14, "title": 14, "legend": 14, "axis_text": 12},
    },
    "tooltip": {
        "font":   "Roboto, sans-serif",
        "size":   14,
        "text":   "#f8f9fa",
        "bg":     "rgba(33,37,41,0.95)",
        "border": "#6c757d",
    },
    "overlay_presets": {
        "raw_points":    0.4,
        "overlay_point": 0.6,
        "labels":        0.7,
        "fill":          0.9,
        "ci_ribbon":     0.10,
        "ci_band":       0.15,
        "draw_order":    "arrange(desc(size_var)) before geom_point -- larger drawn first, smaller on top",
    },
    "sc_mapping": {
        "theme_a11y": [
            "1.4.3 Contrast (Minimum)",
            "1.4.11 Non-text Contrast",
            "1.4.12 Text Spacing",
        ],
        "scale_a11y_color": [
            "1.4.1 Use of Color",
        ],
        "a11y_alt_text": [
            "1.1.1 Non-text Content",
        ],
        "a11y_layout": [
            "1.4.3 Contrast (Minimum)",
            "1.4.4 Resize text",
            "1.4.11 Non-text Contrast",
        ],
    },
}

palettes = {
    "dark2_8": {
        "source":   "rcolorbrewer",
        "palette":  "Dark2",
        "n_colors": 8,
        "colors": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A",
                   "#66A61E", "#E6AB02", "#A6761D", "#666666"],
        "safe_on": "labeled",
        "purpose": "fill",
        "notes": "RColorBrewer Dark2. Two of eight fail AA on white -- pair with cell labels.",
    },
    "set2_8": {
        "source":   "rcolorbrewer",
        "palette":  "Set2",
        "n_colors": 8,
        "colors": ["#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3",
                   "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3"],
        "safe_on": "labeled",
        "purpose": "fill",
        "notes": "RColorBrewer Set2. Pastel categorical for labeled fills.",
    },
    "paired_12": {
        "source":   "rcolorbrewer",
        "palette":  "Paired",
        "n_colors": 12,
        "colors": ["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C",
                   "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00",
                   "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928"],
        "safe_on": "labeled",
        "purpose": "fill",
        "notes": "RColorBrewer Paired (light/dark pairs). Twelve categories.",
    },
    "aaa_5": {
        "source": "literal",
        "colors": ["#154E8A", "#7C2C5E", "#5C5108", "#8A3A1F", "#2D5C53"],
        "safe_on": "white",
        "purpose": "both",
        "notes": "Custom AAA-on-white categorical (deep blue / purple / olive / terracotta / teal). All five > 7.5:1 on white. Distinguishability under color-vision differences not formally validated -- pair with shape or linetype for redundant encoding (WCAG 1.4.1).",
    },
}

_rdbu_11 = ["#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7",
            "#F7F7F7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"]
_puor_11 = ["#7F3B08", "#B35806", "#E08214", "#FDB863", "#FEE0B6",
            "#F7F7F7", "#D8DAEB", "#B2ABD2", "#8073AC", "#542788", "#2D004B"]
_brbg_11 = ["#543005", "#8C510A", "#BF812D", "#DFC27D", "#F6E8C3",
            "#F5F5F5", "#C7EAE5", "#80CDC1", "#35978F", "#01665E", "#003C30"]

diverging = {
    "rdbu":      {"source": "rcolorbrewer", "colors": _rdbu_11, "positions": [10, 6, 2],
                  "safe_on": "white", "purpose": "gradient",
                  "notes": "RColorBrewer RdBu. Endpoints AA on white."},
    "puor":      {"source": "rcolorbrewer", "colors": _puor_11, "positions": [10, 6, 2],
                  "safe_on": "white", "purpose": "gradient",
                  "notes": "RColorBrewer PuOr. Endpoints AA on white. Use when red has unwanted connotation."},
    "brbg":      {"source": "rcolorbrewer", "colors": _brbg_11, "positions": [10, 6, 2],
                  "safe_on": "white", "purpose": "gradient",
                  "notes": "RColorBrewer BrBG. Brown-blue-green; endpoints AA on white."},
    "rdbu_dual": {"source": "rcolorbrewer", "colors": _rdbu_11, "positions": [9, 6, 3],
                  "safe_on": "both", "purpose": "gradient",
                  "notes": "RColorBrewer RdBu mid-saturation. Endpoints clear non-text 3:1 on white and #1a1a1a dark."},
    "puor_dual": {"source": "rcolorbrewer", "colors": _puor_11, "positions": [9, 6, 3],
                  "safe_on": "both", "purpose": "gradient",
                  "notes": "RColorBrewer PuOr mid-saturation. Endpoints clear non-text 3:1 on white and #1a1a1a dark."},
    "brbg_dual": {"source": "rcolorbrewer", "colors": _brbg_11, "positions": [9, 6, 3],
                  "safe_on": "both", "purpose": "gradient",
                  "notes": "RColorBrewer BrBG mid-saturation. Endpoints clear non-text 3:1 on white and #1a1a1a dark."},
    "coolwarm_aaa": {"source": "literal", "low": "#3b4cc0", "mid": "#ffffff", "high": "#b40426",
                     "safe_on": "white", "purpose": "gradient",
                     "notes": "Custom diverging. Both endpoints AAA on white (>7:1). Fails on dark; pick *_dual for both backgrounds."},
}

sequential = {
    "cividis": {"source": "viridislite", "option": "cividis",
                "safe_on": "both", "purpose": "gradient",
                "notes": "viridisLite cividis. Readable in greyscale; spans the full lightness range."},
    "viridis": {"source": "viridislite", "option": "viridis",
                "safe_on": "both", "purpose": "gradient",
                "notes": "viridisLite viridis (Smith & van der Walt). Perceptually uniform default."},
    "plasma":  {"source": "viridislite", "option": "plasma",
                "safe_on": "both", "purpose": "gradient",
                "notes": "viridisLite plasma. Higher dynamic range; emphasizes extremes."},
}

plotly_sequences = {
    "Plotly":  ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
                "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"],
    "D3":      ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD",
                "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"],
    "G10":     ["#3366CC", "#DC3912", "#FF9900", "#109618", "#990099",
                "#0099C6", "#DD4477", "#66AA00", "#B82E2E", "#316395"],
    "T10":     ["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#54A24B",
                "#EECA3B", "#B279A2", "#FF9DA6", "#9D755D", "#BAB0AC"],
    "Vivid":   ["#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0",
                "#24796C", "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#CC3A8E", "#A5AA99"],
    "Bold":    ["#7F3C8D", "#11A579", "#3969AC", "#F2B701", "#E73F74",
                "#80BA5A", "#E68310", "#008695", "#CF1C90", "#F97B72", "#4B4B8F", "#A5AA99"],
    "Pastel":  ["#66C5CC", "#F6CF71", "#F89C74", "#DCB0F2", "#87C55F",
                "#9EB9F3", "#FE88B1", "#C9DB74", "#8BE0A4", "#B497E7", "#D3B484", "#B3B3B3"],
}

wcag_slug = {
    "1.1.1":  "non-text-content",
    "1.3.1":  "info-and-relationships",
    "1.4.1":  "use-of-color",
    "1.4.3":  "contrast-minimum",
    "1.4.4":  "resize-text",
    "1.4.6":  "contrast-enhanced",  # W3C-set fragment id; do not rename
    "1.4.10": "reflow",
    "1.4.11": "non-text-contrast",
    "1.4.12": "text-spacing",
    "1.4.13": "content-on-hover-or-focus",
    "2.4.6":  "headings-and-labels",
    "2.4.7":  "focus-visible",
    "2.4.10": "section-headings",
    "3.1.5":  "reading-level",
    "4.1.3":  "status-messages",
}
