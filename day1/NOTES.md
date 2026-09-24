hof is a higher order funciton that takes or returns a function. 

call at bind : wrapper(func) call at use : func()

closure is keeping the enclosing name (func) alive after outer function returns, but high order function is the shape of the take/return calllable 

if we return func, side effect is skipped
if we return func(), not a callable, it means execute func() at that point and it wont be stored later to use