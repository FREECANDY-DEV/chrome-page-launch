#!/bin/sh
set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/profterm-handler.desktop" << EOF
[Desktop Entry]
Name=Professional Terminal Message
Comment=Open the terminal message on this computer
Exec=$DIR/launch-terminal.sh %u
Type=Application
NoDisplay=true
Terminal=false
MimeType=x-scheme-handler/profterm;
EOF
chmod +x "$DIR/launch-terminal.sh"
xdg-mime default profterm-handler.desktop x-scheme-handler/profterm
update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
echo "Registered on this computer."
echo "Start the page, open it, and accept the open prompt. The terminal opens here, not in Chrome."
