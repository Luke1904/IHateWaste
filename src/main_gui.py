"""
main_gui.py
-----------
Entry point for the Restaurant Inventory Analyzer desktop application.
Provides a Tkinter-based GUI that allows the user to:
    1. Load and clean a raw Excel inventory file
    2. Run various analyses on the cleaned data
    3. Display results as interactive charts or scrollable tables
"""

from data_cleaner_package.data_cleaner import table_merger, null_deleter, duplicate_deleter
from data_analysis_package.data_analyzer_first_half import weekday_income, holiday_earnings
from data_analysis_package.data_analyzer_second_half import most_popular_dishes, volume_of_dishes, dish_volume_by_day
from regex_package.regex_exception_handeling import excel_checker
import tkinter as tk
import pandas as pd
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional


# ── Colour palette ────────────────────────────────────────────────────────────
# All colours are defined here so they can be changed in one place
BG        : str = "#1a1a2e"   # main window background
PANEL     : str = "#16213e"   # sidebar and bar backgrounds
ACCENT    : str = "#e94560"   # primary accent (header, titles, clean button)
ACCENT2   : str = "#0f3460"   # secondary accent (analysis buttons, entry fields)
TEXT      : str = "#eaeaea"   # primary text colour
SUBTEXT   : str = "#a0a0b0"   # muted text (labels, section headers)
SUCCESS   : str = "#2ecc71"   # status bar text colour
WARNING   : str = "#f39c12"   # reserved for warning messages
BTN_ACTIVE: str = "#c73652"   # button colour on hover/click

# Colours assigned to bars in charts — cycles through this list
CHART_COLORS : list[str] = ["#e94560","#f39c12","#2ecc71","#3498db","#9b59b6","#1abc9c","#e67e22"]

# ── Matplotlib global styling ─────────────────────────────────────────────────
# Applied to all charts so they match the dark theme of the app
plt.rcParams.update({
    "figure.facecolor":  BG,      # chart background
    "axes.facecolor":    PANEL,   # plot area background
    "axes.edgecolor":    ACCENT2, # axis border colour
    "axes.labelcolor":   TEXT,    # axis label colour
    "xtick.color":       SUBTEXT, # x-axis tick colour
    "ytick.color":       SUBTEXT, # y-axis tick colour
    "text.color":        TEXT,    # general text colour
    "grid.color":        ACCENT2, # gridline colour
    "grid.alpha":        0.3,     # gridline transparency
})

# ── Global state ──────────────────────────────────────────────────────────────
# Stores the cleaned DataFrame after the user clicks "Clean Data"
# All analysis functions read from this variable
cleaned_df: Optional[pd.DataFrame] = None

# ── Window setup ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Restaurant Analyzer")
root.geometry("1280x840")
root.configure(bg=BG)

# ── Status bar ────────────────────────────────────────────────────────────────
# Displays feedback messages at the bottom of the window
# Packed before the body so it doesn't get squashed by expand=True
status = tk.StringVar()
status_label = tk.Label(
    root,
    textvariable=status,
    bg=PANEL,
    fg=SUCCESS,
    font=("Arial", 20),
    anchor="w",
    padx=12
)
status_label.pack(fill="x", side="bottom")

# ── Header bar ────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT, height=50)
header.pack(fill="x")
tk.Label(
    header,
    text="Restaurant Inventory Analyzer",
    bg=ACCENT,
    fg="white",
    font=("Georgia", 15, "bold")
).pack(side="left", padx=16, pady=10)

# ── File picker bar ───────────────────────────────────────────────────────────
# Allows the user to browse for their Excel file
# The selected path is stored in file_path (a Tkinter StringVar)
picker = tk.Frame(root, bg=PANEL, pady=8)
picker.pack(fill="x")

file_path = tk.StringVar()  # holds the path to the user-selected Excel file

def browse() -> None:
    """Open a file dialog filtered to .xlsx files and store the selected path."""
    path: str = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if path:
        file_path.set(path)
        status.set(f"File selected: {path}")

tk.Label(picker, text="File:", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 9)).pack(side="left", padx=(16, 4))
tk.Entry(picker, textvariable=file_path, width=70,
         bg=ACCENT2, fg=TEXT, insertbackground=TEXT,
         relief="flat", font=("Courier New", 9)).pack(side="left", padx=4, ipady=4)
