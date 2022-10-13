#Import commands
import itasca as it
from itasca import ballarray as ba
import os, stat, csv, math
import shutil as sh
from shutil import copytree, ignore_patterns
import sys
import datetime
from datetime import datetime

#Python state is not cleared by the model new or model restore commands:
it.command("python-reset-state false")
#Define source code folder as src
src = "h:/dem/biaxial_stress/Dense_10m/"
#Destination folders of files are defined in each of the for-loops as dst

# Homogeneous Sediment Trials
coh_ten_matrix = [[1e5,1e5],[5e5,5e5],[10e5,10e5],[15e5,15e5],[20e5,20e5]]# [[10e5,1e5],[10e5,5e5],[10e5,15e5],[10e5,20e5],[1e5,1e5],[5e5,5e5],[10e5,10e5],[15e5,15e5],[20e5,20e5],[1e5,10e5],[5e5,10e5],[15e5,10e5],[20e5,10e5]]#[[10e6,10e6],[20e6,20e6],[30e6,30e6],[40e6,40e6],[50e6,50e6]]#
pb_fric = [0.3]
pb_rmul = [0.1]
dp_nratio = [0.7]
print('define parameters')

for ct in coh_ten_matrix:
    g_pre_growth_pb_coh = ct[0]
    g_pre_growth_pb_ten = ct[1]
    for g_fric in pb_fric:
        for g_rmul in pb_rmul: 
            for g_dp in dp_nratio: 
                it.command("""
                model new
                plot 'Test' movie index 1 interval 100 
                ;model restore 'unbonded' 
                model restore 'parallel_bonded_50xsand_20m'
                contact model linearpbond range contact type 'ball-ball'
                contact method bond gap 0.0125
                contact method deform emod 1e9 kratio 1.0
                contact method pb_deform emod 1e9 kratio 1.0
                contact property pb_ten {ten} pb_coh {coh} pb_rmul {rmul} pb_fa 32.6 dp_nratio {dp}
                contact property fric {fric} range contact type 'ball-ball' 
                ball attribute displacement multiply 0.0
                contact property lin_force 0.0 0.0 lin_mode 1
                ball attribute force-contact multiply 0.0 moment-contact multiply 0.0 
                model cycle 1
                model solve ratio-average 1e-4
                ball delete range position-y @target_topo @max_domain
                model save 'parallel_bonded_50xsand_20m' 
                program call 'biaxial_test'
                history export 1 vs 2 file 'D10_coh{coh:.1e}_ten{ten:.1e}.his' truncate
                history export 1 vs 2 file 'D10_coh{coh:.1e}_ten{ten:.1e}.txt' truncate
                model save 'end_pb_biaxial_test'
                project save
                program return
                """.format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, fric = g_fric, rmul = g_rmul, dp = g_dp))
                #Copy all files to new directory except guidebug.txt (error)
                dst = "h:/dem/biaxial_stress/Results/Lade_50xsand_size20m_coh{coh:.1e}_ten{ten:.1e}".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten)
                sh.copytree(src,dst, ignore=ignore_patterns('guidebug*'))
                #Delete everything that ends in .png or .csv
                png_files = os.listdir(src)
                png_filtered_files = [file for file in png_files if file.endswith(".png")]
                for file in png_filtered_files: 
                    path_to_file1 = os.path.join(src, file)
                    os.remove(path_to_file1)
                his_files = os.listdir(src)
                his_filtered_files = [file for file in his_files if file.endswith(".his")]
                for file in his_filtered_files: 
                    path_to_file2 = os.path.join(src, file)
                    os.remove(path_to_file2)
                txt_files = os.listdir(src)
                txt_filtered_files = [file for file in txt_files if file.endswith(".txt")]
                for file in txt_filtered_files: 
                    path_to_file2 = os.path.join(src, file)
                    os.remove(path_to_file2)