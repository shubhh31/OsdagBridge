# =============================================================================
# Centralized Formatting & Style System — Single Source of Truth
# All report styling constants, colors, page geometry, table formatting,
# header/footer themes, and cell paddings are defined here.
# =============================================================================

# ── Page Geometry ─────────────────────────────────────────────────────────────
PAGE_MARGIN = "1in"
PAGE_SIZE = "a4paper"
LINE_SPACING = "1.15"

# ── Colors (HTML hex, used with \definecolor) ─────────────────────────────────
COLOR_OSDAG_GREEN = "91B014"
COLOR_PASS = "000000"       # black
COLOR_FAIL = "FF0000"       # red
COLOR_WARN = "FF8C00"       # dark orange
COLOR_HEADER_BG = "E8F5E9"  # light green for table headers
COLOR_CHART_BAR = "4472C4"  # blue bars in charts
COLOR_CHART_PASS = "2E7D32" # green for UR ≤ 1.0
COLOR_CHART_FAIL = "C62828" # red for UR > 1.0
COLOR_THRESHOLD = "FF0000"  # red dashed threshold line

# ── Font Sizes ────────────────────────────────────────────────────────────────
FONT_SIZE_DOCUMENT = "12pt"
FONT_SIZE_TITLE = r"\Huge"
FONT_SIZE_SUBTITLE = r"\large"
FONT_SIZE_TABLE_HEADER = r"\textbf"
FONT_SIZE_TABLE_NOTE = r"\footnotesize"
FONT_SIZE_FOOTER_NOTE = r"\footnotesize"

# ── Table Formatting ──────────────────────────────────────────────────────────
TABLE_COL_SEP = "6pt"
TABLE_ARRAY_STRETCH = "1.12"
TABLE_RULE_WIDTH = "0.5pt"
TABLE_EXTRA_ROW_HEIGHT = "0.6pt"
TABLE_ROW_PADDING = "6pt"       # vertical padding between rows ([6pt])
TABLE_LT_PRE = "0pt"            # longtable pre-skip
TABLE_LT_POST = "6pt"           # longtable post-skip

# ── Longtable Header Repetition ───────────────────────────────────────────────
# Minimum baselines required before a table (needspace)
TABLE_NEEDSPACE_LINES = 5

# ── Chart Dimensions (inches) ─────────────────────────────────────────────────
CHART_WIDTH = 7.0
CHART_HEIGHT_UR = 4.0            # Utilization Ratio chart
CHART_HEIGHT_MATERIAL = 4.5      # Material quantity chart
CHART_DPI = 150
CHART_THRESHOLD_VALUE = 1.0      # UR threshold line

# ── Header / Footer ──────────────────────────────────────────────────────────
HEADER_RULE_HEIGHT = "1pt"
FOOTER_RULE_HEIGHT = "1pt"
FOOTER_VSPACE_DEFAULT = "-8pt"   # vertical space above footer rule
FOOTER_VSPACE_SD = "-20pt"       # when software-default note is shown

# ── Page Bottom Guard (prevents table/text bleeding into footer) ──────────────
# textheight reduction applied via geometry to leave breathing room
TEXTHEIGHT_REDUCTION = "1.2cm"

# ── Spacing ───────────────────────────────────────────────────────────────────
VSPACE_BETWEEN_TABLES = r"\vspace{1em}"
VSPACE_BEFORE_CHAPTER = "0pt"
VSPACE_AFTER_CHAPTER = "10pt"


# =============================================================================
# Helper: generate the LaTeX preamble color definitions from above constants
# =============================================================================
def latex_color_definitions():
    """Return LaTeX \\definecolor lines for all report colors."""
    return "\n".join([
        rf"\definecolor{{osdagGreen}}{{HTML}}{{{COLOR_OSDAG_GREEN}}}",
        rf"\definecolor{{headerBg}}{{HTML}}{{{COLOR_HEADER_BG}}}",
    ])


def latex_table_settings():
    """Return LaTeX commands that set global table spacing from style constants."""
    return "\n".join([
        rf"\setlength{{\tabcolsep}}{{{TABLE_COL_SEP}}}",
        rf"\renewcommand{{\arraystretch}}{{{TABLE_ARRAY_STRETCH}}}",
        rf"\setlength{{\LTpre}}{{{TABLE_LT_PRE}}}",
        rf"\setlength{{\LTpost}}{{{TABLE_LT_POST}}}",
        rf"\setlength{{\arrayrulewidth}}{{{TABLE_RULE_WIDTH}}}",
        rf"\setlength{{\extrarowheight}}{{{TABLE_EXTRA_ROW_HEIGHT}}}",
    ])
