program aa;
type mas = array [0..5] of real;
function gor(a:mas; x:real; n:integer):real;
var f, s:real;
    i:integer;
begin
  f := 1;
  n := 5;
  s := a[5];
  for i := 1 to 5 do begin
    f := f * x;
    s := s + a[5 - i] * f;
   end;
  gor := s;
end;
var i, n , c:integer;
    f, s, x:real;
    a:mas;
begin
  write('Введите х:');
  readln(x);
  c := 1;
  for i := 1 to 5 do begin
    writeln('Введите коэфицент  ', c, '  члена');
    readln(a[i]);
    c := c + 1;
  end;
  write('Ответ:  ', gor(a, x, 5));
end.