tk.Button(picker, text="Browse", command=browse,
          bg=ACCENT2, fg="white", activebackground=BTN_ACTIVE,
          relief="flat", font=("Courier New", 9, "bold"),
          cursor="hand2", padx=10).pack(side="left", padx=4)

# ── Body layout ───────────────────────────────────────────────────────────────
# Splits the window into a sidebar (buttons) and a results area (charts/tables)
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=PANEL, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)  # prevents sidebar from shrinking to fit its contents

results_frame = tk.Frame(body, bg=BG)
results_frame.pack(side="left", fill="both", expand=True)

def make_btn(text: str, cmd: callable, color: str = ACCENT) -> tk.Button:
    """
    Create a styled sidebar button.

    Parameters
    ----------
    text  : str      — button label
    cmd   : callable — function to call when clicked
    color : str      — background hex colour (defaults to ACCENT)

    Returns
    -------
    tk.Button
    """
    return tk.Button(
        sidebar, text=text, command=cmd,
        bg=color, fg="white",
        activebackground=BTN_ACTIVE, activeforeground="white",
        relief="flat", font=("Courier New", 9, "bold"),
        cursor="hand2", pady=8, anchor="w", padx=12
    )

tk.Label(sidebar, text="PIPELINE", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8, "bold")).pack(pady=(18, 4))

# ── Display helpers ───────────────────────────────────────────────────────────

def show_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None
) -> None:
    """
    Render a bar chart inside results_frame.
    Clears any previously displayed content before drawing.

    Parameters
    ----------
    df     : pd.DataFrame    — data to plot
    x_col  : str             — column name for the x-axis (categories)
    y_col  : str             — column name for the y-axis (values)
    title  : str             — chart title
    xlabel : Optional[str]   — optional x-axis label (defaults to x_col)
    ylabel : Optional[str]   — optional y-axis label (defaults to y_col)
    """
    for w in results_frame.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(9, 5))
    colors: list[str] = CHART_COLORS[:len(df)]  # assign one colour per bar

    bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors, edgecolor=BG, linewidth=0.5)
    ax.bar_label(bars, fmt="%.1f", padding=3, color=TEXT, fontsize=8)  # value labels on bars
    ax.set_title(title, color=ACCENT, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.tick_params(axis="x", rotation=30)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    ax.grid(axis="y", linestyle="--")
    fig.tight_layout()

    # Embed the matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def show_table(df: pd.DataFrame) -> None:
    """
    Render a scrollable table inside results_frame using ttk.Treeview.
    Clears any previously displayed content before drawing.

    Parameters
    ----------
    df : pd.DataFrame — data to display as a table
    """
    for w in results_frame.winfo_children():
        w.destroy()

    # Apply dark styling to the Treeview widget
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.Treeview",
                    background=PANEL, foreground=TEXT,
                    rowheight=26, fieldbackground=PANEL)
    style.configure("Dark.Treeview.Heading",
                    background=ACCENT2, foreground=TEXT,
                    relief="flat", font=("Courier New", 9, "bold"))
    style.map("Dark.Treeview", background=[("selected", ACCENT)])

    cols: list[str] = list(df.columns)
    tree = ttk.Treeview(results_frame, columns=cols, show="headings", style="Dark.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=160, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", "end", values=[
            f"{v:.2f}" if isinstance(v, float) else str(v) for v in row
        ])

    # Vertical scrollbar
    vsb = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")


# ── Pipeline functions ────────────────────────────────────────────────────────

def run_clean() -> None:
    """
    Read the selected Excel file, run the full cleaning pipeline,
    and display the cleaned DataFrame as a table.
    Sets cleaned_df so analysis functions can use it.
    """
    global cleaned_df
    path: str = file_path.get()

    if not path:
        status.set("Please select a file first!")
        return

    # Validate file type — redundant since the file picker filters for .xlsx,
    # but acts as a safety net if the user types a path manually
    try:
        excel_checker(path)
    except ValueError:
        status.set("Error: Please select an Excel (.xlsx) file!")
        return

    df: pd.DataFrame = pd.read_excel(path, sheet_name=None)  # reads all sheets into a dict
    df = table_merger(df)       # merges all sheets into one DataFrame
    df = null_deleter(df)       # removes rows with missing values
    df = duplicate_deleter(df)  # removes duplicate rows
    cleaned_df = df

    status.set(f"Cleaning done!  ({len(cleaned_df):,} rows)")
    show_table(cleaned_df)


