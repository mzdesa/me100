function dS = arm(t,y)
m = 10; %mass in kg
l = 10; %length in meters
g = 9.81;
t_motor = 0.5; %motor torque in newton-meters
I = 1/2*m*l^3;

%evaluate the eqn
dydt = [y(2);t_motor/I-m*g*l/(2*I)*cos(y(1)];
end
