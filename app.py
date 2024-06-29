import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys

def install_dependencies():
    try:
        from deep_translator import GoogleTranslator
    except ModuleNotFoundError:
        messagebox.showinfo("Installing Module", "The 'deep-translator' module is not installed. Attempting to install it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "deep-translator"])
        messagebox.showinfo("Module Installed", "The required modules have been installed successfully.")
        # Attempt to import again after installation
        from deep_translator import GoogleTranslator
    return GoogleTranslator

GoogleTranslator = install_dependencies()

import ttkbootstrap as tb

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        self.translator = GoogleTranslator()

        # Create a themed frame
        self.frame = tb.Frame(root, padding=20)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Create the input text box
        self.input_label = tb.Label(self.frame, text="Input Text:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_text = tk.Text(self.frame, height=10, width=50)
        self.input_text.grid(row=1, column=0, padx=10, pady=10)

        # Create the output text box
        self.output_label = tb.Label(self.frame, text="Translated Text:")
        self.output_label.grid(row=0, column=1, padx=10, pady=10)
        self.output_text = tk.Text(self.frame, height=10, width=50, state=tk.DISABLED)
        self.output_text.grid(row=1, column=1, padx=10, pady=10)

        # Create the source language dropdown
        self.src_lang_label = tb.Label(self.frame, text="Source Language:")
        self.src_lang_label.grid(row=2, column=0, padx=10, pady=10)
        self.src_lang = tk.StringVar()
        self.src_lang_menu = ttk.Combobox(self.frame, textvariable=self.src_lang)
        self.src_lang_menu.grid(row=3, column=0, padx=10, pady=10)

        # Create the destination language dropdown
        self.dest_lang_label = tb.Label(self.frame, text="Destination Language:")
        self.dest_lang_label.grid(row=2, column=1, padx=10, pady=10)
        self.dest_lang = tk.StringVar()
        self.dest_lang_menu = ttk.Combobox(self.frame, textvariable=self.dest_lang)
        self.dest_lang_menu.grid(row=3, column=1, padx=10, pady=10)

        # Populate dropdown menus with supported languages
        self.populate_language_menus()

        # Create the translate button
        self.translate_button = tb.Button(self.frame, text="Translate", command=self.translate_text)
        self.translate_button.grid(row=4, column=0, columnspan=2, pady=20)

    def populate_language_menus(self):
        try:
            supported_languages = self.translator.get_supported_languages(as_dict=True)
            language_names = list(supported_languages.values())

            self.src_lang_menu['values'] = language_names
            self.dest_lang_menu['values'] = language_names

            # Set default selections
            self.src_lang_menu.current(0)
            self.dest_lang_menu.current(1)  # Select the second language as default

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch supported languages: {e}")

    def translate_text(self):
        src_lang_name = self.src_lang.get()
        dest_lang_name = self.dest_lang.get()
        text = self.input_text.get("1.0", tk.END).strip()

        try:
            supported_languages = self.translator.get_supported_languages(as_dict=True)
            src_lang_code = supported_languages.get(src_lang_name)
            dest_lang_code = supported_languages.get(dest_lang_name)

            if not src_lang_code or not dest_lang_code:
                messagebox.showerror("Error", "Invalid language selection")
                return

            translation = self.translator.translate(text, source=src_lang_code, target=dest_lang_code)

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translation)
            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Translation Error", f"Translation error: {e}")

if __name__ == "__main__":
    root = tb.Window(themename="journal")
    app = TranslatorApp(root)
    root.mainloop()
