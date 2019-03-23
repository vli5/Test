# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 12:04:15 2019

@author: Vicky Li
"""

path = ('G:/My Drive/URMC Corning/Corning_HSI_Data/HIM-2 Study/')

import spectral.io.envi as envi
import matplotlib.pyplot as plt

def intensity(img, file,
              isxaxistimeorbands,
              incrementfactorfortime,
              incrementfactorforbands,
              scantimefactor,
              plottrueorfalse):

#    print(img)
    listoftimepoints = range(0,img.nrows,incrementfactorfortime)
    listofbands = range(0,img.nbands,incrementfactorforbands)
#    print(listoftimepoints,listofbands,sep='\n')
    
    band_indexes = listofbands#[]
#    for band in listofbands:
##        print('band',band)
#        temp = float('inf')
#        i = 0
#        band_index = None
#        for x in img.metadata['wavelength']:
##            print('x',x)
#            if abs(float(x) - band) < temp:
#                temp = abs(float(x) - band)
##                print('temp',temp)
#                band_index = i
##                print('ind',band_index)
#            i += 1
##            print(i)
#        band_indexes += [band_index]
#    print(band_indexes)
    if(isxaxistimeorbands == 'time'):
        time = [x*scantimefactor for x in listoftimepoints];
        timebyintensitybybands = []
        for x in listoftimepoints:
            temp= []
            for z in band_indexes:
                temp += [img[x,:,z].mean()*1000]
            timebyintensitybybands += [temp]
        if(plottrueorfalse):
            plt.figure()
            plt.plot(time,timebyintensitybybands)    
            plt.title(file)
            plt.xlabel('Time (min)');
            plt.ylabel('Relative Intensity');
        return timebyintensitybybands
    elif(isxaxistimeorbands == 'bands'):
        bandsbyintensitybytime = []
        for z in band_indexes:
            temp = []
            for x in listoftimepoints:
                temp += [img[x,:,z].mean()*1000]
            bandsbyintensitybytime += [temp]
        if(plottrueorfalse):
            plt.figure()
            plt.plot(listofbands,bandsbyintensitybytime)    
            plt.title(file)
            plt.xlabel('Bands');
            plt.ylabel('Relative Intensity');
        return bandsbyintensitybytime

scantimefactor = 490/7000/60;

def top5(time, incrementfactorfortime):    
#    print(int(1/ scantimefactor))# / 100))
    timesliced = time[int(1/ scantimefactor / incrementfactorfortime) :
                      int(7/ scantimefactor / incrementfactorfortime) + 1]
    bandsbytime = []
    for i in range(len(timesliced[0])):
        temp = []
        for t in timesliced:
            temp += [t[i]]
        bandsbytime += [temp]
    bandintensityrange = []
    bandintensityrangetimetakes = []
    for band in bandsbytime:
        bandintensityrange += [max(band) - min(band)]
        bandintensityrangetimetakes += [round(
                (band.index(max(band)) - band.index(min(band))) * 
                (scantimefactor * incrementfactorfortime), 3)]
    temp = []
    for i in range(len(bandsbytime)):
        temp += [bandintensityrange[i]/bandintensityrangetimetakes[i]]
    sortedrangebandindexes = []
    for range_ in sorted(bandintensityrange,reverse=True):
        sortedrangebandindexes += [bandintensityrange.index(range_)]
    sortedtemp = []
    for range_ in sorted(temp,reverse=True):
        sortedtemp += [temp.index(range_)]
    print(sortedrangebandindexes,'sortedrangebandindexes')
    print(sortedtemp,'sortedtemp')
    i = 0
    temp = []
    for index in sortedrangebandindexes:
        if i < 5:
            temp += [bandsbytime[index]]
        else:
            break
        i += 1
    temp2 = []
    for i in range(len(temp[0])):
        temp3 = []
        for t in temp:
            temp3 += [t[i]]
        temp2 += [temp3]
    return temp2 ### 652.31 band with the most and fastest change on release of ischemia

incrementfactorfortime = 50
incrementfactorforbands = 5
#time = []

#import pandas as pd

#def df(img, file, incrementfactorfortime,
#       incrementfactorforbands, scantimefactor):
#    
#    time = intensity(img, file, 'time', 
#                     incrementfactorfortime, 
#                     incrementfactorforbands, 
#                     scantimefactor)
#    d = {}
#    temp = []
#    for i in range(len(time)):
#        temp += [i / scantimefactor / incrementfactorfortime]    
#    d['time'] = temp
#    temp = []
#    for i in range(len(time[0])):
#        temp += [img.metadata['wavelength'][i * incrementfactorforbands]]
#    d['wavelength'] = temp
#    
#    return df

def read(files):
    temp = []
    for file in files:
        if '.hdr' in file:
            temp += [file.split('.')[0]]
    return temp

from os import walk
from os import listdir
folders = listdir(path)
#print(folders)
temp = []
for folder in folders:
    if not '.' in folder:
        temp += [folder]
folders = temp

def data(path,folder,
         incrementfactorfortime, 
         incrementfactorforbands, 
         scantimefactor):
    data = {}
    files = []
    for (dirpath, dirnames, filenames) in walk(path+folder):
        files.extend(filenames)
        break    
    files = read(files)
#    print(files)
    for file in files:
        print(path + folder + '/' + file + '.hdr')
        img = envi.open(path + folder + '/' + file + '.hdr', 
                    image= path + folder + '/' + file + '.hsi')
        time = intensity(img, file, 'time', 
                         incrementfactorfortime, 
                         incrementfactorforbands, 
                         scantimefactor, False)
        data[folder+'/'+file] = time
    return data
#    break
#    bands = intensity(folder, files[1], 'bands', 100, 10, scantimefactor)
#    break
#        top5(time, incrementfactorfortime)

#print(len(data))
for folder in folders:
    data = data(path,folder,
         incrementfactorfortime, 
         incrementfactorforbands, 
         scantimefactor)
    break
#    folderpath = unixpath+folder+'\\'
#    print(folderpath)

data.keys()

#for d in data:
#    print(len(data[d]))
data.keys()
