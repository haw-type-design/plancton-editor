input ../global;

height = 40;

baseline := 18;
xHeight := 14 + baseline;
ascHeight := 21 + baseline;
descHeight := -9 + baseline;
capHeight := 21 + baseline;

vardef cadratin(expr width)=
	draw (0 * ux, 0 * uy)--(width * ux, 0 * uy)--(width * ux, height * uy)--(0 * ux, height * uy);
enddef;

def beginchar(expr keycode, width)=
  beginfig(keycode);
	pickup pencircle scaled .2;

	draw (0 * ux, 0 * uy) -- (width * ux, 0 * uy) -- (width * ux, height * uy) -- (0 * ux, height * uy) -- cycle scaled 0 withcolor red;
	if grid = 1:
		defaultscale :=.2;
		for i=0 upto width:
			draw (i*ux, height*uy) -- (i*ux, 0*uy) withcolor .3white;
		endfor;
		for i=0 upto height:
			draw (width*ux, i*uy) -- (0*ux, i*uy) withcolor .3white;
		endfor;
	fi;
	pickup pencircle scaled 1;

	if hints = 1:
		draw (0 * ux, xHeight * uy) -- (width * ux, xHeight * uy)  withcolor (green + blue);
		draw (0 * ux, capHeight * uy) -- (width * ux, capHeight * uy)  withcolor (green + blue);
		draw (0 * ux, ascHeight * uy) -- (width * ux, ascHeight * uy)  withcolor (green + blue);
		draw (0 * ux, descHeight * uy) -- (width * ux, descHeight * uy)  withcolor (green + blue);
		draw (0 * ux, baseline * uy) -- (width * ux, baseline * uy)  withcolor green;
	fi;


	pickup pencircle xscaled sx yscaled sy rotated rot;
enddef;

def endchar(expr lenDots)=
	if dot_label = 1:
		defaultscale := 1;
		for i=1 upto lenDots:
		  dotlabels.urt([i]) withcolor magenta;
		endfor;
	fi;
	endfig;
enddef;
