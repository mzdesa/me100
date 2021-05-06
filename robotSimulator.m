m = 0.5; %mass in kg
l = 1; %length in meters
g = 9.81;
t_motor = 0.5; %motor torque in newton-meters
ratio = 7.5;

I = 1/3*m*l^3; %inertia of the bar



theta = @(t)((t_motor*ratio-m*g)/I).*t.^2/2;
theta_data = theta(0:0.5:10);

coeff1 = 2/(t_motor*ratio-m*g)/I);
r = roots([coeff1,0,0]);

t = @(angle)sqrt(2*angle/((t_motor*ratio-m*g)/I));

