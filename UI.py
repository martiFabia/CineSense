import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import shutil
import os

# Folder where CSV files are stored
CSV_FOLDER = "Review/Final"

# Create main window
root = tk.Tk()
root.title("CineSense - Decoding Audience Insights, Shaping Better Films")
root.geometry("900x800")
root.resizable(False, False)

# Modern style with ttk
style = ttk.Style(root)
style.configure("TButton", font=("Helvetica", 14), padding=(10, 10), foreground="black")
style.map("TButton", background=[("active", "#45a049")], foreground=[("!disabled", "black")])

# Main frame (global container)
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

# --- TOP FRAME: Input, buttons, log, and results ---
top_frame = ttk.Frame(frame)
top_frame.pack(side="top", fill="x", padx=10, pady=10)

# Title
title_label = ttk.Label(top_frame, text="🎬 CineSense - Decoding Audience Insights, Shaping Better Films", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Genre input field
genre_label = ttk.Label(top_frame, text="Enter the movie genre you want to analyze:", font=("Helvetica", 15))
genre_label.pack(pady=5)

genre_entry = ttk.Entry(top_frame, width=50, font=("Helvetica", 16))
genre_entry.pack(pady=5)

# Button frame (horizontal layout)
button_frame = ttk.Frame(top_frame)
button_frame.pack(pady=10)

# Button to search for CSV and start processing
search_button = ttk.Button(button_frame, text="🔍 Find and Process", style="TButton", command=lambda: find_csv_and_process())
search_button.pack(side="left", padx=5)

# Button to download PDF (not displayed initially)
download_button = ttk.Button(button_frame, text="📥 Download PDF Report", style="TButton", command=lambda: download_pdf())

# Label to display the result
result_label = ttk.Label(top_frame, text="", font=("Helvetica", 12))
result_label.pack(pady=5)

# LOG AREA WITH SCROLLBAR
log_frame = tk.Frame(top_frame)
log_frame.pack(expand=False, fill="both", pady=10)

log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(log_frame, height=10, width=80, state="disabled", font=("Helvetica", 15),
                    yscrollcommand=log_scroll.set, wrap="word")
log_text.pack(expand=True, fill="both")
log_scroll.config(command=log_text.yview)

# --- BOTTOM FRAME: Scrollable images ---
bottom_frame = ttk.Frame(frame)
bottom_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Canvas for images
image_canvas = tk.Canvas(bottom_frame, height=300)
image_canvas.pack(side="top", fill="both", expand=True)

# Horizontal scrollbar for canvas
image_scrollbar = tk.Scrollbar(bottom_frame, orient="horizontal", command=image_canvas.xview)
image_scrollbar.pack(side="bottom", fill="x")
image_canvas.configure(xscrollcommand=image_scrollbar.set)

# Internal frame inside the canvas to hold images
image_frame = tk.Frame(image_canvas, bg="black")
image_window = image_canvas.create_window((0, 0), window=image_frame, anchor="nw")

def update_scroll_region(event=None):
    image_canvas.configure(scrollregion=image_canvas.bbox("all"))

image_frame.bind("<Configure>", update_scroll_region)

# Function to update log messages
def log_message(message):
    log_text.configure(state="normal")
    log_text.insert(tk.END, message + "\n")
    log_text.configure(state="disabled")
    log_text.see(tk.END)

# Function to show the download button
def show_download_button():
    if not download_button.winfo_ismapped():
        download_button.pack(side="left", padx=5)
    download_button.lift()

# Function to complete the processing
def finish_processing():
    log_message("✅ Analysis completed. You can download the PDF report.")
    result_label.configure(text="✅ Analysis completed.")
    show_download_button()

# Function to display images one by one every 2 seconds
def display_next_image(index, image_files):
    if index < len(image_files):
        img_path = image_files[index]
        try:
            img = Image.open(img_path)
            try:
                resample_mode = Image.Resampling.LANCZOS
            except AttributeError:
                resample_mode = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
            img = img.resize((250, 250), resample_mode)
            img_photo = ImageTk.PhotoImage(img)
            label = tk.Label(image_frame, image=img_photo, bg="black")
            label.image = img_photo  # Keep reference to avoid garbage collection
            label.pack(side="left", padx=10, pady=10)
        except Exception as e:
            log_message(f"Error loading image {img_path}: {e}")
        image_canvas.update_idletasks()
        image_canvas.configure(scrollregion=image_canvas.bbox("all"))
        image_canvas.xview_moveto(0)
        # Schedule next image display after 2000ms (2 seconds)
        root.after(2000, lambda: display_next_image(index+1, image_files))
    else:
        # After all images are displayed, call finish_processing()
        finish_processing()

# Function to load and display images sequentially
def show_images_sequentially(genre):
    img_folder = os.path.join("Grafici", genre)
    if not os.path.exists(img_folder):
        messagebox.showerror("Error", f"❌ No image folder found for genre '{genre}'.")
        return

    image_files = [os.path.join(img_folder, f)
                   for f in os.listdir(img_folder)
                   if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not image_files:
        messagebox.showerror("Error", f"❌ No images found in '{img_folder}'.")
        return

    # Remove any previous images
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Start sequential image display
    display_next_image(0, image_files)

# Function to "process" the CSV file (simulation)
def process_reviews(csv_file, genre):
    log_message(f"✅ File found: {csv_file}")
    root.after(1000, lambda: log_message(f"🔄 Processing file '{csv_file}' for genre '{genre}'..."))
    root.after(2000, lambda: show_images_sequentially(genre))

REPORTS_FOLDER = "Report"

def download_pdf():
    genre = genre_entry.get().strip()  # Get user-entered genre
    if not genre:
        messagebox.showerror("Error", "Please enter a movie genre before downloading the PDF.")
        return

    # Construct file name based on genre
    pdf_source = os.path.join(REPORTS_FOLDER, f"{genre}_Analysis.pdf")  

    if not os.path.exists(pdf_source):
        messagebox.showerror("Error", f"Report not found for genre '{genre}'. Make sure the analysis was completed.")
        return

    # Set the user's Downloads folder as default save location
    downloads_folder = os.path.expanduser("~/Downloads")
    default_filename = f"Movie_Analysis_{genre}.pdf"

    # Open file dialog to choose save location
    pdf_path = filedialog.asksaveasfilename(
        initialdir=downloads_folder,
        title="Save PDF Report",
        initialfile=default_filename,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if pdf_path:
        try:
            shutil.copy(pdf_source, pdf_path)  # Copy PDF file from reports folder
            messagebox.showinfo("Success", f"PDF successfully saved to:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the PDF: {e}")

# Function to find the CSV file and process the selected genre
def find_csv_and_process():
    genre = genre_entry.get().strip().lower()
    if not genre:
        messagebox.showerror("Error", "Please enter a movie genre!")
        return

    log_message(f"🔍 Searching for file 'reviews_{genre}.csv'...")
    csv_filename = f"reviews_{genre}.csv"
    csv_path = os.path.join(CSV_FOLDER, csv_filename)

    if os.path.exists(csv_path):
        process_reviews(csv_path, genre)
    else:
        messagebox.showerror("Error", f"❌ File '{csv_filename}' not found in '{CSV_FOLDER}'.")
        log_message(f"❌ File '{csv_filename}' not found.")

# Start the UI
root.mainloop()
