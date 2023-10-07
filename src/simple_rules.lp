#program rules.

% 2x1 patterns
% legal(2, 0, (a, a), (a, a)).
% legal(2, 0, (a, b), (b, b)).
% legal(2, 0, (a, b), (c, b)).

% legal(-2, 0, (a, a), (a, a)).
% legal(-2, 0, (b, b), (a, b)).
% legal(-2, 0, (c, b), (a, b)).

% legal(0, 2, (a, a), (a, b)).
% legal(0, 2, (a, a), (b, b)).
% legal(0, 2, (a, b), (a, b)).
% legal(0, 2, (b, b), (c, b)).
% legal(0, 2, (b, b), (b, c)).
% legal(0, 2, (b, c), (b, b)).
% legal(0, 2, (c, b), (b, b)).

% legal(0, -2, (a, b), (a, a)).
% legal(0, -2, (b, b), (a, a)).
% legal(0, -2, (a, b), (a, b)).
% legal(0, -2, (c, b), (b, b)).
% legal(0, -2, (b, c), (b, b)).
% legal(0, -2, (b, b), (b, c)).
% legal(0, -2, (b, b), (c, b)).

% legal(2, 0, ((a, a), (a, b)), ((a, a), (b, b))).
% legal(2, 0, ((a, b), (a, b)), ((b, b), (c, b))).
% legal(2, 0, ((a, b), (a, b)), ((c, b), (b, b))).
% legal(-2, 0, ((a, a), (b, b)), ((a, a), (a, b))).
% legal(-2, 0, ((b, b), (c, b)), ((a, b), (a, b))).
% legal(-2, 0, ((c, b), (b, b)), ((a, b), (a, b))).

% legal(0, 2, ((a, a), (a, b)), ((a, b), (a, b))).
% legal(0, 2, ((a, a), (b, b)), ((b, c), (b, b))).
% legal(0, 2, ((a, a), (b, b)), ((c, b), (b, b))).
% legal(0, -2, ((a, b), (a, b)), ((a, a), (a, b))).
% legal(0, -2, ((b, c), (b, b)), ((a, a), (b, b))).
% legal(0, -2, ((c, b), (b, b)), ((a, a), (b, b))).

legal(1, 0, ((a, a), (a, b)), ((a, a), (b, b))).
legal(1, 0, ((a, a), (b, b)), ((a, a), (b, b))).
legal(1, 0, ((a, b), (a, b)), ((b, b), (b, c))).
legal(1, 0, ((b, b), (b, c)), ((b, b), (c, b))).
legal(1, 0, ((a, b), (a, b)), ((b, c), (b, b))).
legal(1, 0, ((b, c), (b, b)), ((c, b), (b, b))).

legal(0, 1, ((a, a), (a, b)), ((a, b), (a, b))).
legal(0, 1, ((a, b), (a, b)), ((a, b), (a, b))).
legal(0, 1, ((a, a), (b, b)), ((b, b), (b, c))).
legal(0, 1, ((b, b), (b, c)), ((b, c), (b, b))).
legal(0, 1, ((a, a), (b, b)), ((b, b), (c, b))).
legal(0, 1, ((b, b), (c, b)), ((c, b), (b, b))).

legal(-1, 0, Right, Left) :- legal(1, 0, Left, Right).
legal(0, -1, Down, Up) :- legal(0, 1, Up, Down).

% legal(1, 0, ((P1, P2), (P3, P4)), ((P1, P2), (P3, P4)))

pattern(P) :- legal(_, _, P, _).
pattern(P) :- legal(_, _, _, P).

% pattern(((a, a), (a, b))).
% pattern(((a, b), (a, b))).
% pattern(((a, a), (b, b))).
% pattern(((b, b), (c, b))).
% pattern(((b, b), (b, c))).
% pattern(((c, b), (b, b))).
% pattern(((b, c), (b, b))).