spacex flight data
==================


extract telemetry data from spacex webcasts


Dependencies:
* python3
* opencv 3+


Download a video of a spacex falcon9 launch from youtube. place it in a folder `data/F??/video`.

```python
import spacex_flight_data

spacex_flight_data.analyze_video('F??')
```

will extract the clock, velocity and altitude telemetry from the video and save it in `data/F??/flight_data`.

You will need to train the image recognition using e.g. `altitude_training_select.py` and `altitude_train.py` scripts. A sample model is included.

