import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class AIJobApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Job Market Insights")
        self.root.geometry("1080x640")

        self.df = None

        self.create_widgets()

    def create_widgets(self):
        # Кнопка загрузки CSV
        self.load_button = tk.Button(self.root, text="Загрузить CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        # Информация о данных
        self.info_label = tk.Label(self.root, text="Информация о датасете появится здесь")
        self.info_label.pack(pady=10)

        # Фильтры
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(pady=10)

        tk.Label(self.filter_frame, text="Фильтр по категории:").grid(row=0, column=0)
        self.category_cb = ttk.Combobox(self.filter_frame, state="readonly")
        self.category_cb.grid(row=0, column=1)

        tk.Label(self.filter_frame, text="Фильтр по региону:").grid(row=1, column=0)
        self.region_cb = ttk.Combobox(self.filter_frame, state="readonly")
        self.region_cb.grid(row=1, column=1)

        tk.Label(self.filter_frame, text="Фильтр по размеру:").grid(row=2, column=0)
        self.company_cb = ttk.Combobox(self.filter_frame, state="readonly")
        self.company_cb.grid(row=2, column=1)

        tk.Label(self.filter_frame, text="Фильтр по внедрению ИИ:").grid(row=3, column=0)
        self.ai_cb = ttk.Combobox(self.filter_frame, state="readonly")
        self.ai_cb.grid(row=3, column=1)

        # Кнопка фильтрации
        self.filter_button = tk.Button(self.filter_frame, text="Применить фильтры", command=self.apply_filters)
        self.filter_button.grid(row=5, columnspan=2, pady=5)

        # Кнопка рекомендаций
        self.recommend_button = tk.Button(self.root, text="Вывод рекомендаций", command=self.show_recommendations)
        self.recommend_button.pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill=tk.BOTH)

    def load_csv(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            self.df.columns = self.df.columns.str.lower().str.replace(" ", "_")

            self.info_label.config(text=f"Строк: {self.df.shape[0]}, Столбцов: {self.df.shape[1]}")

            # Настройка выпадающих списков
            if 'job_title' in self.df.columns:
                self.category_cb['values'] = [''] + sorted(self.df['job_title'].dropna().unique().tolist())
            if 'location' in self.df.columns:
                self.region_cb['values'] = [''] + sorted(self.df['location'].dropna().unique().tolist())
            if 'company_size' in self.df.columns:
                self.company_cb['values'] = [''] + sorted(self.df['company_size'].dropna().unique().tolist())
            if 'ai_adoption_level' in self.df.columns:
                self.ai_cb['values'] = [''] + sorted(self.df['ai_adoption_level'].dropna().unique().tolist())

            self.show_table(self.df)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def apply_filters(self):
        if self.df is None:
            return
        filtered_df = self.df.copy()

        category = self.category_cb.get()
        region = self.region_cb.get()
        company = self.company_cb.get()
        ai = self.ai_cb.get()

        if category:
            filtered_df = filtered_df[filtered_df['job_title'] == category]
        if region:
            filtered_df = filtered_df[filtered_df['location'] == region]
        if company:
            filtered_df = filtered_df[filtered_df['job_title'] == company]
        if ai:
            filtered_df = filtered_df[filtered_df['ai_adoption_level'] == ai]

        self.show_table(filtered_df)

    def show_table(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = list(data.columns)
        self.tree["show"] = "headings"

        for col in data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def show_recommendations(self):
        rec_window = tk.Toplevel(self.root)
        rec_window.title("Рекомендации")
        rec_window.geometry("400x300")

        text = tk.Text(rec_window, wrap=tk.WORD)
        text.insert(tk.END, (
            "1. Развивайте технические навыки, особенно в области Python, SQL и анализа данных.\n"
            "2. Следите за трендами: переходите из уязвимых профессий в растущие сегменты.\n"
            "3. Ищите вакансии в компаниях, активно внедряющих ИИ — они предлагают больше возможностей и рост зарплат."
        ))
        text.pack(expand=True, fill=tk.BOTH)

if __name__ == '__main__':
    root = tk.Tk()
    app = AIJobApp(root)
    root.mainloop()