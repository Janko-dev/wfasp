
#program base(width, height).

cell((1..width, 1..height)).

% cell (X2, Y2) is adjacent to cell (X1, Y1) with offset (DX, DY) 
adj((X1, Y1), (X2, Y2), (DX, DY)) :-
        cell((X1, Y1)), cell((X2, Y2)),
        offset(DX, DY),
        (X1-X2) = DX, 
        (Y1-Y2) = DY.

% external input
#external force(X, Y, P) : cell((X, Y)), pattern(P).

% convert input to assigned tiles
assigned((X, Y), P) :- force(X, Y, P).

% superpos_helper(C, P, N) with C = (X, Y), P is the pattern, and N is the number of assigned neighbours w.r.t. C.
% These helpers compute for each number of neighbours the corresponding super positions.  
superpos_helper(C, P, N) :- 
    cell(C),
    not assigned(C, _),
    pattern(P),
    N = #count{C1,D1: assigned(C1,P1), legal(D1,P1,P), adj(C,C1,D1)}.

% State constraint: superpos(C, P) if not assigned(C, _), superpos_helper(C, P, N) where N = #(assigned neighbours).
superpos(C, P) :- 
    N = #count{ C1, D : adj(C1, C, D), assigned(C1, _) },
    superpos_helper(C, P, N).

% Count number of super positions for each cell
superpos_count(C, N) :- 
        superpos(C, _), 
        N = #count{ P : superpos(C, P) }.

% Compute the super positions with the lowest entropy
% i.e., the super positions of the cell that has the 
% fewest occurrences 
lowest_entropy(C, P, W) :- 
        superpos(C, P), 
        superpos_count(C, M),
        pattern_weight(P, W),
        M = #min{ N : superpos_count(C1, N) },
        M != 0.

#show lowest_entropy/3.
#show assigned/2.

#program input.
% force(5, 8, (((191, 232, 242, 255), (191, 232, 242, 255), (191, 232, 242, 255)), ((185, 122, 87, 255), (185, 122, 87, 255), (185, 122, 87, 255)), ((185, 122, 87, 255), (185, 122, 87, 255), (185, 122, 87, 255)))).

% force(4, 4, (((185, 122, 87, 255), (185, 122, 87, 255)), ((185, 122, 87, 255), (185, 122, 87, 255)))).

% initial state
% force(3, 3, (cross, 0)).
% force(4, 1, (cross, 0)).
% force(1, 1, (v_line, 0)).
