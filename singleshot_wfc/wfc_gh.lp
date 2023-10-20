#script (python)

import time

class Visigator:
    def init(self, init):
        self.prop_iter = 0
        self.triples = {}
        self.world = {}
        for atom in init.symbolic_atoms:
            if(atom.symbol.name == 'assign'):
                print(atom.symbol)
                s_lit = init.solver_literal(atom.literal)
                init.add_watch(s_lit)
                self.triples[s_lit] = (
                    atom.symbol.arguments[0].number,
                    atom.symbol.arguments[1].number,
                    atom.symbol.arguments[2])
    
    def propagate(self, ctl, changes):
        for l in changes:
            x,y,p = self.triples[l]
            self.world[x,y] = p
        if self.prop_iter % 100 == 0:
            self.dump_world()
        self.prop_iter += 1
        return True
    
    def undo(self, solver_id, assign, undo):
        for l in undo:
            x,y,p = self.triples[l]
            del self.world[x,y]
    
    def dump_world(self):
        lines = []
        for j in range(1, 6):
            line = []
            for i in range(1, 6):
                if (i,j) in self.world:
                    line.append(str(self.world[i,j])[1] + str(self.world[i,j])[-2])
                else:
                    line.append('..')
            lines.append(''.join(line))
        print('\n'.join(lines), '\n')
        time.sleep(0.1)

def main(prg):
    prg.register_propagator(Visigator())
    prg.ground([("base", [])])
    prg.solve()
#end.

#const n = 5.
#const m = 5.
% define?
cell(1..m, 1..n).

% tiles, format: 
% pdef((tile name, 0), bottom edge, right edge, top edge, left edge)

pdef((line_v, 0), empty, path, empty, path).

pdef((none, 0), empty, empty, empty, empty).

pdef((plus, 0), path, path, path, path).

pdef((corner, 0), path, path, empty, empty).

pdef((tee, 0), empty, path, path, path).

% generate rotations of the tile
pdef((P, I), E4, E1, E2, E3) :- pdef((P, I - 1), E1, E2, E3, E4), I <= 4, I >= 0.

pattern(P) :- pdef(P, _, _, _, _).

walkable(path).

dx( 0, 1).
dx( 1, 0).
dx( 0,-1).
dx(-1, 0).

% any pattern can be placed on itself
legal(0, 0, P, P) :- pattern(P).

% P1 can be above P2 if P1's bottom edge and P2'
% top edge are connectable
legal(0, 1, P1, P2) :-
  pdef(P1, E1, _, _, _), 
  pdef(P2, _, _, E2, _), 
  E1 == E2.

% P1 can be left of P2 if P1's right edge and P2's
% left edge are connectable
legal(1, 0, P1, P2) :-
  pdef(P1, _, E1, _, _), 
  pdef(P2, _, _, _, E2), 
  E1 == E2.

% P1 can be below P2 if P1's top edge and P2's
% bottom edge are connectable
legal(0, -1, P1, P2) :-
  pdef(P1, _, _, E1, _), 
  pdef(P2, E2, _, _, _), 
  E1 == E2.

% P1 can be right of P2 if P1's left edge and P2's
% right edge are connectable
legal(-1, 0, P1, P2) :-
  pdef(P1, _, _, _, E1), 
  pdef(P2, _, E2, _, _), 
  E1 == E2.

% walkable means that it's possible to walk from 
% p1 to p2 in direction (DX, DY)
walkable(0, 1, P1, P2) :-
  pdef(P1, E1, _, _, _), 
  pdef(P2, _, _, E1, _),
  walkable(E1).

walkable(1, 0, P1, P2) :-
  pdef(P1, _, E1, _, _), 
  pdef(P2, _, _, _, E1),
  walkable(E1).

walkable(0, -1, P1, P2) :-
  pdef(P1, _, _, E1, _), 
  pdef(P2, E1, _, _, _),
  walkable(E1). 

walkable(-1, 0, P1, P2) :-
  pdef(P1, _, _, _, E1), 
  pdef(P2, _, E1, _, _),
  walkable(E1).

% there's an edge between two tiles if 
% we can walk from that tile to the other
% (we'll use this to check for connectivity later)
edge((X1, Y1), (X2, Y2)) :- 
  assign(X1, Y1, P1), 
  assign(X2, Y2, P2),
  walkable(X1 - X2, Y1 - Y2, P1, P2).

edge(X,Y) :- edge(Y,X).

connected(X,Y):- edge(X,Y).

connected(X,Z):- edge(X,Y) ; connected(Y,Z).

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
:- pattern(P), not 1 { assign(X,Y,P):cell(X,Y) }.

% the top left corner must be connected to any tile with Y=n
:- not 1 { connected((1, 1), (X, n)):cell(X,n) }.


#show assign/3.
#show edge/2.