import os
import random
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
import threading
import time
import math
from moviepy import VideoFileClip 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
VIDEO_FILE = os.path.join(PROJECT_DIR, "futureHUD.mp4")
AUDIO_DIR = SCRIPT_DIR 
video_finished = threading.Event()

def play_intro_video(video_path):
    print("System Boot-Up Sequence: Initiated (Close the video window to continue)")
    try:
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            video_finished.set()
            return
        if not os.environ.get("DISPLAY"):
            print("No display found — skipping video playback.")
            video_finished.set()
            return
        clip = VideoFileClip(video_path)
        clip.preview(fps=clip.fps, audio=True)
        clip.close()
    except Exception as e:
        print(f"[MoviePy Error] Could not play video: {e}")
    finally:
        try:
            if mixer.get_init():
                mixer.quit()
        except Exception:
            pass
        print("Intro video finished. Ready to load GUI.")
        video_finished.set()

def start_boot_sequence():
    video_thread = threading.Thread(
        target=play_intro_video, 
        args=(VIDEO_FILE,),
        daemon=True
    )
    video_thread.start()
    video_finished.wait()
    time.sleep(0.3)
    try:
        mixer.quit()
        time.sleep(0.1)
        mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    except Exception as e:
        print(f"[GUI Audio Re-init Error] {e}")

class AudioPlayer:
    def __init__(self, audio_dir=AUDIO_DIR):
        self.audio_dir = audio_dir
        self.suspense = [os.path.join(audio_dir, f"suspense{i}.mp3") for i in range(1, 11)]
        self.fail = os.path.join(audio_dir, "fail.mp3")
        self.success = os.path.join(audio_dir, "success.mp3")

    def play_random_suspense(self):
        tracks = [p for p in self.suspense if os.path.exists(p)]
        if not tracks: return
        mixer.music.load(random.choice(tracks))
        mixer.music.play(-1)
    def stop_music(self):
        try: mixer.music.stop()
        except Exception: pass
    def play_fail(self):
        self.stop_music()
        if os.path.exists(self.fail):
            mixer.music.load(self.fail)
            mixer.music.play()
    def play_success(self):
        self.stop_music()
        if os.path.exists(self.success):
            mixer.music.load(self.success)
            mixer.music.play()

class SnowfallAnimation:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.snowflakes = []
        self.running = True
        self.animation_thread = None
        self.snow_symbols = ["❄", "❅", "✦", "✧", "❋", "✱", "⋄", "◆"]
        self.snow_colors = ["#47e7ff", "#87ceeb", "#b0e0e6", "#add8e6", "#e0ffff", "#f0f8ff"]
        self.start_animation()

    def create_snowflake(self):
        return {
            'x': random.uniform(-50, self.width + 50),
            'y': random.uniform(-100, -20),
            'symbol': random.choice(self.snow_symbols),
            'color': random.choice(self.snow_colors),
            'speed': random.uniform(0.5, 2.5),
            'size': random.randint(8, 24),
            'drift': random.uniform(-0.3, 0.3),
            'swing': random.uniform(0.5, 1.5),
            'swing_offset': random.uniform(0, 2 * math.pi),
            'opacity': random.uniform(0.4, 1.0),
            'canvas_id': None,
            'life_time': 0
        }
    def update_snowflakes(self):
        self.snowflakes = [s for s in self.snowflakes if s['y'] < self.height + 100]
        if len(self.snowflakes) < 50 and random.random() < 0.4:
            self.snowflakes.append(self.create_snowflake())
        for snowflake in self.snowflakes:
            snowflake['life_time'] += 0.1
            snowflake['y'] += snowflake['speed']
            swing_x = math.sin(snowflake['life_time'] * snowflake['swing'] + snowflake['swing_offset']) * 15
            snowflake['x'] += snowflake['drift'] + swing_x * 0.1
            if snowflake['canvas_id']:
                try: self.canvas.delete(snowflake['canvas_id'])
                except: pass
            try:
                snowflake['canvas_id'] = self.canvas.create_text(
                    snowflake['x'], snowflake['y'],
                    text=snowflake['symbol'],
                    fill=snowflake['color'],
                    font=("Arial", snowflake['size'], "bold"),
                    tags="snowflake"
                )
            except: pass
    def animate(self):
        while self.running:
            try:
                self.update_snowflakes()
                time.sleep(0.08)
            except: break
    def start_animation(self):
        if not self.animation_thread or not self.animation_thread.is_alive():
            self.running = True
            self.animation_thread = threading.Thread(target=self.animate, daemon=True)
            self.animation_thread.start()
    def stop_animation(self):
        self.running = False
        try: self.canvas.delete("snowflake")
        except: pass
    def update_size(self, width, height):
        self.width = width
        self.height = height

