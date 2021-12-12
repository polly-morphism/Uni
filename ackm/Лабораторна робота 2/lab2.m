disp("Інтегрування:")
quad('sqrt(4 - x**2)/x',0.2,1,0.01)
disp("Диференціювання:")
x_start = 0.2;
x_end = 1;
h_dif = 0.01;
N = 40;

f = @(x) sqrt(4 - x.^2);
F = @(x) sqrt(4 - x.^2) - 2*log((2 + sqrt(4 - x.^2)) / x);

x = linspace(x_start, x_end, N);

h = (x_end - x_start) / 2 * (N - 1);
xi = x_start:h:x_end;

real = h / 3 * (f(xi(1)) + 2 * sum(f(xi(3: 2: end - 2))) + 4 * sum(f(xi(2: 2: end))) + f(xi(end)));

real_result = F(x_end) - F(x_start);
real;


x = 0.5;
x0 = x_start:h_dif:x_end;

n = size(x0, 2) - 1;
new_real = 0;

for idx=1:n
    if ((x < x0(idx+1)) && (x >= x0(idx)))
        if (idx == 0)
            new_real += (-3 * F(x0(idx)) + 4 * F(x0(idx + 1)) - F(x0(idx + 2))) / (2 * h_dif);
            break;
        elseif (idx == n)
            new_real += (3 * F(x0(idx)) - 4 * F(x0(idx - 1)) + F(x0(idx - 2))) / (2 * h_dif);
            break;
        else
            new_real += (F(x0(idx + 1)) - F(x0(idx - 1))) / (2 * h_dif);
            break;
        endif;
    endif;
endfor;

disp(new_real);
