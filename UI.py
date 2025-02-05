import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Cartella dove sono memorizzati i file CSV
CSV_FOLDER = "Review/Final"

# Creazione della finestra principale
root = tk.Tk()
root.title("Movie Analysis - Report Generator")
root.geometry("900x800")
root.resizable(False, False)

# Stile moderno con ttk
style = ttk.Style(root)
style.configure("TButton", font=("Helvetica", 14), padding=(10, 10), foreground="black")
style.map("TButton", background=[("active", "#45a049")], foreground=[("!disabled", "black")])

# Frame principale (contenitore globale)
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

# --- FRAME SUPERIORE: per input, bottoni, log e risultati ---
top_frame = ttk.Frame(frame)
top_frame.pack(side="top", fill="x", padx=10, pady=10)

# Titolo
title_label = ttk.Label(top_frame, text="🎬 Movie Analysis - Report Generator", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Campo di input per il genere
genre_label = ttk.Label(top_frame, text="Inserisci il genere del film:", font=("Helvetica", 15))
genre_label.pack(pady=5)

genre_entry = ttk.Entry(top_frame, width=50, font=("Helvetica", 16))
genre_entry.pack(pady=5)

# Frame per i bottoni (disposti orizzontalmente)
button_frame = ttk.Frame(top_frame)
button_frame.pack(pady=10)

# Bottone per cercare il CSV e avviare il processo
search_button = ttk.Button(button_frame, text="🔍 Find and Process", style="TButton", command=lambda: find_csv_and_process())
search_button.pack(side="left", padx=5)

# Bottone per scaricare il PDF (inizialmente non posizionato)
download_button = ttk.Button(button_frame, text="📥 Download PDF Report", style="TButton", command=lambda: download_pdf())
# Verrà mostrato dopo il completamento dell'elaborazione

# Etichetta per mostrare il risultato
result_label = ttk.Label(top_frame, text="", font=("Helvetica", 12))
result_label.pack(pady=5)

# AREE DI LOG CON SCROLLBAR
log_frame = tk.Frame(top_frame)
log_frame.pack(expand=False, fill="both", pady=10)

log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(log_frame, height=10, width=80, state="disabled", font=("Helvetica", 15),
                    yscrollcommand=log_scroll.set, wrap="word")
log_text.pack(expand=True, fill="both")
log_scroll.config(command=log_text.yview)

# --- FRAME INFERIORE: per le immagini scrollabili ---
bottom_frame = ttk.Frame(frame)
bottom_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Canvas per le immagini
image_canvas = tk.Canvas(bottom_frame, height=300)
image_canvas.pack(side="top", fill="both", expand=True)

# Scrollbar orizzontale per il canvas
image_scrollbar = tk.Scrollbar(bottom_frame, orient="horizontal", command=image_canvas.xview)
image_scrollbar.pack(side="bottom", fill="x")
image_canvas.configure(xscrollcommand=image_scrollbar.set)

# Frame interno al canvas che ospiterà le immagini
image_frame = tk.Frame(image_canvas, bg="black")
image_window = image_canvas.create_window((0, 0), window=image_frame, anchor="nw")

def update_scroll_region(event=None):
    image_canvas.configure(scrollregion=image_canvas.bbox("all"))

image_frame.bind("<Configure>", update_scroll_region)

# Funzione per aggiornare il log
def log_message(message):
    log_text.configure(state="normal")
    log_text.insert(tk.END, message + "\n")
    log_text.configure(state="disabled")
    log_text.see(tk.END)

# Funzione per mostrare il bottone di download
def show_download_button():
    if not download_button.winfo_ismapped():
        download_button.pack(side="left", padx=5)
    download_button.lift()

# Funzione per completare l'elaborazione:
# Verrà chiamata al termine della visualizzazione di tutte le immagini.
def finish_processing():
    log_message("✅ Analisi completata. Puoi scaricare il report PDF.")
    result_label.configure(text="✅ Analisi completata.")
    show_download_button()

# Funzione che visualizza le immagini una alla volta, con un intervallo di 2 secondi
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
            label.image = img_photo  # Mantiene il riferimento per evitare la garbage collection
            label.pack(side="left", padx=10, pady=10)
        except Exception as e:
            log_message(f"Errore nel caricamento dell'immagine {img_path}: {e}")
        image_canvas.update_idletasks()
        image_canvas.configure(scrollregion=image_canvas.bbox("all"))
        image_canvas.xview_moveto(0)
        # Pianifica la visualizzazione della prossima immagine dopo 2000 millisecondi (2 secondi)
        root.after(2000, lambda: display_next_image(index+1, image_files))
    else:
        # Dopo aver visualizzato tutte le immagini, chiama finish_processing()
        finish_processing()

# Funzione per caricare le immagini e visualizzarle una alla volta
def show_images_sequentially(genre):
    img_folder = os.path.join("Grafici", genre)
    if not os.path.exists(img_folder):
        messagebox.showerror("Errore", f"❌ Nessuna cartella di immagini trovata per il genere '{genre}'.")
        return

    image_files = [os.path.join(img_folder, f)
                   for f in os.listdir(img_folder)
                   if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not image_files:
        messagebox.showerror("Errore", f"❌ Nessuna immagine trovata in '{img_folder}'.")
        return

    # Rimuove eventuali immagini precedenti
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Avvia la visualizzazione sequenziale delle immagini
    display_next_image(0, image_files)

# Funzione per "processare" il file CSV (simulazione)
def process_reviews(csv_file, genre):
    log_message(f"✅ File trovato: {csv_file}")
    # Dopo 1 secondo mostra il messaggio di elaborazione
    root.after(1000, lambda: log_message(f"🔄 Elaborazione del file '{csv_file}' per il genere '{genre}'..."))
    # Dopo 2 secondi (dopo il messaggio di elaborazione) inizia a mostrare le immagini una alla volta
    root.after(2000, lambda: show_images_sequentially(genre))

# Funzione per simulare il download del PDF
def download_pdf():
    genre = genre_entry.get().strip()
    if genre:
        log_message("📥 Download del report PDF in corso...")
        log_message(f"✅ Report PDF per '{genre}' scaricato con successo!")
    else:
        messagebox.showerror("Errore", "Nessun genere selezionato per il PDF!")

# Funzione per cercare il CSV e processare il genere selezionato
def find_csv_and_process():
    genre = genre_entry.get().strip().lower()
    if not genre:
        messagebox.showerror("Errore", "Inserisci un genere di film!")
        return

    log_message(f"🔍 Ricerca del file 'reviews_{genre}.csv'...")
    csv_filename = f"reviews_{genre}.csv"
    csv_path = os.path.join(CSV_FOLDER, csv_filename)

    if os.path.exists(csv_path):
        process_reviews(csv_path, genre)
    else:
        messagebox.showerror("Errore", f"❌ Il file '{csv_filename}' non è stato trovato in '{CSV_FOLDER}'.")
        log_message(f"❌ File '{csv_filename}' non trovato.")

# Avvio dell'interfaccia
root.mainloop()
