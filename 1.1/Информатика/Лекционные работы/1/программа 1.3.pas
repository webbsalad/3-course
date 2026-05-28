program aa;
var r, a, b: real;

begin
  read(a, b);
  r := (b / a * (1 + 0.707 * sqrt(1 - a / b)) - 1) * (b / a * (1 + 0.707 * sqrt(1 - a / b)) - 1);
  write (r);
end.