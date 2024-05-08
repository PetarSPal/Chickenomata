# Chickenomata

Cellular automata playground written in Python

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lvOOSHP0FyM
" target="_blank"><img src="http://img.youtube.com/vi/lvOOSHP0FyM/0.jpg" 
alt="Chickenomata" width="240" height="180" border="10" /></a>


### Usage:
```bash
git clone
```
```bash
python main.py 
```
or
```bash
python test.py
```

Chickenomata is a project I've been working on for learning purposes.
Uploading in case someone finds my experience useful.
AS IS use at your own risk

Current iteration relies upon numpy ndarrays for underlying computation.
Performance is therefore far from optimal, due to blocking single-thread.
Multiple rendering options -> console, pygame raster or pygame + moderngl

###  Features I'd like to work on:
 - Move computation to GPU
 - Add colors for nonbinary automata to moderngl rendering
 - Add an interface -Further rendering and computation optimizations
 - Refactor
 - Tests
 - Additional automata types
