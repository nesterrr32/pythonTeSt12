import tkinter as tk
from tkinter import font, ttk


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("таймер")
        self.root.geometry("700x800")
        self.root.configure(bg="#2E3440")

        self.time_left = 60  # Начальное время в секундах
        self.initial_time = 60
        self.running = False
        self.paused = False
        self.timer_id = None
 # Темы
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "bg": "#2E3440",
                "fg": "#D8DEE9",
                "button_bg": "#4C566A",
                "canvas_bg": "#2E3440",
                "progress_color": "#88C0D0",
                "circle_outline": "#D8DEE9",
                "finish_mark": "#A3BE8C",
                "expired": "#BF616A"
            },
            "light": {
                "bg": "#ECEFF4",
                "fg": "#2E3440",
                "button_bg": "#D8DEE9",
                "canvas_bg": "#ECEFF4",
                "progress_color": "#5E81AC",
                "circle_outline": "#2E3440",
                "finish_mark": "#A3BE8C",
                "expired": "#BF616A"
            }
        }

        # Шрифты
        self.custom_font = font.Font(family="Helvetica", size=40, weight="bold")
        self.small_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Метка для отображения времени
        self.label = tk.Label(root, text=self.format_time(self.time_left), font=self.custom_font,
                              fg=self.themes[self.current_theme]["fg"],
                              bg=self.themes[self.current_theme]["bg"])
        self.label.pack(pady=20)

        # Выбор длительности
        self.duration_var = tk.StringVar(value="1 мин")
        durations = ["1 мин", "5 мин", "10 мин", "15 мин", "30 мин", "60 мин"]
        self.duration_menu = ttk.Combobox(root, textvariable=self.duration_var, values=durations,
                                          state="readonly", width=10)
        self.duration_menu.pack(pady=5)
        self.duration_menu.bind('<<ComboboxSelected>>', self.on_duration_change)

        # Фреймы для регулировки времени
        self.minutes_frame = tk.Frame(root, bg=self.themes[self.current_theme]["bg"])
        self.minutes_frame.pack(pady=10)

        self.minutes_label = tk.Label(self.minutes_frame, text="Минуты:", font=self.small_font,
                                      fg=self.themes[self.current_theme]["fg"],
                                      bg=self.themes[self.current_theme]["bg"])
        self.minutes_label.pack(side=tk.LEFT, padx=10)

        self.minus_minutes_button = tk.Button(self.minutes_frame, text="−", font=self.small_font,
                                              command=lambda: self.adjust_time(-60),
                                              bg=self.themes[self.current_theme]["button_bg"],
                                              fg=self.themes[self.current_theme]["fg"])
        self.minus_minutes_button.pack(side=tk.LEFT, padx=5)

        self.plus_minutes_button = tk.Button(self.minutes_frame, text="+", font=self.small_font,
                                             command=lambda: self.adjust_time(60),
                                             bg=self.themes[self.current_theme]["button_bg"],
                                             fg=self.themes[self.current_theme]["fg"])
        self.plus_minutes_button.pack(side=tk.LEFT, padx=5)

        self.seconds_frame = tk.Frame(root, bg=self.themes[self.current_theme]["bg"])
        self.seconds_frame.pack(pady=10)

        self.seconds_label = tk.Label(self.seconds_frame, text="Секунды:", font=self.small_font,
                                      fg=self.themes[self.current_theme]["fg"],
                                      bg=self.themes[self.current_theme]["bg"])
        self.seconds_label.pack(side=tk.LEFT, padx=10)

        self.minus_seconds_button = tk.Button(self.seconds_frame, text="−", font=self.small_font,
                                              command=lambda: self.adjust_time(-1),
                                              bg=self.themes[self.current_theme]["button_bg"],
                                              fg=self.themes[self.current_theme]["fg"])
        self.minus_seconds_button.pack(side=tk.LEFT, padx=5)

        self.plus_seconds_button = tk.Button(self.seconds_frame, text="+", font=self.small_font,
                                             command=lambda: self.adjust_time(1),
                                             bg=self.themes[self.current_theme]["button_bg"],
                                             fg=self.themes[self.current_theme]["fg"])
        self.plus_seconds_button.pack(side=tk.LEFT, padx=5)

        # Кнопки управления
        self.control_frame = tk.Frame(root, bg=self.themes[self.current_theme]["bg"])
        self.control_frame.pack(pady=20)

        self.start_button = tk.Button(self.control_frame, text="Старт", command=self.start_timer,
                                      bg=self.themes[self.current_theme]["button_bg"],
                                      fg=self.themes[self.current_theme]["fg"],
                                      font=self.button_font)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(self.control_frame, text="Пауза", command=self.pause_timer,
                                      bg=self.themes[self.current_theme]["button_bg"],
                                      fg=self.themes[self.current_theme]["fg"],
                                      font=self.button_font, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.resume_button = tk.Button(self.control_frame, text="Продолжить", command=self.resume_timer,
                                       bg=self.themes[self.current_theme]["button_bg"],
                                       fg=self.themes[self.current_theme]["fg"],
                                       font=self.button_font, state=tk.DISABLED)
        self.resume_button.grid(row=0, column=2, padx=10)

        self.reset_button = tk.Button(self.control_frame, text="Сброс", command=self.reset_timer,
                                      bg=self.themes[self.current_theme]["button_bg"],
                                      fg=self.themes[self.current_theme]["fg"],
                                      font=self.button_font)
        self.reset_button.grid(row=0, column=3, padx=10)

        # Переключатель темы
        self.theme_button = tk.Button(root, text="Светлая тема", command=self.toggle_theme,
                                      bg=self.themes[self.current_theme]["button_bg"],
                                      fg=self.themes[self.current_theme]["fg"],
                                      font=self.button_font)
        self.theme_button.pack(pady=10)

        # Canvas для круга
        self.canvas = tk.Canvas(root, width=300, height=300,
                                bg=self.themes[self.current_theme]["canvas_bg"],
                                highlightthickness=0)
        self.canvas.pack(pady=20)

        # Параметры циферблата
        self.center_x = 150
        self.center_y = 150
        self.radius = 100

        # Круг для прогресса (смещён на 90°, чтобы заполнялся сверху)
        self.progress_arc = self.canvas.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=90, extent=0,
            fill=self.themes[self.current_theme]["progress_color"],
            style=tk.PIESLICE, outline=""
        )

        # Основной круг
        self.canvas.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            outline=self.themes[self.current_theme]["circle_outline"], width=3,
            tags="oval"
        )

        # Отметка в положении 12 часов
        self.canvas.create_line(
            self.center_x, self.center_y - self.radius - 10,
            self.center_x, self.center_y - self.radius + 10,
            fill=self.themes[self.current_theme]["finish_mark"], width=3
        )

        # Инициализация прогресса
        self.update_progress()

    def format_time(self, seconds):
        """Форматирует время в формат MM:SS."""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def on_duration_change(self, event=None):
        value = self.duration_var.get()
        mapping = {"1 мин": 60, "5 мин": 300, "10 мин": 600, "15 мин": 900, "30 мин": 1800, "60 мин": 3600}
        self.initial_time = mapping.get(value, 60)
        if not self.running:
            self.time_left = self.initial_time
            self.label.config(text=self.format_time(self.time_left))
            self.update_progress()

    def adjust_time(self, delta):
        """Регулирует время на указанное количество секунд."""
        if not self.running:
            self.time_left = max(0, self.time_left + delta)
            self.label.config(text=self.format_time(self.time_left))
            self.update_progress()

    def update_timer(self):
        """Обновляет таймер каждую секунду."""
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.update_progress()
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            self.paused = False
            self.label.config(text="Время вышло!")
            self.canvas.itemconfig(self.progress_arc, fill=self.themes[self.current_theme]["expired"])
            self.root.bell()  # Системный звук
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)

    def update_progress(self):
        """Обновляет заполнение прогресса."""
        if self.initial_time != 0:
            progress_ratio = (self.initial_time - self.time_left) / self.initial_time
            extent = int(progress_ratio * 360)
            # Заполняем по часовой стрелке, начиная с 90° (вверху)
            self.canvas.itemconfig(self.progress_arc, extent=-extent)

    def start_timer(self):
        """Запускает таймер."""
        if not self.running:
            if self.time_left > 0:
                self.running = True
                self.paused = False
                self.canvas.itemconfig(self.progress_arc, fill=self.themes[self.current_theme]["progress_color"])
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                self.resume_button.config(state=tk.DISABLED)
                self.update_timer()

    def pause_timer(self):
        """Ставит таймер на паузу."""
        if self.running and not self.paused:
            self.paused = True
            self.running = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

    def resume_timer(self):
        """Продолжает таймер после паузы."""
        if self.paused:
            self.paused = False
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.update_timer()

    def reset_timer(self):
        """Сбрасывает таймер."""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.running = False
        self.paused = False
        self.time_left = self.initial_time
        self.label.config(text=self.format_time(self.time_left))
        self.canvas.itemconfig(self.progress_arc, fill=self.themes[self.current_theme]["progress_color"])
        self.update_progress()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)

    def toggle_theme(self):
        """Переключает между темной и светлой темой."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_button.config(text="Темная тема")
        else:
            self.current_theme = "dark"
            self.theme_button.config(text="Светлая тема")

        # Применяем цвета темы к элементам
        theme = self.themes[self.current_theme]

        # Обновляем фон главного окна
        self.root.configure(bg=theme["bg"])

        # Обновляем метку времени
        self.label.config(bg=theme["bg"], fg=theme["fg"])

        # Обновляем фреймы
        self.minutes_frame.config(bg=theme["bg"])
        self.seconds_frame.config(bg=theme["bg"])
        self.control_frame.config(bg=theme["bg"])

        # Обновляем метки
        self.minutes_label.config(bg=theme["bg"], fg=theme["fg"])
        self.seconds_label.config(bg=theme["bg"], fg=theme["fg"])

        # Обновляем кнопки
        buttons = [
            self.minus_minutes_button, self.plus_minutes_button,
            self.minus_seconds_button, self.plus_seconds_button,
            self.start_button, self.pause_button,
            self.resume_button, self.reset_button,
            self.theme_button
        ]

        for button in buttons:
            button.config(bg=theme["button_bg"], fg=theme["fg"])

        # Обновляем canvas
        self.canvas.config(bg=theme["canvas_bg"])

        # Обновляем элементы canvas
        self.canvas.itemconfig(self.progress_arc, fill=theme["progress_color"])
        self.canvas.itemconfig("oval", outline=theme["circle_outline"])

        # Обновляем Combobox
        self.duration_menu.config(background=theme["bg"], foreground=theme["fg"])

        # Если таймер завершен, обновляем цвет для "Время вышло!"
        if self.time_left == 0:
            self.canvas.itemconfig(self.progress_arc, fill=theme["expired"])


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()