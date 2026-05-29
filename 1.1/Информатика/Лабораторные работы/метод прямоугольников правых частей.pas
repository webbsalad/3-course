program aa;
var 
  a, b, x, s, n, h: real;
function integ(x: real): real;
begin
  integ := ((cos(0.3 * x + 0.5)) / (1.8 + sin(x*x + 0.8)));
end;
begin
  writeln('Введите отрезок измерения: ');
  a:= 0.3;
  b:= 1.1;
  writeln('Введите колличество отрезков: ');
  read(n);
  s := 0;
  h := (b - a) / n;
  x := a;
  while x < (b - h) do begin
    s := s + integ(x);
    x := x + h;
  end;
  s := h * s;
  writeln('Шаг: ', h);
  write('Ответ: ', s);
end.