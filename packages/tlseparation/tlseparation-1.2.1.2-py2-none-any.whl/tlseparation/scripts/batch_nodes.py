# Copyright (c) 2017, Matheus Boni Vicari, TLSeparation Project
# All rights reserved.
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


__author__ = "Matheus Boni Vicari"
__copyright__ = "Copyright 2017, TLSeparation Project"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "1.2.1.1"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"


import tlseparation as sep
import numpy as np
import glob
import os


files = glob.glob('D:\\Dropbox\\PhD\\Data\\LiDAR\\french_guiana\\2015\\clouds4\\*txt')
path = 'D:\\Dropbox\\PhD\\Data\\LiDAR\\french_guiana\\2015\\clouds4_sep\\'
#files = glob.glob(r'D:\Dropbox\PhD\Data\LiDAR\Whytam Woods\trees_walkway\*txt')
#path = r'D:\\Dropbox\\PhD\\Data\\LiDAR\\Whytam Woods\\trees_walkway\\separated\\'
class_file = 'D:\\Dropbox\\PhD\\Scripts\\phd-geography-ucl\\lidar_data\\tls\\tlseparation\\tlseparation\\config\\class_means.csv'

extension = '.txt'
delim = ' '

knn = [20, 60, 100, 150]


for i in files:

    for k in knn:

        arr = np.loadtxt(i, delimiter=delim)
        filename = i.split(os.sep)[-1].split(extension)[0]
        print('Starting %s' % filename)

        if os.path.isfile(path + filename + '_' + str(knn) + '_wood.txt') is False:

            try:
                w_out, l_out, p = sep.auto_separation(arr, knn, class_file)

                if (w_out.shape[0] > 0) & (l_out.shape[0] > 0):

                    np.savetxt(path + filename + '_' + str(knn) +
                               '_wood.txt', w_out, delimiter=' ', fmt='%1.3f')
                    np.savetxt(path + filename + '_' + str(knn) +
                               '_leaf.txt', l_out, delimiter=' ', fmt='%1.3f')

                else:
                    print('Error %s' % filename)
            except:
                print('Failed to process %s' % filename)
        else:
            print('File %s already exists. Skipping to next file.' % filename)