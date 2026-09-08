#!/bin/sh
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec xfce4-terminal --geometry 72x10+16+16 --title "vuln part" --hold -x python3 "$DIR/show-vuln-art.py"
