# chrome-page-launch

A quiet little notes page with a loud little secret.

You open what looks like a grocery list. Chrome asks to open the link. Accept that prompt and a terminal wakes up on this computer, then a small dialog steps in, shows the mark, and waits for you to close it.

## The open prompt

The page does not draw the terminal inside the site. It asks this computer to open it.

Register that open once, from this folder:

```bash
./register-handler.sh
```

Then start the page:

```bash
python3 server.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). After a second, accept the prompt. The terminal opens on this computer, then the dialog with the art and Close. Decline the prompt and nothing opens. Another computer does not get the window until that same register step is done there.

Linux wants `python3-tk` and `xfce4-terminal`.

## What you are looking at

| Piece | What it pretends to be | What it actually does |
| --- | --- | --- |
| `index.html` | A normal kitchen-notes page | The page you visit |
| `visitor-gui.js` | A quiet page script | Asks this computer to open the terminal |
| `register-handler.sh` | A one-time setup | Points that open at the terminal, not Chrome |
| `launch-terminal.sh` | The opener | Starts the terminal and the dialog |
| `show-vuln-art.py` | The script the terminal runs | Opens a dialog that fits the machine it is on |
| `vuln-art.txt` | The drawing | The mark shown in the dialog |

The notes page stays ordinary on purpose. The dialog is the part that announces itself: title, one sentence, the art, Close.

## The dialog, in plain terms

It is one window.

- It reads the art from `vuln-art.txt`, next to the script.
- It measures the art, then sizes the window so the sentence, the drawing, and Close all fit.
- If the screen is tight, it drops the art size instead of clipping the button.
- Escape or Close dismisses it.

## Files

```
index.html            the notes page
visitor-gui.js        asks this computer to open
register-handler.sh   points the open at the terminal
launch-terminal.sh    starts the terminal
server.py             visit handler
show-vuln-art.py      the dialog
show-vuln-art.bat     Windows starter
vuln-art.txt          the drawing
```

## A note on taste

This is a local demo. The fun is the contrast: a bland list, then a window on this computer that tells you exactly what just happened.
