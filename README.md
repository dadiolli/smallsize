# smallsize
Resizes all images in a folder and its subfolders to a fixed long side using PIL.
---
## settings
Standard is set as follows:
```python
longsidemax = 720
fullsizepath = 'full_size'
smallsizepath = 'small'
mode = "log" # use print to see output on console as well.
```
* `longsidemax` gives the __minimum__ and __maximum__ size of the longest side of the image.
* `fullsizepath` gives the source folder name
* `smallsizepath` gives the target folder name
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
