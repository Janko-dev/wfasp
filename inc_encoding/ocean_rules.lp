#program rules.

pattern(beach).


legal((1, 0), (beach, 0), (beach_shallow, 2)).
legal((1, 0), (beach, 0), (beach_shallow_curve_in, 2)).
legal((1, 0), (beach, 0), (grass_beach, 0)).
legal((1, 0), (beach, 0), (grass_beach_curve_out, 0)).
legal((1, 0), (beach, 0), (grass_beach_curve_out, 1)).


offset(1, 0).
offset(-1, 0).
offset(0, 1).
offset(0, -1).

% each pattern occurs once in the input tiles.
% in other words, there is no example image
% to base the weights off of.
pattern_weight(P, 1) :- pattern(P).
