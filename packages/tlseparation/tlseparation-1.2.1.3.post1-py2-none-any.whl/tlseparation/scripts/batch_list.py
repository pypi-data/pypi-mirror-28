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
__version__ = "1.2.1.3"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"


import os
import numpy as np
from automated_separation import large_tree_1
import mayavi.mlab as mlab


if __name__ == "__main__":

    mlab.options.offscreen = True

    output_folder = r'D:\Dropbox\PhD\Data\LiDAR\separation_paper\clouds\automated/'

    class_file = r'D:/Dropbox/PhD/Scripts/phd-geography-ucl/lidar_data/tls/tlseparation/tlseparation/config/class_means.csv'
    filelist = r'D:\Dropbox\PhD\Projects\Automated Wood-Leaf Separation\paper_processing\filelist.txt'

    with open(filelist, 'r') as f:
        files = f.read().split('\n')

    for f in files:

        fname = os.path.basename(f)
        out_name = output_folder + fname
        if not os.path.isfile(out_name + '_wood.txt'):

            print('Processing file: %s' % fname)
            try:
                try:
                    arr = np.loadtxt(f, delimiter=',')
                except:
                    arr = np.loadtxt(f, delimiter=' ')

                wood, leaf = large_tree_1(arr, class_file)

                mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
                mlab.points3d(wood[:, 0], wood[:, 1], wood[:, 2],
                              color=(0.4, 0.2, 0), mode='point')
                mlab.points3d(leaf[:, 0], leaf[:, 1], leaf[:, 2],
                              color=(0, 0.55, 0), mode='point')
                mlab.savefig(output_folder + fname + '_separated.png',
                             size=(1920, 1080))
                mlab.close()

                np.savetxt(out_name + '_wood.txt', wood, fmt='%1.4f')
                np.savetxt(out_name + '_leaf.txt', leaf, fmt='%1.4f')

            except:
                print('Failed to process file: %s' % fname)