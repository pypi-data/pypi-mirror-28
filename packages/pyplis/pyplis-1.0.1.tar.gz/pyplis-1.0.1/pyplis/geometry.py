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
Pyplis module containing functionality for all relevant geometrical 
calculations
"""
from numpy import nan, arctan, deg2rad, linalg, sqrt, abs, array, radians,\
    sin, cos, arcsin, tan, rad2deg, zeros, linspace, isnan, asarray, ones,\
    arange, argmin
from collections import OrderedDict as od
from warnings import warn
from matplotlib.pyplot import figure
from copy import deepcopy

from .image import Img
from .helpers import check_roi, isnum
try:
    from geonum import GeoSetup, GeoPoint, GeoVector3D, TopoData
    from geonum.topodata import TopoAccessError
except:
    warn("Geonum library could not be found")
    
class MeasGeometry(object):
    """Class for calculations and management of the measurement geometry

    All calculations are based on provided information about camera (stored
    in dictionary :attr:`cam`, check e.g. ``self.cam.keys()`` for valid keys), 
    source (stored in dictionary :attr:`source`, check e.g. 
    ``self.source.keys()`` for valid keys) and meteorological wind direction
    (stored in dictionary :attr:`wind`). If you want to change these parameters
    you can directly change the dictionaries, e.g.:: 
        
        self.cam["altitude"]=3000.0 #m
        
    or better, use the correpdonding update methods :func:`update_cam_specs`, 
    :func:`update_source_specs` and :func:`update_wind_specs`. The latter 
    by default also update the most important attribute of this class 
    :attr:`geo_setup` which is an instance of the :class:`geonum.GeoSetup`
    class and which is central for all geometrical calculations (e.g. camera
    to plume distance).
    
    Attributes
    ----------
    geo_setup : GeoSetup
        class containing information about the current measurement setup.
        Most of the relevant geometrical calculations are performed within
        this object
    source : dict
        dictionary containing information about emission source (valid 
        keys: ``name, lon, lat, altitude``)
    wind : dict
        dictionary containing information about meteorology at source 
        position (valid keys: ``dir, dir_err, velo, velo_err``)
    cam : dict
        dictionary containing information about the camera (valid keys: 
        ``cam_id, ser_no, lon, lat, altitude, elev, elev_err, azim, 
        azim_err, focal_length, pix_width, pix_height, pixnum_x, pixnum_y
        alt_offset``
        
    Parameters
    ----------
    source_info : dict
        dictionary containing source parameters (see :attr:`source` for 
        valid keys)
    cam_info : dict
        dictionary containing camera parameters (see :attr:`cam` for 
        valid keys)
    wind_info : dict
        dictionary conatining meteorology information (see :attr:`wind`
        for valid keys)
    """
    def __init__(self, source_info={}, cam_info={}, wind_info={},
                 auto_topo_access=True):
        
        self.source     =   od([("name"         ,   ""),
                                ("lon"          ,   nan),
                                ("lat"          ,   nan),
                                ("altitude"     ,   nan)])
        
        self.wind       =   od([("dir"      ,   nan),
                                ("dir_err"  ,   nan),
                                ("velo"      ,   nan),
                                ("velo_err"  ,   nan)])
                                
        self.cam        =   od([("cam_id"       ,   ""),
                                ("ser_no"       ,   9999),
                                ("lon"          ,   nan),
                                ("lat"          ,   nan),
                                ("altitude"     ,   nan),
                                ("elev"         ,   nan),
                                ("elev_err"     ,   nan),
                                ("azim"         ,   nan),
                                ("azim_err"     ,   nan),
                                ("focal_length" ,   nan), #in m
                                ("pix_width"    ,   nan), #in m
                                ("pix_height"   ,   nan), #in m
                                ('pixnum_x'     ,   nan),
                                ('pixnum_y'     ,   nan),
                                ('alt_offset'   ,   0.0)])  #altitude above 
                                                            #topo in m
        
        self.auto_topo_access = auto_topo_access
        self.geo_setup = GeoSetup(id=self.cam_id)
        
        self.update_source_specs(source_info, update_geosetup=False)
        self.update_cam_specs(cam_info, update_geosetup=False)
        self.update_wind_specs(wind_info, update_geosetup=False)
        if any([bool(x)==True for x in [source_info, cam_info, wind_info]]):
            self.update_geosetup()
    
    @property
    def cam_id(self):
        """ID of current camera"""
        return self.cam["cam_id"]
    
    @property
    def azim_cfov(self):
        """Azimuth of camera viewing direction (CFOV)"""
        return self.cam["azim"]
        
    def get_cam_specs(self, img_obj):
        """Reads camera meta information from image meta data
            
            1. Focal length lense
            2. Image sensor
                i. Pixel width
                #. Pixel height
        
        Parameters
        ----------
        img_obj : Img
            image data containing information about camera specs in meta
            dictionary
        """
        #self.cam["pixLengthY"],self.cam["pixLengthX"]=img_obj.img.shape
        param_keys = ["focal_length","pix_width","pix_height"]
        for key in param_keys:
            if isnan(self.cam[key]):
                self.cam[key] = img_obj.meta[key]
    
    def update_cam_specs(self, info_dict=None, update_geosetup=True,
                         **kwargs):
        """Update camera settings
        
        Update camera info dictionary (:attr:`cam`) either by providing a 
        dictionary containing valid key / value pairs (:param:`info_dict` or by 
        providing valid key / value pairs directly using :param:`kwargs`)
        
        Parameters
        ----------
        info_dict : dict
            dictionary containing camera information (see :attr:`cam` for 
            valid keys)  
        update_geosetup : bool
            If True, the method :func:`update_geosetup` is called at the end
            of this method
        **kwargs
            alternative way to update the camera dictionary using valid 
            keywords directly 
        """
        if isinstance(info_dict, dict):
            for key, val in info_dict.iteritems():
                if key in self.cam.keys() and val is not None:
                    self.cam[key] = val
        self.cam.update(**kwargs)
        if update_geosetup:
            self.update_geosetup()
            
    def update_source_specs(self, info_dict=None, update_geosetup=True, 
                            **kwargs):
        """Update source settings
        
        Update source info dictionary (:attr:`source`) either by providing a 
        dictionary containing valid key / value pairs (:param:`info_dict` or by 
        providing valid key / value pairs directly using :param:`kwargs`)
        
        Parameters
        ----------
        info_dict : dict
            dictionary containing source information (see :attr:`source` 
            for valid keys) 
        update_geosetup : bool
            If True, the method :func:`update_geosetup` is called at the end
            of this method
        **kwargs
            alternative way to update the source dictionary using valid 
            keywords directly
        """
        if isinstance(info_dict, dict):
            for key, val in info_dict.iteritems():
                if self.source.has_key(key) and val is not None:
                    self.source[key] = val
        self.source.update(**kwargs)
        if update_geosetup:
            self.update_geosetup()
            
    def update_wind_specs(self, info_dict=None, update_geosetup=True, 
                          **kwargs):
        """Update meteorological settings
        
        Update wind info dictionary (:attr:`wind`) either by providing a 
        dictionary containing valid key / value pairs (:param:`info_dict` or by 
        providing valid key / value pairs directly using :param:`kwargs`)
        
        Parameters
        ----------
        info_dict : dict
            dictionary containing meterology information (see :attr:`wind` 
            for valid keys) 
        update_geosetup : bool
            If True, the method :func:`update_geosetup` is called at the end
            of this method
        **kwargs
            alternative way to update the wind dictionary using valid 
            keywords directly
        """
        if isinstance(info_dict, dict):
            for key, val in info_dict.iteritems():
                if key in self.wind.keys() and isnum(val):
                    self.wind[key] = val
        self.wind.update(**kwargs)
        if update_geosetup:
            self.update_geosetup()
    
    def _check_geosetup_info(self):
        """Checks if relevant information for :attr:`geo_setup` is ready"""
        check = ["lon", "lat", "elev", "azim", "dir"]
        cam_ok, source_ok = True, True
        for key in check:
            if self.cam.has_key(key) and not isnum(self.cam[key]):
                #print "missing info in cam, key %s" %key
                cam_ok = False
            if self.source.has_key(key) and not isnum(self.source[key]):
                #print "missing info in source, key %s" %key
                source_ok = False
        if not isnum(self.wind["dir"]) and cam_ok:
            print ("setting orientation angle of wind direction relative to "
                "camera cfov")
            self.wind["dir"] = (self.cam["azim"] + 90)%360
            self.wind["dir_err"] = 45
            
        return cam_ok, source_ok
        
    def update_geosetup(self):
        """Update the current GeoSetup object
            
        Note
        ----
        The borders of the range are determined considering cam pos, source
        pos and the position of the cross section of viewing direction with 
        plume
            
        """   
        cam_ok, source_ok = self._check_geosetup_info()
        mag = 20
        if cam_ok:
            print "Updating camera in GeoSetup of MeasGeometry"
            cam = GeoPoint(self.cam["lat"], self.cam["lon"],
                           self.cam["altitude"], name="cam",
                           auto_topo_access=self.auto_topo_access)
            self.geo_setup.add_geo_point(cam)
            
        if source_ok:       
            print "Updating source in GeoSetup of MeasGeometry"
            source = GeoPoint(self.source["lat"], self.source["lon"],
                              self.source["altitude"], name="source",
                              auto_topo_access=self.auto_topo_access)
            self.geo_setup.add_geo_point(source)

        if cam_ok and source_ok:
            source2cam = cam - source #Vector pointing from source to camera
            mag = source2cam.norm #length of this vector
            source2cam.name = "source2cam"
            #vector representing the camera center pix viewing direction (CFOV),
            #anchor at camera position
            cam_view_vec = GeoVector3D(azimuth=self.cam["azim"], 
                                       elevation=self.cam["elev"], 
                                       dist_hor=mag, anchor=cam, 
                                       name="cfov")
            print ("Updating source2cam and cam viewing direction "
                   "vectors in GeoSetup of MeasGeometry")

            #vector representing the emission plume 
            #(anchor at source coordinates)
            plume_vec = GeoVector3D(azimuth=self.plume_dir[0],
                                    dist_hor=mag, anchor=source, 
                                    name="plume_vec")
            
            self.geo_setup.add_geo_vectors(source2cam, cam_view_vec, 
                                           plume_vec)
            #horizontal intersection of plume and viewing direction
            offs = plume_vec.intersect_hor(cam_view_vec)
            #Geopoint at intersection
            intersect = source + offs
            intersect.name = "intersect"
            self.geo_setup.add_geo_point(intersect)
            self.geo_setup.set_borders_from_points(extend_km=
                                                   self._map_extend_km(),
                                                   to_square=True)
            print "MeasGeometry was updated and fulfills all requirements"
            return True
        
        elif cam_ok:
            cam_view_vec = GeoVector3D(azimuth=self.cam["azim"], 
                                       elevation=self.cam["elev"], 
                                       dist_hor=mag, anchor=cam, 
                                       name="cfov")
            self.geo_setup.add_geo_vector(cam_view_vec)
            print "MeasGeometry was updated but misses source specifications"
        print "MeasGeometry not (yet) ready for analysis"
        
        return False
                                                 
    def get_coordinates_imgborders(self):
        """Get elev and azim angles corresponding to camera FOV"""
        det_width = self.cam["pix_width"] * self.cam["pixnum_x"]
        det_height = self.cam["pix_height"] * self.cam["pixnum_y"]
        del_az = rad2deg(arctan(det_width /\
                (2.0 * self.cam["focal_length"])))
        del_elev = rad2deg(arctan(det_height/\
                (2.0 * self.cam["focal_length"])))
    
        return {"azim_left"     :   self.cam["azim"] - del_az,
                "azim_right"    :   self.cam["azim"] + del_az,
                "elev_bottom"   :   self.cam["elev"] - del_elev,
                "elev_top"      :   self.cam["elev"] + del_elev}
    
    def horizon_analysis(self, skip_cols=30):
        """Searches pixel coordinates of horizon for image columns
        
        The algorithm performs a topography analysis for a number of image
        columns. Elevation profiles are determined for each column (azimuth)
        and from those, the horizon elevation angle is searched. The retrieved
        values are returned in pixel coordinates.
        
        :param skip_cols: distance between pixel columns for which the analysis
            is performed
            
        .. note::
        
            This is a Beta version, please report any problems
        
        """
        cam = self.cam_pos
        cols = arange(0, self.cam["pixnum_x"], skip_cols)
        rows = arange(0, self.cam["pixnum_y"], 1)
        azims, elevs = self.get_azim_elev(cols, rows)
        dist = self.geo_len_scale() * 1.2
        idx_x, idx_y, dists = [], [], []
        elev_min, elev_max = min(elevs), max(elevs)
        for k in range(len(azims)):
            azim = azims[k]
            elev_profile = cam.get_elevation_profile(azimuth=azim,
                                                     dist_hor=dist)
            (elev, 
             elev_secs, 
             dist_secs) = elev_profile.find_horizon_elev(elev_start=elev_min,
                                                         elev_stop=elev_max, 
                                                         step_deg=0.1,
                                                         view_above_topo_m=
                                                         self.cam["alt_offset"])
                                                       
            idx_x.append(cols[k])
            idx_y.append(argmin(abs(elev - elevs)))
            try:
                dists.append(dist_secs[-1])
            except:
                warn("Temporary solution, need a fix here...")
                dists.append(nan)
        return idx_x, idx_y, dists
                        
    def get_viewing_directions_line(self, line):
        """Determine viewing direction coords for a line in an image
        
        :param list line: start / stop pixel coordinates of line, i.e.
            ``[x0, y0, x1, y1]``
        """
        f = self.cam["focal_length"]
        
        x0, y0, x1, y1 = line[0], line[1], line[2], line[3]
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        
        delx = abs(x1 - x0)
        dely = abs(y1 - y0)
        
        l = sqrt(delx ** 2 + dely ** 2)
        x = linspace(x0, x1, l)
        y = linspace(y0, y1, l)
        dx = self.cam["pix_width"] * (x - self.cam["pixnum_x"] / 2)
        dy = self.cam["pix_height"] * (y - self.cam["pixnum_y"] / 2)
        azims = rad2deg(arctan(dx / f)) + self.cam["azim"]
        elevs = -rad2deg(arctan(dy / f)) + self.cam["elev"]
        return (azims, elevs, x, y)
            
    def get_distances_to_topo_line(self, line, skip_pix=30, topo_res_m=5.,
                                   min_slope_angle=5.):
        """Retrieve distances to topography for a line on an image
        
        Calculates distances to topography based on pixels on the line. This is 
        being done by retriving a elevation profile in the azimuthal viewing
        direction of each pixel (i.e. pixel column) and then using this profile
        and the corresponding camera elevation (pixel row) to find the first
        intersection of the viewing direction (line) with the topography
        
        :param list line: list with line coordinates: ``[x0, y0, x1, y1]`` 
            (can also be :class:`LineOnImage` object)
        :param int skip_pix: step width for retrieval along line
        :param float topo_res_m: desired resolution of topographic data
            (is interpolated)
        :param float min_slope_angle: mininum angle of slope, pixels 
            pointing into flatter topographic areas are ignored
        """
        try:
            print self.cam_pos
        except:
            print ("Failed to retrieve distance to topo for line %s in "
                "MeasGeometry: geo location of camera is not available" %line)
            return False
        if not isinstance(self.geo_setup.topo_data, TopoData):
            try:
                self.geo_setup.load_topo_data()
            except:
                print ("Failed to retrieve distance to topo for line %s in "
                    "MeasGeometry: topo data could not be accessed..." %line)
                return False
        azims, elevs, i_pos, j_pos = self.get_viewing_directions_line(line)
        cond = ~isnan(azims)
        azims, elevs, i_pos, j_pos = azims[cond], elevs[cond], i_pos[cond],\
                                                                    j_pos[cond]
        if not len(azims) > 0:
            print ("Failed to retrieve distance to topo for line %s in "
                    "MeasGeometry: viewing directions (azim, elev) could not "
                    "be retrieved..." %line)
            return False
        #Take only every "skip_pix" pixel on the line
        azims, elevs = azims[::int(skip_pix)], elevs[::int(skip_pix)]
        i_pos, j_pos = i_pos[::int(skip_pix)], j_pos[::int(skip_pix)]
    
        max_dist = self.source2cam.magnitude * 1.10
        #initiate results
        res = { "dists"         : [], 
                "dists_err"     : [],
                "geo_points"    : [],
                "ok"            : []} 
        
        for k in range(len(azims)):
            ep = None
            #try:
            ep = self.get_elevation_profile(azim = azims[k], dist_hor = 
                max_dist, topo_res_m = topo_res_m)

            d, d_err, p , l, _ = ep.get_first_intersection(elevs[k],\
                        view_above_topo_m = self.cam["alt_offset"])
            if d is not None and min_slope_angle > 0:
                slope = ep.slope_angle(d)
                if slope <  min_slope_angle:
                    print "Slope angle too small, remove point at dist %.1f" %d
                    d = None
            ok = True
            if d is None: #then, the intersection could be found
                ok = False
                d, d_err = nan, nan
                
            res["dists"].append(d)
            res["dists_err"].append(d_err)
            res["geo_points"].append(p)
            res["ok"].append(ok)
            
        res["azims"] = azims
        res["elevs"] = elevs
        res["i_pos"] = i_pos
        res["j_pos"] = j_pos
        for key in res:
            res[key] = asarray(res[key])
        return res
    
    def get_angular_displacement_pix_to_cfov(self, pos_x, pos_y):
        """Get the angular difference between pixel coordinate and detector 
        center coordinates
        
        :param int pos_x: x position on detector
        :param int pos_y: y position on detector
        """
        dx = self.cam["pix_width"] * (pos_x - self.cam["pixnum_x"] / 2)
        dy = self.cam["pix_height"] * (pos_y - self.cam["pixnum_y"] / 2)
        f = self.cam["focal_length"]
        del_az = rad2deg(arctan(dx / f))
        del_elev = rad2deg(arctan(dy / f))
        return del_az, del_elev
    
    def get_azim_elev(self, pos_x, pos_y):
        """Get values of azimuth and elevation in pixel (x|y)
        
        :param int pos_x: x position on detector
        :param int pos_y: y position on detector
        """
        del_az, del_elev = self.get_angular_displacement_pix_to_cfov(\
                                                            pos_x, pos_y)
        return self.cam["azim"] + del_az, self.cam["elev"] - del_elev
    
    def _check_topo(self):
        """Checks if topo data can be accessed (returns True or False)"""
        if not isinstance(self.geo_setup.topoData, TopoData):
            try:
                self.geo_setup.load_topo_data()
                return True
            except Exception as e:
                print ("Failed to retrieve topo data in MeasGeometry..: %s" 
                    %repr(e))
                return False
        return True
        
    def get_elevation_profile(self, col_num=None, azim=None, dist_hor=None,
                                topo_res_m=5.):
        """Retrieves elev profile from camera into a certain azim direction
        
        :param int col_num: pixel column number of profile, if None or
            not in image detector range then try to use second input parameter 
            azim
        :param float azim: is only used if input param col_num == None,
            then profile is retrieved from camera in direction of 
            specified azimuth angle
        :param float dist_hor: horizontal distance (from camera, in km) 
            up to witch the profile is determined. If None, then use 1.05 times 
            the camera source distance
        :param float topo_res_m: desired horizontal grid resolution in m ()
        """
        try:
            az = azim
            if 0 <= col_num < self.cam["pixnum_x"]:
                az, _ = self.get_azim_elev(col_num, 0)        
            
            if dist_hor == None:
                dist_hor = (self.cam_pos - self.source_pos).norm * 1.05
            p = self.cam_pos.get_elevation_profile(azimuth=az, dist_hor=
                dist_hor, resolution=topo_res_m)
            print "Succesfully determined elevation profile for az = %s" %az
            return p
        
        except:
            print "Failed to retrieve elevation profile"
            return False
    
    def get_distance_to_topo(self, col_num = None, row_num = None, azim = None, 
                                 elev = None, min_dist = 0.2, max_dist = None):
        """Determine distance to topography based on pixel coordinates
        
        :param int col_num: pixel column number for elevation profile, 
            from which the intersection with viewing direction is retrieved. If 
            None or not in image detector range then try to use third input 
            parameter (azim)
        :param int row_num: pixel row number for which the intersection 
            with elevation profile is is retrieved. If None or not in image 
            detector range then try to use 4th input parameter elev, row_num
            is only considerd if col_num is valid
        :param float azim: camera azimuth angle of intersection: is only 
            used if input param col_num == None
        :param float elev: camera elevation angle for distance 
            estimate: is only used if input param row_num == None
        :param float min_dist: minimum distance (in km) from camera for 
            retrieval of first intersection. Intersections of viewing direction 
            with topography closer than this distance are disregarded 
            (default:  0.2)
        :param float max_dist: maximum distance (in km) from camera for 
            which intersections with topography are searched
            
        """   
        az, el = azim, elev           
        try:
            # if input row and column are valid, use azimuth ane elevation 
            # angles for the corresponding pixel
            if (0 <= col_num < self.cam["pixnum_x"]) and\
                                (0 <= row_num < self.cam["pixnum_y"]):
                az, el = self.get_azim_elev(col_num, row_num)    
            # Check if azim and elev are valid numbers
            if not all([self._check_float(val) for val in [az, el]]):
                raise ValueError("Invalid value encounterd for azim, elev " 
                    "while trying to estimate cam to topo distance: %s,%s" 
                    %(az,el))
            # determine elevation profile
            p = self.get_elevation_profile(azim = az, dist_hor = max_dist)
            if not bool(p):
                raise TopoAccessError("Failed to retrieve topography profile")
            # Find first intersection
            d, d_err, pf = p.get_first_intersection(elev, min_dist)
            return d, d_err, pf
        except Exception as e:
            print ("Failed to retrieve distance to topo:" %repr(e))
            return False
    
    def _check_float(self, val):
        """Returns bool"""
        if not isinstance(val, float) or isnan(val):
            return False
        return True
    
    def _correct_view_dir_lowlevel(self, pix_x, pix_y, obj_pos):
        #get the angular differnce of the object position to CFOV of camera
        del_az, del_elev = self.get_angular_displacement_pix_to_cfov(\
                                                            pix_x, pix_y)
        cam_pos = self.geo_setup.points["cam"]
        v = obj_pos - cam_pos
        
        az_obj = (v.azimuth + 360)%360
        elev_obj = v.elevation#rad2deg(arctan(delH/v.magnitude/1000))#the true elevation of the object
        elev_cam = elev_obj + del_elev
        az_cam = az_obj - del_az
        
        return elev_cam, az_cam
        
    def find_viewing_direction(self, pix_x, pix_y, pix_pos_err=10, 
                               obj_id="", geo_point=None, lon_pt=None, 
                               lat_pt=None, alt_pt=None, update=True, 
                               draw_result=False):
        """Retrieve camera viewing direction from point in image
        
        Uses the geo coordinates of a characteristic point in the image (e.g.
        the summit of a mountain) and the current position of the camera
        (Lon / Lat) to determine the viewing direction of the camera (azimuth,
        elevation).
        

        :param int pix_x: x position of object on camera detector 
            (measured from left)
        :param int pix_y: y position of object on camera detector 
            (measured from top)
        :param int pix_pos_err: radial uncertainty in pixel location (used to
            estimate and update ``self.cam["elev_err"], self.cam["azim_err"]``)
        :param bool update: if True current data will be updated and
            ``self.geo_setup`` will be updated accordingly
        :param str obj_id: string ID of object, if this object is available
            as :class:`GeoPoint` in ``self.geo_setup`` then the corresponding 
            coordinates will be used, if not, please provide the position of 
            the characteristic point either using :param:`geo_point` or by 
            providing  its coordinates using params lat_pt, lon_pt, alt_pt
        :param GeoPoint geo_point: geo point object of characteristic point
        :param float lon_pt: longitude of characteristic point
        :param float lat_pt: latitude of characteristic point
        :param float alt_pt: altitude of characteristic point (unit m)
        :param bool update: if True, camera azim and elev are updated 
            within this object
        :param bool draw_result: if True, a 2D map is drawn showing 
            results
        
        :returns:
            - float, retrieved camera elevation
            - float, retrieved camera azimuth
            - MeasGeometry, initial state of this object, a deepcopy of 
            this class, before changes where applied (if they were applied, 
            see also :param:`update`)
            
        """
        geom_old = deepcopy(self)
        if obj_id in self.geo_setup.points:
            obj_pos = self.geo_setup.points[obj_id]
        elif isinstance(geo_point, GeoPoint):
            obj_pos = geo_point
            self.geo_setup.add_geo_point(obj_pos)
        else:
            try:
                obj_pos = GeoPoint(lat_pt, lon_pt, alt_pt, name=obj_id)
                self.geo_setup.add_geo_point(obj_pos)
            except:
                raise IOError("Invalid input, characteristic point for "
                    "retrieval of viewing direction could not be extracted"
                    "from input params..")
        
        elev_cam, az_cam = self._correct_view_dir_lowlevel(pix_x, pix_y,
                                                           obj_pos)
        
        pix_range_x = [pix_x - pix_pos_err,
                       pix_x - pix_pos_err]
        pix_range_y = [pix_y - pix_pos_err,
                       pix_y + pix_pos_err]
        elevs, azims = [], []
        for xpos in pix_range_x:
            for ypos in pix_range_y:
                elev, azim = self._correct_view_dir_lowlevel(xpos, ypos,
                                                             obj_pos)
                elevs.append(elev), azims.append(azim)
        elev_err = max(abs(elev_cam - asarray(elevs)))
        azim_err = max(abs(az_cam - asarray(azims)))
                
        if update:
            elev_old, az_old = geom_old.cam["elev"], geom_old.cam["azim"]
            print ("Old Elev / Azim cam CFOV: %.2f / %.2f" %(elev_old, az_old))
            print ("New Elev / Azim cam CFOV: %.2f / %.2f" %(elev_cam, az_cam))
            self.cam["elev"] = elev_cam
            self.cam["azim"] = az_cam
            self.cam["elev_err"] = elev_err
            self.cam["azim_err"] = azim_err
            stp = self.geo_setup
            plume_vec = stp.vectors["plume_vec"]
            #new vector representing the camera center pixel viewing direction (CFOV),
            #anchor at camera position
            cam_pos = self.geo_setup.points["cam"]
            cam_view_vec = GeoVector3D(azimuth=self.cam["azim"],
                                       elevation=self.cam["elev"], 
                                       dist_hor=stp.magnitude,
                                       anchor=cam_pos, name="cfov")
            #horizontal intersection of plume and viewing direction
            offs = plume_vec.intersect_hor(cam_view_vec)
            #Geopoint at intersection
            p3 = stp.points["source"] + offs
            p3.name = "intersect"
            
            #Delete the old stuff
            stp.delete_geo_vector("cfov")
            stp.delete_geo_point("intersect")
            stp.delete_geo_point("ll")
            stp.delete_geo_point("tr")
            #and write the new stuff
            stp.add_geo_point(p3)
            stp.add_geo_vector(cam_view_vec)
            stp.set_borders_from_points(extend_km=self._map_extend_km(),
                                        to_square=True)
            if isinstance(stp.topo_data, TopoData):
                stp.load_topo_data()
        map = None
        if draw_result:
            s=self.geo_setup
            nums = [int(255.0 / k) for k in range(1, len(s.vectors)+3)]
            map = self.draw_map_2d(draw_fov=False)
            map.draw_geo_vector_2d(self.cam_view_vec,
                                   c=s.cmap(nums[1]),
                                   ls="-",
                                   label="cam cfov (corrected)")
            self.draw_azrange_fov_2d(map, poly_id="fov (corrected)")
            view_dir_vec_old = geom_old.geo_setup.vectors["cfov"]
            view_dir_vec_old.name = "cfov_old"
            
            map.draw_geo_vector_2d(view_dir_vec_old,
                                   c=s.cmap(nums[1]),
                                   ls="--",
                                   label="cam cfov (initial)")
            map.legend()
    
        return elev_cam, az_cam, geom_old, map
    
    def calculate_pixel_col_distances(self):
        """Determine pix to pix distances for all pix cols on the detector
        
        Based on angle between horizontal plume propagation and the individual
        horizontal viewing directions for each pixel column in original image
        coordinates. Thus, note that these values need to be converted in 
        case binning was applied or the images were downscaled (i.e. using
        gaussian pyramid).

        .. note::
        
            this is inadequate for complicated viewing geometries (i.e if 
            the the angles between viewing direction and plume are sharp)
            
        """
        ratio = self.cam["pix_width"] / self.cam["focal_length"] #in m
        azims = self.all_azimuths_camfov()
        dists = self.plume_dist(azims) * 1000.0 #in m
        pix_dists_m = dists * ratio
        return pix_dists_m, dists
        
    def pix_dist_err(self, col_num, pyrlevel=0):
        """Get uncertainty measure for pixel distance of a pixel column 

        Parameters
        ----------
        colnum : int
           column number for which uncertainty in pix-to-pix distance is
           computed
        pyrlevel : int
            convert to pyramid level
        
        Returns
        -------
        float
            pix-to-pix distance in m corresponding to input column number and
            pyramid level
        """
        az = self.all_azimuths_camfov()[int(col_num)]
        return self.plume_dist_err(az) *1000 * self.cam["pix_width"] /\
                        self.cam["focal_length"] * 2**pyrlevel
                                        
    def compute_all_integration_step_lengths(self, pyrlevel=0, roi_abs=None):
        """Determine images containing pixel and plume distances
        
        Computes and returns three images where each pixel value corresponds 
        to 1. the horizontal physical integration step length in units of m 
        corresponding to the plum
        :param int pyrlevel: returns images at a given gauss pyramid level
        :param roi_abs: ROI in absolute detector coordinates, if valid, then 
            the images are cropped
        :return:
            - Img, col_dist_img: image where each pixel corresponds to pixel 
                column distances in m
            - Img, row_dist_img: image where each pixel corresponds to pixel 
                row distances in m (same as col_dist_img if pixel width and
                height are equal)
            - Img, plume_dist_img: image where each pixel corresponds to plume
                distance in m
        """
        col_dists_m, plume_dists = self.calculate_pixel_col_distances()
        row_dists_m = col_dists_m * self.cam["pix_height"] /\
                                                    self.cam["pix_width"]
                                                
        h = self.cam["pixnum_y"]
        col_dist_img = Img(col_dists_m * ones(h).reshape((h, 1)))
        row_dist_img = Img(row_dists_m * ones(h).reshape((h, 1)))
        plume_dist_img = Img(plume_dists * ones(h).reshape((h, 1)))
        #the pix-to-pix distances need to be transformed based on pyrlevel
        col_dist_img.pyr_down(pyrlevel)
        col_dist_img = col_dist_img * 2**pyrlevel
        row_dist_img.pyr_down(pyrlevel)
        row_dist_img = row_dist_img * 2**pyrlevel
        plume_dist_img.pyr_down(pyrlevel)
        if check_roi(roi_abs):
            col_dist_img.crop(roi_abs)
            row_dist_img.crop(roi_abs)
            plume_dist_img.crop(roi_abs)
        return col_dist_img, row_dist_img, plume_dist_img
        
    def get_plume_direction(self):
        """Return the plume direction plus error based on wind direction"""
        return (self.wind["dir"] + 180) % 360, self.wind["dir_err"]

    """
    Plotting / visualisation etc
    """
    def plot_view_dir_pixel(self, col_num, row_num):
        """2D plot of viewing direction within elevation profile
        
        Determines and plots elevation profile for azimuth angle of input pixel 
        coordinate (column number). The viewing direction line is plotted based
        on the specified elevation angle (corresponding to detector row number)
        
        :param int col_num: column number of pixel on detector
        :param int row_num: row number of pixel on detector (measured from 
            top)
        :returns: elevation profile
        
        """
        azim, elev = self.get_azim_elev(col_num, row_num)    
        sc = self.geo_len_scale()
        ep = self.get_elevation_profile(azim = azim, dist_hor = sc * 1.10)
        if not bool(ep):
            raise TopoAccessError("Failed to retrieve topography profile")
        # Find first intersection
        d, d_err, pf = ep.get_first_intersection(elev, min_dist = sc * 0.05,\
                                                                plot = True)
        return ep
            
    def draw_map_2d(self, draw_cam=True, draw_source=True, draw_plume=True,
                    draw_fov=True, draw_topo=True, draw_coastline=True,
                    draw_mapscale=True, draw_legend=True, *args, **kwargs):
        """Draw the current setup in a map            
        
        :param bool draw_cam: insert camera position into map
        :param bool draw_source: insert source position into map
        :param bool draw_plume: insert plume vector into map
        :param bool draw_fov: insert camera FOV (az range) into map
        :param bool draw_topo: plot topography
        :param bool draw_coastline: draw coastlines
        :param bool draw_mapscale: insert a map scale
        :param bool draw_legend: insert a legend
        :param *args: additional non-keyword arguments for setting up the base
            map (`see here <http://matplotlib.org/basemap/api/basemap_api.
            html#mpl_toolkits.basemap.Basemap>`_)
        :param **kwargs: additional keyword arguments for setting up the base
            map (`see here <http://matplotlib.org/basemap/api/basemap_api.html
            #mpl_toolkits.basemap.Basemap>`_) 
        """
        s = self.geo_setup
        nums = [int(255.0 / k) for k in range(1, len(s.vectors)+3)]
        m = s.plot_2d(0, 0, draw_topo, draw_coastline, draw_mapscale,
                      draw_legend=0, *args, **kwargs)
        
        if draw_cam:
            m.draw_geo_point_2d(self.cam_pos)
            m.write_point_name_2d(self.cam_pos,\
                            self.geo_setup.magnitude*.05, -45)
        if draw_source:
            m.draw_geo_point_2d(self.source_pos)
            m.write_point_name_2d(self.source_pos,\
                            self.geo_setup.magnitude*.05, -45)
        if draw_plume:
            m.draw_geo_vector_2d(self.plume,
                                 c=s.cmap(nums[0]),
                                 ls="-",
                                 label="plume direction")
        if draw_fov:
            m.draw_geo_vector_2d(self.cam_view_vec, 
                                 c=s.cmap(nums[1]),
                                 label="camera cfov")
            self.draw_azrange_fov_2d(m)
        if draw_legend:
            m.legend()
        return m

    def draw_azrange_fov_2d(self, m, fc="lime", ec="none", alpha=0.15,
                            poly_id="fov"):
        """Insert the camera FOV in a 2D map
        
        :param geonum.mapping.Map m: the map object
        :param fc: face color of polygon
        :Param ec: edge color of polygon
        :param float alpha: alpha value of polygon
        """
        coords = self.get_coordinates_imgborders()
        l = self.geo_len_scale() * 1.5
        pl = self.cam_pos.offset(azimuth = coords["azim_left"], dist_hor = l)
        pr = self.cam_pos.offset(azimuth = coords["azim_right"], dist_hor = l)
        pts = [self.cam_pos, pl, pr]
        m.add_polygon_2d(pts, poly_id = poly_id, fc = fc, ec = ec,\
                                                            alpha = alpha)
        
    def draw_map_3d(self, draw_cam=True, draw_source=True, draw_plume=True,
                    draw_fov=True, cmap_topo="Oranges", 
                    contour_color="#708090", contour_antialiased=True,
                    contour_lw=0.2, ax=None, **kwargs):
        """Draw the current setup in a 3D map
        
        Parameters
        ----------
        draw_cam : bool
            insert camera position into map
        draw_source : bool
            insert source position into map
        draw_plume : bool
            insert plume vector into map
        draw_fov : bool
            insert camera FOV (az range) into map
        cmap_topo : str
            string ID of colormap for topography surface plot, defaults to
            "Oranges"
        contour_color : str
            string specifying color of contour lines colors of topo contour 
            lines (default: "#708090")
        contour_antialiased : bool
            apply antialiasing to surface plot of topography, defaults to False
        contour_lw : 
            width of drawn contour lines, defaults to 0.5, use 0 if you do not 
            want contour lines inserted
        ax : Axes3D
            3D axes object (default: None -> creates new one)
        *args : 
            non-keyword arguments for setting up the base map
            (`see here <http://matplotlib.org/basemap/api/basemap_api.
            html#mpl_toolkits.basemap.Basemap>`_)
        **kwargs: keyword arguments for setting up the basemap 
            (`see here <http://matplotlib.org/basemap/api/basemap_api.html
            #mpl_toolkits.basemap.Basemap>`_)    
            
        Returns
        -------
        Basemap
            plotted basemap
        """
        if ax is None:
            fig = figure(figsize = (14, 8))
            ax = fig.add_subplot(1, 1, 1, projection='3d')  
        s = self.geo_setup
        m = s.plot_3d(False, False, cmap_topo=cmap_topo, 
                      contour_color=contour_color, 
                      contour_antialiased=contour_antialiased,
                      contour_lw=contour_lw, ax=ax, **kwargs)
       
        zr = self.geo_setup.topo_data.alt_range * 0.05
        if draw_cam:
            self.cam_pos.plot_3d(m, add_name=True, dz_text=zr)
        if draw_source:
            self.source_pos.plot_3d(m, add_name=True, dz_text=zr)
        if draw_fov:
            self.draw_azrange_fov_3d(m)
        if draw_plume:
            m.draw_geo_vector_3d(self.plume)
        try:
            m.legend()
        except:
            pass
        return m
        
    def draw_azrange_fov_3d(self, m, fc="lime", ec="none", alpha=0.8):
        """Insert the camera FOV in a 2D map
        
        :param geonum.mapping.Map m: the map object
        :param fc: face color of polygon ("lime")
        :Param ec: edge color of polygon ("none")
        :param float alpha: alpha value of polygon (0.8)
        """
        coords = self.get_coordinates_imgborders()
        v = self.geo_setup.points["intersect"] - self.cam_pos
        pl = self.cam_pos.offset(azimuth = coords["azim_left"], dist_hor =\
                                            v.dist_hor, dist_vert = v.dz)
        pr = self.cam_pos.offset(azimuth = coords["azim_right"], dist_hor =\
                                            v.dist_hor, dist_vert = v.dz)
        pts = [self.cam_pos, pl, pr]
        m.add_polygon_3d(pts, poly_id = "fov", facecolors = fc, edgecolors = ec,\
                                                alpha = alpha, zorder = 1e8)
        
    """
    Helpers
    """     
    @property  
    def plume_dir(self):
        """Return current plume direction angle"""
        return self.get_plume_direction()
    
    @property
    def view_azim(self):
        """Return vector containing azimuth (+ uncertainty) of CFOV"""
        return (self.cam["azim"], self.cam["azim_err"])
        
    @property
    def cam_pos(self):
        """Return camera Geopoint"""
        return self.geo_setup.points["cam"]
    
    @property
    def source_pos(self):
        """Return camera Geopoint"""
        return self.geo_setup.points["source"]
    
    @property
    def intersect_pos(self):
        """Return camera Geopoint"""
        return self.geo_setup.points["intersect"]
        
    @property
    def plume(self):
        """Return the plume center vector"""
        return self.geo_setup.vectors["plume_vec"]
    
    @property
    def source2cam(self):
        """Return vector pointing camera to source"""
        return self.geo_setup.vectors["source2cam"]
    
    @property
    def cam_view_vec(self):
        """Returns vector corresponding to CFOV azimuth of camera view dir"""
        return self.geo_setup.vectors["cfov"]
        
    @property
    def all_geo_points(self):
        """Returns dict containing all :class:`GeoPoint` objects"""
        return self.geo_setup.points
        
    @property
    def all_geo_vectors(self):
        """Returns dict containing all :class:`GeoVector3D` objects"""
        return self.geo_setup.vectors
            
    def print_config(self):
        """Print the current configuration of the measurement geometry"""
        print
        print "++++++++++++++++++++++++++++++++++"        
        print "+++DETAILS MEASUREMENT GEOMEtrY+++"
        print "++++++++++++++++++++++++++++++++++"
        print 
        print "Camera ID: " + str(self.cam_id)
        print "Source ID: " + str(self.sourceId)
        print
        print "---- Details source ----"
        for key,val in self.source.iteritems():
            print str(key) + ":" + str(val)
        print        
        print "---- Details gas camera ----"
        for key,val in self.cam.iteritems():
            print str(key) + ":" + str(val)
        print 
        print "---- Details default wind ----"
        for key,val in self.wind.iteritems():
            print str(key) + ":" + str(val)
        print 
        print "---- Vectors ----"
        for key,val in self.vectors.iteritems():
            print val.name + "\n" + repr(val)
        print
    
    def haversine(self, lon0, lat0, lon1, lat1, radius = 6371.0):
        """Haversine formula
        
        Approximate horizontal distance between 2 points assuming a spherical 
        earth
        
        :param float lon0: longitude of first point in decimal degrees
        :param float lat0: latitude of first point in decimal degrees
        :param float lon1: longitude of second point in decimal degrees
        :param float lat1: latitude of second point in decimal degrees
        :param float radius: average earth radius in km (6371.0)
        """
        hav = lambda d_theta: sin(d_theta / 2.0) ** 2
        
        d_lon = radians(lon1 - lon0)
        d_lat = radians(lat1 - lat0)
        lat0 = radians(lat0)
        lat1 = radians(lat1)
 
        a = hav(d_lat) + cos(lat0) * cos(lat1) * hav(d_lon)
        c = 2 * arcsin(sqrt(a))
 
        return radius * c
    
    def geo_len_scale(self):
        """Returns the distance between cam and source in km 
        
        Uses haversine formula (:func:`haversine`) to determine the distance 
        between source and cam to estimate the geoprahic dimension of this 
        setup
        
        :returns: float, distance between source and camera
        """
        return self.haversine(self.cam["lon"], self.cam["lat"],\
                                self.source["lon"], self.source["lat"])
    
    def _map_extend_km(self, fac=5.0):
        """Helper to estimate the extend of map borders for plotting
        
        :param float fac: fraction of geo length scale used to determine the
            extend         
        """
        return self.geo_len_scale() / fac
                                
    def del_az(self, pixel_col1=0, pixel_col2=1):
        """Determine the difference in azimuth angle between 2 pixel columns
        
        Par
        :param int pixel_col1: first pixel column
        :param int pixel_col2: second pixel column
        :return: float, azimuth difference
        """
        delta = int(abs(pixel_col1 - pixel_col2))
        return rad2deg(arctan((delta * self.cam["pix_width"]) /\
                                        self.cam["focal_length"]))
    
    def plume_dist(self, az):
        """Return plume distance for input azimuth angle(s)
        
        :param az: azimuth value(s) (single val or array of values)
        """
        try:
            len(az)
        except TypeError:
            az = [az]
        diff_vec = self.geo_setup.vectors["source2cam"]
        dv = array((diff_vec.dx, diff_vec.dy)).reshape(2, 1)
        pdrad = deg2rad(self.plume_dir[0])
        azrad = deg2rad(az)
        y = (diff_vec.dx - tan(azrad) * diff_vec.dy) /\
                                    (tan(pdrad) - tan(azrad))
        x = tan(pdrad) * y
        v = array((x,y)) - dv
        return linalg.norm(v, axis = 0)
    
    def plume_dist_err(self, az=None):
        """Estimate plume distance error from uncertainties"""
        try:
            az=float(az)
        except:
            warn("invalid input, using camera CFOV azimuth")
            az = self.cam["azim"]
        #the vector between camera and source (errors here are assumed
        #negligible)
        diff_vec = self.geo_setup.vectors["source2cam"]
        dv = array((diff_vec.dx, diff_vec.dy)).reshape(2, 1)
        pdir, pdir_err = self.plume_dir

        plume_dirs = [(pdir - pdir_err)%360,
                      (pdir + pdir_err)%360]

        cam_azims = [(az - self.cam["azim_err"])%360,
                     (az + self.cam["azim_err"])%360]

        azrads = deg2rad(cam_azims)
        pdrads = deg2rad(plume_dirs)
        dists = []
        for pdrad in pdrads:
            for azrad in azrads:
                y = (diff_vec.dx - tan(azrad) * diff_vec.dy) /\
                                        (tan(pdrad) - tan(azrad))
                x = tan(pdrad) * y
                v = array((x,y)) - dv
            dists.append(linalg.norm(v, axis = 0))
        dists = asarray(dists)
        return dists.max() - dists.mean()
    
    def all_azimuths_camfov(self):
        colnum = self.cam["pixnum_x"]
        offs = 0.0
        daz = self.del_az(0,1)
        if colnum%2 == 0: #even number of pixels
            offs = -daz/2.0
        angles_rel = linspace(-colnum/2., colnum/2., colnum)*daz
        return self.azim_cfov + angles_rel + offs
    
    def col_to_az(self, colnum):
        """Convert pixel column number (in absolute coords) into azimuth angle
        
        Note
        ----
        - See also :func:`az_to_col` for the inverse operation
        - Not super efficient, just convenience function which should not\
            be used if performance is required
        
        Parameters
        ----------
        colnum : int
            pixel column number (left column corresponds to 0)
        
        Returns
        -------
        float
            corresponding azimuth angle
        """
        return self.all_azimuths_camfov()[colnum]

    def az_to_col(self, azim):
        """Convert azimuth into pixel number 
        
        Note
        ----
        The pixel number is calculated relative to the leftmost column of the
        image
        
        Parameters
        ----------
        azim : float
            azimuth angle which is supposed to be converted into column 
            number
        
        Returns
        -------
        int
            column number
            
        Raises
        ------
        IndexError
            if input azimuth is not within camera FOV
        """
        azs = self.all_azimuths_camfov()
        if azim < azs[0] or azim > azs[-1]:
            raise IndexError("Input azimuth is out of camera FOV")
        return argmin(abs(azs-azim))
        
        
# =============================================================================
#     
#     def all_azimuths_camfov(self):
#         """Returns array containing azimuth angles for all pixel columns"""
#         tot_num = self.cam["pixnum_x"]
#         idx_cfov = tot_num / 2.0
#         az0 = self.cam["azim"] - self.del_az(0, idx_cfov)
#         del_az = self.del_az(0, 1)
#         az_angles = zeros(tot_num)
#         for k in range(tot_num):
#             az_angles[k] = az0 + k * del_az
#         return az_angles          
# =============================================================================
        
    """
    Magic methods (overloading)
    """
    def __str__(self):
        """String representation of this object"""
        s = "pyplis MeasGeometry object\n##################################\n"
        s += "\nCamera specifications\n-------------------\n"
        for k, v in self.cam.iteritems():
            s += "%s: %s\n" %(k, v)
        s += "\nSource specifications\n-------------------\n"
        for k, v in self.source.iteritems():
            s += "%s: %s\n" %(k, v)
        s += "\nWind specifications\n-------------------\n"
        for k, v in self.wind.iteritems():
            s += "%s: %s\n" %(k, v)
        return s
            
    def __call__(self, item):
        """Return class attribute with a specific name
        
        :param item: name of attribute
        """
        for key, val in self.__dict__.iteritems():
            try:
                if val.has_key(item):
                    return val[item]
            except:
                pass