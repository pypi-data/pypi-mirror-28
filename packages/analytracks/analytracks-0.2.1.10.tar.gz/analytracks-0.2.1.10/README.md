analytracks
===========
Workout tracks analytics


Installation 
------------
pip install -e .

Parsing
-------
```python
run1 = atrk.tracks.Track('LLN_10miles.tcx') # should also work with gpx
run1.points # track points
run1.data # track data
run1.rideRun # should be either 'ride' or 'run'
```

Pre-processing
--------------
```python
run1.add_google_elevation() # assuming you have an api key provided
                           # googleElevationApi.key
                           # otherwise use ele_name='ele' 
                           # it will use elevations from the track file
run1.add_slope(sf=0.05,ele_name='googleElevation',plot=True) # or ele_name='ele'
run1.add_speed(sf=0.05,plot=True)
```


