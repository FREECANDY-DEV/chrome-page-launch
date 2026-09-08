#!/usr/bin/env python3
"""Show the vuln ASCII art in a GUI window. Works on Windows and Linux."""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART_FILE = HERE / "vuln-art.txt"
MESSAGE = "This window is the vuln part. The terminal opened it."


def load_art():
    return ART_FILE.read_text(encoding="utf-8")


def show_tk(art, message):
    import tkinter as tk
    from tkinter import font as tkfont

    root = tk.Tk()
    root.title("vuln part")
    root.configure(bg="#111111")
    root.geometry("760x640+80+40")
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    family = "Consolas" if sys.platform == "win32" else "DejaVu Sans Mono"
    title_font = tkfont.Font(family=family, size=16)
    body_font = tkfont.Font(family=family, size=11)
    art_font = tkfont.Font(family=family, size=10)

    frame = tk.Frame(root, bg="#111111", padx=18, pady=16)
    frame.pack(fill="both", expand=True)
    tk.Label(
        frame, text="vuln part", fg="#f3efe6", bg="#111111", font=title_font, anchor="w"
    ).pack(fill="x")
    tk.Label(
        frame,
        text=message,
        fg="#c8c2b6",
        bg="#111111",
        font=body_font,
        anchor="w",
        justify="left",
    ).pack(fill="x", pady=(6, 12))
    box = tk.Text(
        frame,
        bg="#111111",
        fg="#f3efe6",
        font=art_font,
        borderwidth=0,
        highlightthickness=0,
        wrap="none",
    )
    box.insert("1.0", art)
    box.configure(state="disabled")
    box.pack(fill="both", expand=True)
    print("vuln part GUI is on screen. Close that window when you are done.", flush=True)
    root.mainloop()


def show_wish(art, message):
    path = Path(tempfile.gettempdir()) / "vuln-part-art.tcl"
    escaped = art.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    path.write_text(
        "\n".join(
            [
                'wm title . "vuln part"',
                "wm geometry . 760x640+80+40",
                ". configure -background #111111",
                "catch {wm attributes . -topmost 1}",
                'label .h -text "vuln part" -foreground #f3efe6 -background #111111 -font {Courier 16} -anchor w',
                'label .m -text "%s" -foreground #c8c2b6 -background #111111 -font {Courier 11} -anchor w -justify left' % message,
                'text .t -background #111111 -foreground #f3efe6 -font {Courier 10} -borderwidth 0 -highlightthickness 0 -wrap none',
                "pack .h -fill x -padx 18 -pady {16 4}",
                "pack .m -fill x -padx 18",
                "pack .t -fill both -expand 1 -padx 18 -pady 8",
                ".t insert end {%s}" % escaped,
                ".t configure -state disabled",
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
                "$form.Size = New-Object System.Drawing.Size(780,660)",
                "$form.StartPosition = 'CenterScreen'",
                "$form.BackColor = [System.Drawing.Color]::FromArgb(17,17,17)",
                "$form.TopMost = $true",
                "$title = New-Object System.Windows.Forms.Label",
                "$title.Text = 'vuln part'",
                "$title.ForeColor = [System.Drawing.Color]::FromArgb(243,239,230)",
                "$title.Font = New-Object System.Drawing.Font('Consolas', 16)",
                "$title.AutoSize = $true",
                "$title.Location = New-Object System.Drawing.Point(18,16)",
                "$msg = New-Object System.Windows.Forms.Label",
                "$msg.Text = '%s'" % message,
                "$msg.ForeColor = [System.Drawing.Color]::FromArgb(200,194,182)",
                "$msg.Font = New-Object System.Drawing.Font('Consolas', 11)",
                "$msg.AutoSize = $true",
                "$msg.Location = New-Object System.Drawing.Point(18,48)",
                "$box = New-Object System.Windows.Forms.TextBox",
                "$box.Multiline = $true",
                "$box.ReadOnly = $true",
                "$box.Text = $art",
                "$box.Font = New-Object System.Drawing.Font('Consolas', 10)",
                "$box.BackColor = [System.Drawing.Color]::FromArgb(17,17,17)",
                "$box.ForeColor = [System.Drawing.Color]::FromArgb(243,239,230)",
                "$box.BorderStyle = 'None'",
                "$box.Location = New-Object System.Drawing.Point(18,84)",
                "$box.Size = New-Object System.Drawing.Size(730,520)",
                "$form.Controls.Add($title)",
                "$form.Controls.Add($msg)",
                "$form.Controls.Add($box)",
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
