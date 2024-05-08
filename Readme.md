# Chickenomata

Cellular automata playground written in Python

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lvOOSHP0FyM
" target="_blank"><img src="http://img.youtube.com/vi/lvOOSHP0FyM/0.jpg" 
alt="Chickenomata" width="240" height="180" border="10" /></a>

Usage:
git clone
python main.py
or
python test.py

It's a project I've been working on for learning purpouses
Sharing in case someone finds my experience useful
AS IS use at your own risk

Current iteration is using numpy ndarrays for underlying computation
Implementation is far from performant, due to blocking single-thread
Rendering uses Pygame + Moderngl

Current features I'd like to work on:
-Move computation to GPU
-Add colors for nonbinary automata to moderngl rendering
-Add an interface
-Further rendering and computation optimizations
-Refactor
-Tests
-Additional automata types
