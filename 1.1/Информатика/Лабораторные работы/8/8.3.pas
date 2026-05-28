program aa;
function f(i: integer): integer;
var m, n: integer;
begin
  n := 1;
  for m := 1 to i do
    n := n * m;
  f := n;
end;

var x, u, s, e: real;
    k, n: integer;
begin
  x := Pi / 6;
  u := x;
  s := x;
  k := 1;
  e := power(10, -4);
  while abs(u) > e do
    begin
      n := 2 * k + 1;
      if (k div 2 <> 0) then
        u := (-1) * (exp(n * ln(x)) / f(n))
      else
        u := (exp(n * ln(x)) / f(n));
      s := s + u;
      k := k + 1;
    end;
  writeln(s:0:6);
end.
