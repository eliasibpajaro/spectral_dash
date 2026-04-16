BLUE = "#4F81BD"
BLUE_DARK = "#243B55"
BLUE_MID = "#355C7D"
BLUE_LIGHT = "#DCEAF7"
BLUE_PALE = "#EEF5FC"
BLUE_GRID = "#D7E3F0"
BLUE_FILL = "rgba(79,129,189,0.20)"
TEXT_MAIN = "#2C3E50"
TEXT_SUBTLE = "#64748B"
CARD_BG = "white"
PLOT_BG = "#F8FAFC"

HEATMAP_BLUES = "Blues"

def base_layout(title=None, height=360):
    return dict(
        title=title,
        template="plotly_white",
        plot_bgcolor=PLOT_BG,
        paper_bgcolor="white",
        font=dict(color=TEXT_MAIN),
        height=height,
    )

def blue_marker(size=7, opacity=0.7):
    return dict(color=BLUE, size=size, opacity=opacity)