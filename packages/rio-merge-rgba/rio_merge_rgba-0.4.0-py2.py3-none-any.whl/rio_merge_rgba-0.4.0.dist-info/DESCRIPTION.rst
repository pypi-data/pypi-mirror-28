
A `rio merge` alternative optimized for large RGBA scenetifs

`rio merge-rgba` is a CLI with nearly identical arguments to `rio merge`. They accomplish the same task, merging many rasters into one. The differences are in the implementation:

`rio merge-rgba`::

1. only accepts 4-band RGBA rasters
2. writes the destination data to disk rather than an in-memory array
3. reads/writes in windows corresponding to the destination block layout
4. once a window is filled with data values, the rest of the source files are skipped for that window

This is both faster and more memory efficient but limited to RGBA rasters.


