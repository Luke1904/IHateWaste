from data_cleaner import table_merger, null_deleter, duplicate_deleter
from data_analyzer_first_half import weekday_income, holiday_earnings
from data_analyzer_second_half import most_popular_dishes, volume_of_dishes, dish_volume_by_day
import tkinter as tk
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

cleaned_df = None  # global variable to store the cleaned df


root = tk.Tk()
root.title("Restaurant Analyzer")
root.geometry("1280x840")  # width x height

# for a status symbol
status = tk.StringVar()
tk.Label(root, textvariable=status).pack()

def run_clean():
    global cleaned_df
    path = file_path.get()  # get the path from the browse box
    df = pd.read_excel(path, sheet_name=None)
    df = table_merger(df)
    df = null_deleter(df)
    df = duplicate_deleter(df)
    cleaned_df = df
    status.set("Cleaning done!") # sets status to "Cleaning done!"



# variable to store the file path
file_path = tk.StringVar()

def browse():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_path.set(path)

# widgets for the file picker
tk.Entry(root, textvariable=file_path, width=60).pack()
tk.Button(root, text="Browse", command=browse).pack()

def run_weekday():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = weekday_income(cleaned_df)
    result = result.reset_index()
    show_chart(result, "day", "Average income by day", "Average Income by Weekday")

def run_most_popular():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = most_popular_dishes(cleaned_df)
    result = result.head(10)
    show_chart(result, "Name of dish", "count", "Top 10 Most Popular Dishes")

def run_volume_of_dishes():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = volume_of_dishes(cleaned_df)
    show_chart(result, "day_of_week", "count", "Dish Volume by Day")

def run_holiday():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    
    result1, result2 = holiday_earnings(cleaned_df)
    result1 = result1.reset_index()
    result2 = result2.reset_index()

    for widget in results_frame.winfo_children():
        widget.destroy()

    # split results_frame into left and right
    left = tk.Frame(results_frame)
    left.pack(side="left", fill="both", expand=True)
    right = tk.Frame(results_frame)
    right.pack(side="left", fill="both", expand=True)

    # chart 1 in left
    fig1, ax1 = plt.subplots()
    ax1.bar(result1["is_holiday"], result1["Holiday vs non-holiday earnings"])
    ax1.set_title("Total Earnings")
    FigureCanvasTkAgg(fig1, left).get_tk_widget().pack(fill="both", expand=True)

    # chart 2 in right
    fig2, ax2 = plt.subplots()
    ax2.bar(result2["is_holiday"], result2["Average earnings on either holiday or non-holiday"])
    ax2.set_title("Average Earnings")
    FigureCanvasTkAgg(fig2, right).get_tk_widget().pack(fill="both", expand=True)

def show_table(df):
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    for widget in results_frame.winfo_children():
        widget.destroy()

    from tkinter import ttk
    tree = ttk.Treeview(results_frame, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(fill="both", expand=True)

def run_dish_volume_by_day():
    if cleaned_df is None:
        status.set("Please clean the data first!")
        return
    result = dish_volume_by_day(cleaned_df)
    result = result.reset_index()
    show_table(result)

# Buttons
tk.Button(root, text="1. Clean Data",         command=run_clean).pack()
tk.Button(root, text="2. Weekday Income",      command=run_weekday).pack()
tk.Button(root, text="3. Holiday Earnings",    command=run_holiday).pack()
tk.Button(root, text="4. Most Popular Dishes", command=run_most_popular).pack()
tk.Button(root, text="5. Volume of Dishes",    command=run_volume_of_dishes).pack()
tk.Button(root, text="6. Dish Volume by Day",  command=run_dish_volume_by_day).pack()

# frame for results
results_frame = tk.Frame(root)
results_frame.pack(fill="both", expand=True)

def show_chart(df, x_col, y_col, title):
    # clear whatever was displayed before
    for widget in results_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)

    # embed the chart into the tkinter window
    canvas = FigureCanvasTkAgg(fig, results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def on_close():
    # This is to close all matplotlib functions when closing the window for efficiency
    plt.close("all")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()