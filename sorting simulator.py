import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Global variables
array = []
bar_colors = 'gray'
speed = 100  # milliseconds
sort_type = 'Bubble Sort'
canvas = None
bars = None
labels = None
sorting = False  # To control if sorting is active

# Function to generate a random array of 20 numbers
def generate_array():
    global array, bars, labels
    array = np.random.randint(1, 100, 20)  # 20 numbers for visualization
    ax.clear()
    bars = ax.bar(range(len(array)), array, color=bar_colors)
    labels = [ax.text(i, val + 1, str(val), ha="center", va="bottom") for i, val in enumerate(array)]
    canvas.draw()

# Function to draw the array with updated heights and labels
def draw_array(color_positions=None):
    color_positions = color_positions or {}
    for rect, label, height in zip(bars, labels, array):
        rect.set_height(height)
        rect.set_color(color_positions.get(height, bar_colors))
        label.set_y(height + 1)
        label.set_text(str(height))
    canvas.draw()

# Sorting Algorithms with after() to prevent blocking
def bubble_sort_step(i=0, j=0):
    global sorting
    if not sorting:
        return
    if i < len(array):
        if j < len(array) - i - 1:
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            draw_array({array[j]: 'blue', array[j + 1]: 'red'})
            canvas.get_tk_widget().after(speed, bubble_sort_step, i, j + 1)
        else:
            canvas.get_tk_widget().after(speed, bubble_sort_step, i + 1, 0)
    else:
        draw_array()  # Final draw with original color

def selection_sort_step(i=0, min_idx=0, j=0):
    global sorting
    if not sorting:
        return
    if i < len(array):
        if j < len(array):
            if array[j] < array[min_idx]:
                min_idx = j
            canvas.get_tk_widget().after(speed, selection_sort_step, i, min_idx, j + 1)
        else:
            array[i], array[min_idx] = array[min_idx], array[i]
            draw_array({array[i]: 'blue', array[min_idx]: 'red'})
            canvas.get_tk_widget().after(speed, selection_sort_step, i + 1, i + 1, i + 2)
    else:
        draw_array()  # Final draw with original color


def insertion_sort_step(i=1, j=0):
    global sorting
    if not sorting:
        return
    if i < len(array):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        draw_array({array[j + 1]: 'blue', key: 'red'})
        canvas.get_tk_widget().after(speed, insertion_sort_step, i + 1)
    else:
        draw_array()  # Final draw with original color

def quick_sort_step(stack=None):
    global sorting
    if not sorting:
        return
    if stack is None:
        stack = [(0, len(array) - 1)]

    if stack:
        low, high = stack.pop()
        if low < high:
            pi = partition(low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))
            draw_array({array[pi]: 'blue'})
            canvas.get_tk_widget().after(speed, quick_sort_step, stack)
    else:
        draw_array()  # Final draw with original color


def partition(low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

def heap_sort_step(n=None, i=None):
    global sorting
    if not sorting:
        return
    if n is None:
        n = len(array)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
    elif i is not None:
        if i > 0:
            array[i], array[0] = array[0], array[i]
            draw_array({array[i]: 'blue', array[0]: 'red'})
            canvas.get_tk_widget().after(speed, heap_sort_step, i - 1, None)
            heapify(i, 0)
    else:
        draw_array()  # Final draw with original color


def heapify(n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and array[i] < array[l]:
        largest = l
    if r < n and array[largest] < array[r]:
        largest = r
    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        heapify(n, largest)

# Function to start the selected sorting algorithm
def start_sorting():
    global sorting
    sorting = True
    if sort_type == 'Bubble Sort':
        bubble_sort_step()
    elif sort_type == 'Selection Sort':
        selection_sort_step()
    elif sort_type == 'Insertion Sort':
        insertion_sort_step()
    elif sort_type == 'Quick Sort':
        quick_sort_step()
    elif sort_type == 'Heap Sort':
        heap_sort_step()

def stop_sorting():
    global sorting
    sorting = False  # This will stop the ongoing sorting

# Event handler for algorithm selection
def set_sort_algorithm(algorithm):
    global sort_type
    sort_type = algorithm

# Set up the Tkinter window
root = tk.Tk()
root.title("Sorting Algorithm Visualizer with Numbers")

# Set up matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=5)

# Speed Slider
speed_var = tk.IntVar(value=100)
speed_label = tk.Label(root, text="Speed (ms)")
speed_label.grid(row=1, column=0)
speed_slider = tk.Scale(root, from_=1, to=1000, resolution=1, orient='horizontal', variable=speed_var)
speed_slider.grid(row=1, column=1)

# Color Selector
color_var = tk.StringVar(value='gray')
color_label = tk.Label(root, text="Bar Color")
color_label.grid(row=1, column=2)
color_menu = ttk.Combobox(root, textvariable=color_var, values=['gray', 'blue', 'red', 'green', 'purple'])
color_menu.grid(row=1, column=3)

# Generate Array Button
generate_button = tk.Button(root, text="Generate Array", command=generate_array)
generate_button.grid(row=2, column=0)

# Start Sort Button
sort_button = tk.Button(root, text="Start Sorting", command=start_sorting)
sort_button.grid(row=2, column=1)

# Stop Sort Button
stop_button = tk.Button(root, text="Stop Sorting", command=stop_sorting)
stop_button.grid(row=2, column=2)

# Dropdown for Sorting Algorithm Selection
sort_label = tk.Label(root, text="Algorithm")
sort_label.grid(row=2, column=3)
sort_menu = ttk.Combobox(root, values=['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Quick Sort', 'Heap Sort'])
sort_menu.set('Bubble Sort')
sort_menu.grid(row=2, column=4)
sort_menu.bind("<<ComboboxSelected>>", lambda event: set_sort_algorithm(sort_menu.get()))

# Initialize and run the window
generate_array()
root.mainloop()
