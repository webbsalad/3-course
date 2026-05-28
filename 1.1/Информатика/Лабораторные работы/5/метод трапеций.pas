program aa;
var 
  a, b, x, s, i, n, h: real;
function integ(x: real): real;
begin
  integ := x*x;
end;
begin
  writeln('Введите отрезок измерения: ');
  a:= 0.3;
  b:= 1.1;
  writeln('Введите колличество отрезков: ');
  read(n);
  s := 0;
  h := (b - a) / n;
  x := a + h;
  while x < (b - h) do begin
    s := s + ((integ(x) + integ(x + h)) / 2);
    x := x + h;
  end;
  s := h * (((integ(a) + integ(b)) / 2) + s);
  writeln('Шаг: ',h);
  writeln('Ответ: ', s);
end.