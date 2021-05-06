%make a bode plot of gain and phase for an RLC circuit in HW4
%define resistance and capacitance
r = 100; %resistance (ohms)
c = 270*10^(-12); %capacitance (F)
num = 1;
den = [r*c,1]; %ALREADY accounts for the complex component!

sys = tf(num,den);
bode(sys);