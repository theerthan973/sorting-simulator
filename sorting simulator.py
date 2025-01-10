import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sorting Algorithm Visualizer")
        self.root.configure(bg='#2C3E50')
        
        # Initialize variables
        self.array = []
        self.sorting = False
        self.speed = 100
        self.array_size = 30
        self.current_algorithm = None
        self.merge_steps = []
        self.quick_steps = []
        
        self.setup_ui()
        self.setup_plot()
        self.generate_array()
    
    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Controls frame
        controls = ttk.Frame(self.main_frame)
        controls.grid(row=1, column=0, pady=10)
        
        # Array size control
        ttk.Label(controls, text="Array Size:").grid(row=0, column=0, padx=5)
        self.size_var = tk.IntVar(value=30)
        ttk.Scale(controls, from_=10, to=100, variable=self.size_var,
                 orient='horizontal', length=200).grid(row=0, column=1, padx=5)
        
        # Speed control
        ttk.Label(controls, text="Speed (ms):").grid(row=0, column=2, padx=5)
        self.speed_var = tk.IntVar(value=100)
        ttk.Scale(controls, from_=1, to=500, variable=self.speed_var,
                 orient='horizontal', length=200).grid(row=0, column=3, padx=5)
        
        # Algorithm selection
        ttk.Label(controls, text="Algorithm:").grid(row=1, column=0, padx=5, pady=10)
        algorithms = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Quick Sort', 'Merge Sort']
        self.algo_var = tk.StringVar(value='Bubble Sort')
        ttk.Combobox(controls, textvariable=self.algo_var, 
                    values=algorithms).grid(row=1, column=1, padx=5, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(controls)
        button_frame.grid(row=1, column=2, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate Array", 
                  command=self.generate_array).pack(side=tk.LEFT, padx=5)
        self.start_button = ttk.Button(button_frame, text="Start Sorting", 
                                     command=self.start_sorting)
        self.start_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop", 
                  command=self.stop_sorting).pack(side=tk.LEFT, padx=5)
    
    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
    def generate_array(self):
        self.stop_sorting()
        self.array = np.random.randint(1, 100, self.size_var.get())
        self.update_plot()
    
    def update_plot(self, highlights=None):
        self.ax.clear()
        colors = ['#3498DB'] * len(self.array)
        
        if highlights:
            for idx, color in highlights.items():
                if 0 <= idx < len(colors):
                    colors[idx] = color
        
        self.ax.bar(range(len(self.array)), self.array, color=colors)
        self.ax.set_title(f'{self.algo_var.get()} Visualization')
        self.canvas.draw()

    def start_sorting(self):
        if self.sorting:
            return
        
        self.sorting = True
        self.start_button.config(state='disabled')
        algorithm = self.algo_var.get()
        
        if algorithm == 'Quick Sort':
            self.quick_steps = []
            self.prepare_quick_sort(0, len(self.array) - 1)
            self.process_quick_sort()
        elif algorithm == 'Merge Sort':
            self.merge_steps = []
            self.prepare_merge_sort(0, len(self.array) - 1)
            self.process_merge_sort()
        elif algorithm == 'Bubble Sort':
            self.bubble_sort()
        elif algorithm == 'Selection Sort':
            self.selection_sort()
        elif algorithm == 'Insertion Sort':
            self.insertion_sort()

    def prepare_quick_sort(self, low, high):
        if low < high:
            pivot_idx = self.partition(low, high)
            self.quick_steps.append(('partition', low, high, pivot_idx))
            self.prepare_quick_sort(low, pivot_idx - 1)
            self.prepare_quick_sort(pivot_idx + 1, high)

    def process_quick_sort(self, step_index=0):
        if not self.sorting:
            return
        
        if step_index < len(self.quick_steps):
            operation, low, high, pivot = self.quick_steps[step_index]
            self.update_plot({pivot: '#E74C3C', low: '#2ECC71', high: '#2ECC71'})
            self.root.after(self.speed_var.get(), 
                          lambda: self.process_quick_sort(step_index + 1))
        else:
            self.sorting_complete()

    def prepare_merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.prepare_merge_sort(left, mid)
            self.prepare_merge_sort(mid + 1, right)
            self.merge_steps.append((left, mid, right))

    def process_merge_sort(self, step_index=0):
        if not self.sorting:
            return
        
        if step_index < len(self.merge_steps):
            left, mid, right = self.merge_steps[step_index]
            self.merge(left, mid, right)
            self.update_plot({left: '#E74C3C', right: '#2ECC71', mid: '#F1C40F'})
            self.root.after(self.speed_var.get(), 
                          lambda: self.process_merge_sort(step_index + 1))
        else:
            self.sorting_complete()

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1
    
    def merge(self, left, mid, right):
        left_part = self.array[left:mid + 1].copy()
        right_part = self.array[mid + 1:right + 1].copy()
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1
            k += 1
        
        while i < len(left_part):
            self.array[k] = left_part[i]
            i += 1
            k += 1
            
        while j < len(right_part):
            self.array[k] = right_part[j]
            j += 1
            k += 1

    def bubble_sort(self, i=0, j=0):
        if not self.sorting:
            return
            
        if i < len(self.array) - 1:
            if j < len(self.array) - i - 1:
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                self.update_plot({j: '#E74C3C', j + 1: '#2ECC71'})
                self.root.after(self.speed_var.get(), 
                              lambda: self.bubble_sort(i, j + 1))
            else:
                self.root.after(self.speed_var.get(), 
                              lambda: self.bubble_sort(i + 1, 0))
        else:
            self.sorting_complete()
    
    def selection_sort(self, i=0):
        if not self.sorting:
            return
            
        if i < len(self.array) - 1:
            min_idx = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.update_plot({i: '#2ECC71', min_idx: '#E74C3C'})
            self.root.after(self.speed_var.get(), 
                          lambda: self.selection_sort(i + 1))
        else:
            self.sorting_complete()
    
    def insertion_sort(self, i=1):
        if not self.sorting:
            return
            
        if i < len(self.array):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.array[j] > key:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
            self.update_plot({i: '#2ECC71', j + 1: '#E74C3C'})
            self.root.after(self.speed_var.get(), 
                          lambda: self.insertion_sort(i + 1))
        else:
            self.sorting_complete()
    
    def stop_sorting(self):
        self.sorting = False
        self.start_button.config(state='normal')
        self.merge_steps = []
        self.quick_steps = []
        
    def sorting_complete(self):
        self.sorting = False
        self.start_button.config(state='normal')
        self.update_plot()
        messagebox.showinfo("Complete", "Sorting Complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
