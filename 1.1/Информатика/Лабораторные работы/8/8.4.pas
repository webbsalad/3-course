program aa;
var x, u, s, e, M: real;
    k: integer;
begin
  x := Pi / 6;
  u := 1;
  s := 1;
  k := 1;
  e := power(10, -4);
  repeat
    M := -(x*x) / (4 *k*k - 2*k);
    u := u * M;
    s := s + u;
    k := k + 1;
  until abs(u) <= e;
  writeln(s:0:6);
end.