import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import PyPDF2
import os
import sys
import webbrowser

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        try:
            self.root.iconbitmap(resource_path("logo.ico"))
        except Exception as e:
            print(f"Icon hatası: {e}")
            pass
        
        self.bg_color = "#f0f0f0"
        self.btn_color = "#0078D7"
        self.text_color = "#ffffff"
        self.root.configure(bg=self.bg_color)

        self.pdf_list = []
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=10)

        title_label = tk.Label(header_frame, text="PDF Merger", font=("Arial", 18, "bold"), bg=self.bg_color)
        title_label.pack()

        subtitle_label = tk.Label(header_frame, text="Drag and drop files or use the buttons", font=("Arial", 10), bg=self.bg_color, fg="#555")
        subtitle_label.pack()

        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Arial", 10), activestyle='none')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop)

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10)

        btn_style = {"font": ("Arial", 10, "bold"), "width": 15, "bd": 0, "cursor": "hand2"}

        tk.Button(btn_frame, text="Add Files", bg="#28a745", fg=self.text_color, command=self.add_files, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Remove Selected", bg="#dc3545", fg=self.text_color, command=self.remove_file, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Move Up", bg="#6c757d", fg=self.text_color, command=self.move_up, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Move Down", bg="#6c757d", fg=self.text_color, command=self.move_down, **btn_style).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="MERGE PDFs", bg=self.btn_color, fg=self.text_color, font=("Arial", 12, "bold"), width=30, height=2, command=self.merge_pdfs, bd=0, cursor="hand2").pack(pady=10)

        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side=tk.BOTTOM, pady=10)
        
        link_label = tk.Label(footer_frame, text="GitHub", font=("Arial", 9, "underline"), fg="blue", bg=self.bg_color, cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self.open_github())

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith('.pdf'):
                self.pdf_list.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
            else:
                messagebox.showwarning("Error", f"{os.path.basename(f)} is not a PDF file.")

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")])
        for f in files:
            self.pdf_list.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))

    def remove_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            idx = selected_index[0]
            self.listbox.delete(idx)
            self.pdf_list.pop(idx)
        else:
            messagebox.showwarning("Warning", "Please select a file to remove.")

    def move_up(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        idx = selected_index[0]
        if idx > 0:
            text = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx-1, text)
            self.listbox.selection_set(idx-1)
            
            self.pdf_list[idx], self.pdf_list[idx-1] = self.pdf_list[idx-1], self.pdf_list[idx]

    def move_down(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        idx = selected_index[0]
        if idx < self.listbox.size() - 1:
            text = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx+1, text)
            self.listbox.selection_set(idx+1)

            self.pdf_list[idx], self.pdf_list[idx+1] = self.pdf_list[idx+1], self.pdf_list[idx]

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Warning", "No PDFs in the list to merge.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not save_path:
            return

        merger = PyPDF2.PdfMerger()
        try:
            for pdf in self.pdf_list:
                merger.append(pdf)
            
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Success", "PDF files merged successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def open_github(self):
        webbrowser.open("https://github.com/Cl0ckSkew/PDFMerger")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()