outputtemplate := "output-svg/%c.svg"; outputformat := "svg";

u = 7pt;
ux = 1*u; 
uy = 1*u;
sx = 1*u; 
sy = 1*u;
rot = 45;

height = 40;
grid = 1;

vardef cadratin(expr width)=
	draw (0 * ux, 0 * uy)--(width * ux, 0 * uy)--(width * ux, height * uy)--(0 * ux, height * uy);
enddef;

def beginchar(expr keycode, width)=
  beginfig(keycode);
	pickup pencircle scaled .2;

	draw (0 * ux, 0 * uy) -- (width * ux, 0 * uy) -- (width * ux, height * uy) -- (0 * ux, height * uy) -- cycle scaled 0 withcolor red;
	height = 40;
	if grid = 1:
		defaultscale :=.2;
		for i=0 upto width:
			draw (i*ux, height*uy) -- (i*ux, 0*uy) withcolor blue;
		endfor;
		for i=0 upto height:
			draw (width*ux, i*uy) -- (0*ux, i*uy) withcolor blue;
		endfor;
	fi;

	pickup pencircle xscaled sx yscaled sy rotated rot;
enddef;

def endchar(expr lenDots)=
    defaultscale :=.5;
	for i=1 upto lenDots:
	  dotlabels.urt([i]) withcolor magenta;
	endfor;
	endfig;
enddef;


