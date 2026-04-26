import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import subprocess
import os
import re
import datetime
import time

MIC_DEVICE = "YOUR_MIC_DEVICE_NAME"
SYSTEM_DEVICE = "YOUR_SYSTEM_AUDIO_DEVICE_NAME"
LINEAR_ALGEBRA_CATEGORY = "Linear Algebra"

BG         = "#FBFCFD"
SURFACE    = "#F6F9FB"
SURFACE2   = "#EEF4F7"
ACCENT     = "#0B4DA6"
ACCENT2    = "#2E7AB8"
TEXT       = "#0F1724"
TEXT_LIGHT = "#F5F9FF"
TEXT_DIM   = "#4B5563"
SUCCESS    = "#5EA67A"
WARNING    = "#C89B45"
MEETING_BG = "#F3FAFF"
MEETING_AC = "#0B4DA6"

FONT_TITLE = ("Microsoft YaHei", 12, "bold")
FONT_BODY  = ("Microsoft YaHei", 11)
FONT_TIMER = ("Consolas", 32, "bold")
FONT_SMALL = ("Microsoft YaHei", 10)
FONT_BTN   = ("Microsoft YaHei", 11, "bold")

STRINGS = {
    "zh": {
        "title":                 "課程自動化錄音助理",
        "subtitle":              "自動同步 · AI 轉寫 · 一鍵筆記",
        "category_label":        "錄音類別",
        "meeting_mode_off":      "  會議模式  ·  關閉  ",
        "meeting_mode_on":       "  會議模式  ·  開啟  ",
        "meeting_name":          "會議名稱",
        "meeting_default":       "實驗室會議",
        "meeting_warn":          "含非法字元 {}，存檔時自動替換為「-」",
        "la_hint":               "將自動產出 KnowTube 特殊心智圖",
        "btn_record":            "開始錄音",
        "btn_stop":              "停止並存檔",
        "status_ready":          "就緒",
        "add_cat_title":         "新增類別",
        "add_cat_prompt":        "請輸入課程名稱：",
        "add_cat_success":       "已新增類別：{}",
        "add_cat_exists":        "該類別已存在！",
        "remove_cat_title":      "確認刪除",
        "remove_cat_msg":        "確定要刪除「{}」？",
        "warn_no_meeting":       "請輸入會議名稱！",
        "warn_no_cat":           "請先選擇類別！",
        "path_error":            "無法建立目錄：\n{}\n\n{}",
        "auto_fix_title":        "名稱已自動修正",
        "auto_fix_msg":          "會議名稱含非法字元，已修正為：\n\n「{}」\n\n確定繼續？",
        "recording_meeting":     "會議錄音中...",
        "recording_normal":      "錄音中 — 麥克風 + 系統音效",
        "packing":               "封裝中，請稍候...",
        "stopping":              "停止中，封裝中，請稍候...",
        "file_too_small_title":  "錄音異常",
        "file_too_small_msg":    "檔案異常小，可能沒錄到聲音。\n請檢查：{}",
        "pack_fail_title":       "封裝失敗",
        "pack_fail_msg":         "已保留原始 MKV，n8n 仍可正常處理。\n{}",
        "save_done_status":      "已儲存：{}",
        "save_done_title":       "儲存成功",
        "save_done_msg":         "錄音已儲存！\n\n{}\n\nSyncthing 將自動同步，AI 後台處理中。",
        "unexpected_status":     "錄音意外中斷！",
        "unexpected_title":      "錄音中斷",
        "unexpected_msg":        "ffmpeg 意外結束，錄音已中斷。\n原始 MKV 可能仍可用。\n\n請檢查：{}",
        "close_title":           "確認關閉",
        "close_msg":             "錄音進行中！\n確定要停止錄音並關閉視窗？\n（將等待封裝完成）",
        "rec_error_title":       "錄音錯誤",
        "warn_title":            "警告",
        "notice_title":          "注意",
        "success_title":         "成功",
        "lang_btn":              "EN",
    },
    "en": {
        "title":                 "Course Recording Assistant",
        "subtitle":              "Auto Sync · AI Transcription · One-Click Notes",
        "category_label":        "Recording Category",
        "meeting_mode_off":      "  Meeting Mode  ·  Off  ",
        "meeting_mode_on":       "  Meeting Mode  ·  On  ",
        "meeting_name":          "Meeting Name",
        "meeting_default":       "Lab Meeting",
        "meeting_warn":          "Illegal characters {} will be replaced with '-' on save",
        "la_hint":               "Will auto-generate KnowTube special mind map",
        "btn_record":            "Start Recording",
        "btn_stop":              "Stop & Save",
        "status_ready":          "Ready",
        "add_cat_title":         "Add Category",
        "add_cat_prompt":        "Enter course name:",
        "add_cat_success":       "Category added: {}",
        "add_cat_exists":        "Category already exists!",
        "remove_cat_title":      "Confirm Delete",
        "remove_cat_msg":        "Delete \"{}\"?",
        "warn_no_meeting":       "Please enter a meeting name!",
        "warn_no_cat":           "Please select a category first!",
        "path_error":            "Cannot create directory:\n{}\n\n{}",
        "auto_fix_title":        "Name Auto-Corrected",
        "auto_fix_msg":          "Meeting name contains illegal characters, corrected to:\n\n\"{}\"\n\nContinue?",
        "recording_meeting":     "Meeting recording...",
        "recording_normal":      "Recording — Mic + System Audio",
        "packing":               "Packaging, please wait...",
        "stopping":              "Stopping, packaging, please wait...",
        "file_too_small_title":  "Recording Error",
        "file_too_small_msg":    "File is abnormally small, audio may not have been captured.\nCheck: {}",
        "pack_fail_title":       "Packaging Failed",
        "pack_fail_msg":         "Raw MKV preserved, n8n can still process it.\n{}",
        "save_done_status":      "Saved: {}",
        "save_done_title":       "Saved Successfully",
        "save_done_msg":         "Recording saved!\n\n{}\n\nSyncthing will auto-sync, AI processing in background.",
        "unexpected_status":     "Recording interrupted unexpectedly!",
        "unexpected_title":      "Recording Interrupted",
        "unexpected_msg":        "ffmpeg exited unexpectedly.\nRaw MKV may still be usable.\n\nCheck: {}",
        "close_title":           "Confirm Close",
        "close_msg":             "Recording in progress!\nStop recording and close window?\n(Will wait for packaging to complete)",
        "rec_error_title":       "Recording Error",
        "warn_title":            "Warning",
        "notice_title":          "Notice",
        "success_title":         "Success",
        "lang_btn":              "中文",
    },
}


