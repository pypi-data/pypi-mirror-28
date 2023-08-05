# -*- coding: utf-8 -*-
#
# Pyplis is a Python library for the analysis of UV SO2 camera data
# Copyright (C) 2017 Jonas Gliß (jonasgliss@gmail.com)
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License a
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Pyplis introduction script 1 - Image import

This script loads an exemplary image which is part of the pyplis suppl.
data. Image data in pyplis is represented by the ``Img`` class, which also
allows for storage of image meta data and keeps track of changes applied to 
the image data (e.g. cropping, blurring, dark correction).

The script also illustrates how to manually work with image meta data 
encrypted in the image file name. The latter can be performed automatically in 
pyplis using file name conventions (which can be specified globally, see next 
script).
"""
from os.path import join
from datetime import datetime
from matplotlib.pyplot import close
import pyplis

from SETTINGS import check_version

# Raises Exception if conflict occurs
check_version()

# file name of test image stored in data folder 
IMG_FILE_NAME = "test_201509160708_F01_335.fts"

IMG_DIR = join(pyplis._LIBDIR, "data")

if __name__ == "__main__":
    close("all")    
    
    img_path = join(IMG_DIR, IMG_FILE_NAME)
    
    # Create Img object
    img = pyplis.image.Img(img_path)
    
    # The file name includes some image meta information which can be set manually
    # (this is normally done automatically by defining a file name convention, see
    # next script)
    
    # split filename using delimiter "_"
    spl = IMG_FILE_NAME.split(".")[0].split("_")
    
    # extract acquisition time and convert to datetime 
    acq_time = datetime.strptime(spl[1], "%Y%m%d%H%M")
    # extract and convert exposure time from filename (convert from ms -> s)
    texp = float(spl[3]) / 1000
    
    img.meta["start_acq"] = acq_time
    img.meta["texp"] = texp 
    
    # add some blurring to the image
    img.add_gaussian_blurring(sigma_final=3)
    
    # crop the image edges 
    roi_crop = [100, 100, 1244, 924] #[x0, y0, x1, y1]
    img.crop(roi_abs=roi_crop)
    
    # apply down scaling (gauss pyramid)
    img.to_pyrlevel(2)

    ### Show image
    img.show()
    
    # print image information
    print img
    
