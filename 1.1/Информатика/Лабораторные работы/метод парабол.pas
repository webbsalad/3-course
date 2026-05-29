program aa;
var
  x, a, b, h, s: real;
  n: integer;
function integ(t: real): real;
begin
  integ := ((cos(0.3 * x + 0.5)) / (1.8 + sin(x*x + 0.8)));
end;
begin 
  writeln('отрезок интегрирования: ');
  a:= 0.3;
  b:= 1.1;
  writeln('колличество отрезков: ');
  read(n);
  h := (b - a) / n;
  s := 0;
  x := a + h;
  while x < (b-h) do begin
    s := s + 4 * integ(x);
    s := s + 2 * integ(x+h);
    x := x + (2 * h);
  end;
  s := (h / 3) * (s + integ(a) + integ(b));
  writeln('Шаг: ', h);
  writeln('ответ: ', s);
end.
