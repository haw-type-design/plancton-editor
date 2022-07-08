
cp 97.svg tt.svg 

inkscape  --verb EditSelectAll \
          --verb SelectionUnGroup \
          --verb EditSelectAll \
          --verb SelectionCombine \
          --verb FileSave \
          --verb FileClose \
          --verb FileQuit \
    			tt.svg 
