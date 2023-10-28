
#program base(height, width).

cell((1..width, 1..height)).

% input
#external force(C, P) : cell(C), pattern(P).

% for every cell, choose a pattern and assign it to the cell
{ assigned(C, P): pattern(P) } = 1 :- cell(C).

% adj(C1, C2, D): derive all cells C2 adjacent to C1 with offset D. 
adj((X1, Y1), (X2, Y2), (DX, DY)) :-
        cell((X1, Y1)), cell((X2, Y2)),
        offset(DX, DY),
        (X1-X2) = DX, 
        (Y1-Y2) = DY.

% input from python api
assigned(C, P) :- force(C, P).

% Reject answer sets where there are no legal assignments to cells adjacent to another assigned cell
:- adj(C1, C2, D), assigned(C1, P1), { assigned(C2, P2) : legal(D, P2, P1)} 0.

% Extending WFC:
% Only keep answer sets where every assigned cell is reachable via a path
% from all other assigned cells. 
% open_slot(open).

% open_slot((1, 0), P1, P2) :-  slots(P1, _, _, _, S), slots(P2, _, _, S, _), open_slot(S).
% open_slot((-1, 0), P1, P2) :- slots(P1, _, _, S, _), slots(P2, _, _, _, S), open_slot(S).
% open_slot((0, 1), P1, P2) :-  slots(P1, _, S, _, _), slots(P2, S, _, _, _), open_slot(S).
% open_slot((0, -1), P1, P2) :- slots(P1, S, _, _, _), slots(P2, _, S, _, _), open_slot(S).

% edge((X1, Y1), (X2, Y2)) :- 
%         assigned((X1, Y1), P1), 
%         assigned((X2, Y2), P2), 
%         open_slot((X2-X1, Y2-Y1), P1, P2).

% edge(C1, C2) :- edge(C2, C1).

% reachable(C1, C2) :- edge(C1, C2).
% reachable(C1, C3) :- edge(C1, C2), reachable(C2, C3).

% :- assigned(C1, P1), assigned(C2, P2), not reachable(C1, C2), C1 != C2.

% #show assigned/2.
#show.

#program input.
force((3, 3), (cross, 0)).
force((4, 1), (cross, 0)).
force((1, 1), (v_line, 0)).

