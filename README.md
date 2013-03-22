doppler
=======

Filtering
---------

To check out the dart filtering:

 * import util
 * util.draw_all()

There's no piping yet and it's only running on test data but the filter seems to work.

Detection Flow
--------------

If you have already filtered data, you can pass it through the zero-detection, event alignment, and multilateration steps via:
`python util.py | python zero_detection.py | python alignment.py | python multilateration.py`

`python util.py` generates a sin wave.
