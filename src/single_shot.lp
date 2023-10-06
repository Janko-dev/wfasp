% https://github.com/aman-tiwari/asp-vox/tree/master


#const n = 2.
#const m = 2.
% define?
cell(1..m, 1..n).

% tiles, format: 
% pdef((tile name, rotation in 90deg increments), bottom edge, right edge, top edge, left edge)


% pdef(c, empty, empty, path, path).


% pdef((line_v_a, 0), empty, path, empty, path).
% pdef((corner_a,0), path, path, empty, empty).
% pdef((line_v_a, 1), path, empty, path, empty).

% pdef((line_v_b, 0), empty, path, empty, path).

% pdef((none,0), empty, empty, empty, empty).
% pdef((plus,0), path, path, path, path).

% pdef((corner,0), path, path, empty, empty).
% pdef((corner,3), path, empty, empty, path).

% pdef((corner,1), empty, path, path, empty).
% pdef((corner,2), empty, empty, path, path).

% pattern(P) :- pdef(P, _, _, _, _).

pattern(a; b; c).

% Input image
% a a a
% a b b
% a b c

% P1 above P2
legal(0, 1, a, a).
legal(0, 1, a, b).
legal(0, -1, a, a).
legal(1, 0, a, a).
legal(1, 0, a, b).
legal(-1, 0, a, a).

legal(0, 1, b, b).
legal(0, 1, b, c).
legal(0, -1, b, a).
legal(0, -1, b, b).
legal(1, 0, b, b).
legal(1, 0, b, c).
legal(-1, 0, b, a).
legal(-1, 0, b, b).

legal(0, -1, c, b).
legal(-1, 0, c, b).

dx( 0, 1).
dx( 1, 0).
dx( 0,-1).
dx(-1, 0).

% any pattern can be placed on itself
legal(0, 0, P, P) :- pattern(P).

% P1 can be above P2 if P1's bottom edge and P2'
% top edge are connectable
% legal(0, 1, P1, P2) :-
%   pdef(P1, E1, _, _, _), 
%   pdef(P2, _, _, E2, _), 
%   E1 == E2.

% % P1 can be left of P2 if P1's right edge and P2's
% % left edge are connectable
% legal(1, 0, P1, P2) :-
%   pdef(P1, _, E1, _, _), 
%   pdef(P2, _, _, _, E2), 
%   E1 == E2.

% % P1 can be below P2 if P1's top edge and P2's
% % bottom edge are connectable
% legal(0, -1, P1, P2) :-
%   pdef(P1, _, _, E1, _), 
%   pdef(P2, E2, _, _, _), 
%   E1 == E2.

% % P1 can be right of P2 if P1's left edge and P2's
% % right edge are connectable
% legal(-1, 0, P1, P2) :-
%   pdef(P1, _, _, _, E1), 
%   pdef(P2, _, E2, _, _), 
%   E1 == E2.

% walkable means that it's possible to walk from 
% p1 to p2 in direction (DX, DY)
% walkable(0, 1, P1, P2) :-
%   pdef(P1, path, _, _, _), 
%   pdef(P2, _, _, path, _).

% walkable(1, 0, P1, P2) :-
%   pdef(P1, _, path, _, _), 
%   pdef(P2, _, _, _, path).

% walkable(0, -1, P1, P2) :-
%   pdef(P1, _, _, path, _), 
%   pdef(P2, path, _, _, _). 

% walkable(-1, 0, P1, P2) :-
%   pdef(P1, _, _, _, path), 
%   pdef(P2, _, path, _, _).

% there's an edge between two tiles if 
% we can walk from that tile to the other
% (we'll use this to check for connectivity later)
% edge((X1, Y1), (X2, Y2)) :- 
%   assign(X1, Y1, P1), 
%   assign(X2, Y2, P2).
%   % walkable(X1- X2, Y1 - Y2, P1, P2).

% edge(X,Y) :- edge(Y,X).

% connected(X,Y):- edge(X,Y).

% connected(X,Z):- edge(X,Y), connected(Y,Z).

% P1 can be left/below of P2 if P2 can be right/above P1
% legal(DX, DY, P1, P2) :- legal(-DX, -DY, P2, P1).

% two positions are adjacent if they are within cells and the difference
% in x and y is equal to dx and dy
adj(X1, Y1, X2, Y2, DX, DY) :-
  cell(X1, Y1), cell(X2, Y2),
  dx(DX, DY), (X1 - X2)==DX, (Y1 - Y2)==DY.

% generate?
1 { assign(X,Y,P):pattern(P) } 1 :- cell(X,Y).

% fail if two cells are adjacent and one of them is assigned P1 at X1 Y1
% but no legal assignment for X2 Y2 exists
:- adj(X1,Y1,X2,Y2,DX,DY), assign(X1,Y1,P1),
  not 1 { assign(X2,Y2,P2):legal(DX,DY,P1,P2) }.
  
% every pattern must be present at least 1 times
% :- pattern(P), not 1 { assign(X,Y,P):cell(X,Y) }.

% assign(1,1,c).

% the top left corner and the bottom right corner must be connected
% :- not connected((1, 1), (m, n)).


#show assign/3.
% #show edge/2.