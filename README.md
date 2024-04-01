# Chickenomata
Experimenting with cellular automata concepts


Premise:
I was fascinated by S.Wolfram, J.Conway and V.Neumann.
In particular their research on Cellular Automata.
I'm not the first nor the last to end on this path.
Fascinated is a weak word, perhaps enthalled or captivated better expresses the condition.
As such I was spellbound to give my own shot at producing some automata.

My first objective was to create a minimum viable automata.
Which turned out to be a rather simple task.
As expected from a "complexity out of simplicity" concept perhaps?
Copied some code, got some LLM spaghetti and it was done.

But that wasn't enough, it never is with these things.
I had Ideas. Aspirations. Delusions. Passion.

First idea had to with. I forgot.
--Insert here--
Had to do with iteration one. It is recorded, but I forgot what the code does.

Second idea: I was exploring Wolfram's Elementary Automata I saw a familiar pattern.
I observed that Elementary Automata are very similar to 3-input Logic Gates.
Logic gates ordered sequentially on a tape where their first and last inputs overlap.

I wondered - how could these be called elementary automata?
Obviously they can be reduced further down to logic gates.
Furthermore they if they are the same logic gate copied over sequentially ->
wouldn't it be cool to have different logic gates for each set of 3 inputs?

I went down the first rabit hole and I successfuly reduced the elementary automata to logic gates.
One of the key problems was symmetery.
Should a 2-input automata Have it's first input on the left or on the right?
While that's a frustrating issue to solve, I found it to be the lesser problem.
The significantly more perplexing problem to me was the following:
How do I produce Elementary Automata from logic gate based automata?
Furthermore I observed that Elementary Automata can be reduced even further to:
1 Input -> 1 output automata with 4 rules:
Rule 00: 10 -> 00, Rule 01:  10 -> 01, Rule 10: 10 -> 10, Rule 11: 10 -> 11
Compared to the 16 rules of 2 in automata or 256 of Elementary Automata.
For 2-input it begins like so:
Rule 0000:
11 10 01 00
 0  0  0  0

Rule 0001:
11 10 01 00
 0  0  0  1

 And so on.

But how do I reverse the process?

Funnily enough in order to produce a logic gate from a 1 in 1 out automata,
it would appear I would need a logic gate, which is 2 in 1 out.
I could not find a convenient, straightforward method to use the 4 Rules in and of themselves
to produce the 16 rules or subsequently to use 16 rules to produce 256.
While one of the 16 rules of 2 input automata is the NAND gate,
which is deemed capable of universal computation.
It still requires a large number of steps.

I was stuck on this on a longer time that I wish to admit.
And then it hit me. How could I have been so silly?
The operation that can be used to reverse the process is cartesian product.
If I get the product of '00', '01', '10', '11'
I end up with '0000', '0001' etc
Which is convenient, because instead of expressing a huge rule for larger input-size automata.
I can express them as a combination of elementary automata.
For example concatenating 2-input rule 1(01) + rule 2(10) = Elementary Rule 110

I could potentially go even further than that and express the method of combination.
Rather than concatenating I could do another product
In the sense of
prod(01 10) -> 0011, 0101, 0110, 1010, 1100
And select the product I wish to use for the elevation to higher input automata.

Which could be convenient if for example I only wished to explore higher input automata.
That are products of Elementary Rule 110 with itself?

Furthermore arguably binary automata can be reduced even further to 0 input, 1 output with 2 rules.
Rule 0: N/A -> 0, Rule 1 N/A -> 1

--Insert more here, reiterate and synthesize above, add visual aid and markup--

Going down this train of thought, it would appear to me that elementary automata can be reduced to:
A universal automata:
f(x) -> x

Basicaly a function that given a parameter x, then produces to call the parameter.
E.g. 

x = return 0
f(return 0):
    return 0

x = return 1
f(return 1):
    return 1

x = return 2
f(return 2):
    return 2

x = do something()
f(do something()):
    do something()


The structures that decide what happens in this mindset are:
    #1 The Rule itself
    #2 The Input data

What I observed next is the following:
Since the rule is a product in (reverse) order
Then it is an n-tree
A binary rule is a binary tree
First bit denotes the n halves of the rule space
Second bit denotes the n halves of the half it's in, and so on.

Therefore the input is the naviator that says which branches to take.

Why is this useful however?
Modern computers are more than capable of storing Elementary rules in memory.
And directly storing them in memory is much faster.

While that's definitely true.
What if I wanted to run multiple rules at once?
Mutate the rules while running.
Run very large rules for many inputs?
Or some other crazy shinaningans?

Ideas upon ideas upon ideas.
Optimize, expand, squash my previous naivities, find practical uses.
All while wanting to come up with an abstract model.
All this was driving me nuts, I almost gave up.

And this is how I stopped at chicken automata.
To be honest, it might also have to do with delving into cloud platforms.
And watching some birds at the nearby park.
Or trying to learn some basic BF.

But what is a chicken automata to begin with one might ask?
The answer is that it's an automata that started as an egg.

Jokes aside I seem to have come to a conclusion.
That computation is a bit like having a chicken coop.
Perhaps everything is a bit like chicken. Ornitomorphication.