c = [-5, -8]';
b = [300, 400, 100, 200]';
A = [2, 5; 4, 5; 3, 0; 0, 4];

lb=[0, 0]';
ub = [];
ctype = "UUUU";
vartype = "CC";


[xmin, fmin, status, extra] = glpk (c, A, b, lb, ub, ctype, vartype);
disp(xmin);
disp(fmin);