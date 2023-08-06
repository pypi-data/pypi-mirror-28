# TiMemory
C++ and Python Timing + Memory Utilities including auto-timers and temporary memory calculation

[Source code documentation for TiMemory](https://jrmadsen.github.io/TiMemory)

Dependancies
------------

- Operating systems

  - Linux (tested on Ubuntu 14.04)
  - macOS (tested on 10.13 - High Sierra)
  - Windows support is generally untested

    - memory measurements may not have correct units if compiles

- C++

  - C++11 compiler

    - Known support for:

      - GCC (Linux + macOS, 4.9 - 7.2)
      - Clang (Linux + macOS, 4.0, 5.0)
      - Intel (Linux, 18.0.1)

  - MPI (optional)
  - cereal (git submodule)
  - pybind11 (git submodule)

- Python

  - version >= 2.6
  - packages

    - argparse
    - numpy
    - matplotlib
    - unittest

Python setup.py installation
----------------------------

```
# with MPI
python setup.py build install
# without MPI
python setup.py config --disable-mpi build install
```

Overview
--------

There are essentially two components of the output:

- a text file (e.g. `timing_report_XXX.out` file)

  - general ASCII report

- a JSON file with more detailed data

  - used for plotting purposes
  - can be directly called by module: `timemory.util.plot(["output.json"], display=False)`
  - `python/plot.py` in the source tree can be directly used

- Implementation uses “auto-timers”. Essentially, at the beginning of a function, you create a timer. 
- The timer starts automatically and when the timer is “destroyed”, i.e. goes out of scope at the end of the function, it stops the timer and records the time difference and also some memory measurements. 
- The way the auto-timers are setup is that they will automatically record the name of the function they were created in.
- Additional info is sometimes added when you have similar function names, for example, a python `__init__` function will want to create an auto-timer that provides the class the function is being called from, e.g. `autotimer = timemory.auto_timer(type(self).__name__)` 
- All this info will show up with an ensuing “@‘ tag on the end of the function name. Other options are the name of the file, etc.

  - `timemory.FILE(nback=2)`
  - `'{}'.format(timemory.LINE(nback=1))`
  - `timemory.FUNC(nback=1)`
  - `t = timemory.timer('{}@{}:{}'.format(timemory.FUNC(), timemory.FILE(), timemory.LINE()))`
  - where "nback" is a parameter specifying how far back in the call tree
  

Example
-------

For the interpretation of text output, here is an example and the explanation of it’s structure

```
> rank 0
|0> [pyc] main@'toast_ground_sim_simple.py'            : 41.104 wall, 69.150 user +  4.690 system = 73.840 CPU [sec] (179.6%) : RSS {tot,self}_{curr,peak} : (1146.5|2232.7) | (1072.4|2158.6) [MB]
|0> [pyc] |_create_observations                        :  5.047 wall,  5.060 user +  0.060 system =  5.120 CPU [sec] (101.4%) : RSS {tot,self}_{curr,peak} : ( 110.3| 122.3) | (  35.8|  47.8) [MB]
|0> [pyc]   |___init__@TODGround                       :  5.041 wall,  5.040 user +  0.060 system =  5.100 CPU [sec] (101.2%) : RSS {tot,self}_{curr,peak} : ( 122.2| 122.3) | (   9.3|   9.4) [MB] (total # of laps: 24)
|0> [pyc]     |_simulate_scan@TODGround                :  0.071 wall,  0.020 user +  0.000 system =  0.020 CPU [sec] ( 28.2%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.1|   0.1) [MB] (total # of laps: 24)
|0> [pyc]     |_translate_pointing@TODGround           :  4.950 wall,  5.010 user +  0.060 system =  5.070 CPU [sec] (102.4%) : RSS {tot,self}_{curr,peak} : ( 122.3| 122.3) | (   9.3|   9.3) [MB] (total # of laps: 24)
|0> [pyc]       |_from_angles                          :  0.014 wall,  0.050 user +  0.010 system =  0.060 CPU [sec] (431.8%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.4|   0.4) [MB] (total # of laps: 24)
|0> [cxx]         |_ctoast_qarray_from_angles          :  0.011 wall,  0.050 user +  0.010 system =  0.060 CPU [sec] (547.2%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.4|   0.4) [MB] (total # of laps: 24)
|0> [pyc]       |_rotate                               :  0.012 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] ( 85.0%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.8|   0.8) [MB] (total # of laps: 24)
|0> [cxx]         |_ctoast_qarray_rotate               :  0.008 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] (123.1%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.4|   0.4) [MB] (total # of laps: 24)
|0> [cxx]       |_ctoast_healpix_vec2ang               :  0.006 wall,  0.020 user +  0.000 system =  0.020 CPU [sec] (342.7%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.0|   0.0) [MB] (total # of laps: 24)
|0> [pyc]       |_read_times@TODGround                 :  0.003 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] (349.9%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.3|   0.3) [MB] (total # of laps: 24)
|0> [pyc]         |__get_times@TODGround               :  0.002 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] (639.0%) : RSS {tot,self}_{curr,peak} : ( 120.5| 120.9) | (   0.3|   0.3) [MB] (total # of laps: 24)
|0> [cxx]       |_ctoast_healpix_ang2vec               :  0.011 wall,  0.030 user +  0.000 system =  0.030 CPU [sec] (272.9%) : RSS {tot,self}_{curr,peak} : ( 120.5| 121.8) | (   0.0|   0.0) [MB] (total # of laps: 48)
|0> [pyc]       |_radec2quat@TODGround                 :  0.045 wall,  0.070 user +  0.010 system =  0.080 CPU [sec] (179.0%) : RSS {tot,self}_{curr,peak} : ( 120.7| 121.8) | (   2.5|   1.3) [MB] (total # of laps: 24)
|0> [pyc]         |_rotation                           :  0.025 wall,  0.020 user +  0.000 system =  0.020 CPU [sec] ( 79.1%) : RSS {tot,self}_{curr,peak} : ( 120.7| 121.8) | (   1.0|   0.2) [MB] (total # of laps: 72)
|0> [cxx]           |_ctoast_qarray_from_axisangle     :  0.012 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] ( 82.2%) : RSS {tot,self}_{curr,peak} : ( 120.7| 121.8) | (   0.6|   0.2) [MB] (total # of laps: 72)
|0> [pyc]         |_mult                               :  0.012 wall,  0.040 user +  0.010 system =  0.050 CPU [sec] (432.9%) : RSS {tot,self}_{curr,peak} : ( 120.7| 121.8) | (   0.7|   0.7) [MB] (total # of laps: 48)
|0> [cxx]           |_ctoast_qarray_mult               :  0.005 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] (194.7%) : RSS {tot,self}_{curr,peak} : ( 120.7| 121.8) | (   0.4|   0.4) [MB] (total # of laps: 48)
|0> [pyc] |_expand_pointing                            :  3.874 wall,  5.040 user +  1.280 system =  6.320 CPU [sec] (163.1%) : RSS {tot,self}_{curr,peak} : (1279.7|1290.1) | (1169.5|1167.9) [MB]
|0> [pyc]   |_exec@OpPointingHpix                      :  3.869 wall,  5.040 user +  1.280 system =  6.320 CPU [sec] (163.3%) : RSS {tot,self}_{curr,peak} : (1290.1|1290.1) | (1179.9|1167.9) [MB]
|0> [pyc]     |_read_pntg@TODGround                    :  0.623 wall,  0.800 user +  0.170 system =  0.970 CPU [sec] (155.7%) : RSS {tot,self}_{curr,peak} : (1289.2|1289.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|0> [pyc]       |__get_pntg@TODGround                  :  0.542 wall,  0.750 user +  0.120 system =  0.870 CPU [sec] (160.4%) : RSS {tot,self}_{curr,peak} : (1289.2|1289.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|0> [pyc]         |_mult                               :  0.469 wall,  0.690 user +  0.100 system =  0.790 CPU [sec] (168.3%) : RSS {tot,self}_{curr,peak} : (1289.2|1289.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|0> [cxx]           |_ctoast_qarray_mult               :  0.164 wall,  0.450 user +  0.090 system =  0.540 CPU [sec] (329.8%) : RSS {tot,self}_{curr,peak} : (1289.2|1289.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|0> [cxx]     |_ctoast_pointing_healpix_matrix         :  2.744 wall,  3.850 user +  1.100 system =  4.950 CPU [sec] (180.4%) : RSS {tot,self}_{curr,peak} : (1290.1|1290.1) | (   1.8|   1.8) [MB] (total # of laps: 1464)
|0> [pyc] |_get_submaps                                :  0.250 wall,  0.250 user +  0.000 system =  0.250 CPU [sec] ( 99.8%) : RSS {tot,self}_{curr,peak} : (1280.9|1290.1) | (   1.1|   0.0) [MB]
|0> [pyc]   |_exec@OpLocalPixels                       :  0.250 wall,  0.250 user +  0.000 system =  0.250 CPU [sec] (100.0%) : RSS {tot,self}_{curr,peak} : (1281.6|1290.1) | (   1.8|   0.0) [MB]
|0> [pyc] |_scan_signal                                :  1.480 wall,  1.250 user +  0.170 system =  1.420 CPU [sec] ( 96.0%) : RSS {tot,self}_{curr,peak} : (1597.6|1612.9) | ( 316.7| 322.8) [MB]
|0> [pyc]   |_read_healpix_fits@DistPixels             :  0.395 wall,  0.260 user +  0.080 system =  0.340 CPU [sec] ( 86.0%) : RSS {tot,self}_{curr,peak} : (1392.1|1425.8) | ( 111.3| 135.7) [MB]
|0> [pyc]   |_exec@OpSimScan                           :  1.080 wall,  0.990 user +  0.090 system =  1.080 CPU [sec] (100.0%) : RSS {tot,self}_{curr,peak} : (1612.9|1612.9) | ( 222.1| 187.1) [MB]
|0> [cxx]     |_ctoast_sim_map_scan_map32              :  0.149 wall,  0.180 user +  0.000 system =  0.180 CPU [sec] (120.8%) : RSS {tot,self}_{curr,peak} : (1612.9|1612.9) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|0> [pyc] |_build_npp                                  :  4.935 wall,  6.430 user +  0.410 system =  6.840 CPU [sec] (138.6%) : RSS {tot,self}_{curr,peak} : (1881.3|2044.1) | ( 296.0| 431.2) [MB]
|0> [pyc]   |_exec@OpAccumDiag                         :  1.927 wall,  3.700 user +  0.130 system =  3.830 CPU [sec] (198.7%) : RSS {tot,self}_{curr,peak} : (1556.9|1612.9) | (   0.0|   0.0) [MB]
|0> [pyc]     |_read_flags@TODGround                   :  0.035 wall,  0.030 user +  0.020 system =  0.050 CPU [sec] (144.6%) : RSS {tot,self}_{curr,peak} : (1588.1|1612.9) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|0> [cxx]     |_ctoast_cov_accumulate_diagonal_invnpp  :  0.801 wall,  2.600 user +  0.040 system =  2.640 CPU [sec] (329.6%) : RSS {tot,self}_{curr,peak} : (1588.9|1612.9) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|0> [pyc]   |_write_healpix_fits@DistPixels            :  2.855 wall,  2.590 user +  0.250 system =  2.840 CPU [sec] ( 99.5%) : RSS {tot,self}_{curr,peak} : (1896.5|2044.1) | ( 221.2| 368.0) [MB] (total # of laps: 3)
|0> [pyc]   |_covariance_invert@'map/noise.py'         :  0.012 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (328.8%) : RSS {tot,self}_{curr,peak} : (1881.2|2044.1) | (   0.0|   0.0) [MB]
|0> [cxx]     |_ctoast_cov_eigendecompose_diagonal     :  0.012 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (331.6%) : RSS {tot,self}_{curr,peak} : (1881.2|2044.1) | (   0.0|   0.0) [MB]
|0> [pyc] |_exec@OpCacheCopy                           :  0.306 wall,  0.140 user +  0.080 system =  0.220 CPU [sec] ( 71.9%) : RSS {tot,self}_{curr,peak} : (2118.4|2118.4) | ( 239.5|  74.3) [MB]
|0> [pyc] |_bin_maps                                   :  4.520 wall,  6.850 user +  0.350 system =  7.200 CPU [sec] (159.3%) : RSS {tot,self}_{curr,peak} : (2055.7|2119.0) | (   0.0|   0.6) [MB] (total # of laps: 2)
|0> [pyc]   |_exec@OpAccumDiag                         :  3.123 wall,  5.610 user +  0.200 system =  5.810 CPU [sec] (186.1%) : RSS {tot,self}_{curr,peak} : (1973.5|2119.0) | (   0.0|   0.6) [MB] (total # of laps: 2)
|0> [cxx]     |_ctoast_cov_accumulate_zmap             :  1.205 wall,  3.780 user +  0.120 system =  3.900 CPU [sec] (323.6%) : RSS {tot,self}_{curr,peak} : (2051.4|2119.0) | (   0.0|   0.0) [MB] (total # of laps: 2928)
|0> [pyc]   |_write_healpix_fits@DistPixels            :  1.320 wall,  1.180 user +  0.130 system =  1.310 CPU [sec] ( 99.2%) : RSS {tot,self}_{curr,peak} : (2056.6|2119.0) | ( 193.9|   0.0) [MB] (total # of laps: 2)
|0> [pyc] |_apply_polyfilter                           :  1.289 wall,  2.550 user +  0.680 system =  3.230 CPU [sec] (250.5%) : RSS {tot,self}_{curr,peak} : (2051.0|2119.0) | (   0.0|   0.0) [MB]
|0> [pyc]   |_exec@OpPolyFilter                        :  1.288 wall,  2.550 user +  0.680 system =  3.230 CPU [sec] (250.8%) : RSS {tot,self}_{curr,peak} : (2051.0|2119.0) | (   0.0|   0.0) [MB]
|0> [cxx]     |_ctoast_filter_polyfilter               :  0.935 wall,  2.200 user +  0.670 system =  2.870 CPU [sec] (307.1%) : RSS {tot,self}_{curr,peak} : (2051.0|2119.0) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|0> [pyc] |_exec@OpCacheClear                          :  0.038 wall,  0.000 user +  0.030 system =  0.030 CPU [sec] ( 79.2%) : RSS {tot,self}_{curr,peak} : (1554.0|2119.0) | (   0.0|   0.0) [MB]
|0> [pyc] |_apply_madam                                : 19.336 wall, 41.570 user +  1.630 system = 43.200 CPU [sec] (223.4%) : RSS {tot,self}_{curr,peak} : (1146.5|2232.7) | (   0.0| 113.7) [MB]
|0> [pyc]   |_exec@OpMadam                             : 19.327 wall, 41.560 user +  1.630 system = 43.190 CPU [sec] (223.5%) : RSS {tot,self}_{curr,peak} : (1146.5|2232.7) | (   0.0| 113.7) [MB]
|0> [pyc] |___del__@TODGround                          : 19.799 wall, 19.590 user +  0.160 system = 19.750 CPU [sec] ( 99.8%) : RSS {tot,self}_{curr,peak} : (1048.8|2232.7) | (   0.0|   0.0) [MB] (total # of laps: 24)
> rank 1
|1> [pyc] main@'toast_ground_sim_simple.py'            : 41.104 wall, 68.760 user +  5.120 system = 73.880 CPU [sec] (179.7%) : RSS {tot,self}_{curr,peak} : (1138.0|2223.7) | (1064.0|2149.8) [MB]
|1> [pyc] |_create_observations                        :  5.046 wall,  5.050 user +  0.060 system =  5.110 CPU [sec] (101.3%) : RSS {tot,self}_{curr,peak} : ( 111.1| 123.1) | (  36.8|  48.8) [MB]
|1> [pyc]   |___init__@TODGround                       :  5.039 wall,  5.040 user +  0.060 system =  5.100 CPU [sec] (101.2%) : RSS {tot,self}_{curr,peak} : ( 123.1| 123.1) | (   9.5|   9.6) [MB] (total # of laps: 24)
|1> [pyc]     |_simulate_scan@TODGround                :  0.075 wall,  0.050 user +  0.000 system =  0.050 CPU [sec] ( 66.8%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.0|   0.0) [MB] (total # of laps: 24)
|1> [pyc]     |_translate_pointing@TODGround           :  4.950 wall,  4.970 user +  0.040 system =  5.010 CPU [sec] (101.2%) : RSS {tot,self}_{curr,peak} : ( 123.1| 123.1) | (   9.4|   9.4) [MB] (total # of laps: 24)
|1> [pyc]       |_from_angles                          :  0.014 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (284.2%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.4|   0.4) [MB] (total # of laps: 24)
|1> [cxx]         |_ctoast_qarray_from_angles          :  0.011 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (357.1%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.4|   0.4) [MB] (total # of laps: 24)
|1> [pyc]       |_rotate                               :  0.012 wall,  0.010 user +  0.010 system =  0.020 CPU [sec] (171.4%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.9|   0.9) [MB] (total # of laps: 24)
|1> [cxx]         |_ctoast_qarray_rotate               :  0.008 wall,  0.010 user +  0.010 system =  0.020 CPU [sec] (239.5%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.5|   0.5) [MB] (total # of laps: 24)
|1> [cxx]       |_ctoast_healpix_vec2ang               :  0.006 wall,  0.010 user +  0.010 system =  0.020 CPU [sec] (339.2%) : RSS {tot,self}_{curr,peak} : ( 121.3| 121.8) | (   0.0|   0.0) [MB] (total # of laps: 24)
|1> [cxx]       |_ctoast_healpix_ang2vec               :  0.011 wall,  0.040 user +  0.010 system =  0.050 CPU [sec] (457.1%) : RSS {tot,self}_{curr,peak} : ( 121.3| 122.6) | (   0.0|   0.0) [MB] (total # of laps: 48)
|1> [pyc]       |_radec2quat@TODGround                 :  0.045 wall,  0.060 user +  0.000 system =  0.060 CPU [sec] (132.3%) : RSS {tot,self}_{curr,peak} : ( 121.5| 122.6) | (   2.9|   1.6) [MB] (total # of laps: 24)
|1> [pyc]         |_rotation                           :  0.025 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (158.5%) : RSS {tot,self}_{curr,peak} : ( 121.5| 122.6) | (   0.9|   0.5) [MB] (total # of laps: 72)
|1> [cxx]           |_ctoast_qarray_from_axisangle     :  0.012 wall,  0.010 user +  0.000 system =  0.010 CPU [sec] ( 84.7%) : RSS {tot,self}_{curr,peak} : ( 121.5| 122.6) | (   0.6|   0.5) [MB] (total # of laps: 72)
|1> [pyc] |_expand_pointing                            :  3.874 wall,  5.040 user +  1.280 system =  6.320 CPU [sec] (163.2%) : RSS {tot,self}_{curr,peak} : (1280.7|1291.1) | (1169.6|1168.0) [MB]
|1> [pyc]   |_exec@OpPointingHpix                      :  3.872 wall,  5.040 user +  1.280 system =  6.320 CPU [sec] (163.2%) : RSS {tot,self}_{curr,peak} : (1291.1|1291.1) | (1180.0|1168.0) [MB]
|1> [pyc]     |_read_pntg@TODGround                    :  0.624 wall,  0.780 user +  0.120 system =  0.900 CPU [sec] (144.3%) : RSS {tot,self}_{curr,peak} : (1290.2|1290.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|1> [pyc]       |__get_pntg@TODGround                  :  0.542 wall,  0.740 user +  0.110 system =  0.850 CPU [sec] (156.8%) : RSS {tot,self}_{curr,peak} : (1290.2|1290.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|1> [pyc]         |_mult                               :  0.468 wall,  0.670 user +  0.110 system =  0.780 CPU [sec] (166.8%) : RSS {tot,self}_{curr,peak} : (1290.2|1290.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|1> [cxx]           |_ctoast_qarray_mult               :  0.163 wall,  0.350 user +  0.090 system =  0.440 CPU [sec] (270.0%) : RSS {tot,self}_{curr,peak} : (1290.2|1290.2) | (   0.7|   0.0) [MB] (total # of laps: 1464)
|1> [cxx]     |_ctoast_pointing_healpix_matrix         :  2.749 wall,  3.930 user +  1.160 system =  5.090 CPU [sec] (185.2%) : RSS {tot,self}_{curr,peak} : (1291.1|1291.1) | (   1.8|   1.8) [MB] (total # of laps: 1464)
|1> [pyc] |_get_submaps                                :  0.250 wall,  0.240 user +  0.010 system =  0.250 CPU [sec] ( 99.8%) : RSS {tot,self}_{curr,peak} : (1281.9|1291.1) | (   1.2|   0.0) [MB]
|1> [pyc]   |_exec@OpLocalPixels                       :  0.247 wall,  0.240 user +  0.010 system =  0.250 CPU [sec] (101.0%) : RSS {tot,self}_{curr,peak} : (1282.6|1291.1) | (   1.9|   0.0) [MB]
|1> [pyc] |_scan_signal                                :  1.476 wall,  1.300 user +  0.160 system =  1.460 CPU [sec] ( 98.9%) : RSS {tot,self}_{curr,peak} : (1521.3|1522.6) | ( 239.4| 231.5) [MB]
|1> [pyc]   |_read_healpix_fits@DistPixels             :  0.395 wall,  0.310 user +  0.070 system =  0.380 CPU [sec] ( 96.1%) : RSS {tot,self}_{curr,peak} : (1286.8|1291.1) | (   4.9|   0.0) [MB]
|1> [pyc]   |_exec@OpSimScan                           :  1.080 wall,  0.990 user +  0.090 system =  1.080 CPU [sec] (100.0%) : RSS {tot,self}_{curr,peak} : (1522.6|1522.6) | ( 235.8| 231.5) [MB]
|1> [cxx]     |_ctoast_sim_map_scan_map32              :  0.149 wall,  0.130 user +  0.000 system =  0.130 CPU [sec] ( 87.0%) : RSS {tot,self}_{curr,peak} : (1522.6|1522.6) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|1> [pyc] |_build_npp                                  :  4.939 wall,  6.070 user +  0.740 system =  6.810 CPU [sec] (137.9%) : RSS {tot,self}_{curr,peak} : (1580.8|1580.8) | (  60.1|  58.2) [MB]
|1> [pyc]   |_exec@OpAccumDiag                         :  1.941 wall,  3.710 user +  0.120 system =  3.830 CPU [sec] (197.3%) : RSS {tot,self}_{curr,peak} : (1548.5|1548.5) | (  26.9|  26.0) [MB]
|1> [pyc]     |_read_flags@TODGround                   :  0.035 wall,  0.040 user +  0.000 system =  0.040 CPU [sec] (113.2%) : RSS {tot,self}_{curr,peak} : (1548.5|1548.5) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|1> [cxx]     |_ctoast_cov_accumulate_diagonal_invnpp  :  0.809 wall,  2.530 user +  0.080 system =  2.610 CPU [sec] (322.7%) : RSS {tot,self}_{curr,peak} : (1548.5|1548.5) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|1> [pyc]   |_write_healpix_fits@DistPixels            :  0.146 wall,  0.090 user +  0.040 system =  0.130 CPU [sec] ( 88.8%) : RSS {tot,self}_{curr,peak} : (1580.8|1580.8) | (   2.5|   2.4) [MB] (total # of laps: 3)
|1> [pyc]   |_covariance_invert@'map/noise.py'         :  0.013 wall,  0.050 user +  0.000 system =  0.050 CPU [sec] (389.0%) : RSS {tot,self}_{curr,peak} : (1580.8|1580.8) | (   0.0|   0.0) [MB]
|1> [cxx]     |_ctoast_cov_eigendecompose_diagonal     :  0.013 wall,  0.050 user +  0.000 system =  0.050 CPU [sec] (392.1%) : RSS {tot,self}_{curr,peak} : (1580.8|1580.8) | (   0.0|   0.0) [MB]
|1> [pyc] |_exec@OpCacheCopy                           :  0.305 wall,  0.140 user +  0.070 system =  0.210 CPU [sec] ( 68.9%) : RSS {tot,self}_{curr,peak} : (1819.0|1819.0) | ( 238.3| 238.2) [MB]
|1> [pyc] |_bin_maps                                   :  4.523 wall,  6.690 user +  0.490 system =  7.180 CPU [sec] (158.8%) : RSS {tot,self}_{curr,peak} : (1817.1|1821.7) | (   0.0|   2.7) [MB] (total # of laps: 2)
|1> [pyc]   |_exec@OpAccumDiag                         :  3.100 wall,  5.580 user +  0.200 system =  5.780 CPU [sec] (186.5%) : RSS {tot,self}_{curr,peak} : (1821.7|1821.7) | (   2.7|   2.7) [MB] (total # of laps: 2)
|1> [cxx]     |_ctoast_cov_accumulate_zmap             :  1.201 wall,  3.780 user +  0.150 system =  3.930 CPU [sec] (327.3%) : RSS {tot,self}_{curr,peak} : (1821.7|1821.7) | (   0.0|   0.0) [MB] (total # of laps: 2928)
|1> [pyc]   |_write_healpix_fits@DistPixels            :  0.060 wall,  0.050 user +  0.020 system =  0.070 CPU [sec] (117.4%) : RSS {tot,self}_{curr,peak} : (1817.1|1821.7) | (   0.0|   0.0) [MB] (total # of laps: 2)
|1> [pyc] |_apply_polyfilter                           :  1.289 wall,  2.550 user +  0.710 system =  3.260 CPU [sec] (252.9%) : RSS {tot,self}_{curr,peak} : (1817.1|1821.7) | (   0.1|   0.0) [MB]
|1> [pyc]   |_exec@OpPolyFilter                        :  1.289 wall,  2.550 user +  0.710 system =  3.260 CPU [sec] (252.9%) : RSS {tot,self}_{curr,peak} : (1817.1|1821.7) | (   0.1|   0.0) [MB]
|1> [cxx]     |_ctoast_filter_polyfilter               :  0.943 wall,  2.170 user +  0.700 system =  2.870 CPU [sec] (304.3%) : RSS {tot,self}_{curr,peak} : (1817.1|1821.7) | (   0.0|   0.0) [MB] (total # of laps: 1464)
|1> [pyc] |_exec@OpCacheClear                          :  0.029 wall,  0.010 user +  0.020 system =  0.030 CPU [sec] (105.1%) : RSS {tot,self}_{curr,peak} : (1545.1|1821.7) | (   0.0|   0.0) [MB]
|1> [pyc] |_apply_madam                                : 19.346 wall, 41.650 user +  1.580 system = 43.230 CPU [sec] (223.5%) : RSS {tot,self}_{curr,peak} : (1138.0|2223.7) | (   0.0| 402.1) [MB]
|1> [pyc]   |_exec@OpMadam                             : 19.345 wall, 41.650 user +  1.580 system = 43.230 CPU [sec] (223.5%) : RSS {tot,self}_{curr,peak} : (1138.0|2223.7) | (   0.0| 402.1) [MB]
|1> [pyc] |___del__@TODGround                          : 18.149 wall, 17.950 user +  0.150 system = 18.100 CPU [sec] ( 99.7%) : RSS {tot,self}_{curr,peak} : (1040.3|2223.7) | (   0.0|   0.0) [MB] (total # of laps: 24)
```

GENERAL LAYOUT
--------------

- The "rank" line(s) give the MPI process/rank (and x=rank in `|x>`)
- The first (non ">") column tells whether the “auto-timer” originated from C++ (`[cxx]`) or Python (`[pyc]`) code
- The second column is the function name the auto-timer was created in

  - The indentation signifies the call tree along with `|_`

- The last column referring to “laps” is the number of times the function was invoked

  - If the number of laps are not noted, the total number of laps is implicitly one

TIMING FIELDS
-------------

- Then you have 5 time measurements

  (1) Wall clock time (e.g. how long it took according to a clock “on the wall”)
  
  (2) User time (the time spent executing the code)
  
  (3) System time (thread-specific CPU time, e.g. an idle thread waiting for synchronization, etc.)
  
  (4) CPU time (user + system time)
  
  (5) Percent CPU utilization (cpu / wall * 100)
  
- For perfect speedup on 4 threads, the CPU time would be 4x as long as the wall clock time and would have a % CPU utilization of 400%

  - This also includes vectorization. If each thread ran a calculation that calculated 4 values with a single CPU instruction (SIMD), we would have a speed up of 16x (4 threads x 4 values at one time == 16x) 

- Relative time (i.e. self-cost) for a function at a certain indent level (i.e. indented with `2\*level` spaces from [pyc]/[cxx]) can be calculated from the function(s) at `level+1` until you reach another function at the same level
- This is better understood by an example

  - function A is the main (it is “level 0”) and takes 35 seconds
  - function B is called from main (it is "level 1”)
  - function C is called from main (it is “level 1”)
  - function B does some calculations and calls function D (it is “level 2”) five times (e.g. a loop calling function D)
  - function B takes 20 seconds
  - function D, called from B, takes a total of 10 seconds (which is what is reported). The average time of function D is thus 2 seconds (10 sec / 5 laps)
  - function C does some calculations and also calls function D (again “level 2”) five times 
  - The call to function D from function C will be reported as separate from the calls to D from B thanks to a hashing technique we use to identify function calls originating from different call trees/sequences
  - function C takes 9 seconds 
  - function D, called from C, takes a total of 8 seconds (avg. of 1.6 seconds)
  - Thus we know that function B required 10 seconds of compute time by subtracting out the time spent in its calls to function D
  - We know that function C required 1 second of compute time by subtracting out the time spent in it’s calls to function D
  - We can subtract the time from function B and C to calculate the “self-cost” in function A (35 - 20 - 9 = 6 seconds)
  
    - When calculating the self-cost of A, one does not subtract the time spent in function D. These times are included in the timing of both B and C


MEMORY FIELDS
-------------

- The memory measurements are a bit confusing, admittedly. The two types "curr" ("current", which I will refer to as such from here on out) and "peak" have to do with different memory measurements

  - They are both "RSS" measurements, which stand for "resident set size". This is the amount of physical memory in RAM that is currently private to the process
  
    - It does not include the "swap" memory, which is when the OS puts memory not currently being used onto the hard drive
    - Typical Linux implementations will start using swap when ~60% of your RAM is full (you can override this easily in Linux by switching the “swapiness” to say, 90% for better performance since swap is slower than RAM)

- All memory measurements with “laps” > 0, are the max memory measurement of each "lap"

  - The “current” and “peak” max measurements are computed independently
  - E.g. the “current” max doesn’t directly correspond to the “peak” max — one “lap” may record the largest “current” RSS measurement but that does not (necessarily) mean that the same “lap” is responsible for the max “peak” RSS measurement
  - This is due to our belief that the max values are the ones of interest — the instances we must guard against to avoid running out of memory

- With respect to “total” vs. “self”, this is fairly straightforward

  - For the “total”, I simply take a measurement of the memory usage at the destruction of the timer
  - The “self” measurement is the difference in the memory measurements between the creation of the auto-timer and when it is destroyed
  - The "total" memory at the start of the timer can be determined from the memory measurement of the timer one level higher up the call tree or by `"total" - "self"`
  
    - This measurement shows is how much persistent memory was created in the function
    - It is valuable primarily as a metric to see how much memory is being created in the function and returned to the calling function
    - For example, if function X called function Y and function Y allocated 10 MB of memory and returned an object using this memory to function X, you would see function Y have a “self-cost” of 10 MB in memory

- The difference between “current” and “peak” is how the memory is measured

  - The “peak” value is what the OS reports as the max amount of memory being used is
  - I find this to be slightly more informative than “current” which is measurement of the “pages” allocated in memory
  - The reason "current" is included is because of the following:
  
    - Essentially, a “page” of memory can be thought of as street addresses separated into “blocks”, i.e. 1242 MLK Blvd. is in the 1200 block of MLK Blvd. 
    - A “page” is thus similar to a “block” — it is a starting memory address
    - The size of the pages is defined by the OS and just like the “swappiness”, it can be modified
    - For example, the default page size may be 1 KB and when a process has memory allocation need for 5.5 KB, the OS will provide 6 “pages” 
    
      - This is why one will see performance improvements when dealing with certain applications that application require large contiguous memory blocks, larger “pages” require fewer page requests and fewer reallocations to different pages when more memory is requested for an existing object with contiguous memory)
      
    - Within the page itself, the entire page might be used or it might not be fully used
    - When a page is not entirely used, you will get a “current” RSS usage greater than the “peak” memory usage — the memory is reserved for the process but is not actually used so it is thus not contained in the “peak” RSS usage number
    - However, when several pages is requested and allocated within a function but then released when returning to the calling function (i.e. temporary/transient page usage), you will have a “peak” RSS exceeding the “current” RSS memory usage since the “current” is measured after the pages are released back to the OS
    - Thus, with these two numbers, one can then deduce how much temporary/transient memory usage is being allocated in the function — if a function reports a self-cost of 243.2 MB of “current” RSS and a “peak” RSS of 403.9 MB, then you know that the “build_npp” function created 243.2 MB of persistent memory but creating the object requiring the persistent 243.2 MB required an additional 160.7 MB of temporary/transient memory (403.9 MB - 243.2 MB).


USING AUTO-TIMERS
-----------------

If you have new Python code you would like to use the auto-timers with, here is general guide:

- Import the timing module (obvious, I guess)
- Always add the auto-timer at the very beginning of the function. 

  - You can use an variable name you wish but make sure it is a named variable (e.g. `autotimer = timemory.auto_timer()`, not `timemory.auto_timer()`)
  - The auto-timer functionality requires the variable to exist for the scope of the function
  
- For free-standing function without any name conflicts, just add: `autotimer = timemory.auto_timer()`
- For functions within a class, add: `autotimer = timemory.auto_timer(type(self).__name__)`
- For the primary auto-timer, use: `autotimer = timemory.auto_timer(timemory.FILE())` — this will tag “main” with the python file name
- In some instances, you may want to include the directory of the filename, for this use: `autotimer = timemory.auto_timer(timemory.FILE(use_dirname = True))`
- Add `tman = timemory.timing_manager() ; tman.report()` at the end of your main file. 
  
  - It is generally recommended to do this in a different scope than the primary autotimer but not necessary. 
  - Some control options are available with: `tim.util.add_arguments_and_parse(parser)` in Python
  - In other words, put all your work in a “main()” function looking like this:
 
```python

import timemory

# optional (will catch SIGINT + other signals such as SIGABRT, SIGQUIT, SIGHUP, etc.)
timemory.enable_signal_detection()

# ...


#------------------------------------------------------------------------------#
def main(args):
    # this will be the top-level timer in timing + memory report because it is
    # the first added
    autotimer = timemory.auto_timer(timemory.FILE(), timemory.LINE())
    # ...


#------------------------------------------------------------------------------#
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size",
                        help="Size of array allocations",
                        default=array_size, type=int)
    # ...
    args = timemory.util.add_arguments_and_parse(parser)
    
    timemory.util.opts.set_report(timemory.util.opts.report_fname)
    timemory.util.opts.set_serial(timemory.util.opts.serial_fname)

    try:
        main(args)
        
        # get the handle for the timing manager
        timing_manager = timemory.timing_manager()
        # will output to stdout if "set_report" not called
        timing_manager.report()
        # serialization will be called in above if "set_serial" is called
        # but to serialize to file:
        timing_manager.serialize('output.json')
        # will create timing and memory plot with avg + err for files 
        # (even though output is identical in this example...)
        timemory.util.plot(files=[timemory.util.opts.serial_fname, "output.json"], display=False)
        
    except Exception as e:
        print (e.what())
        print ("Error! Unable to plot 'output.json'")

    print ('')
```
  
