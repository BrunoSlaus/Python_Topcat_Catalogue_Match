"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created on Fri May 12 16:03:09 2017

VERSION 2
The program does the matching with the zphot catalogue and exports the
matched files as .fits files.
            
Author: Bruno Slaus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from Topcat_Match import skymatch
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import math

############################################################################
#                    Sliding Parameters:                                   # 
############################################################################
Field_1_Name = 'xxl_gmrt.fits'
Field_2_Name = 'xxl_irac_mini.fits'

#Parameters of the match
match_limit_min=1
match_limit_max=10
match_limit_step=1

#Number of random fields generated
N_Random_Fields=2 

#Counterpart area params:
Ra_Min =31
Ra_Max =33
Dec_Min=-4
Dec_Max=-6

#Random field source number
N_random=157071

#N_random=6697788 
############################################################################



#First we create the random fields 
for i in np.arange(N_Random_Fields):
    random_field_norm = np.random.random((N_random, 2))
    RA_random = random_field_norm[0:,0]
    DEC_random = random_field_norm[0:,1]
    RA_random = (Ra_Max-Ra_Min)*RA_random + Ra_Min         
    DEC_random = (Dec_Max-Dec_Min)*DEC_random + Dec_Min         

    col1 = fits.Column(name='RA', format='D', array=RA_random)
    col2 = fits.Column(name='DEC', format='D', array=DEC_random)
    cols = fits.ColDefs([col1, col2])
    Fits_random = fits.BinTableHDU.from_columns(cols)
    Fits_random.writeto('log/Random_'+str(i)+'.fits', overwrite='True')


Match_Radius = np.arange(match_limit_min,match_limit_max,match_limit_step)


#We Match the RANDOM fields
Random_Match_Dict = {}
for i in np.arange(N_Random_Fields):
    array_temp_x_integrated = np.array([])
    array_temp_y_integrated = np.array([])
    array_temp_x_difference = np.array([])
    array_temp_y_difference = np.array([])    
    for r in Match_Radius:
        skymatch(
            'Input/' + Field_1_Name,
            ["RA", "DEC"],
            'log/Random_'+str(i)+'.fits',
            ["RA", "DEC"],
            r, 'log/Matched_Temp.fits')
        Data=fits.open('log/Matched_Temp.fits')[1].data
        Integrated_Count        = np.count_nonzero(Data["RA_1"])
        array_temp_x_integrated = np.append(array_temp_x_integrated, r)
        array_temp_y_integrated = np.append(array_temp_y_integrated, Integrated_Count)

        if r>match_limit_min:
            Difference_Counts = array_temp_y_integrated[-1]-array_temp_y_integrated[-2]
            array_temp_x_difference = np.append(array_temp_x_difference, r)
            array_temp_y_difference = np.append(array_temp_y_difference, Difference_Counts)
        else:
            Difference_Counts = array_temp_y_integrated[-1]
            array_temp_x_difference = np.append(array_temp_x_difference, r)
            array_temp_y_difference = np.append(array_temp_y_difference, Difference_Counts) 

    Integrated = np.column_stack([array_temp_x_integrated, array_temp_y_integrated])
    Difference = np.column_stack([array_temp_x_difference, array_temp_y_difference])
    Random_Match_Dict[str(i) + '_Integrated'] = Integrated
    Random_Match_Dict[str(i) + '_Difference'] = Difference
    


#We Match the REAL fields
array_temp_x_integrated = np.array([])
array_temp_y_integrated = np.array([])
array_temp_x_difference = np.array([])
array_temp_y_difference = np.array([])    
for r in Match_Radius:
    skymatch(
        'Input/xxl_gmrt.fits',
        ["RA", "DEC"],
        'Input/xxl_irac_mini.fits',
        ["RA", "DEC"],
        r, 'log/Matched_Temp.fits')
    Data=fits.open('log/Matched_Temp.fits')[1].data
    Integrated_Count        = np.count_nonzero(Data["RA_1"])
    array_temp_x_integrated = np.append(array_temp_x_integrated, r)
    array_temp_y_integrated = np.append(array_temp_y_integrated, Integrated_Count)

    if r>match_limit_min:
        Difference_Counts = array_temp_y_integrated[-1]-array_temp_y_integrated[-2]
        array_temp_x_difference = np.append(array_temp_x_difference, r)
        array_temp_y_difference = np.append(array_temp_y_difference, Difference_Counts)
    else:
        Difference_Counts = array_temp_y_integrated[-1]
        array_temp_x_difference = np.append(array_temp_x_difference, r)
        array_temp_y_difference = np.append(array_temp_y_difference, Difference_Counts)        

Real_Match_Integrated = np.column_stack([array_temp_x_integrated, array_temp_y_integrated])
Real_Match_Difference = np.column_stack([array_temp_x_difference, array_temp_y_difference])



#Calculating the mean random difference array
Random_Match_Difference_Sum_y = np.zeros(len(Random_Match_Dict['0_Difference'][:,0]))
for i in np.arange(N_Random_Fields):
    Random_Match_Difference_Sum_y = Random_Match_Difference_Sum_y + Random_Match_Dict[str(i) + '_Difference'][:,1]
Random_Match_Difference_Mean_x = Random_Match_Dict['0_Difference'][:,0]    #x-axis is the same for all
Random_Match_Difference_Mean_y = Random_Match_Difference_Sum_y / N_Random_Fields
Random_Match_Difference_Mean   = np.column_stack([Random_Match_Difference_Mean_x, Random_Match_Difference_Mean_y])



#Plotting the results
plt.figure(figsize=(4,5))
plt1 = plt.axes((0.2, 0.1, 0.7, 0.4), facecolor='w')
for i in np.arange(N_Random_Fields):
    plt1.plot(Random_Match_Dict[str(i) + '_Integrated'][:,0], Random_Match_Dict[str(i) + '_Integrated'][:,1])
plt1.plot(Real_Match_Integrated[:,0], Real_Match_Integrated[:,1])
plt.xlabel('Matching Radius')
plt.ylabel('N')

plt2 = plt.axes((0.2, 0.5, 0.7, 0.4), facecolor='w')
for i in np.arange(N_Random_Fields):
    plt2.plot(Random_Match_Dict[str(i) + '_Difference'][:,0], Random_Match_Dict[str(i) + '_Difference'][:,1])
plt2.plot(Random_Match_Difference_Mean[:,0], Random_Match_Difference_Mean[:,1])
plt2.plot(Real_Match_Difference[:,0], Real_Match_Difference[:,1])
plt.ylabel('dN')

plt.savefig('Output/Matching_Plot.png', dpi=300)
plt.close()

print('\n\n*************************************')
print('Random fields saved in log file.')
print('Resulting plot saved in Output.')
print('Ending the code.')
print('*************************************\n')




