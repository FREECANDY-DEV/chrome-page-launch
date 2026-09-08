#!/usr/bin/env python3
"""A small dialog that shows the vuln ASCII art. Adapts to Windows or Linux."""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART_FILE = HERE / "vuln-art.txt"
MESSAGE = "This window is the vuln part. The terminal opened it."


def load_art():
    return ART_FILE.read_text(encoding="utf-8").rstrip("\n")


def prepare_windows_display():
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def first_font(candidates, fallback):
    import tkinter.font as tkfont
    available = set(tkfont.families())
    for name in candidates:
        if name in available:
            return name
    return fallback


def show_tk(art, message):
    import tkinter as tk
    from tkinter import font as tkfont

    prepare_windows_display()
    root = tk.Tk()
    root.title("vuln part")
    root.configure(bg="#f4f1ea")
    root.resizable(False, False)

    windows = sys.platform == "win32"
    ui = first_font(
        ["Segoe UI", "Ubuntu", "DejaVu Sans", "Noto Sans"],
        "TkDefaultFont",
    )
    mono_name = first_font(
        ["Cascadia Mono", "Consolas", "DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono"],
        "TkFixedFont",
    )
    art_size = 9 if windows else 10
    mono = tkfont.Font(family=mono_name, size=art_size)
    lines = art.splitlines() or [""]
    art_px = max(mono.measure(line) for line in lines) + 36
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    max_w = max(480, screen_w - 80)
    max_h = max(360, screen_h - 80)
    while art_px > max_w and art_size > 7:
        art_size -= 1
        mono.configure(size=art_size)
        art_px = max(mono.measure(line) for line in lines) + 36

    pad = 20
    content_w = min(max(art_px, 520), max_w)
    shell = tk.Frame(root, bg="#f4f1ea", padx=pad, pady=pad)
    shell.pack(fill="both", expand=True)

    tk.Label(
        shell,
        text="vuln part",
        bg="#f4f1ea",
        fg="#1c1916",
        font=(ui, 16),
        anchor="w",
    ).pack(fill="x")
    tk.Label(
        shell,
        text=message,
        bg="#f4f1ea",
        fg="#5c564e",
        font=(ui, 11),
        anchor="w",
        justify="left",
        wraplength=content_w,
    ).pack(fill="x", pady=(6, 14))

    card = tk.Frame(
        shell,
        bg="#111111",
        padx=16,
        pady=14,
        highlightthickness=1,
        highlightbackground="#d9d2c6",
    )
    card.pack(fill="x")
    tk.Label(
        card,
        text=art,
        bg="#111111",
        fg="#f3efe6",
        font=mono,
        justify="left",
        anchor="nw",
    ).pack()

    bar = tk.Frame(shell, bg="#f4f1ea")
    bar.pack(fill="x", pady=(16, 0))
    close = tk.Button(
        bar,
        text="Close",
        command=root.destroy,
        font=(ui, 10),
        padx=18,
        pady=4,
    )
    close.pack(side="right")

    root.bind("<Escape>", lambda _event: root.destroy())
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.update_idletasks()

    width = min(max(root.winfo_reqwidth(), content_w + pad * 2), max_w)
    height = min(root.winfo_reqheight(), max_h)
    x = max(0, (screen_w - width) // 2)
    y = max(0, (screen_h - height) // 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.lift()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass
    close.focus_set()

    print("vuln part GUI is on screen. Close that window when you are done.", flush=True)
    root.mainloop()


def show_wish(art, message):
    path = Path(tempfile.gettempdir()) / "vuln-part-art.tcl"
    escaped = art.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    path.write_text(
        "\n".join(
            [
                'wm title . "vuln part"',
                "wm resizable . 0 0",
                ". configure -background #f4f1ea",
                'label .h -text "vuln part" -foreground #1c1916 -background #f4f1ea -font {Sans 16} -anchor w',
                'label .m -text "%s" -foreground #5c564e -background #f4f1ea -font {Sans 11} -anchor w -justify left' % message,
                'frame .c -background #111111 -padx 16 -pady 14',
                'label .c.a -text {%s} -foreground #f3efe6 -background #111111 -font {Courier 10} -justify left -anchor nw' % escaped,
                "pack .c.a",
                "button .b -text Close -command exit",
                "pack .h -fill x -padx 20 -pady {18 4}",
                "pack .m -fill x -padx 20",
                "pack .c -padx 20 -pady 14",
                "pack .b -anchor e -padx 20 -pady {0 18}",
                "tk::PlaceWindow . center",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print("vuln part GUI is on screen. Close that window when you are done.", flush=True)
    subprocess.call(["wish", str(path)])


def show_windows_forms(art, message):
    ps1 = Path(tempfile.gettempdir()) / "vuln-part-art.ps1"
    art_path = Path(tempfile.gettempdir()) / "vuln-part-art.txt"
    art_path.write_text(art, encoding="utf-8")
    ps1.write_text(
        "\n".join(
            [
                "$art = Get-Content -Raw -Encoding UTF8 '%s'" % art_path,
                "Add-Type -AssemblyName System.Windows.Forms",
                "Add-Type -AssemblyName System.Drawing",
                "$form = New-Object System.Windows.Forms.Form",
                "$form.Text = 'vuln part'",
                "$form.FormBorderStyle = 'FixedDialog'",
                "$form.MaximizeBox = $false",
                "$form.MinimizeBox = $false",
                "$form.StartPosition = 'CenterScreen'",
                "$form.BackColor = [System.Drawing.Color]::FromArgb(244,241,234)",
                "$form.Font = New-Object System.Drawing.Font('Segoe UI', 10)",
                "$form.AutoSize = $true",
                "$form.AutoSizeMode = 'GrowAndShrink'",
                "$form.Padding = New-Object System.Windows.Forms.Padding(20)",
                "$title = New-Object System.Windows.Forms.Label",
                "$title.Text = 'vuln part'",
                "$title.Font = New-Object System.Drawing.Font('Segoe UI', 16)",
                "$title.AutoSize = $true",
                "$msg = New-Object System.Windows.Forms.Label",
                "$msg.Text = '%s'" % message,
                "$msg.ForeColor = [System.Drawing.Color]::FromArgb(92,86,78)",
                "$msg.AutoSize = $true",
                "$msg.Margin = New-Object System.Windows.Forms.Padding(0,6,0,12)",
                "$card = New-Object System.Windows.Forms.Label",
                "$card.Text = $art.TrimEnd()",
                "$card.Font = New-Object System.Drawing.Font('Consolas', 9)",
                "$card.BackColor = [System.Drawing.Color]::FromArgb(17,17,17)",
                "$card.ForeColor = [System.Drawing.Color]::FromArgb(243,239,230)",
                "$card.AutoSize = $true",
                "$card.Padding = New-Object System.Windows.Forms.Padding(16,14,16,14)",
                "$close = New-Object System.Windows.Forms.Button",
                "$close.Text = 'Close'",
                "$close.DialogResult = 'OK'",
                "$close.AutoSize = $true",
                "$form.AcceptButton = $close",
                "$form.CancelButton = $close",
                "$layout = New-Object System.Windows.Forms.FlowLayoutPanel",
                "$layout.FlowDirection = 'TopDown'",
                "$layout.WrapContents = $false",
                "$layout.AutoSize = $true",
                "$layout.Controls.Add($title)",
                "$layout.Controls.Add($msg)",
                "$layout.Controls.Add($card)",
                "$layout.Controls.Add($close)",
                "$form.Controls.Add($layout)",
                "[void]$form.ShowDialog()",
            ]
        ),
        encoding="utf-8",
    )
    print("vuln part GUI is on screen. Close that window when you are done.", flush=True)
    subprocess.call(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)]
    )


def main():
    art = load_art()
    print("vuln part", flush=True)
    print("Opening a GUI message with the ASCII art.", flush=True)
    try:
        show_tk(art, MESSAGE)
        return
    except Exception:
        pass
    if sys.platform == "win32":
        show_windows_forms(art, MESSAGE)
        return
    show_wish(art, MESSAGE)


if __name__ == "__main__":
    main()
