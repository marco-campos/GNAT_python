# GNAT_python
## An implementation of GNATFinder in python
## Original Sources:
- Source Code: [https://github.com/sandialabs/GNATFinder]( Sandia Github's GNATFinder)
- Arxiv Pub: [https://arxiv.org/abs/2306.16684]( Decomposing spiking neural networks with Graphical Neural Activity Threads)

## Python Implementation Progress:
- network
  - [x] Code
  - [x] Test
- quadtree
  - [x] Code
  - [ ] Test
- gnats
  - [x] Code
  - [ ] Test
- raster
  - [x] Code
  - [ ] Test
- gnatfinder
  - [x] Code
    - Note: There are several things I need to debug here, from the top down.
  - [ ] Test
- compute_activity_threads
  - [x] Code
  - [ ] Test
    - *** Look at the change ms to ticks thing ***
    - [x] SpikeRaster
    - [x] Network
    - [ ] compute_activity_threads
        - It appears like this is working but I think I need to test this with larger network data to truly verifying everything is working properly. It seems to be good though!
