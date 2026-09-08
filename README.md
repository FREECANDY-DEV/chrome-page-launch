# chrome-page-launch

A normal-looking notes page. Visiting it opens a terminal that runs a script. The script shows a GUI window with the vuln ASCII art.

## Run

```bash
python3 server.py
```

Then open http://127.0.0.1:8765/

On Windows, run `python server.py` the same way. The terminal starts `show-vuln-art.bat`, which runs `show-vuln-art.py`.

Needs Python with tkinter. On Windows that is the usual Python install. On Linux, install `python3-tk`.
