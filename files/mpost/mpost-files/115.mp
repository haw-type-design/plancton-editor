
% s
input ../def;
beginchar(115, 14);
    x1 := 6.0 * ox;
    y1 := 14.0 * oy;
    x2 := 11.0 * ox;
    y2 := 11.0 * oy;
    x3 := 11.0 * ox;
    y3 := 12.0 * oy;
    x4 := 6.0 * ox;
    y4 := 14.0 * oy;
    x5 := 2.0 * ox;
    y5 := 11.0 * oy;
    x6 := 7.0 * ox;
    y6 := 7.0 * oy;
    x7 := 12.0 * ox;
    y7 := 3.0 * oy;
    x8 := 7.0 * ox;
    y8 := 0.0 * oy;
    x9 := 2.0 * ox;
    y9 := 3.0 * oy;
    x10 := 2.0 * ox;
    y10 := 2.0 * oy;
    x11 := 7.0 * ox;
    y11 := 0.0 * oy;
    x12 := 12.0 * ox;
    y12 := 3.0 * oy;
    x13 := 7.0 * ox;
    y13 := 8.0 * oy;
    x14 := 2.0 * ox;
    y14 := 11.0 * oy; 
    draw z1{right} .. z2 -- z3 .. z4 .. z5 .. tension 1 .. {down}z7; 
    draw z8{left} .. z9 -- z10 .. z11{dir 0} .. z12 .. tension .1 .. {up}z14; 

endchar(14);
end;
