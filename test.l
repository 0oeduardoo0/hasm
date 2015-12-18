.inc "foo.l"
.inc "std.l"

main  ; this is a comment
{  
   add "string 1", "string 2"    ; this is a comment
   foo
   bar
}

foo 
{
   mov n1, n2
   lea dx
   out "foo"
}