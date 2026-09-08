#!/bin/bash
n="${1:-1}"
dir="/tmp/chrome-opened/${n}"
url="http://127.0.0.1:8765/opened.html?n=${n}"
mkdir -p "$dir"

cat << 'ART'
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠁⠀⠀⠀⠀⠀⠀⠀⠀⣠⠂⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⡴⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢀⣤⣤⡄⠀⢀⠞⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢆⣟⣾⣿⡿⢠⠏⠀⡠⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡖⠤⣈⣟⣿⣿⣟⠇⠔⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣿⡿⣏⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢖⡯⠛⠛⢳⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⣯⠴⠋⠀⠀⠀⢸⠿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡀⡴⠋⠀⠀⠀⠀⠀⠀⢸⡃⠙⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠈⠂⠀⠀⠀⠀⠀
⠀⠀⠀⢀⠔⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀
ART

echo
echo "vuln part"
echo "This terminal opened Chrome instance ${n} because the page was visited."
echo
echo "google-chrome --user-data-dir=${dir} --new-window ${url}"
echo

nohup google-chrome \
  --user-data-dir="${dir}" \
  --no-first-run \
  --no-default-browser-check \
  --new-window \
  --window-position=560,220 \
  --window-size=720,560 \
  "${url}" >/tmp/chrome-opened/"${n}.log" 2>&1 &
disown || true
echo "Chrome instance ${n} is open. This terminal stays here so you can see the vuln part."
(
  sleep 1
  xdotool search --name "vuln part ${n}" windowmove 16 16 windowraise >/dev/null 2>&1 || true
  sleep 2
  xdotool search --name "vuln part ${n}" windowraise >/dev/null 2>&1 || true
) >/dev/null 2>&1 &
exec bash
