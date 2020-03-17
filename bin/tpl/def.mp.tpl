input ../global;

height = {height};
baseline := 0;
xHeight := {x_height};
ascHeight := {ascent};
descHeight := -{descent};
capHeight := {height};

ox = ux;
oy = uy;

% OverShots Values
os_bsln = - .3uy;
os_x = .3uy;

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
			draw (i*ux, ascHeight*uy) -- (i*ux, descHeight*uy) withcolor .3white;
		endfor;
		for i=-9 upto (ascHeight):
			draw (width*ux, i*uy) -- (0*ux, i*uy) withcolor .3white;
		endfor;
	fi;
	pickup pencircle scaled 1;

	if hints = 1:
		draw (0 * ux, (xHeight * uy) + os_x) -- (width * ux, (xHeight * uy) + os_x)  withcolor green;
		draw (0 * ux, xHeight * uy) -- (width * ux, xHeight * uy)  withcolor (green + blue);

        draw (0 * ux, capHeight * uy) -- (width * ux, capHeight * uy)  withcolor (green + blue);
		draw (0 * ux, ascHeight * uy) -- (width * ux, ascHeight * uy)  withcolor (green + blue);
		draw (0 * ux, descHeight * uy) -- (width * ux, descHeight * uy)  withcolor (green + blue);
		draw (0 * ux, baseline * uy) -- (width * ux, baseline * uy)  withcolor green;
	fi;
    % linejoin := beveled;
    % linecap := rounded;
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

def serifOff(expr x_start, x_end)(suffix posi)=
    draw (x_start, posi srf_H) --
    (x_start + srf_L, posi 0 ) -- 
    (x_end + srf_R , posi 0 ) -- 
    (x_end, posi srf_H);
enddef;

def \. =
    ..
enddef;

