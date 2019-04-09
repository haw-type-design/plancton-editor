#!/usr/bin/env bash
inotifywait -c -m -r 'input-svg/' -e create -e moved_to -e modify |
while read path action file; do
  date=$(date '+%d/%m/%Y %H:%M:%S');
  python svg2mpost.py -all 
  # chromium --headless --disable-gpu --print-to-pdf=date.pdf http://localhost/svg2mpost/www/
  echo 'compileeeeeeee !!!'; 
  echo $date;
done

