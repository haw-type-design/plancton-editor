#!/usr/bin/env bash

for gly in tmp/svg/*.svg
do
  file=`basename $gly .svg`
	echo $gly
  inkscape --verb EditSelectAllInAllLayers \
          --verb SelectionUnGroup \
          --verb ObjectToPath \
          --verb StrokeToPath \
          --verb SelectionUnion \
          --verb SelectionReverse \
          --verb FileSave \
          --verb FileClose \
          --verb FileQuit \
    			$gly 
done
