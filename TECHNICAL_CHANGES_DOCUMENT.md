# Technical Changes Document
## OsdagBridge LaTeX Report Generator Refactoring & Enhancements

**Candidate / GitHub:** shubhh31  
**Project:** Osdag / OsdagBridge  
**Screening Task:** LaTeX Report Generator Refactoring & Enhancements  
**Branch:** `dev`  
**Repository:** https://github.com/shubhh31/OsdagBridge  

---

### Executive Summary

The report generation module in OsdagBridge converts structural design outputs into a compiled PDF design report using PyLaTeX and LaTeX. Prior to this refactoring, the report suffered from several layout, formatting, visual, and architectural shortcomings (table headers not repeating across page breaks, footer overlap, merged load tables, absence of UR summary visualizations, lack of material charts, and scattered hardcoded style parameters).

This submission delivers a complete refactor of the report generation codebase under `src/osdagbridge/core/reports/`, addressing all 6 key scope requirements.

---

### Detailed Scope of Work & Implementation Details

#### 1. Repeated Table Headers Across Page Breaks (`LongTable` with `\endfirsthead` and `\endhead`)
- **Issue Addressed:** Multi-page tables split across page breaks without repeating column headers, degrading readability.
- **Implementation:**
  - Standardized all multi-page tables across `chap2.py`, `chap3.py`, `chap4.py`, `chap5.py`, and `chap7.py` to use PyLaTeX / LaTeX `longtable` environments.
  - Implemented explicit `\endfirsthead` and `\endhead` blocks for every table. The initial column headers are presented on the first page, and dynamically repeated at the top of every subsequent page break.
  - Added `\Needspace` / `\needspace{8\baselineskip}` threshold guards to prevent orphaned table header rows at the bottom of pages.

#### 2. Layout, Footer Overlap, and Vertical Spacing Fixes
- **Issue Addressed:** Section content, text, and table rows bled into footer margins (e.g. Page 30 footer overlap).
- **Implementation:**
  - Adjusted page geometry in `report_generator.py`:
    ```latex
    \usepackage[a4paper, margin=1in, bottom=1.2in, footskip=0.6in]{geometry}
    ```
  - Increased bottom margin buffer from `1in` to `1.2in` and set explicit `footskip=0.6in` to provide adequate clearance between the lowest table rule and the footer rule.
  - Set table layout spacing parameters centrally: `\tabcolsep=6pt`, `\arraystretch=1.12`, `\LTpre=0pt`, `\LTpost=6pt`, and `\extrarowheight=0.6pt`.
  - Added pre-table threshold constraints (`\BeforeBeginEnvironment{longtable}{\needspace{8\baselineskip}}`) ensuring a table only starts on a page if at least 8 baselines remain.

#### 3. Load & Geometry Table Refactoring (Separated Live Loads & Footway Tables)
- **Issue Addressed:** Live Loads (LL) and Footway Load in Chapter 3 were merged into an ambiguous single table.
- **Implementation in `chap3.py`:**
  - Separated vehicle live loads and footpath live loads into distinct, clearly structured PyLaTeX `longtable` environments.
  - **Vehicle Live Loads Table:** Dynamic table iterating through selected vehicles (Class A, Class 70R Wheeled/Tracked, Class AA, Class SV, Class Fatigue, and custom vehicles). Includes columns: S.N., Vehicle Class, Selected (Yes/No), Impact Factor (IRC 6 Cl. 208), and Braking Force (IRC 6 Cl. 211.2).
  - **Footway / Footpath Live Load Table:** Distinct table detailing footpath pressure value, pressure mode (IRC 6 Cl. 206.1 or custom), and design reference.

#### 4. Utilization Ratio (Demand/Capacity) Summary Visualizations
- **Issue Addressed:** Lack of graphical summary of critical design checks in Section 5.5.
- **Implementation in `chart_generator.py` and `chap5.py`:**
  - Created `generate_ur_summary_chart()` to programmatically generate bar charts summarizing the Utilization Ratio ($\text{UR} = \text{Demand} / \text{Capacity}$) across all primary structural components:
    1. Steel Plate Girders
    2. Concrete Deck Slab
    3. Cross Bracing
    4. End Diaphragms
  - **Plot Details:**
    - Y-Axis: Utilization Ratio ($\text{UR} = \text{Demand} / \text{Capacity}$).
    - Red dashed horizontal reference line at $\text{UR} = 1.0$ (`ax.axhline(y=1.0, color='r', linestyle='--')`).
    - Color-coded bars: Green for passing checks ($\text{UR} \le 1.0$), Red for failing checks ($\text{UR} > 1.0$).
  - Dynamically saved to temporary image assets during generation and embedded directly into Section 5.5 (*Overall Design Check Summary*) as a LaTeX figure.