def rounded_rect(canvas, x1, y1, x2, y2, r=16, **kw):
    points = [
        x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
        x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
        x1, y2, x1, y2-r, x1, y1+r, x1, y1, x1+r, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kw)

NEON_BG = "#0c0f1c"
NEON_PANEL = "#0f1222"
NEON_CYAN = "#47e7ff"
NEON_GREEN = "#66ffb3"
NEON_PINK = "#ff5aa5"
NEON_PURPLE = "#8a7dff"
NEON_LIME = "#a7ff2e"
NEON_BUTTON_FG = "#0b1020"
NEON_BUTTON_ACTIVE_BG = "#9bf0ff"

TABLE1 = [
    ["A","B","C","D","E"],
    ["F","G","H","I","J"],
    ["K","L","M","N","O"],
    ["P","Q","R","S","T"],
    ["U","V","W","X","Y"],
    ["Z","","","",""]
]

class MindReaderGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mind Reader — Neon")
        self.geometry("1000x720")
        self.configure(bg=NEON_BG)
        self.resizable(True, True)

        total_width = 1000
        game_width = int(0.8 * total_width)
        rule_width = total_width - game_width

        self.wrapper = tk.Frame(self, bg=NEON_BG)
        self.wrapper.place(x=0, y=0, relwidth=1, relheight=1)

        self.game_frame = tk.Frame(self.wrapper, width=game_width, height=720, bg=NEON_BG)
        self.game_frame.pack(side="left", fill="both", expand=True)

        self.rule_frame = tk.Frame(self.wrapper, width=rule_width, height=720, bg="#151b2c", bd=0, highlightthickness=0)
        self.rule_frame.pack(side="right", fill="y")

        self.bg_canvas = tk.Canvas(self.game_frame, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_canvas.configure(bg=NEON_BG)
        self.snowfall_animation = None
        self.after(100, self.init_snowfall_animation)

        self.audio = AudioPlayer()
        self.audio.play_random_suspense()

        self.word_len = 0
        self.first_cols = []
        self.second_cols = []
        self.table2 = []

        self.title_label = tk.Label(self.game_frame, text="MIND READER",
                                    font=("Segoe UI Black", 32), fg=NEON_CYAN, bg=NEON_BG)
        self.title_label.pack(pady=(18, 6))

        # Main game panel IN game_frame (keep as is)
        self.panel = tk.Canvas(self.game_frame, width=game_width-40, height=500, bg=NEON_BG, highlightthickness=0)
        self.panel.pack()

        rounded_rect(self.panel, 20, 20, game_width-60, 500, r=28, fill=NEON_PANEL, outline=NEON_PURPLE, width=3)
        self.table_area = tk.Canvas(self.panel, width=game_width-100, height=330, bg=NEON_PANEL, highlightthickness=0)
        self.panel.create_window(60, 40, anchor="nw", window=self.table_area)

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self.panel, textvariable=self.input_var,  # now inside panel, not game_frame
                              font=("Segoe UI", 16), bd=0, fg="#111", justify="center")
        rounded_rect(self.panel, 180, 400, 550, 440, r=18, fill="#1a1f35", outline=NEON_CYAN, width=3)
        self.panel.create_window(410, 420, window=self.entry, width=430, height=34)

        self.btn_continue = tk.Button(self.panel, text="CONTINUE", command=self.on_continue,
                                      font=("Segoe UI Semibold", 16), fg=NEON_BUTTON_FG,
                                      bg=NEON_GREEN, activebackground="#b1ffd9",
                                      bd=0, relief="flat", cursor="hand2")
        self.btn_exit = tk.Button(self.panel, text="EXIT", command=self.on_exit,
                                  font=("Segoe UI Semibold", 16), fg=NEON_BUTTON_FG,
                                  bg="#ff7b7b", activebackground="#b43030",
                                  bd=0, relief="flat", cursor="hand2")
        rounded_rect(self.panel, 80, 445, 340, 495, r=20, fill="#163224", outline=NEON_GREEN, width=3)
        rounded_rect(self.panel, 400, 445, 680, 495, r=20, fill="#3a1620", outline="#ff6b6b", width=3)
        self.panel.create_window(210, 470, window=self.btn_continue, width=200, height=36)
        self.panel.create_window(540, 470, window=self.btn_exit, width=200, height=36)

        self._start_infinite_flicker(self.btn_continue, colors=[NEON_GREEN, NEON_CYAN, NEON_PINK, NEON_PURPLE], delay=180)
        self._start_infinite_flicker(self.btn_exit, colors=[NEON_PINK, "#ff7b7b", NEON_PURPLE, NEON_CYAN], delay=180)

        # ---- The info label appears BELOW the panel, never in it ----
        self.info = tk.Label(self.game_frame, text="Step 1: Think of a name. Enter the number of letters.",
                             font=("Segoe UI", 14), fg="#d8e1ff", bg=NEON_BG)
        self.info.pack(pady=(10, 10))

        self.col_btn_frame = tk.Frame(self.panel, bg=NEON_BG)  # place inside panel so it doesn’t overlap below!
        self.col_btns = []

        self.bind('<Return>', lambda event: self.on_continue())
        self.bind('<Configure>', self.on_window_resize)

        self.render_table1()
        self.entry.focus_set()

        # --- Rules Panel Content ---
        self.rule_title = tk.Label(self.rule_frame, text="RULES", font=("Segoe UI Black", 21),
                                   fg=NEON_PINK, bg="#151b2c")
        self.rule_title.pack(pady=(20,10), padx=6, anchor="n")

        self.rule_text = tk.Label(self.rule_frame, text=self._rules_content(),
                                  font=("Segoe UI", 13), fg=NEON_LIME, bg="#151b2c",
                                  wraplength=rule_width-28, justify="left")
        self.rule_text.pack(padx=12, anchor="n")

    def _rules_content(self):
        return (
            "1. Think of any name using only the letters shown.\n\n"
            "2. Enter the number of letters in the name.\n\n"
            "3. For each letter, choose the correct column from the main grid using the button or field.\n\n"
            "4. On the next screen, for each row, choose again the column for each letter in your name.\n\n"
            "5. The mind reader will reveal your chosen name. Try with different inputs!"
        )

    def init_snowfall_animation(self):
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            if width > 1 and height > 1:
                self.snowfall_animation = SnowfallAnimation(self.bg_canvas, width, height)
            else:
                self.after(100, self.init_snowfall_animation)
        except: pass
    
    def on_window_resize(self, event):
        if event.widget == self and self.snowfall_animation:
            self.snowfall_animation.update_size(event.width, event.height)

    def _start_infinite_flicker(self, button, colors, delay=120):
        def loop(step=0):
            color = colors[step % len(colors)]
            button.config(bg=color, activebackground=color)
            self.after(delay, lambda: loop(step + 1))
        loop()

    def render_table1(self):
        self.table_area.delete("all")
        for c in range(5):
            x = 60 + c*120
            self._neon_tile(self.table_area, x, 0, 40, 60, text=str(c+1), color=NEON_CYAN, big=True)
        for r in range(6):
            for c in range(5):
                ch = TABLE1[r][c] if TABLE1[r][c] else " "
                x = 60 + c*100
                y = 80 + r*40
                self.table_area.create_text(x+20, y+18, text=ch, fill=NEON_LIME, font=("Consolas", 20, "bold"))
        self.panel.create_text(380, 385, text="Enter your choice number", fill="#bdeaff", font=("Segoe UI Semibold", 12))
        self._show_col_buttons([])   # Hide buttons at start

    def render_table2(self):
        self.table_area.delete("all")
        total_rows = len(self.table2)
        maxc = max(len(r) for r in self.table2) if self.table2 else 0
        base_height = 330
        row_height = base_height / (total_rows + 1) if total_rows > 0 else 40
        font_size = max(12, min(22, int(row_height * 0.5)))
        for c in range(maxc):
            x = 20 + c * 105
            self._neon_tile(self.table_area, x, 0, 85, 60, text=str(c + 1), color=NEON_PINK, big=True)
        for r, row in enumerate(self.table2):
            for c, ch in enumerate(row):
                x = 40 + c * 110
                y = row_height * (r + 1)
                self.table_area.create_text(
                    x + 15, y + row_height / 2, text=ch, fill=NEON_LIME, font=("Consolas", font_size, "bold")
                )

    def _neon_tile(self, canvas, x, y, w, h, text, color=NEON_CYAN, big=False):
        rounded_rect(canvas, x, y, x+w, y+h, r=14, fill="#151b2c", outline=color, width=3)
        canvas.create_text(x+w/2, y+h/2, text=text, fill=color, font=("Segoe UI Black", 22 if big else 16))

    def _show_col_buttons(self, labels):
        for w in self.col_btns: w.destroy()
        self.col_btns.clear()
        if not labels:
            self.col_btn_frame.place_forget()
            return
        self.col_btn_frame.place(x=800, y=604)
        
        glow_colors = [NEON_CYAN, NEON_PINK, NEON_PURPLE, NEON_GREEN]
        delay_ms = 150 
        for lab in labels:
            b = tk.Button(self.col_btn_frame, text=lab, width=4, font=("Segoe UI Semibold", 13),
                fg=NEON_BUTTON_FG, bg=NEON_CYAN, activebackground=NEON_BUTTON_ACTIVE_BG, bd=0, relief="flat",
                command=lambda t=lab: self._fill_entry_and_continue(t))
            b.pack(side="left", padx=6)
            self.col_btns.append(b)
            self._start_infinite_flicker(b, colors=glow_colors, delay=delay_ms)
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=NEON_PINK))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=NEON_CYAN))

    def _fill_entry_and_continue(self, text):
        self.input_var.set(text)
        self.on_continue()

    def on_continue(self):
        if self.word_len == 0:
            raw = self.input_var.get().strip()
            if not raw.isdigit() or int(raw) <= 0:
                self.audio.play_fail()
                messagebox.showerror("Error", "Invalid number of letters.")
                self.audio.play_random_suspense()
                return
            self.word_len = int(raw)
            self.input_var.set("")
            self.info.config(text="Step 2: For each letter, type or tap the column number (1–5).")
            return

        if len(self.first_cols) < self.word_len:
            v = self.input_var.get().strip()
            self.input_var.set("")
            if v not in {"1","2","3","4","5"}:
                self.audio.play_fail()
                messagebox.showerror("Error", "Wrong choice! Game over.")
                self.word_len = 0
                self.first_cols.clear()
                self.second_cols.clear()
                self.table2 = []
                self.render_table1()
                self.info.config(text="Step 1: Think of a name. Enter the number of letters.")
                self.audio.play_random_suspense()
                return
            self.first_cols.append(v)
            if len(self.first_cols) < self.word_len:
                self.info.config(text=f"Choose column for letter {len(self.first_cols)+1} of {self.word_len}.")
                return
            self.table2 = self._build_table2_from_cols(self.first_cols)
            self.render_table2()
            self.info.config(text="Final step: For each letter's column, choose the corresponding row's column again.")
            return

        if len(self.second_cols) < self.word_len:
            v = self.input_var.get().strip()
            self.input_var.set("")
            current_row_index = len(self.second_cols)
            if current_row_index >= len(self.table2):
                self.audio.play_fail()
                messagebox.showerror("Error", "Internal game error (row not found). Restarting.")
                self.word_len = 0
                self.first_cols.clear()
                self.second_cols.clear()
                self.table2 = []
                self.render_table1()
                self.audio.play_random_suspense()
                return
            row_len = len(self.table2[current_row_index])
            if (not v.isdigit()) or not (1 <= int(v) <= row_len):
                self.audio.play_fail()
                messagebox.showerror("Error", "Wrong choice! Game over.")
                self.word_len = 0
                self.first_cols.clear()
                self.second_cols.clear()
                self.table2 = []
                self.render_table1()
                self.info.config(text="Step 1: Think of a name. Enter the number of letters.")
                self.audio.play_random_suspense()
                return
            self.second_cols.append(int(v))
            if len(self.second_cols) < self.word_len:
                next_row_index = len(self.second_cols)
                next_row_len = len(self.table2[next_row_index])
                self.info.config(text=f"Letter {next_row_index + 1} of {self.word_len}: choose column 1..{next_row_len}.")
                self._show_col_buttons([str(i+1) for i in range(next_row_len)])
                return

        letters = [self.table2[i][self.second_cols[i]-1] for i in range(self.word_len)]
        word = "".join(letters)
        self.audio.play_success()
        messagebox.showinfo("Mind Reader", f"✨ The name in your mind is: {word}")
        self.info.config(text="Thanks for playing! Press Exit to quit or type a new length to play again.")
        self._show_col_buttons([])
        self.word_len = 0
        self.first_cols.clear()
        self.second_cols.clear()
        self.table2 = []
        self.render_table1()
        self.audio.play_random_suspense()

    def _build_table2_from_cols(self, col_sequence):
        rows = []
        for col in col_sequence:
            idx = int(col) - 1
            row = [r[idx] for r in TABLE1 if r[idx]]
            rows.append(row)
        return rows

    def on_exit(self):
        if self.snowfall_animation: self.snowfall_animation.stop_animation()
        self.audio.play_success()
        self.after(700, self.destroy)
    def destroy(self):
        if self.snowfall_animation: self.snowfall_animation.stop_animation()
        super().destroy()

# Main execution block
print("Boot sequence start")
start_boot_sequence()
print("Loading game UI")
app = MindReaderGUI()
app.mainloop()
