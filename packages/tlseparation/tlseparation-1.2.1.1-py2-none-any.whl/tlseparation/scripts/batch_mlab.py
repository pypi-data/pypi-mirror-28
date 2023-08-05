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
import glob
import mayavi.mlab as mlab
import os

files_path = r'D:\Dropbox\PhD\Data\LiDAR\separation_paper\clouds2/'
images_path = r'D:\Dropbox\PhD\Data\LiDAR\separation_paper\images2/'

wood_files = glob.glob(files_path + '*wood*txt')
leaf_files = glob.glob(files_path + '*leaf*txt')

extension = '.txt'
delim = ' '


for w, l in zip(wood_files, leaf_files):

    filename = w.split(os.sep)[-1].split('_wood')[0]

    wood = np.loadtxt(w, delimiter=delim)
    leaf = np.loadtxt(l, delimiter=delim)

    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(wood[:, 0], wood[:, 1], wood[:, 2], color=(0.4, 0.2, 0),
                  mode='point')
    mlab.savefig(images_path + filename + '_wood.png', size=(1366, 768))
    mlab.close()

    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(leaf[:, 0], leaf[:, 1], leaf[:, 2], color=(0, 0.6, 0),
                  mode='point')
    mlab.savefig(images_path + filename + '_leaf.png', size=(1366, 768))
    mlab.close()

    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(wood[:, 0], wood[:, 1], wood[:, 2], color=(0.4, 0.2, 0),
                  mode='point')
    mlab.points3d(leaf[:, 0], leaf[:, 1], leaf[:, 2], color=(0, 0.6, 0),
                  mode='point')
    mlab.savefig(images_path + filename + '_sep.png', size=(1366, 768))
    mlab.close()
