#program rules.

% slots((name, rotation 90 degrees counter-clockwise), up, down, left, right)
slots((v_line, 0), open, open, closed, closed).
slots((v_line, 1), closed, closed, open, open).

slots((cross, 0), open, open, open, open).

slots((t_split, 0), open, open, closed, open).
slots((t_split, 1), open, closed, open, open).
slots((t_split, 2), open, open, open, closed).
slots((t_split, 3), closed, open, open, open).

slots((edge, 0), open, closed, closed, open).
slots((edge, 1), open, closed, open, closed).
slots((edge, 2), closed, open, open, closed).
slots((edge, 3), closed, open, closed, open).

slots((empty, 0), closed, closed, closed, closed).

% Rule to generate all rotations
% slots((P, I), E4, E1, E2, E3) :- slots((P, I - 1), E1, E2, E3, E4), I = 0..4.

% P1 with x-offset 1 is P2 if P1 has 'right' slot and P2 has 'left' slot
legal((1, 0), P1, P2) :- slots(P1, _, _, _, S), slots(P2, _, _, S, _).

% P1 with x-offset -1 is P2 if P1 has 'left' slot and P2 has 'right' slot
legal((-1, 0), P1, P2) :- slots(P1, _, _, S, _), slots(P2, _, _, _, S).

% P1 with y-offset 1 is P2 if P1 has 'down' slot and P2 has 'up' slot
legal((0, 1), P1, P2) :- slots(P1, _, S, _, _), slots(P2, S, _, _, _).

% P1 with y-offset -1 is P2 if P1 has 'up' slot and P2 has 'down' slot
legal((0, -1), P1, P2) :- slots(P1, S, _, _, _), slots(P2, _, S, _, _).

pattern(P) :- slots(P, _, _, _, _).

offset(1, 0).
offset(-1, 0).
offset(0, 1).
offset(0, -1).

% each pattern occurs once in the input tiles.
% in other words, there is no example image
% to base the weights off of.
pattern_weight(P, 1) :- pattern(P).

% #show pattern_weight/2.

