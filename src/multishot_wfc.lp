
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

% initial
#external assigned(R, C, S, T) : R = 1..height, C = 1..width, state(S), T = 0..max_time.

cell(R, C) :- R = 1..height, C = 1..width.

#program step(t).

% assigned(R, C, S, t) :- assigned(R, C, S, t-1).

superpos(R+DY, C+DX, S', t) :- 
        assigned(R, C, S, t-1), 
        rule(S, offset(DY, DX), S'), 
        not assigned(R+DY, C+DX, _, _),
        cell(R+DY, C+DX).

superpos(R, C, S, t) :- superpos(R, C, S, t-1).

superpos_count(R, C, N, t) :- 
        superpos(R, C, _, t), 
        N = #count{ S : superpos(R, C, S, t) }.

least_entropy(R, C, S, t) :- 
        superpos(R, C, S, t), 
        superpos_count(R, C, M, t), 
        M = #min{ N : superpos_count(R1, C1, N, t) }, 
        M != 0.

#show assigned/4.
#show superpos(R, C, S) : superpos(R, C, S, t).

% assigned(2,2,b,0) 
% assigned(2,1,a,1) 
% assigned(1,1,a,2) 
% assigned(1,2,a,3) 
% assigned(1,3,a,4) 
% assigned(2,3,a,5) 
% assigned(2,4,a,6) 
% assigned(1,4,a,7)

% #show superpos_count/4.
% #show least_entropy/4.

% #script(python)

% from clingo.symbol import Number, Function

% def get_least_entropy(model, t):

%     for atom in model.symbols(atoms=True):
%         if atom.match("least_entropy", 4) and atom.arguments[3].number == t:
            
%             r = atom.arguments[0].number
%             c = atom.arguments[1].number
            
%             s = atom.arguments[2].name

%             return (r, c, s)

% def main(prg):

%     width = 4
%     height = 2
%     iters = width*height

%     prg.ground([("base", [Number(height), Number(width), Number(iters-1)])])
    
%     # initialize
%     prg.assign_external(
%         Function("assigned", [
%             Number(2), Number(2),
%             Function("b"), Number(0)
%         ]), True)

%     prg.assign_external(
%         Function("assigned", [
%             Number(1), Number(1),
%             Function("a"), Number(2)
%         ]), True)
    
%     prg.solve()

%     return

%     # iteration
%     for i in range(1, iters):

%         prg.ground([("step", [Number(i)])])
%         r, c, s = 0, 0, ""
%         with prg.solve(yield_=True) as handle:
            
%             for model in handle:    
%                 r, c, s = get_least_entropy(model, i)

%         print(r, c, s, i)

%         prg.assign_external(
%             Function("assigned", [
%                 Number(r), Number(c),
%                 Function(s), Number(i)
%             ]), True)
    
%     prg.solve()

% #end.