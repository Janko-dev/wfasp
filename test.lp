
#program base(n).
% #const n = 3.

state(a; b; c).


% collapsed position
% collapsed(1, 1, a).

% a a a
% a b b
% a b c

% rules formulation based on image
rule(a, right, a).
rule(a, right, b).
rule(a, left, a).
rule(a, up, a).
rule(a, down, a).
rule(a, down, b).

rule(b, right, b).
rule(b, right, c).
rule(b, left, a).
rule(b, left, b).
rule(b, up, a).
rule(b, up, b).
rule(b, down, b).
rule(b, down, c).

rule(c, left, b).
rule(c, up, b).

% superpositions
{ superpos(R, C, S) : state(S) } = 1 :- R = 1..n, C = 1..n.

#external collapsed(R, C, S) : superpos(R, C, S).

:- collapsed(R, C, S1), superpos(R, C, S2), S1 != S2.

#program step.

% apply rules
:- not rule(P, right, Wrt), collapsed(R, C, P), superpos(R, C+1, Wrt).
:- not rule(P, left, Wrt),  collapsed(R, C, P), superpos(R, C-1, Wrt).
:- not rule(P, up, Wrt),    collapsed(R, C, P), superpos(R+1, C, Wrt).
:- not rule(P, down, Wrt),  collapsed(R, C, P), superpos(R-1, C, Wrt).

#show superpos/3.
% #show entropy/3.