
#program base(height, width, max_time).

% Input image
% a a a
% a b b
% a b c

% pattern symbols/identifiers
% pattern(a; b; c).

% based on input image, legal(DX, DY, P1, P2), 
% a pattern P1 and P2 with offset (DX, DY) 
% is a legal rule
% legal(0, 1, a, a).
% legal(0, 1, a, b).
% legal(0, -1, a, a).
% legal(1, 0, a, a).
% legal(1, 0, a, b).
% legal(-1, 0, a, a).

% legal(0, 1, b, b).
% legal(0, 1, b, c).
% legal(0, -1, b, a).
% legal(0, -1, b, b).
% legal(1, 0, b, b).
% legal(1, 0, b, c).
% legal(-1, 0, b, a).
% legal(-1, 0, b, b).

% legal(0, -1, c, b).
% legal(-1, 0, c, b).

cell(X, Y) :- X = 1..width, Y = 1..height.

% initial 
#external assigned(X, Y, P, T) : cell(X, Y), pattern(P), T = 0..max_time.


#program step(t).

% for each assigned cell at t-1, derive all 
% legal super positions at time t
superpos(X+DX, Y+DY, P', t) :- 
        assigned(X, Y, P, t-1), 
        legal(DY, DX, P, P'), 
        not assigned(X+DX, Y+DY, _, _),
        cell(X+DX, Y+DY).

% -superpos(X, Y, P, t) :- not superpos(X, Y, P, t), cell(X, Y), pattern(P).

% inertia
superpos(X, Y, P, t) :- superpos(X, Y, P, t-1).

% Count number of super positions for each cell
superpos_count(X, Y, N, t) :- 
        superpos(X, Y, _, t), 
        N = #count{ P : superpos(X, Y, P, t) }.

% derive minimal super position count at time step t
least_entropy(X, Y, P, t) :- 
        superpos(X, Y, P, t), 
        superpos_count(X, Y, M, t), 
        M = #min{ N : superpos_count(X1, Y1, N, t) }, 
        M != 0.

% #show cell/2.
#show assigned/4.
#show superpos(X, Y, P) : superpos(X, Y, P, t).