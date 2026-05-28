program aa;
var c, r, h, e, t, U, k, Uv: real;

begin
  c := 0.01;
  r := 2;
  h := 0.01;
  U := 50;
  t := 0.01;
  e := power(10, -3);
  k := r * c;
  repeat
    Uv := U * (1 - exp(-t / k));
    writeln(t:0:2, '  ', Uv:0:6);
    t := t + h;
  until abs(Uv - U) < e;
end.
