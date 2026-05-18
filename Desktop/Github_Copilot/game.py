import random, sys, threading, time, tkinter as tk
try:
    winsound = __import__('winsound') if sys.platform == "win32" else None
except ImportError:
    winsound = None
try:
    import numpy as np
    import simpleaudio as sa
    _SA_AVAILABLE = True
except Exception:
    np = sa = None
    _SA_AVAILABLE = False

CONFIG = {
    'colors': {'bg': "#e8f2ff", 'header': "#3a64b5", 'white': "#ffffff", 'canvas': "#d9ecff", 'game_bg': "#eef7ff", 'button': "#fff7d5", 'button_hover': "#ffe79a", 'success': "#9df29f", 'error': "#ffb3b3"},
    'fonts': {'title': ("Comic Sans MS", 24, "bold"), 'label': ("Comic Sans MS", 18, "bold"), 'text': ("Comic Sans MS", 14), 'small': ("Comic Sans MS", 12)},
    'sounds': {'correct': [660, 825, 990], 'wrong': [220, 330], 'missed': [196, 147], 'finish': [880, 660, 440], 'start': [440, 550, 660]},
    'total_q': 10, 'canvas_w': 540, 'canvas_h': 350, 'option_deltas': [-12, -9, -6, -4, -3, 3, 4, 6, 9, 12]
}

class KidsNumberMatchGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Float Adventure")
        self.configure(bg=CONFIG['colors']['bg'])
        self.geometry("580x860")
        self.resizable(False, False)
        self.current_question = self.score = self.target_number = self.correct_index = self.floating_y = 0
        self.is_playing = self.music_active = False
        self.animation_after_id = self.cloud_animation_id = None
        self.total_questions = CONFIG['total_q']
        self.progress_dots = self.cloud_items = []
        self._music_thread = self._music_stop_event = self._music_play_obj = None
        self._sa_available = _SA_AVAILABLE
        self.setup_ui()
        self.reset_game()

    def create_label(self, parent, text, bg, fg, font, **kwargs):
        return tk.Label(parent, text=text, bg=bg, fg=fg, font=font, **kwargs)

    def create_button(self, parent, text, bg, command=None, **kwargs):
        font = kwargs.pop('font', CONFIG['fonts']['label'])
        return tk.Button(parent, text=text, bg=bg, fg="white", font=font, command=command, **kwargs)

    def setup_ui(self):
        hf = tk.Frame(self, bg=CONFIG['colors']['header'], height=80)
        hf.pack(fill="x")
        self.create_label(hf, "Number Float Adventure", CONFIG['colors']['header'], "white", CONFIG['fonts']['title'], pady=16).pack(side="left", padx=20)
        self.create_label(hf, "Level 1", "#ffe58f", "#3e3a30", CONFIG['fonts']['text'], padx=14, pady=10, bd=2, relief="ridge").pack(side="right", padx=20, pady=12)

        self.start_screen_frame = tk.Frame(self, bg=CONFIG['colors']['game_bg'])
        self.start_screen_frame.pack(fill="both", expand=True)
        self.start_card = tk.Frame(self.start_screen_frame, bg=CONFIG['colors']['white'], bd=6, relief="ridge")
        self.start_card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=520)

        self.start_title = self.create_label(self.start_card, "🧠 Ready for a Number Adventure?", CONFIG['colors']['white'], "#2f3e79", CONFIG['fonts']['title'], wraplength=460, justify="center")
        self.start_title.pack(pady=(40, 16))
        self.start_desc = self.create_label(self.start_card, "Watch the number float up and tap the right answer before it disappears!", CONFIG['colors']['white'], "#515f8a", CONFIG['fonts']['text'], wraplength=460, justify="center")
        self.start_desc.pack(pady=(0, 28))
        self.start_button = self.create_button(self.start_card, "Start Game", "#ff7f3f", self.start_game, bd=0, relief="raised", activebackground="#ff9b6a", font=("Comic Sans MS", 18, "bold"))
        self.start_button.pack(pady=(0, 28), ipadx=12, ipady=8)
        self.create_label(self.start_card, "10 questions · Only correct answers count", CONFIG['colors']['white'], "#5c6b89", CONFIG['fonts']['small']).pack()

        self.game_frame = tk.Frame(self, bg=CONFIG['colors']['game_bg'])
        self.canvas = tk.Canvas(self.game_frame, width=CONFIG['canvas_w'], height=CONFIG['canvas_h'], bg=CONFIG['colors']['canvas'], bd=0, highlightthickness=4, highlightbackground="#9dc6ff", relief="ridge")
        self.canvas.pack(pady=(18, 4))
        self.draw_background_decorations()

        pf = tk.Frame(self.game_frame, bg=CONFIG['colors']['game_bg'])
        pf.pack(fill="x", padx=18, pady=(0, 10))
        self.question_label = self.create_label(pf, "Question 0 / 10", CONFIG['colors']['game_bg'], "#35377b", CONFIG['fonts']['label'])
        self.question_label.pack(side="left")
        self.score_label = self.create_label(pf, "Score: 0", CONFIG['colors']['game_bg'], "#1a6f4e", CONFIG['fonts']['label'])
        self.score_label.pack(side="right")

        self.progress_dots_frame = tk.Frame(self.game_frame, bg=CONFIG['colors']['game_bg'])
        self.progress_dots_frame.pack(fill="x", padx=18, pady=(0, 10))

        af = tk.Frame(self.game_frame, bg=CONFIG['colors']['game_bg'])
        af.pack(pady=10)
        self.option_buttons = []
        for idx in range(4):
            btn = tk.Button(af, text="", width=14, height=2, bg=CONFIG['colors']['button'], fg="#2d2f4f", activebackground="#ffd768", activeforeground="#2d2f4f", font=("Comic Sans MS", 16, "bold"), relief="raised", bd=4, command=lambda index=idx: self.check_answer(index), state="disabled")
            btn.grid(row=idx // 2, column=idx % 2, padx=14, pady=12)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CONFIG['colors']['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=CONFIG['colors']['button']))
            self.option_buttons.append(btn)

        self.status_label = self.create_label(self.game_frame, "Press START to begin your adventure!", CONFIG['colors']['game_bg'], "#4a5c82", CONFIG['fonts']['text'], wraplength=520, justify="center", pady=10)
        self.status_label.pack(pady=(6, 10))

        tc = tk.Frame(self.game_frame, bg=CONFIG['colors']['white'], bd=5, relief="ridge")
        tc.pack(fill="x", padx=18, pady=(0, 18))
        self.create_label(tc, "Watch the floating number carefully and choose the correct answer before it escapes!", CONFIG['colors']['white'], "#556582", CONFIG['fonts']['small'], wraplength=500, justify="center", pady=12).pack(padx=12)

    def draw_background_decorations(self):
        self.cloud_items = []
        self.canvas.delete("decor")
        self.canvas.create_rectangle(0, 0, CONFIG['canvas_w'], CONFIG['canvas_h'], fill=CONFIG['colors']['canvas'], outline="", tags="decor")
        for _ in range(10):
            x, y, sz = random.randint(20, 520), random.randint(20, 300), random.randint(22, 60)
            self.canvas.create_oval(x, y, x + sz, y + sz, fill=random.choice(["#fff1a0", "#c6eeff", "#ffbce5", "#c3ffc9"]), outline="", tags="decor")
        for _ in range(7):
            self.canvas.create_text(random.randint(40, 500), random.randint(30, 280), text=random.choice(["⭐", "✨", "🌟"]), font=("Segoe UI Emoji", random.randint(18, 32)), fill=random.choice(["#f49e42", "#8c4dff", "#4db8ff"]), tags="decor")
        for x, y in [(70, 70), (360, 40), (200, 120)]:
            self.cloud_items.extend([self.canvas.create_oval(x, y, x + 120, y + 60, fill=CONFIG['colors']['white'], outline="", tags="decor"), 
                                      self.canvas.create_oval(x + 20, y - 20, x + 130, y + 50, fill=CONFIG['colors']['white'], outline="", tags="decor")])
        self.canvas.create_text(270, 170, text="🎈", font=("Segoe UI Emoji", 56), fill="#7d5cff", tags="decor")

    def draw_progress_dots(self):
        for w in self.progress_dots_frame.winfo_children():
            w.destroy()
        self.progress_dots = []
        for _ in range(self.total_questions):
            dc = tk.Canvas(self.progress_dots_frame, width=26, height=26, bg=CONFIG['colors']['game_bg'], highlightthickness=0)
            dc.pack(side="left", padx=2)
            self.progress_dots.append((dc, dc.create_oval(4, 4, 22, 22, fill="#cbd6ff", outline="#aac0ff")))

    def update_progress_dots(self):
        for idx, (dc, oval) in enumerate(self.progress_dots):
            dc.itemconfig(oval, fill="#6d8cff" if idx < self.current_question else "#cbd6ff")

    def animate_clouds(self):
        if not self.is_playing:
            return
        for item in self.cloud_items:
            self.canvas.move(item, -1, 0)
            coords = self.canvas.coords(item)
            if coords and coords[2] < 0:
                self.canvas.move(item, 580, 0)
        self.cloud_animation_id = self.after(80, self.animate_clouds)

    def start_game(self):
        if self.is_playing:
            return
        self.score = 0
        self.current_question = 0
        self.score_label.config(text="Score: 0")
        self.start_button.config(state="disabled")
        self.status_label.config(text="Catch the floating number!", fg="#3c3b98")
        self.enable_answer_buttons(True)
        self.show_game_screen()
        self.play_sound("start")
        self.start_background_music()
        self.next_question()

    def reset_game(self):
        self.cancel_animation()
        self.stop_background_music()
        self.is_playing = False
        self.current_question = 0
        self.score = 0
        self.target_number = 0
        self.correct_index = 0
        self.score_label.config(text="Score: 0")
        self.question_label.config(text=f"Question 0 / {self.total_questions}")
        self.status_label.config(text="Press START to begin your adventure!", fg="#4a5c82")
        self.start_title.config(text="🧠 Ready for a Number Adventure?")
        self.start_desc.config(text="Watch the number float up and tap the right answer before it disappears!")
        self.start_button.config(state="normal", text="Start Game")
        self.canvas.delete("float")
        self.enable_answer_buttons(False)
        self.draw_background_decorations()
        # Progress dots are drawn after UI widgets are created (see setup_ui flow)
        self.show_start_screen()
        for button in self.option_buttons:
            button.config(text="", bg="#fff7d5")

    def enable_answer_buttons(self, enable: bool):
        state = "normal" if enable else "disabled"
        for button in self.option_buttons:
            button.config(state=state)

    def show_start_screen(self):
        self.game_frame.pack_forget()
        self.start_screen_frame.pack(fill="both", expand=True)

    def show_game_screen(self):
        self.start_screen_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def next_question(self):
        if self.current_question >= self.total_questions:
            self.end_game()
            return

        self.current_question += 1
        self.target_number = random.randint(1, 99)
        options = self.generate_options(self.target_number)
        self.correct_index = options.index(self.target_number)

        for idx, option in enumerate(options):
            self.option_buttons[idx].config(text=str(option), bg="#fff7d5", state="normal")

        self.question_label.config(text=f"Question {self.current_question} / {self.total_questions}")
        self.score_label.config(text=f"Score: {self.score}")
        self.canvas.delete("float")
        self.floating_y = 350
        self.is_playing = True
        self.update_progress_dots()
        self.animate_number()
        self.animate_clouds()

    def generate_options(self, target):
        choices = {target}
        while len(choices) < 4:
            val = target + random.choice(CONFIG['option_deltas'])
            if 1 <= val <= 99:
                choices.add(val)
        opts = list(choices)
        random.shuffle(opts)
        return opts

    def animate_number(self):
        self.canvas.delete("float")
        x = 270
        self.canvas.create_text(
            x,
            self.floating_y,
            text=str(self.target_number),
            tags="float",
            font=("Comic Sans MS", 84, "bold"),
            fill="#ff4d6d",
        )
        self.canvas.create_text(
            x,
            self.floating_y + 140,
            text="🔢",
            tags="float",
            font=("Segoe UI Emoji", 30),
        )

        if self.floating_y <= -70:
            self.handle_missed_question()
            return

        self.floating_y -= 2
        self.animation_after_id = self.after(100, self.animate_number)

    def check_answer(self, index):
        if not self.is_playing:
            return

        self.cancel_animation()
        self.canvas.delete("float")
        self.enable_answer_buttons(False)

        if index == self.correct_index:
            self.play_sound("correct")
            self.score += 1
            self.status_label.config(text="Great job! Correct answer.", fg="#1b5e20")
            self.option_buttons[index].config(bg="#9df29f")
            self.after(700, self.next_question)
        else:
            self.play_sound("wrong")
            self.option_buttons[index].config(bg="#ffb3b3")
            self.option_buttons[self.correct_index].config(bg="#9df29f")
            self.status_label.config(text="Oops! Wrong answer. Next one coming up.", fg="#b71c1c")
            self.after(900, self.next_question)

    def handle_missed_question(self):
        self.cancel_animation()
        self.is_playing = False
        self.enable_answer_buttons(False)
        self.play_sound("missed")
        self.status_label.config(text="Oops! The number floated away. Don't worry, next one!", fg="#d2691e")
        self.after(900, self.next_question)

    def end_game(self):
        self.cancel_animation()
        self.is_playing = self.music_active = False
        self.enable_answer_buttons(False)
        self.stop_background_music()
        self.play_sound("finish")
        msgs = {self.total_questions: "🎉 Congratulations! Perfect score! 🎉", 6: "Awesome! You passed with great marks."}
        msg = msgs.get(self.score if self.score == self.total_questions else (6 if self.score >= 6 else 0), "Keep practicing! You can score higher next time.")
        self.start_title.config(text=msg)
        self.start_desc.config(text=f"Final score: {self.score} / {self.total_questions}\nTap START to play again.")
        self.start_button.config(state="normal", text="Play Again")
        self.show_start_screen()

    def start_background_music(self):
        # Prefer synthesized violin loop if simpleaudio is available
        if self._sa_available and np is not None and sa is not None:
            if self._music_thread and self._music_thread.is_alive():
                return

            def music_loop(stop_event):
                try:
                    buf = self._synthesize_violin_loop(duration=8.0)
                    while not stop_event.is_set():
                        play_obj = sa.play_buffer(buf, 1, 2, 44100)
                        self._music_play_obj = play_obj
                        # wait with small sleeps so we can be responsive to stop_event
                        while play_obj.is_playing() and not stop_event.is_set():
                            time.sleep(0.2)
                        if stop_event.is_set():
                            try:
                                play_obj.stop()
                            except Exception:
                                pass
                            break
                except Exception:
                    return

            self._music_stop_event = threading.Event()
            self._music_thread = threading.Thread(target=music_loop, args=(self._music_stop_event,))
            self._music_thread.daemon = True
            self._music_thread.start()
            self.music_active = True
            return

        # Fallback to winsound on Windows
        if winsound:
            try:
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
                self.music_active = True
            except RuntimeError:
                self.music_active = False

    def stop_background_music(self):
        if self._sa_available and self._music_stop_event is not None:
            try:
                self._music_stop_event.set()
                if self._music_play_obj is not None:
                    try:
                        self._music_play_obj.stop()
                    except Exception:
                        pass
                if self._music_thread is not None:
                    self._music_thread.join(timeout=1.0)
            finally:
                self._music_stop_event = None
                self._music_thread = None
                self._music_play_obj = None
                self.music_active = False
            return

        if winsound and self.music_active:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.music_active = False

    def _synthesize_violin_loop(self, duration=8.0, sample_rate=44100):
        # Generate a mellow violin-like loop using additive synthesis and vibrato
        sr = sample_rate
        t = np.linspace(0, duration, int(sr * duration), False)

        # A simple arpeggio in A major: A4, C#5, E5, A5
        base_notes = [440.0, 554.37, 659.25, 880.0]
        freqs = np.tile(base_notes, int(np.ceil(len(t) / (len(base_notes) * sr * 0.5))))[:len(t)]
        # Instead of per-sample freq, create a slow-moving sequence
        # Build a continuous frequency curve by interpolating between notes
        note_len = int(len(t) / len(base_notes))
        freq_curve = np.zeros_like(t)
        for i, f in enumerate(base_notes):
            start = i * note_len
            end = start + note_len
            if end > len(t):
                end = len(t)
            freq_curve[start:end] = f
        # Vibrato
        vibrato = 0.003 * np.sin(2 * np.pi * 5.5 * t)
        freq_curve = freq_curve * (1 + vibrato)

        # Additive synthesis (several harmonics)
        signal = np.zeros_like(t)
        for h in range(1, 8):
            signal += (1.0 / h) * np.sin(2 * np.pi * freq_curve * h * t)

        # Envelope (slow attack, long release)
        attack = np.linspace(0, 1.0, int(sr * 0.12))
        sustain_len = len(t) - attack.size
        envelope = np.concatenate((attack, np.ones(sustain_len)))
        signal *= envelope

        # Gentle low-pass / fade
        signal *= np.exp(-t * 0.12)

        # Normalize to int16
        signal /= np.max(np.abs(signal)) + 1e-9
        audio = (signal * 32767).astype(np.int16)
        return audio.tobytes()

    def _play_short_tone(self, freqs, duration=0.6):
        if not (self._sa_available and np is not None and sa is not None):
            return
        sr = 44100
        t = np.linspace(0, duration, int(sr * duration), False)
        sig = np.zeros_like(t)
        for f in freqs:
            sig += 0.5 * np.sin(2 * np.pi * f * t)
        # Simple ADSR
        env = np.ones_like(t)
        env_len = len(t)
        env[:int(0.08 * sr)] = np.linspace(0, 1, int(0.08 * sr))
        env[int(0.6 * sr):] *= np.linspace(1, 0.001, env_len - int(0.6 * sr))
        sig *= env
        sig /= np.max(np.abs(sig)) + 1e-9
        audio = (sig * 32767).astype(np.int16)
        try:
            play_obj = sa.play_buffer(audio.tobytes(), 1, 2, sr)
            # Non-blocking; let it play
        except Exception:
            pass

    def play_sound(self, sound_type: str):
        durations = {'correct': 0.45, 'wrong': 0.45, 'missed': 0.55, 'finish': 0.9, 'start': 0.6}
        if self._sa_available and np and sa:
            try:
                if sound_type in CONFIG['sounds']:
                    self._play_short_tone(CONFIG['sounds'][sound_type], duration=durations.get(sound_type, 0.45))
            except Exception:
                pass
            return
        if not winsound:
            return
        beep_map = {'correct': winsound.MB_OK, 'wrong': winsound.MB_ICONHAND, 'missed': winsound.MB_ICONEXCLAMATION, 'finish': winsound.MB_ICONASTERISK}
        if sound_type in beep_map:
            winsound.MessageBeep(beep_map[sound_type])
        elif sound_type == "start":
            try:
                winsound.PlaySound("SystemStart", winsound.SND_ALIAS | winsound.SND_ASYNC)
            except Exception:
                pass

    def cancel_animation(self):
        if self.animation_after_id:
            self.after_cancel(self.animation_after_id)
            self.animation_after_id = None
        if self.cloud_animation_id:
            self.after_cancel(self.cloud_animation_id)
            self.cloud_animation_id = None


if __name__ == "__main__":
    app = KidsNumberMatchGame()
    app.mainloop()
