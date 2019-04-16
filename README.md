# Readme

To run execute:
```bash
python3 pathfinder.py treasure_maps.txt
```
**Note**: In _my_ Mac, Mojave 10.14.4, python command is 2.7 and does
not contain enums, I suppose all examples where with python 3.

Or using docker:
```bash
docker build -t treasure .
docker run treasure
```

## Task #4: Helpful Signposts

For every node we will have distance to the mountains.
In short:
- Node 0 -> distance to mountain 0, distance to mountain 1
- Node 1 -> distance to mountain 0, distance to mountain 1
- ...
- Node N-1 -> distance to mountain 0, distance to mountain 1

If the distance to mountain 0 or 1 is the shortest distance, then we can calculate the
distance in the following way:
- Total distance = _min_(<br/>
    distance from _start_ to mountain 0 + distance from mountain 0 to _treasure_, <br/> 
    distance from _start_ to mountain 1 + distance from mountain 1 to _treasure_)

If the distance from node _i_ to mountain 0 or mountain 1 is not the shortest, we still 
can calculate the shortest distance to the closest of mountain 0 or mountain 1. So we
can divide the graph into two sets, compute the shortest distance to both mountains
and calculate the distance in constant time with the formula above.
