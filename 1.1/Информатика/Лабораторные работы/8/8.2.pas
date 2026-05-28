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
    k: integer;
begin
  x := 0.5;
  u := 1;
  s := 1;
  k := 1;
  e := power(10, -4);
  while u > e do
  begin
    u := (exp(k * ln(x)) / f(k));
    s := s + u;
    k := k + 1;
  end;
  writeln(s:0:6);
end.
