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


import numpy as np
import os
import glob
import mayavi.mlab as mlab
import sys

sys.path.append('..')

import separation2 as sep

mlab.options.offscreen = False

class_file = r'D:\Dropbox\PhD\Scripts\phd-geography-ucl\lidar_data\tls\tlseparation\tlseparation\config/class_means.csv'

input_path = r'D:\Dropbox\PhD\Data\LiDAR\french_guiana\Alvaro\paper/'
files = glob.glob(input_path + '*txt')
output_path = r'D:\Dropbox\PhD\Data\LiDAR\french_guiana\Alvaro\paper\separated\auto_12/'
extension = '.txt'
delim = ' '
slice_length = 0.03
cluster_threshold = 0.1
freq_threshold = 0.8

#
#for i in files[17:]:
#
#    arr = np.loadtxt(i, delimiter=delim)
#    arr = sep.remove_duplicates(arr)
#    filename = i.split(os.sep)[-1].split(extension)[0]
#    print('Starting %s' % filename)
#
#    if os.path.isfile(output_path + filename + '_' + '_wood.txt') is False:
#
#        try:
#            wood_1, leaf_1, noclass1 = sep.wlseparate_abs(arr, 150, n_classes=4)
#            wood_3, leaf_3 = sep.wlseparate_ref_voting(arr, [15, 100, 30, 55, 75], class_file,
#                                                       4, n_classes=4)
#            wood = np.vstack((wood_3, wood_1))
#            wood = sep.remove_duplicates(wood)
#            leaf = sep.get_diff(arr, wood)
#
#            wood1, leaf1 = sep.array_majority(wood, leaf, 10)
#            wood2, leaf2 = sep.continuity_filter(wood1, leaf1, 0.026)
#
#            w_out = wood2.copy()
#            l_out = leaf2.copy()
#
#            if (w_out.shape[0] > 0) & (l_out.shape[0] > 0):
#
#                np.savetxt(output_path + filename + '_wood.txt', w_out, delimiter=' ', fmt='%1.3f')
#                np.savetxt(output_path + filename + '_leaf.txt', l_out, delimiter=' ', fmt='%1.3f')
#
#                mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#                mlab.points3d(w_out[:, 0], w_out[:, 1], w_out[:, 2],
#                              color=(0.4, 0.2, 0), mode='point')
#                mlab.points3d(l_out[:, 0], l_out[:, 1], l_out[:, 2],
#                              color=(0, 0.6, 0), mode='point')
#                mlab.savefig(output_path + filename + '.png',
#                             size=(1920, 1080), magnification='auto')
#                mlab.close()
#
#            else:
#                print('Error %s' % filename)
#        except:
#            print('Failed to process %s' % filename)
#
#    else:
#        print('File %s already exists. Skipping to next file.' % filename)


for i in files[17:]:

    arr = np.loadtxt(i, delimiter=delim)
    arr = sep.remove_duplicates(arr)
    filename = i.split(os.sep)[-1].split(extension)[0]
    print('Starting %s' % filename)

    if os.path.isfile(output_path + filename + '_' + '_wood.txt') is False:

        try:
            wood_s, leaf_s = sep.path_clustering(arr, 20, slice_length, cluster_threshold,
                                                 0.85)
            wood_1, leaf_1, noclass1 = sep.wlseparate_abs(leaf_s, 100, n_classes=4)
            wood_2, leaf_2, noclass2 = sep.wlseparate_abs(arr, 50, n_classes=4)
            wood_3, leaf_3, noclass3 = sep.wlseparate_abs(arr, 200, n_classes=4)
            wood = np.vstack((wood_s, wood_2, wood_1, wood_3))
            wood = sep.remove_duplicates(wood)
            leaf = sep.get_diff(arr, wood)

            wood1, leaf1 = sep.class_filter(wood, leaf, 30, 1)
#            wood2, leaf2 = sep.continuity_filter(wood1, leaf1, 0.026)

            w_out = wood.copy()
            l_out = leaf.copy()

            if (w_out.shape[0] > 0) & (l_out.shape[0] > 0):

                np.savetxt(output_path + filename + '_wood.txt', w_out, delimiter=' ', fmt='%1.3f')
                np.savetxt(output_path + filename + '_leaf.txt', l_out, delimiter=' ', fmt='%1.3f')

                mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
                mlab.points3d(w_out[:, 0], w_out[:, 1], w_out[:, 2],
                              color=(0.4, 0.2, 0), mode='point')
                mlab.points3d(l_out[:, 0], l_out[:, 1], l_out[:, 2],
                              color=(0, 0.6, 0), mode='point')
                mlab.savefig(output_path + filename + '.png',
                             size=(1920, 1080), magnification='auto')
                mlab.close()

            else:
                print('Error %s' % filename)
        except:
            print('Failed to process %s' % filename)

    else:
        print('File %s already exists. Skipping to next file.' % filename)