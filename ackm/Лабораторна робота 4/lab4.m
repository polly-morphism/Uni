x = [-1, -2, -3, -4];
e=0.0001;
h=1; 
n=4;

function res = myfunc(x)
    res = (x(1)-1)**2 + 10*(x(2)-1)**2 + 100*(x(3)-1)**2 + 1000*(x(4)-1)**2;
end
 

xb=x;
rb=myfunc(xb);
 
while (h > e)
    
    x=xb;
    r=rb;
    x1=x;
    for i=1:n
        x1(1,i) = x(1,i) + h;
        r1 = myfunc (x1);
        if (r1 < r)
            x = x1;
            r = r1;
        else
            x1(1,i) = x(1,i) - h;
            r1 = myfunc (x1); 
            if (r1 < r)
                x = x1;
                r = r1;
            end
        end;
    end;
     

    if (r < rb)
 
      while(1)
        xpb = xb;
        rpb = rb;
        xb = x;
        rb = r;    

        xp=zeros(1,n);
        for i=1:n
          xp(1,i) = xpb(1,i) + 2 * (xb(1,i) - xpb(1,i));
        end
      
        x=xp;
        r=myfunc (x);
        x1=x;        
        for i=1:n
            x1(1,i) = x(1,i) + h;
            r1 = myfunc (x1);
            if (r1 < r)
                x = x1;
                r = r1;
            else
                x1(1,i) = x(1,i) - h;
                r1 = myfunc (x1); 
                if (r1 < r)
                    x = x1;
                    r = r1;
                end
            end
        end;
     
        if (r >= rb)
            break;
        end;
      end;  
    end;
    h = h / 10;
end;
disp('Результат ');
disp(xb);
disp("Значення функції: ");
disp(myfunc(xb));