import tkinter as tk
from tkinter import scrolledtext, messagebox
from pyswip import Prolog

# Inisialisasi Prolog
try:
    prolog = Prolog()
    prolog.consult("permasalahan_tanaman.pl")
    print("SWI-Prolog basis pengetahuan berhasil dimuat.")
except Exception as e:
    messagebox.showerror("Error", f"Gagal memuat SWI-Prolog atau file basis pengetahuan.\nPastikan SWI-Prolog terinstall dan plant_expert.pl ada di direktori yang sama.\nError: {e}")
    prolog = None # Set None jika gagal
    # Keluar dari aplikasi atau nonaktifkan fungsi diagnosis

class PlantDiagnoserGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Diagnosis Tanaman")

        self.symptoms = {
            "Daun menguning merata": "daun_menguning_merata",
            "Pertumbuhan terhambat": "pertumbuhan_terhambat",
            "Kehadiran serangga kecil di daun/batang": "kehadiran_serangga_kecil_di_daun",
            "Daun keriting atau melengkung": "daun_keriting_atau_melengkung",
            "Ada zat lengket di daun (honeydew)": "ada_zat_lengket_di_daun",
            "Lapisan putih seperti tepung di daun/batang": "lapisan_putih_seperti_tepung_di_daun",
            "Tanaman layu": "tanaman_layu",
            "Tanah selalu basah meskipun tidak disiram baru": "tanah_selalu_basah",
            "Akar berbau busuk": "akar_berbau_busuk",
        }

        self.symptom_vars = {}

        self.create_widgets()

    def create_widgets(self):
        # Label instruksi
        self.label = tk.Label(self.master, text="Pilih gejala yang Anda amati pada tanaman:")
        self.label.pack(pady=10)

        # Frame untuk checkboxes gejala
        self.symptom_frame = tk.Frame(self.master)
        self.symptom_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Membuat checkboxes untuk setiap gejala
        for text, atom_name in self.symptoms.items():
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.symptom_frame, text=text, variable=var, anchor='w')
            cb.pack(anchor='w')
            self.symptom_vars[atom_name] = var # Simpan variable BooleanVar dengan nama atom Prolog

        # Tombol Diagnosis
        self.diagnose_button = tk.Button(self.master, text="Diagnosa", command=self.run_diagnosis)
        # Nonaktifkan tombol jika Prolog gagal dimuat
        if prolog is None:
            self.diagnose_button.config(state=tk.DISABLED)
        self.diagnose_button.pack(pady=10)

        # Area Teks untuk Hasil Diagnosis
        self.result_label = tk.Label(self.master, text="Hasil Diagnosis:")
        self.result_label.pack()

        self.result_text = scrolledtext.ScrolledText(self.master, width=60, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=5, padx=10)
        self.result_text.config(state=tk.DISABLED) # Buat read-only

    def run_diagnosis(self):
        if prolog is None:
            messagebox.showerror("Error", "SWI-Prolog tidak berhasil dimuat. Diagnosis tidak dapat dijalankan.")
            return

        # Ambil gejala yang dipilih
        selected_symptoms_atoms = [
            atom_name for atom_name, var in self.symptom_vars.items() if var.get()
        ]

        # Tampilkan gejala yang dipilih (opsional, untuk debugging)
        print(f"Gejala yang dipilih (Prolog atoms): {selected_symptoms_atoms}")

        # Kosongkan area hasil sebelumnya
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if not selected_symptoms_atoms:
            self.result_text.insert(tk.END, "Silakan pilih setidaknya satu gejala.")
            self.result_text.config(state=tk.DISABLED)
            return

        # Format gejala menjadi string list Prolog
        prolog_symptom_list = selected_symptoms_atoms

        # Buat query Prolog
        query = f"findall(Diagnosis, diagnose({prolog_symptom_list}, Diagnosis), ListOfDiagnoses)"
        print(f"Executing query: {query}") # Debugging

        try:
            # Jalankan query
            results = list(prolog.query(query))

            # Proses hasil
            if results:
                # Hasil dari findall akan ada di 'ListOfDiagnoses' dari dictionary pertama
                diagnoses = results[0].get('ListOfDiagnoses', [])
                if diagnoses:
                    self.result_text.insert(tk.END, "Kemungkinan Diagnosis:\n")
                    # Hapus duplikat dan tampilkan
                    unique_diagnoses = sorted(list(set(diagnoses)))
                    for diag in unique_diagnoses:
                         # Hapus tanda kutip jika hasil dari Prolog berupa atom string
                        if isinstance(diag, bytes): # Pyswip bisa mengembalikan byte
                            diag = diag.decode('utf-8')
                        self.result_text.insert(tk.END, f"- {diag}\n")
                else:
                     self.result_text.insert(tk.END, "Tidak ada diagnosis yang cocok berdasarkan gejala yang dipilih.")
            else:
                 self.result_text.insert(tk.END, "Tidak ada diagnosis yang cocok berdasarkan gejala yang dipilih.")

        except Exception as e:
            self.result_text.insert(tk.END, f"Terjadi error saat menjalankan diagnosis: {e}")
            print(f"Error during Prolog query: {e}") # Debugging

        self.result_text.config(state=tk.DISABLED)


# Main loop aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantDiagnoserGUI(root)
    root.mainloop()