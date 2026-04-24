from data_cleaner import table_merger, null_deleter, duplicate_deleter
from data_analyzer_first_half import weekday_income, holiday_earnings
from data_analyzer_second_half import most_popular_dishes, volume_of_dishes, dish_volume_by_day
from mypackage import excel_checker
import tkinter as tk
import pandas as pd
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Colour palette
BG        = "#1a1a2e"
PANEL     = "#16213e"
ACCENT    = "#e94560"
ACCENT2   = "#0f3460"
TEXT      = "#eaeaea"
SUBTEXT   = "#a0a0b0"
SUCCESS   = "#2ecc71"
WARNING   = "#f39c12"
BTN_ACTIVE= "#c73652"

CHART_COLORS = ["#e94560","#f39c12","#2ecc71","#3498db","#9b59b6","#1abc9c","#e67e22"]

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    ACCENT2,
    "axes.labelcolor":   TEXT,
    "xtick.color":       SUBTEXT,
    "ytick.color":       SUBTEXT,
    "text.color":        TEXT,
    "grid.color":        ACCENT2,
    "grid.alpha":        0.3,
})

cleaned_df = None

# Window properties
root = tk.Tk()
root.title("Restaurant Analyzer")
root.geometry("1280x840")
root.configure(bg=BG)

# Status bar
status = tk.StringVar()
status_label = tk.Label(root, textvariable=status, bg=PANEL, fg=SUCCESS, font=("Arial", 20), anchor="w", padx=12)
status_label.pack(fill="x", side="bottom")

# Header
header = tk.Frame(root, bg=ACCENT, height=50)
header.pack(fill="x")
tk.Label(header, text="Restaurant Inventory Analyzer",
         bg=ACCENT, fg="white",
         font=("Georgia", 15, "bold")).pack(side="left", padx=16, pady=10)

# File picker
picker = tk.Frame(root, bg=PANEL, pady=8)
picker.pack(fill="x")

file_path = tk.StringVar()

def browse():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
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

# Sidebar
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=PANEL, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

results_frame = tk.Frame(body, bg=BG)
results_frame.pack(side="left", fill="both", expand=True)

def make_btn(text, cmd, color=ACCENT):
    return tk.Button(sidebar, text=text, command=cmd,
                     bg=color, fg="white",
                     activebackground=BTN_ACTIVE, activeforeground="white",
                     relief="flat", font=("Courier New", 9, "bold"),
                     cursor="hand2", pady=8, anchor="w", padx=12)

tk.Label(sidebar, text="PIPELINE", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8, "bold")).pack(pady=(18,4))

# Chart helper
def show_chart(df, x_col, y_col, title, xlabel=None,ylabel=None):
    for w in results_frame.winfo_children():
        w.destroy()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = CHART_COLORS[:len(df)]
    bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors, edgecolor=BG, linewidth=0.5)
    ax.bar_label(bars, fmt="%.1f", padding=3, color=TEXT, fontsize=8)
    ax.set_title(title, color=ACCENT, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.tick_params(axis="x", rotation=30)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment('right')
    ax.grid(axis="y", linestyle="--")
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_table(df):
    for w in results_frame.winfo_children():
        w.destroy()
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.Treeview",
                    background=PANEL, foreground=TEXT,
                    rowheight=26, fieldbackground=PANEL)
    style.configure("Dark.Treeview.Heading",
                    background=ACCENT2, foreground=TEXT,
                    relief="flat", font=("Courier New", 9, "bold"))
    style.map("Dark.Treeview", background=[("selected", ACCENT)])

    cols = list(df.columns)
    tree = ttk.Treeview(results_frame, columns=cols, show="headings", style="Dark.Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=160, anchor="center")
    for _, row in df.iterrows():
        tree.insert("", "end", values=[
            f"{v:.2f}" if isinstance(v, float) else str(v) for v in row
        ])
    vsb = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

# Cleaner function
def run_clean():
    global cleaned_df
    path = file_path.get()
    if not path:
        status.set("Please select a file first!")
        return
    try:    # This is to make sure that the file selected is an excel, even though the program only lets you input .xlsx anyway
        excel_checker(path)
    except ValueError:
        status.set("Error: Please select an Excel (.xlsx) file!")
        return
    df = pd.read_excel(path, sheet_name=None)
    df = table_merger(df)
    df = null_deleter(df)
    df = duplicate_deleter(df)
    cleaned_df = df
    status.set(f"Cleaning done!  ({len(cleaned_df):,} rows)")
    show_table(cleaned_df)

def run_weekday():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = weekday_income(cleaned_df).reset_index()
    show_chart(result, "day", "Average income by day", "Average Income by Weekday", xlabel="Day",ylabel="Number of Orders")
    status.set("Weekday income done")

def run_holiday():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result1, result2 = holiday_earnings(cleaned_df)
    result1 = result1.reset_index()
    result2 = result2.reset_index()
    result1["is_holiday"] = result1["is_holiday"].map({True: "Holiday", False: "Non-Holiday"})
    result2["is_holiday"] = result2["is_holiday"].map({True: "Holiday", False: "Non-Holiday"})
    for w in results_frame.winfo_children():
        w.destroy()
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

def run_most_popular():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = most_popular_dishes(cleaned_df).head(10)
    result["Name of dish"] = result["Name of dish"].apply(lambda x: x[:20] + "..." if len(x) > 20 else x)
    show_chart(result, "Name of dish", "count", "Top 10 Most Popular Dishes", xlabel="Name of Dish", ylabel="Count")
    status.set("Most popular dishes done")

def run_volume_of_dishes():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = volume_of_dishes(cleaned_df)
    show_chart(result, "day_of_week", "count", "Dish Volume by Day", xlabel="Day of Week", ylabel="Count")
    status.set("Volume of dishes done")

def run_dish_volume_by_day():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = dish_volume_by_day(cleaned_df).reset_index()
    show_table(result)
    status.set("Dish volume by day done")

# Buttons
make_btn("1. Clean Data",          run_clean).pack(fill="x", padx=14, pady=4)

tk.Label(sidebar, text="ANALYSIS", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8, "bold")).pack(pady=(14,4))
make_btn("2. Weekday Income",         run_weekday,         ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("3. Holiday Earnings",       run_holiday,         ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("4. Most Popular Dishes",    run_most_popular,    ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("5. Volume of Dishes",       run_volume_of_dishes,ACCENT2).pack(fill="x", padx=14, pady=3)
make_btn("6. Dish Volume by Day",     run_dish_volume_by_day,ACCENT2).pack(fill="x", padx=14, pady=3)

# Closes all matplotlib functions to approve efficiency
def on_close():
    plt.close("all")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()