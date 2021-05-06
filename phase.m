function p = phase(w,c,r)
    g = 1/(1+1j*w*c*r);
    p = angle(g);
end