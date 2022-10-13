# DEM_PFC2D_Biaxial_Stress_Test
General code for running a series of 2D biaxial stress tests in Particle Flow Code 2D (PFC2D) version 7.00. 

# README
The main project file (D10_biaxial_stress_test_project.prj) will open the necessary data and fish files with a plot of the model output. 
A sample of sediment will need to be generated using the make_sample.p2dat script and then bonded with user-defined properties using the parallel_bonded.p2dat script. 
Once this is complete and .sav files are generated for the sample, a series of biaxial stress tests examining the material micro-properties can be automated in for-loops using the homogeneous.py script. This script will also output a CSV file for the axial stress and strain of the trials which is then used to calculate the Young's Modulus and bulk propertiies of the material. A source (src) and destination (dst) folder will need to be defined to organize files when runniing numerous trials. 
