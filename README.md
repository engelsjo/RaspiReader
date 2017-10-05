# RaspiReader
3D models and code for building your own fingerprint reader

# Dependencies
OpenCV
Numpy

# Acknowledgments

PyImageSearch 4 point transform - https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

# DIY Video Instructions

bit.do/RaspiReader

# Note(s)

1) The Raspberry Pi Cameras are fixed focal length cameras. However, in order to get high resolution fingerprint images, the focal length needs to be adjusted. There are many videos available on youtube describing how to break the glue seal on the Raspberry Pi camera and ajust the focal length. 

2) A printed checkerboard pattern can be used as a tool to focus the lens. 

3) Currently RaspiReader does not work well with dry fingers (a shortcoming of any optical fingerprint scanner). Several options are available to help with this. (i) one can place a very thin silicone pad over the prism or (ii) the user can moisten their finger by rubbing their forehead with the finger to be imaged.