#### 5. Material Quantity Bar Charts
- **Issue Addressed:** Bill of Materials in Chapter 7 lacked graphical take-off summaries.
- **Implementation in `chart_generator.py` and `chap7.py`:**
  - Created `generate_material_takeoff_charts()` to programmatically generate two summary visualizations from Chapter 7 data:
    1. **Structural Steel Tonnage:** Bar chart of tonnage breakdown (Girders, Cross Bracing, End Diaphragms) in MT.
    2. **Concrete Volume vs. Rebar Weight:** Dual-panel bar chart comparing concrete volume ($m^3$) and reinforcement steel weight (MT).
  - Automatically saved to the temporary assets directory during report compilation and embedded via LaTeX `figure` environments directly under Table 7.1.

#### 6. Centralized Formatting & Style System (Single Source of Truth)
- **Issue Addressed:** Hardcoded formatting parameters (colors, fonts, padding, margins) scattered across chapters.
- **Implementation:**
  - Established `src/osdagbridge/core/reports/styles.py` as the dedicated, single source of truth for all visual and layout attributes:
    - Page geometry (`PAGE_MARGIN = "1in"`, `PAGE_SIZE = "a4paper"`, `LINE_SPACING = "1.15"`)
    - Color palettes (`COLOR_OSDAG_GREEN`, `COLOR_PASS`, `COLOR_FAIL`, `COLOR_WARN`, `COLOR_HEADER_BG`, `COLOR_CHART_BAR`, `COLOR_THRESHOLD`)
    - Table formatting (`TABLE_COL_SEP`, `TABLE_ARRAY_STRETCH`, `TABLE_RULE_WIDTH`, `TABLE_EXTRA_ROW_HEIGHT`, `TABLE_ROW_PADDING`, `TABLE_NEEDSPACE_LINES`)
    - Header & Footer metrics (`HEADER_RULE_HEIGHT`, `FOOTER_RULE_HEIGHT`, `FOOTER_VSPACE_DEFAULT`)
    - Chart settings (`CHART_WIDTH`, `CHART_DPI`, `CHART_THRESHOLD_VALUE`)
  - All report generator files import formatting parameters from `styles.py`, enabling rapid global theme adjustments.

---

### Files Modified & Added

| File | Status | Description |
|------|--------|-------------|
| `src/osdagbridge/core/reports/styles.py` | **NEW** | Centralized style module & single source of truth |
| `src/osdagbridge/core/reports/chart_generator.py` | **NEW** | UR and material takeoff bar chart generation via matplotlib |
| `src/osdagbridge/core/reports/report_generator.py` | Modified | Geometry fixes, needspace guards, chart pipeline integration |
| `src/osdagbridge/core/reports/chap2.py` | Modified | Added `\endfirsthead` and `\endhead` to all longtables |
| `src/osdagbridge/core/reports/chap3.py` | Modified | Longtable headers + separated Vehicle Live Loads & Footway tables |
| `src/osdagbridge/core/reports/chap4.py` | Modified | Added `\endfirsthead` and `\endhead` to all longtables |
| `src/osdagbridge/core/reports/chap5.py` | Modified | Longtable headers + embedded UR bar chart in Section 5.5 |
| `src/osdagbridge/core/reports/chap7.py` | Modified | Longtable headers + embedded material bar charts in Chapter 7 |

---

### How to Run & Verify

1. Activate your conda environment:
   ```bash
   conda activate osdagbridge-env
   ```
2. Navigate to repository root:
   ```bash
   cd OsdagBridge
   ```
3. Run OsdagBridge:
   ```bash
   python -m osdagbridge.desktop
   ```
4. Perform bridge analysis and click **Generate Report**.
5. Observe:
   - Repeated headers across all page-spanning tables
   - Zero bleeding into footer margins
   - Clean separate Vehicle Live Load and Footway Load tables in Chapter 3
   - UR summary bar chart with red dashed threshold line at UR = 1.0 in Section 5.5
   - Material quantity charts in Chapter 7
