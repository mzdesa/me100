%make a bode plot of gain and phase for an RLC circuit in HW4
%define resistance and capacitance
r = 100; %resistance (ohms)
c = 2.7*10^(-12); %capacitance (F)

n = 10^9;
freq = 1:n; %ddefine the frequency array

%preallocate gain and phase arrays
%gain_array = 1:n;
phase_array = 1:n;
gain_decibels = 1:n;

for i = 1:n
    %gain_array(i) = gain(freq(i),c,r);
    phase_array(i) = phase(freq(i),c,r);
    gain_decibels(i) = 20*log10(gain(freq(i),c,r));
end

%plot results on a "tiled" layout

tiledlayout(2,1)
%gain plot
nexttile
semilogx(freq,gain_decibels)
title('Gain')

%phase plot
nexttile
semilogx(freq,phase_array)
title('Phase')
hold off;
