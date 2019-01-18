# RaspiReader
3D models and code for building your own fingerprint reader

# Affiliated Papers

If you use RaspiReader in your research, please cite the following papers

```
@article{engelsma2018raspireader,
  title={Raspireader: Open source fingerprint reader},
  author={Engelsma, Joshua James and Cao, Kai and Jain, Anil K},
  journal={IEEE transactions on pattern analysis and machine intelligence},
  year={2018},
  publisher={IEEE}
}
@article{engelsma2018fingerprint,
    title={Fingerprint Match in Box},
    author={Engelsma, Joshua J and Cao, Kai and Jain, Anil K},
    journal={arXiv preprint arXiv:1804.08659},
    year={2018}
}
```

# Major Dependencies
OpenCV
Numpy

# Acknowledgments

PyImageSearch 4 point transform - https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

# DIY Video Instructions

http://bit.do/RaspiReader

# Note(s)

1) The Raspberry Pi Cameras are fixed focal length cameras. However, in order to get high resolution fingerprint images, the focal length needs to be adjusted. There are many videos available on youtube describing how to break the glue seal on the Raspberry Pi camera and ajust the focal length. 

2) A printed checkerboard pattern placed on the prism of the assembled RaspiReader can be used as a tool to focus the lens. To get the FTIR camera to image a 2D printed checkerboard pattern, several drops of water can be placed on top of the prism (just be CAREFUL not to let water drip into the assembled RaspiReader) 

3) Currently RaspiReader does not work well with dry fingers (a shortcoming of any optical fingerprint scanner). Several options are available to help with this. (i) one can place a very thin silicone pad over the prism or (ii) the user can moisten their finger by rubbing their forehead with the finger to be imaged.

4) The 3D printer used by us to fabricate the case was the Stratasys Objet Connex350 using the material DM-8530-Gray60


