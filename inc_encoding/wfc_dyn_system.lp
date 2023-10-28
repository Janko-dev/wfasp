% Waver Function Collapse as a dynamic system. 
% This implementation is deprecated due to the fact that it is very slow
% in terms of grounding. Every time de sub-program step(t) is called,
% all rules need to be regrounded for the specific time step

#program base(width, height, max_steps).

cell((1..width, 1..height)).

% fluents
fluent(inertial, assigned(C, P)) :- cell(C), pattern(P).
fluent(defined, superpos(C, P)) :- cell(C), pattern(P).

% actions
action(force(C, P)) :- cell(C), pattern(P).

% cell (X2, Y2) is adjacent to cell (X1, Y1) with offset (DX, DY) 
adj((X1, Y1), (X2, Y2), (DX, DY)) :-
        cell((X1, Y1)), cell((X2, Y2)),
        offset(DX, DY),
        (X1-X2) = DX, 
        (Y1-Y2) = DY.


#external force(X, Y, P, I) : cell((X, Y)), pattern(P), I = 0..max_steps.

occurs(force((X, Y), P), I) :- force(X, Y, P, I).

#program step(t).

% causal law: force(C, P) causes assigned(C, P)
holds(assigned(C, P), t) :- occurs(force(C, P), t-1), t <= max_steps.

% state constraint: superpos(X+DX, Y+DY, P') if assigned(X, Y, P), legal(DX, DY, P, P'), not assigned(X+DX, Y+DY, _, _) 
superpos_helper(C, P, 0, t) :- 
    cell(C),
    not holds(assigned(C, _), t),
    pattern(P).

superpos_helper(C, P, 1, t) :- 
    cell(C),
    not holds(assigned(C, _), t),
    holds(assigned(C1, P1), t),
    legal(D1, P1, P),
    adj(C, C1, D1).

superpos_helper(C, P, 2, t) :- 
    cell(C),
    not holds(assigned(C, _), t),
    holds(assigned(C1, P1), t),
    holds(assigned(C2, P2), t),
    legal(D1, P1, P),
    legal(D2, P2, P),
    adj(C, C1, D1),
    adj(C, C2, D2),
    C1 != C2.

superpos_helper(C, P, 3, t) :- 
    cell(C),
    not holds(assigned(C, _), t),
    holds(assigned(C1, P1), t),
    holds(assigned(C2, P2), t),
    holds(assigned(C3, P3), t),
    legal(D1, P1, P),
    legal(D2, P2, P),
    legal(D3, P3, P),
    adj(C, C1, D1),
    adj(C, C2, D2),
    adj(C, C3, D3),
    C1 != C2,
    C1 != C3,
    C2 != C3.

superpos_helper(C, P, 4, t) :- 
    cell(C),
    not holds(assigned(C, _), t),
    holds(assigned(C1, P1), t),
    holds(assigned(C2, P2), t),
    holds(assigned(C3, P3), t),
    holds(assigned(C4, P4), t),
    legal(D1, P1, P),
    legal(D2, P2, P),
    legal(D3, P3, P),
    legal(D4, P4, P),
    adj(C, C1, D1),
    adj(C, C2, D2),
    adj(C, C3, D3),
    adj(C, C4, D4),
    C1 != C2,
    C1 != C3,
    C1 != C4,
    C2 != C3,
    C2 != C4,
    C3 != C4.

holds(superpos(C, P), t) :- 
    not holds(assigned(C, _), t),
    N = #count{ C1, D : adj(C1, C, D), holds(assigned(C1, _), t) },
    superpos_helper(C, P, N, t).

% executability condition: impossible force(C, P) if assigned(C, P)
-occurs(force(C, P), t) :- holds(assigned(C, P), t).

% inertia
holds(F, t) :- fluent(inertial, F), holds(F, t-1), not -holds(F, t), t <= max_steps.
-holds(F, t) :- fluent(inertial, F), -holds(F, t-1), not holds(F, t), t <= max_steps.

% CWA defined fluents
-holds(F, t) :- fluent(defined, F), not holds(F, t).

% CWA actions
-occurs(A, t) :- action(A), not occurs(A, t).

% Count number of super positions for each cell
superpos_count(C, N, t) :- 
        holds(superpos(C, _), t), 
        N = #count{ P : holds(superpos(C, P), t) }.

least_entropy(C, P, t) :- 
        holds(superpos(C, P), t), 
        superpos_count(C, M, t),
        M = #min{ N : superpos_count(C1, N, t) }, 
        M != 0.

#show.
#show least_entropy(C, P, t) : least_entropy(C, P, t).
#show holds(assigned(C, P), t) : holds(assigned(C, P), t).

#program input.

% initial state
occurs(force((2, 2), (cross, 0)), 0).
occurs(force((3, 1), (cross, 0)), 0).
occurs(force((1, 1), (v_line, 0)), 0).