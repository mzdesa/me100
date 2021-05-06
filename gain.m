function m = gain(w,c,r)
    g = 1/(1+1j*w*c*r);
    m = abs(g);
end

