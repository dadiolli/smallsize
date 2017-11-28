# smallsize
Resizes or standardizes all images in a folder and its subfolders to a fixed long-edge using PIL. Optionally also enlarges images that have smaller than the desired long-edge side.
---
## Example
A folder contains images of sizes 3000x2000, 3000x1000 and 1200x3000px. With setting `longsidemax = 1000`, the images will be resized to 1000x667, 1000x333 and 400x1000px respectively.
---
## settings
Standard is set as follows:
```python
longsidemax = 720
enlarge = False
fullsizepath = 'full_size'
smallsizepath = 'small'
mode = "log" # use print to see output on console as well.
```
* `longsidemax` gives the __minimum__ and __maximum__ size of the longest side of the image.
* `enlarge` if set to `True`, size of images smaller than `longsidemax` will be increased.
* `fullsizepath` gives the source folder name. This can be absolute or direct relative path.
* `smallsizepath` gives the target folder name. This can be absolute or direct relative path.
* `mode` if `print` mode is used, log output is written to console as well.
---

## requirements
* __PIL__ has to be installed
```
pip install PIL
```
* using __progress__ bars and spinner
``` 
pip install progress
```
* using __checksumdir__ package for calculating directory checksum, to improve performance by skipping unchanged directory
``` 
pip install checksumdir
```

