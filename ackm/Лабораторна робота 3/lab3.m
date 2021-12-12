clear; clc; 
function Dy = runge(x, y)
Dy = y(:);
Dy(1) = y(2);
Dy(2) = 3*Dy(1) - 2*y(1) + 2*x - 3;
endfunction


h = 0.2; 
x_fin = 2; 
y0 = 1; 
Dy0 = 2; 
[x, y] = ode45('runge', [0:h:x_fin], [y0 Dy0]); 
plot(x, y, 'LineWidth', 2); grid;  
legend('y(x)', 'y''(x)', 0);
