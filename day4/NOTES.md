easy design:

 Own: after every successful apply, position(symbol) equals signed sum of applied fills for that symbol, 
 and a rejected fill leaves state unchanged.

(FIFO matters when lots close at different entry prices; avg is simpler and valid if you document it.)

Fill = frozen/immutable value (dataclass frozen=True or NamedTuple). Only PositionLedger.apply mutates. Also: reject qty ≤ 0, bad side, empty symbol, duplicate fill_id.
medium design:

hard design:

