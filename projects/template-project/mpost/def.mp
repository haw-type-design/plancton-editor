input ../global;

height := 13;
baseline := 0;
xHeight := 18;
ascHeight := 11;
descHeight := -4;
capHeight := 11;

strokeX := 1u;
strokeY := 1u;
rotation := 45;


def beginchar(expr keycode, width)=
    beginfig(keycode);
		pickup pencircle scaled .2;

		draw (0 * ux, (descHeight - 2) * uy) -- 
			(width * ux, (descHeight - 2) * uy) --
			(width * ux, (ascHeight + 2) * uy) -- 
			(0 * ux, (ascHeight + 2) * uy) -- 
			cycle scaled 0 withcolor red;

		if grid = 1:
			defaultscale := .2;
			for i=0 upto width:
    			draw (i*ux, height*uy) -- (i*ux, descHeight*uy) withcolor .3white;
            endfor;
			for i=descHeight upto (height):
				draw (width*ux, i*uy) -- (0*ux, i*uy) withcolor .3white;
			endfor;
		fi;
		pickup pencircle scaled 1;

		if hints = 1:
			draw (0 * ux, capHeight * uy) -- (width * ux, capHeight * uy)  withcolor (green + blue);
			draw (0 * ux, ascHeight * uy) -- (width * ux, ascHeight * uy)  withcolor (green + blue);
			draw (0 * ux, descHeight * uy) -- (width * ux, descHeight * uy)  withcolor (green + blue);
			draw (0 * ux, baseline * uy) -- (width * ux, baseline * uy)  withcolor green;
		fi;
        
		pickup pencircle xscaled strokeX yscaled strokeY rotated rotation;

enddef;

% Pour s'y retrouver on peut matérialiser et numéroter les points du tracé.
def endchar(expr lenDots)=
	if dot_label = 1:
		defaultscale := 3;
		for i=1 upto lenDots:
			dotlabels.urt([i]) withcolor blue;
		endfor;
	fi;
endfig;
enddef;