program aa;
type m = array [0..5] of integer;
function gor(a: m; x:integer):longint;
var i, f, s:integer;
begin
  f := 1;
  s := a[5];
  for i := 1 to 5 do begin
    f := f * x;
    s := s + a[5 - i] * f;
   end;
  gor := s;
end;


var i, n, c, x, f, s:integer;
    a:m;  
begin
  write('Введите х: ');
  readln(x);
  c := 1;
  for i := 1 to 5 do begin
    write('Введите коэфицент  ', c, '  члена: ');
    readln(a[i]);
    c := c + 1;
  end;
  write('Ответ:  ', gor(a, x));
end.