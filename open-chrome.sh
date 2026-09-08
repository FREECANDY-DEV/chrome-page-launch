#!/bin/bash
n="${1:-1}"
dir="/tmp/chrome-opened/${n}"
url="http://127.0.0.1:8765/opened.html?n=${n}"
mkdir -p "$dir"
echo "Opening Chrome instance ${n}"
echo
echo "google-chrome --user-data-dir=${dir} --new-window ${url}"
echo
# nohup + disown so this terminal can stay open without killing Chrome
nohup google-chrome \
  --user-data-dir="${dir}" \
  --no-first-run \
  --no-default-browser-check \
  --new-window \
  --window-position=560,250 \
  --window-size=680,480 \
  "${url}" >/tmp/chrome-opened/"${n}.log" 2>&1 &
disown || true
echo "Chrome instance ${n} launched. This terminal stays open."
(
  sleep 1
  xdotool search --name "Chrome launch ${n}" windowmove 16 16 windowraise >/dev/null 2>&1 || true
  sleep 2
  xdotool search --name "Chrome launch ${n}" windowraise >/dev/null 2>&1 || true
) >/dev/null 2>&1 &
exec bash