def run_weekday() -> None:
    """Compute and display average income per weekday as a bar chart."""
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result: pd.DataFrame = weekday_income(cleaned_df).reset_index()
    show_chart(result, "day", "Average income by day", "Average Income by Weekday",
               xlabel="Day", ylabel="Average Income")
    status.set("Weekday income done")


def run_holiday() -> None:
    """
    Compute holiday vs non-holiday earnings and display two side-by-side bar charts:
        - Total earnings comparison
        - Average earnings comparison
    """
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return

    result1: pd.DataFrame
    result2: pd.DataFrame
    result1, result2 = holiday_earnings(cleaned_df)
    result1 = result1.reset_index()
    result2 = result2.reset_index()

    # Map boolean values to readable labels
    result1["is_holiday"] = result1["is_holiday"].map({True: "Holiday", False: "Non-Holiday"})
    result2["is_holiday"] = result2["is_holiday"].map({True: "Holiday", False: "Non-Holiday"})

    for w in results_frame.winfo_children():
        w.destroy()

    # Split results_frame into left and right halves for the two charts
    left  = tk.Frame(results_frame, bg=BG)
    left.pack(side="left", fill="both", expand=True)
    right = tk.Frame(results_frame, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.bar(result1["is_holiday"], result1["Holiday vs non-holiday earnings"],
            color=CHART_COLORS[4:6], edgecolor=BG)
    ax1.set_title("Total Earnings", color=ACCENT, fontweight="bold")
    ax1.grid(axis="y", linestyle="--")
    fig1.tight_layout()
    FigureCanvasTkAgg(fig1, left).get_tk_widget().pack(fill="both", expand=True)

    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.bar(result2["is_holiday"], result2["Average earnings on either holiday or non-holiday"],
            color=CHART_COLORS[4:6], edgecolor=BG)
    ax2.set_title("Average Earnings", color=ACCENT, fontweight="bold")
    ax2.grid(axis="y", linestyle="--")
    fig2.tight_layout()
    FigureCanvasTkAgg(fig2, right).get_tk_widget().pack(fill="both", expand=True)

    status.set("Holiday earnings done")


def run_most_popular() -> None:
    """Compute and display the top 10 most ordered dishes as a bar chart."""
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result: pd.DataFrame = most_popular_dishes(cleaned_df).head(10)
    # Truncate long dish names so they fit on the x-axis
    result["Name of dish"] = result["Name of dish"].apply(
        lambda x: x[:20] + "..." if len(x) > 20 else x
    )
    show_chart(result, "Name of dish", "count", "Top 10 Most Popular Dishes",
               xlabel="Dish Name", ylabel="Count")
    status.set("Most popular dishes done")


def run_volume_of_dishes() -> None:
    """Compute and display total dish volume per day of the week as a bar chart."""
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result: pd.DataFrame = volume_of_dishes(cleaned_df)
    show_chart(result, "day_of_week", "count", "Dish Volume by Day",
               xlabel="Day of Week", ylabel="Count")
    status.set("Volume of dishes done")


def run_dish_volume_by_day() -> None:
    """Compute and display average order volume per dish per weekday as a table."""
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result: pd.DataFrame = dish_volume_by_day(cleaned_df).reset_index()
    show_table(result)
    status.set("Dish volume by day done")


# ── Sidebar buttons ───────────────────────────────────────────────────────────
make_btn("1. Clean Data", run_clean).pack(fill="x", padx=14, pady=4)

tk.Label(sidebar, text="ANALYSIS", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8, "bold")).pack(pady=(14, 4))
make_btn("2. Weekday Income",      run_weekday,           ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("3. Holiday Earnings",    run_holiday,           ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("4. Most Popular Dishes", run_most_popular,      ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("5. Volume of Dishes",    run_volume_of_dishes,  ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("6. Dish Volume by Day",  run_dish_volume_by_day,ACCENT2).pack(fill="x", padx=14, pady=3)

# ── Close handler ─────────────────────────────────────────────────────────────
def on_close() -> None:
    """Close all matplotlib figures and destroy the window cleanly on exit."""
    plt.close("all")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()