def sanitize_name(name: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', '-', name).strip()


class CourseRecorder:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.is_recording = False
        self.ffmpeg_process = None
        self.start_time = None
        self.current_filepath = None
        self.meeting_mode = False

        self.base_save_path = r"C:\YOUR_PATH\audio_input"
        os.makedirs(self.base_save_path, exist_ok=True)

        self.category_file = os.path.join(self.base_save_path, "categories.txt")
        self.categories = self.load_categories()

        self._build_ui()
        self._apply_lang()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.root.update_idletasks()
        w = 480
        h = self.root.winfo_reqheight() + 20
        self.root.geometry(f"{w}x{h}")

    def s(self, key):
        return STRINGS[self.lang][key]

    def load_categories(self):
        if os.path.exists(self.category_file):
            with open(self.category_file, "r", encoding="utf-8") as f:
                cats = [l.strip() for l in f if l.strip()]
            if cats:
                return cats
        return ["Operating Systems", "Algorithms", "Linear Algebra", "Data Structures", "Test"]

    def save_categories(self):
        with open(self.category_file, "w", encoding="utf-8") as f:
            f.writelines(f"{c}\n" for c in self.categories)

    def _build_ui(self):
        self.header_frame = tk.Frame(self.root, bg=SURFACE, pady=10)
        self.header_frame.pack(fill=tk.X)
        self.lbl_title = tk.Label(self.header_frame, font=FONT_TITLE, bg=SURFACE, fg=TEXT)
        self.lbl_title.pack()
        self.lbl_subtitle = tk.Label(self.header_frame, font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM)
        self.lbl_subtitle.pack()

        self.btn_lang = tk.Button(
            self.header_frame, command=self.toggle_lang,
            font=FONT_SMALL, bg=SURFACE2, fg=ACCENT,
            relief=tk.FLAT, padx=8, pady=2, cursor="hand2")
        self.btn_lang.pack(pady=(4, 0))

        body = tk.Frame(self.root, bg=BG, padx=20)
        body.pack(fill=tk.BOTH, expand=True, pady=10)

        cat_card = tk.Frame(body, bg=SURFACE, padx=12, pady=10)
        cat_card.pack(fill=tk.X, pady=(0, 8))
        self.lbl_cat_header = tk.Label(cat_card, font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM)
        self.lbl_cat_header.pack(anchor=tk.W)

        cat_row = tk.Frame(cat_card, bg=SURFACE)
        cat_row.pack(fill=tk.X, pady=(4, 0))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TCombobox",
                        fieldbackground=SURFACE2, background=SURFACE2,
                        foreground=TEXT, selectbackground=ACCENT,
                        selectforeground=TEXT_LIGHT, bordercolor=SURFACE2,
                        arrowcolor=TEXT)

        self.category_var = tk.StringVar()
        self.combo = ttk.Combobox(cat_row, textvariable=self.category_var,
                                   values=self.categories, state="readonly",
                                   width=18, style="App.TCombobox", font=FONT_BODY)
        if self.categories:
            self.combo.current(0)
        self.combo.pack(side=tk.LEFT)
        self.combo.bind("<<ComboboxSelected>>", self._on_cat_changed)

        tk.Button(cat_row, text="+", command=self.add_category,
                  font=FONT_SMALL, bg=SURFACE2, fg=ACCENT,
                  relief=tk.FLAT, padx=8, pady=2, cursor="hand2").pack(side=tk.LEFT, padx=(6, 2))
        tk.Button(cat_row, text="-", command=self.remove_category,
                  font=FONT_SMALL, bg=SURFACE2, fg=ACCENT,
                  relief=tk.FLAT, padx=8, pady=2, cursor="hand2").pack(side=tk.LEFT)

        self.la_label = tk.Label(cat_card, text="", font=FONT_SMALL, bg=SURFACE, fg=ACCENT2)
        self.la_label.pack(anchor=tk.W, pady=(4, 0))

        meeting_row = tk.Frame(body, bg=BG)
        meeting_row.pack(fill=tk.X, pady=(0, 8))
        self.btn_meeting = tk.Button(
            meeting_row, command=self.toggle_meeting_mode,
            font=FONT_BODY, bg=SURFACE2, fg=TEXT,
            relief=tk.FLAT, padx=10, pady=6, cursor="hand2",
            activebackground=ACCENT, activeforeground=TEXT_LIGHT)
        self.btn_meeting.pack(fill=tk.X)

        self.meeting_frame = tk.Frame(body, bg=SURFACE, padx=12, pady=8)
        self.lbl_meeting_name = tk.Label(self.meeting_frame, font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM)
        self.lbl_meeting_name.pack(anchor=tk.W)
        self.meeting_var = tk.StringVar()
        self.meeting_entry = tk.Entry(
            self.meeting_frame, textvariable=self.meeting_var,
            font=FONT_BODY, bg=SURFACE2, fg=TEXT,
            insertbackground=TEXT, relief=tk.FLAT, width=28)
        self.meeting_entry.pack(fill=tk.X, pady=(4, 0))
        self.meeting_warn = tk.Label(self.meeting_frame, text="",
                                      font=FONT_SMALL, bg=SURFACE, fg=WARNING)
        self.meeting_warn.pack(anchor=tk.W)
        self.meeting_var.trace_add("write", self._validate_meeting_name)

        self._timer_frame = tk.Frame(body, bg=BG)
        self._timer_frame.pack(pady=8)
        self.time_label = tk.Label(self._timer_frame, text="00:00:00",
                                    font=FONT_TIMER, fg=TEXT_DIM, bg=BG)
        self.time_label.pack()

        btn_frame = tk.Frame(body, bg=BG)
        btn_frame.pack(fill=tk.X, pady=(0, 4))
        self.btn_record = tk.Button(
            btn_frame, command=self.start_recording,
            font=FONT_BTN, bg=ACCENT, fg=TEXT_LIGHT,
            relief=tk.FLAT, pady=14, cursor="hand2",
            activebackground="#083A80", activeforeground=TEXT_LIGHT)
        self.btn_record.pack(fill=tk.X, pady=(0, 6))

        self.btn_stop = tk.Button(
            btn_frame, command=self.stop_recording,
            state="disabled", font=FONT_BTN,
            bg=SURFACE2, fg=TEXT_DIM, relief=tk.FLAT, pady=14, cursor="hand2")
        self.btn_stop.pack(fill=tk.X)

        self.status_bar = tk.Label(
            self.root, font=FONT_SMALL,
            bg=SURFACE, fg=TEXT_DIM, anchor=tk.W, padx=12, pady=6)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _apply_lang(self):
        self.root.title(self.s("title"))
        self.lbl_title.config(text=self.s("title"))
        self.lbl_subtitle.config(text=self.s("subtitle"))
        self.btn_lang.config(text=self.s("lang_btn"))
        self.lbl_cat_header.config(text=self.s("category_label"))
        self.lbl_meeting_name.config(text=self.s("meeting_name"))
        if not self.meeting_var.get():
            self.meeting_var.set(self.s("meeting_default"))
        self.btn_record.config(text=self.s("btn_record"))
        self.btn_stop.config(text=self.s("btn_stop"))
        if self.meeting_mode:
            self.btn_meeting.config(text=self.s("meeting_mode_on"))
        else:
            self.btn_meeting.config(text=self.s("meeting_mode_off"))
        if self.status_bar.cget("text") in (
            STRINGS["zh"]["status_ready"], STRINGS["en"]["status_ready"]
        ):
            self.status_bar.config(text=self.s("status_ready"))
        self._update_la_label()
        self._validate_meeting_name()

    def toggle_lang(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self._apply_lang()

    def _on_cat_changed(self, event=None):
        self._update_la_label()

    def _update_la_label(self):
        if self.category_var.get() == LINEAR_ALGEBRA_CATEGORY and not self.meeting_mode:
            self.la_label.config(text=self.s("la_hint"))
        else:
            self.la_label.config(text="")

    def _validate_meeting_name(self, *_):
        illegal = re.findall(r'[/\\:*?"<>|]', self.meeting_var.get())
        if illegal:
            self.meeting_warn.config(
                text=self.s("meeting_warn").format(' '.join(set(illegal))))
        else:
            self.meeting_warn.config(text="")

    def toggle_meeting_mode(self):
        self.meeting_mode = not self.meeting_mode
        if self.meeting_mode:
            self.btn_meeting.config(text=self.s("meeting_mode_on"),
                                    bg=MEETING_AC, fg=TEXT_LIGHT)
            self.meeting_frame.pack(fill=tk.X, pady=(0, 8), before=self._timer_frame)
            self.combo.config(state="disabled")
            self.root.configure(bg=MEETING_BG)
        else:
            self.btn_meeting.config(text=self.s("meeting_mode_off"),
                                    bg=SURFACE2, fg=TEXT)
            self.meeting_frame.pack_forget()
            self.combo.config(state="readonly")
            self.root.configure(bg=BG)
        self._update_la_label()
        self.root.update_idletasks()
        h = self.root.winfo_reqheight() + 20
        self.root.geometry(f"480x{h}")

    def add_category(self):
        raw = simpledialog.askstring(self.s("add_cat_title"), self.s("add_cat_prompt"), parent=self.root)
        if raw and raw.strip():
            new_cat = sanitize_name(raw.strip())
            if new_cat not in self.categories:
                self.categories.append(new_cat)
                self.save_categories()
                self.combo["values"] = self.categories
                self.combo.set(new_cat)
                os.makedirs(os.path.join(r"C:\YOUR_OBSIDIAN_VAULT", new_cat), exist_ok=True)
                messagebox.showinfo(self.s("success_title"), self.s("add_cat_success").format(new_cat))
            else:
                messagebox.showwarning(self.s("notice_title"), self.s("add_cat_exists"))

    def remove_category(self):
        current = self.category_var.get()
        if not current:
            return
        if messagebox.askyesno(self.s("remove_cat_title"), self.s("remove_cat_msg").format(current)):
            self.categories.remove(current)
            self.save_categories()
            self.combo["values"] = self.categories
            self.combo.current(0) if self.categories else self.combo.set("")

    def start_recording(self):
        if self.meeting_mode:
            raw = self.meeting_var.get().strip()
            if not raw:
                messagebox.showwarning(self.s("warn_title"), self.s("warn_no_meeting"))
                return
            subfolder = sanitize_name(raw)
            if subfolder != raw:
                if not messagebox.askyesno(self.s("auto_fix_title"),
                                            self.s("auto_fix_msg").format(subfolder)):
                    return
            save_dir = os.path.join(self.base_save_path, "meeting", subfolder)
            category_label = f"meeting_{subfolder}"
        else:
            if not self.category_var.get():
                messagebox.showwarning(self.s("warn_title"), self.s("warn_no_cat"))
                return
            save_dir = os.path.join(self.base_save_path, self.category_var.get())
            category_label = self.category_var.get()

        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", self.s("path_error").format(save_dir, e))
            return

        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y-%m-%d_%A')}_{category_label}_{now.strftime('%H%M%S')}.m4a"
        self.current_filepath = os.path.join(save_dir, filename)

        self.is_recording = True
        self.start_time = time.time()

        self.btn_record.config(state="disabled", bg=SURFACE2, fg=TEXT_DIM)
        self.btn_stop.config(state="normal", bg=ACCENT, fg=TEXT_LIGHT)
        self.btn_meeting.config(state="disabled")
        self.combo.config(state="disabled")

        threading.Thread(target=self._record_worker, daemon=True).start()
        self._tick()

    def _record_worker(self):
        try:
            log_path = os.path.join(self.base_save_path, "ffmpeg_last.log")
            self._ffmpeg_log = open(log_path, "w")

            mkv_path = self.current_filepath.replace('.m4a', '_raw.mkv')

            self.ffmpeg_process = subprocess.Popen([
                "ffmpeg", "-y",
                "-f", "dshow", "-audio_buffer_size", "200",
                "-i", f"audio={MIC_DEVICE}",
                "-f", "dshow", "-audio_buffer_size", "200",
                "-i", f"audio={SYSTEM_DEVICE}",
                "-filter_complex", "amix=inputs=2:duration=longest:dropout_transition=0",
                "-c:a", "aac", "-b:a", "256k",
                "-cluster_time_limit", "2000",
                mkv_path
            ], stdin=subprocess.PIPE, stderr=self._ffmpeg_log,
               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

            label = self.s("recording_meeting") if self.meeting_mode else self.s("recording_normal")
            self.root.after(0, lambda: self.status_bar.config(text=label, fg=ACCENT))
            self.ffmpeg_process.wait()
            self._ffmpeg_log.close()

            if self.is_recording:
                self.is_recording = False
                self.root.after(0, self._on_unexpected_stop)

            if not os.path.exists(mkv_path) or os.path.getsize(mkv_path) < 10240:
                self.root.after(0, lambda: messagebox.showwarning(
                    self.s("file_too_small_title"),
                    self.s("file_too_small_msg").format(log_path)))
                return

            self.root.after(0, lambda: self.status_bar.config(
                text=self.s("packing"), fg=WARNING))

            convert = subprocess.run([
                "ffmpeg", "-y", "-i", mkv_path,
                "-c", "copy",
                self.current_filepath
            ], capture_output=True)

            if convert.returncode == 0:
                os.remove(mkv_path)
                final_path = self.current_filepath
            else:
                fallback = self.current_filepath.replace('.m4a', '.mkv')
                os.rename(mkv_path, fallback)
                self.current_filepath = final_path = fallback
                self.root.after(0, lambda p=fallback: messagebox.showwarning(
                    self.s("pack_fail_title"),
                    self.s("pack_fail_msg").format(p)))

            self.root.after(0, lambda p=final_path: self._on_save_done(p))

        except Exception as e:
            if hasattr(self, '_ffmpeg_log') and not self._ffmpeg_log.closed:
                self._ffmpeg_log.close()
            self.root.after(0, lambda: messagebox.showerror(self.s("rec_error_title"), str(e)))

    def _tick(self):
        if not self.is_recording:
            self.time_label.config(fg=TEXT_DIM)
            return
        elapsed = int(time.time() - self.start_time)
        h, m = divmod(elapsed, 3600)
        m, s = divmod(m, 60)
        self.time_label.config(
            text=f"{h:02}:{m:02}:{s:02}",
            fg=ACCENT if elapsed % 2 == 0 else ACCENT2)
        self.root.after(1000, self._tick)

    def stop_recording(self):
        self.is_recording = False

        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            try:
                self.ffmpeg_process.stdin.write(b"q")
                self.ffmpeg_process.stdin.flush()
            except Exception:
                pass

        self.btn_record.config(state="disabled", bg=SURFACE2, fg=TEXT_DIM)
        self.btn_stop.config(state="disabled", bg=SURFACE2, fg=TEXT_DIM)
        self.btn_meeting.config(state="disabled")
        self.combo.config(state="disabled")
        self.time_label.config(fg=TEXT_DIM)
        self.status_bar.config(text=self.s("stopping"), fg=WARNING)

    def _on_save_done(self, filepath: str):
        self.btn_record.config(state="normal", bg=ACCENT, fg=TEXT_LIGHT)
        self.btn_stop.config(state="disabled", bg=SURFACE2, fg=TEXT_DIM)
        self.btn_meeting.config(state="normal")
        if not self.meeting_mode:
            self.combo.config(state="readonly")
        fname = os.path.basename(filepath)
        self.status_bar.config(text=self.s("save_done_status").format(fname), fg=SUCCESS)
        messagebox.showinfo(self.s("save_done_title"),
                            self.s("save_done_msg").format(filepath))

    def _on_unexpected_stop(self):
        self.btn_record.config(state="normal", bg=ACCENT, fg=TEXT_LIGHT)
        self.btn_stop.config(state="disabled", bg=SURFACE2, fg=TEXT_DIM)
        self.btn_meeting.config(state="normal")
        if not self.meeting_mode:
            self.combo.config(state="readonly")
        self.time_label.config(fg=TEXT_DIM)
        log_path = os.path.join(self.base_save_path, "ffmpeg_last.log")
        self.status_bar.config(text=self.s("unexpected_status"), fg=WARNING)
        messagebox.showwarning(self.s("unexpected_title"),
                               self.s("unexpected_msg").format(log_path))

    def _on_close(self):
        if self.is_recording:
            if not messagebox.askyesno(self.s("close_title"), self.s("close_msg")):
                return
            self.stop_recording()
            self.root.after(500, self._poll_close)
        else:
            self.root.destroy()

    def _poll_close(self):
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            self.root.after(300, self._poll_close)
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseRecorder(root)
    root.mainloop()