# natural-representation

Python and C code for converting between the numerator/denominator and natural representation forms of rational numbers.

The natural representation of a rational number is a finite sequence of integers which are all required to be non-zero apart from the first integer and the last integer in the sequence.

This is an order-preserving representation which uniquely expresses each rational number as a novel type of continued fraction. 

The integers in the sequence specify the reciprocals in the continued fraction as well as the route from zero to that rational number in a tree which lists each rational number exactly once in its simplest form. The tree is a binary tree except at the root node, which represents zero and connects to three child nodes, representing 1, -1/2 and -1.

This tree extends the Stern-Brocot tree from positive rationals to all rational numbers. The first 7 levels of this tree are shown in `treeposter.pdf`, for both rational numbers and their natural representations. The forumulae for converting between the two are also shown there.

The code which generated the trees and their tikz-cd LaTeX code is given in the `draw_tree.py` script.

The theory underlying natural representations is presented in the `constituents.pdf` document.
