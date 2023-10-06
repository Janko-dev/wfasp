
#program base(height, width, max_time).

% Input image
% a a a
% a b b
% a b c

state(a; b; c).

% rules formulation based on image
rule(a, offset(0, 1), a).
rule(a, offset(0, 1), b).
rule(a, offset(0, -1), a).
rule(a, offset(1, 0), a).
rule(a, offset(1, 0), b).
rule(a, offset(-1, 0), a).

rule(b, offset(0, 1), b).
rule(b, offset(0, 1), c).
rule(b, offset(0, -1), a).
rule(b, offset(1, 0), b).
rule(b, offset(1, 0), c).
rule(b, offset(-1, 0), b).
rule(b, offset(-1, 0), a).

rule(c, offset(0, -1), b).
rule(c, offset(-1, 0), b).


offset(1, 0).
offset(0, 1).
offset(-1, 0).
offset(0, -1).

cell(R, C) :- R = 1..height, C = 1..width.

% derive all superpositions
{ superpos(R, C, S) : state(S) } = 1 :- cell(R, C).

% external input collapsed
#external assigned(R, C, S, 0..max_time) : superpos(R, C, S).


#program step(t).

% if collapsed, then all superpositions must collapse
:- assigned(R, C, S1, t), superpos(R, C, S2), S1 != S2.

% superpos(R+DY, C+DX, S', t) :- 
%         assigned(R, C, S, t-1), 
%         rule(S, offset(DY, DX), S'), 
%         not assigned(R+DY, C+DX, _, _),
%         cell(R+DY, C+DX).

:- rule(S, offset(DY, DX), S1), assigned(R, C, S, t), superpos(R+DY, C+DX, S2), S1 != S2.

% #minimize{ 1, R, C : superpos(R, C, S), not assigned(R, C, S, t) }.

% apply rules
% :- not rule(P, right, Wrt), collapsed(R, C, P), superpos(R, C+1, Wrt).
% :- not rule(P, left, Wrt),  collapsed(R, C, P), superpos(R, C-1, Wrt).
% :- not rule(P, up, Wrt),    collapsed(R, C, P), superpos(R+1, C, Wrt).
% :- not rule(P, down, Wrt),  collapsed(R, C, P), superpos(R-1, C, Wrt).

#show superpos/3.
#show assigned/4.


% #script(python)

% from clingo.symbol import Number, Function

% def main(prg):
    
%     width = 4
%     height = 2
%     iters = width*height

%     prg.ground([("base", [Number(height), Number(width), Number(iters-1)])])

%     prg.assign_external(
%         Function("assigned", [
%             Number(2), Number(4),
%             Function("c"), Number(0)
%         ]), True)
    
%     prg.ground([("step", [Number(0)])])

%     with prg.solve(yield_=True) as handle:
        
%         for model in handle:    
%             pass
%             #print(model)

% #end.