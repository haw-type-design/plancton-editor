#!/usr/bin/env bash

inkscape --verb EditSelectAllInAllLayers \
				--verb SelectionUnGroup \
				--verb ObjectToPath \
				--verb StrokeToPath \
				--verb SelectionUnion \
				--verb SelectionReverse \
				--verb FileSave \
				--verb FileClose \
				--verb FileQuit \
				$1 \
