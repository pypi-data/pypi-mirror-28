#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classes for binning sky coordinates

Currently there are two fully functional Bins classes:
- SkyBins provides rectangular bins in (RA, Dec)
- HealpixBins provides binning based on HEALPix (requires healpy)

To make a custom binner, use the BaseBins class as parent and add methods 
'hist' (counts the hits per bin) and  'boundary' (provides boundary of bin
to draw the polygon) 
"""

import warnings
import numpy as np
from copy import copy

from astropy.utils.console import ProgressBar

from ...__init__ import BaseObject
#import astrobject.astrobject import baseobject as b
from .skyplot import rot_xz_sph
from ..tools import kwargs_extract,kwargs_update

try:
    import healpy as hp
    HEALPY_IMPORTED = True
except ImportError:
    HEALPY_IMPORTED = False

_d2r = np.pi / 180 

__all__ = ["SkyBins","HealpixBins","SurveyFieldBins","SurveyField"]

class BaseBins( BaseObject ):
    """
    Basic sky binning class
    Currently only defines the methods to split bins that cross RA = 180 deg
    """
    def fix_edges(self, ra_bd, edge):
        """
        Make sure that there is no mix between RA = -180 and 180
        Assumes that the sign of the median has the required sign
        """
        ra_med = np.median(ra_bd)
        if ra_med < 0:
            ra_bd[np.abs(ra_bd) > 180 - edge] = -180 + edge            
        else:                    
            ra_bd[np.abs(ra_bd) > 180 - edge] = 180 - edge

        return ra_bd

    def check_crossing(self, ra, dec, max_stepsize):
        """
        check whether bin boundary crosses the 180 degree line
        If so split patch in two
        """
        ra_bd = np.concatenate((ra, [ra[0]]))
        dec_bd = np.concatenate((dec, [dec[0]]))
        
        cr = np.where((np.abs(ra_bd[1:] - ra_bd[:-1]) > 180) &
                      ((180 - np.abs(ra_bd[1:]) < max_stepsize) |
                       (180 - np.abs(ra_bd[:-1]) < max_stepsize)))

        true_cr = []
        for cross in cr[0]:
            if np.abs(dec_bd[cross]) < 90 and np.abs(dec_bd[cross + 1]) < 90:
                true_cr.append(cross)

        if len(true_cr) > 0:
            return True
        return False

    def split_bin(self, ra_bd, dec_bd, max_stepsize, edge):
        """
        """
        ra_bd = self.fix_edges(ra_bd, edge)

        out = []
        if self.check_crossing(ra_bd, dec_bd, max_stepsize):
            ra_bd1 = ra_bd.copy()
            ra_bd2 = ra_bd.copy()

            # This assumes that the bins do not cover more than 90 deg in RA
            ra_bd1[ra_bd1 > 90] = -180 + edge
            ra_bd2[ra_bd2 < -90] = 180 - edge
           
            for r in [ra_bd1, ra_bd2]:
                # Only draw if really on two sides and not just because of 
                # non-matching sign of 180
                if np.any(np.abs(r) < 180 - edge):
                    out.append((r, dec_bd))
        else:
            out.append((ra_bd, dec_bd))

        return out

    def imshow(self, values, ax=None, savefile=None, show=True, 
               cblabel=None, **kwargs):
        """
        Plot values as pixels in the defined grid
        [Currently copy of TransientGenerator.hist_skycoverage; this method is 
        to take over most of the plotting of the former]
        """
        import matplotlib.pyplot as mpl
        from ..mpladdon import figout, skyhist
        from .skyplot import ax_skyplot
        self._plot = {}

        if ax is None:
            ax_default = dict(fig=None, figsize=(12, 6),
                              rect=[0.1, 0.1, 0.8, 0.8],
                              projection='mollweide',
                              xlabelpad=None,
                              xlabelmode='hist')
            ax_kw, kwargs = kwargs_extract(ax_default, **kwargs)
            fig, ax = ax_skyplot(**ax_kw)
        elif ("MollweideTransform" not in dir(ax) and
              "HammerTransform" not in dir(ax)):
            raise TypeError("The given 'ax' most likely is not a matplotlib axis "+\
                        "with Mollweide or Hammer projection. Transform "+\
                        "function not found.")
        else:
            fig = ax.fig

        collec, cb = ax.skyhist(values=values, cblabel=cblabel, bins=self, 
                                **kwargs)
        cb.set_label(cblabel, fontsize="x-large") 

        # ------------------- #
        # -- Save the data -- #
        self._plot["figure"] = fig
        self._plot["ax"]     = ax
        self._plot["collection"] = collec
        self._plot["cbar"] = cb

        fig.figout(savefile=savefile,show=show)
        return self._plot 

class SkyBins( BaseBins ):
    """
    Object to collect all information for rectangular binning.
    
    # Currently requires that bins do not cross the RA = 180 deg line
    # to work properly. (No warnings issued). Will fix this later.
    """
    PROPERTIES         = ["ra_min", "ra_max", "dec_min", "dec_max",
                          "max_stepsize"]
    SIDE_PROPERTIES    = []
    DERIVED_PROPERTIES = ["nbins"]

    def __init__(self, ra_range=(-180, 180), dec_range=(-90, 90), 
                 ra_nbins=12, dec_nbins=6, dec_sin=True, empty=False,
                 max_stepsize=5):
        """
        """
        self.__build__()
        if empty:
            return
        self.create(ra_range=ra_range, dec_range=dec_range, 
                    ra_nbins=ra_nbins, dec_nbins=dec_nbins,dec_sin=dec_sin,
                    max_stepsize=max_stepsize)
        

    def create(self, ra_range=(-180, 180), dec_range=(-90, 90), 
               ra_nbins=18, dec_nbins=10, dec_sin=True, max_stepsize=5):
        """
        """
        ra_base = np.linspace(ra_range[0], ra_range[1], ra_nbins+1)
        if dec_sin:
            dec_base = np.arcsin(np.linspace(np.sin(dec_range[0] * _d2r), 
                                             np.sin(dec_range[1] * _d2r), 
                                             dec_nbins+1)) / _d2r
        else:
            dec_base = np.linspace(dec_range[0], dec_range[1], dec_nbins+1)

        ra_min, dec_min = np.meshgrid(ra_base[:-1], dec_base[:-1])
        ra_max, dec_max = np.meshgrid(ra_base[1:], dec_base[1:])

        self._properties["ra_min"] = ra_min.flatten() 
        self._properties["ra_max"] = ra_max.flatten() 
        self._properties["dec_min"] = dec_min.flatten() 
        self._properties["dec_max"] = dec_max.flatten() 
                         
        self._properties["max_stepsize"] = max_stepsize
        #self.__update__()

    # =========== #
    # = Binning = #
    # =========== #
    def coord2bin(self, ra, dec):
        """
        """
        k = np.where((ra > self.ra_min) &
                     (ra <= self.ra_max) &
                     (dec > self.dec_min) &
                     (dec <= self.dec_max))[0]

        if len(k) == 0:
            return np.asarray([np.NaN])
        else:
            return k

    def hist(self, ra, dec, verbose=True):
        """
        Return the counts per bin for a list a coordinates.
        If verbose, it will issue warning the number of coordinates outside the bins
        and notify the user if coordinates where in multiple bins.
        """
        outside = 0
        binned = np.zeros(self.nbins)
        
        for r, d in zip(ra, dec):
            k = self.coord2bin(r, d)
            if np.isnan(k[0]):
                outside += 1
                continue
            elif len(k) > 1 and verbose:
                warnings.warn("Some bins appear to be overlapping.")
            binned[k] += 1

        if outside > 0 and verbose:
            warnings.warn("%i points lay outside the binned area.")

        return binned
        
    # ========================== #
    # = Utilities for plotting = #
    # ========================== #
    def boundary(self, k, steps=None, max_stepsize=None, edge=1e-6):
        """
        Return boundary of a bin; used for drawing polygons.
        If steps is None, max_stepsize is used to automatically determine 
        the appropriate step size.
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize
        lkwargs = dict(steps=steps, max_stepsize=max_stepsize)
        
        # Start in top left and work clockwise 
        ra1, dec1 = self._draw_line(self.ra_min[k], self.dec_max[k], 
                                    self.ra_max[k], self.dec_max[k], **lkwargs)
        ra2, dec2 = self._draw_line(self.ra_max[k], self.dec_max[k], 
                                    self.ra_max[k], self.dec_min[k], **lkwargs)
        ra3, dec3 = self._draw_line(self.ra_max[k], self.dec_min[k], 
                                    self.ra_min[k], self.dec_min[k], **lkwargs)
        ra4, dec4 = self._draw_line(self.ra_min[k], self.dec_min[k], 
                                    self.ra_min[k], self.dec_max[k], **lkwargs)
        
        ra = np.concatenate([ra1, ra2[1:], ra3[1:], ra4[1:-1]])
        dec = np.concatenate([dec1, dec2[1:], dec3[1:], dec4[1:-1]])
        
        return self.split_bin(ra, dec, max_stepsize, edge) 
        
    def _draw_line(self, ra1, dec1, ra2, dec2, steps=None, 
                   max_stepsize=None):
        """
        Return 'line' between (ra1, dec1) and (ra2, dec2).
        If steps is None, max_stepsize is used to automatically determine 
        the appropriate step size.
        Note: This treats coordinates as Euclidean in (ra, dec) space.
        Therefore it only works for lines of constant ra or dec. 
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize
        
        if ra1 == ra2:
            if steps is None:
                steps = self._determine_steps(dec1, dec2, 
                                              max_stepsize=max_stepsize)
            ra = ra1 * np.ones(steps)
            dec = np.linspace(dec1, dec2, steps)
        elif dec1 == dec2:
            if steps is None:
                steps = self._determine_steps(ra1, ra2, 
                                              max_stepsize=max_stepsize)
            ra = np.linspace(ra1, ra2, steps)
            dec = dec1 * np.ones(steps)
        else:
            raise ValueError("Either ra1 and ra2 or dec1 and dec2 must be the same.")
        
        return ra, dec

    def _determine_steps(self, x1, x2, max_stepsize=None):
        """
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        return np.ceil(np.abs(float(x2 - x1)) / max_stepsize) + 1

    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def ra_min(self):
        """list of minimum ra of each bin"""
        return self._properties["ra_min"]

    @property
    def ra_max(self):
        """list of maximum ra of each bin"""
        return self._properties["ra_max"]

    @property
    def dec_min(self):
        """list of minimum dec of each bin"""
        return self._properties["dec_min"]

    @property
    def dec_max(self):
        """list of maximum dec of each bin"""
        return self._properties["dec_max"]

    @property
    def max_stepsize(self):
        """maximum stepsize for boundary in degrees"""
        return self._properties["max_stepsize"]


    # --------------------
    # - Derived Properties
    @property
    def nbins(self):
        """number of bins"""
        return len(self._properties["ra_min"])
    


class HealpixBins( BaseBins ):
    """
    HEALPix Binner
    """
    PROPERTIES         = ["nside", "nest", "max_stepsize"]
    SIDE_PROPERTIES    = []
    DERIVED_PROPERTIES = ["nbins"] 

    def __init__(self, nside=8, nest=True, max_stepsize=5, empty=False):
        """
        """
        self.__build__()
        if empty:
            return
        self.create(nside=nside, nest=nest, max_stepsize=max_stepsize)

    def create(self, nside=8, nest=True, max_stepsize=5):
        """
        """
        if not HEALPY_IMPORTED:
            raise ValueError("HealpixBins requires the healpy package.")

        self._properties["nside"] = nside
        self._properties["nest"] = nest
                         
        self._properties["max_stepsize"] = max_stepsize
        #self.__update__()

    # =========== #
    # = Binning = #
    # =========== #
    def hist(self, ra, dec):
        """
        Return the counts per bin for a list a coordinates.
        """
        pixels = hp.ang2pix(self.nside,(90 - dec) * _d2r, ra * _d2r, 
                            nest=self.nest)
        binned = np.histogram(pixels, bins=range(hp.nside2npix(self.nside) + 1))
        
        return binned[0]

    # ========================== #
    # = Utilities for plotting = #
    # ========================== #
    def boundary(self, k, steps=None, max_stepsize=None, edge=1e-6):
        """
        Return boundary of a bin; used for drawing polygons.
        If steps is None, max_stepsize is used to automatically determine
        the appropriate step size.
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        if steps is None:
            steps = self._determine_steps(max_stepsize=max_stepsize)

        bd = hp.boundaries(self.nside, k, step=steps, nest=self.nest)
        dec_raw, ra_raw = hp.vec2ang(np.transpose(bd))

        ra = ((ra_raw / _d2r + 180) % 360) - 180
        dec = 90 - dec_raw / _d2r

        return self.split_bin(ra, dec, max_stepsize, edge) 

    def _determine_steps(self, max_stepsize=None):
        """
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        return np.ceil(hp.nside2resol(self.nside) / _d2r / max_stepsize) + 1

    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def nside(self):
        """HEALPix NSIDE parameter"""
        return self._properties["nside"]

    @property
    def nest(self):
        """HEALPix NESTED parameter"""
        return self._properties["nest"]

    @property
    def max_stepsize(self):
        """maximum stepsize for boundary in degrees"""
        return self._properties["max_stepsize"]

    # --------------------
    # - Derived Properties
    @property
    def nbins(self):
        """number of bins"""
        return hp.nside2npix(self._properties["nside"])


class SurveyFieldBins( BaseBins ):
    """
    Binner for SurveyField objects
    """
    PROPERTIES         = ["ra", "dec", "width", "height", "max_stepsize",
                          "field_id"]
    SIDE_PROPERTIES    = []
    DERIVED_PROPERTIES = ["nbins", "fields", "field_id_index"] 

    def __init__(self, ra, dec, width=6.86, height=6.86, max_stepsize=5, 
                 field_id=None, empty=False):
        """
        """
        self.__build__()
        if empty:
            return
        self.create(ra, dec, width=width, height=height, 
                    max_stepsize=max_stepsize, field_id=field_id)

    # ---------------------- #
    # - Get Method         - #
    # ---------------------- #
    def __getitem__(self, k):
        """
        """
        return self.fields[k]
        
    def create(self, ra, dec, width=6.86, height=6.86, max_stepsize=5,
               field_id=None):
        """
        """
        self._properties["ra"] = np.array(ra)
        self._properties["dec"] = np.array(dec)
        self._properties["width"] = float(width)
        self._properties["height"] = float(height)

        if field_id is None:
            self._properties["field_id"] = range(len(ra))
        else:
            self._properties["field_id"] = np.array(field_id)
                         
        self._properties["max_stepsize"] = max_stepsize

        #self.__update__()

    # =========== #
    # = Binning = #
    # =========== #
    def hist(self, ra, dec):
        """
        Return the counts per bin for a list a coordinates.
        """
        return np.array([np.sum(f.coord_in_field(ra, dec)) 
                         for f in self.fields])

    def coord2field(self, ra, dec, progress_bar=False, notebook=False):
        """
        Return the lists of fields in which a list of coordinates fall.
        Keep in mind that the fields will likely overlap.
        """
        bo = []
        gen = self.fields.values()

        if progress_bar:
            print "Determining field IDs for all objects"
            gen = ProgressBar(gen, ipython_widget=notebook)

        for f in gen:
            bo.append(f.coord_in_field(ra, dec))

        # Handle the single coordinate case first
        if type(bo[0]) is np.bool_:
            return self.field_id[np.where(np.array(bo))[0]]
        
        bo = np.array(bo)
        return [self.field_id[np.where(bo[:,k])[0]]
                for k in xrange(bo.shape[1])]

    # ========================== #
    # = Utilities for plotting = #
    # ========================== #
    def boundary(self, k, steps=None, max_stepsize=None, edge=1e-6):
        """
        Return boundary of a bin; used for drawing polygons.
        If steps is None, max_stepsize is used to automatically determine
        the appropriate step size.
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        ra, dec = self.fields[k].boundary(steps, max_stepsize, edge)

        return self.split_bin(ra, dec, max_stepsize, edge) 

    def _determine_steps(self, max_stepsize=None):
        """
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        return np.ceil(hp.nside2resol(self.nside) / _d2r / max_stepsize) + 1

    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def ra(self):
        """RA of field center"""
        return self._properties["ra"]

    @property
    def dec(self):
        """Dec of field center"""
        return self._properties["dec"]

    @property
    def width(self):
        """field width"""
        return self._properties["width"]

    @property
    def height(self):
        """field height"""
        return self._properties["height"]

    @property
    def field_id(self):
        """field height"""
        return self._properties["field_id"]
        
    @property
    def max_stepsize(self):
        """maximum stepsize for boundary in degrees"""
        return self._properties["max_stepsize"]

    # --------------------
    # - Derived Properties
    @property
    def nbins(self):
        """number of bins"""
        return len(self._properties["ra"])

    @property
    def fields(self):
        """dictionary of survey fields"""
        return {i: SurveyField(r, d, self.width, self.height, self.max_stepsize) 
                for i, r, d in zip(self.field_id, self.ra, self.dec)}

    @property
    def field_id_index(self):
        """lookup array which list index corresponds to field_id"""
        out = np.empty(self.field_id.max()+1, dtype=int)
        out[:] = -999999999
        out[self.field_id] = range(len(self.field_id))

        return out
        
class SurveyField( BaseObject ):
    """
    SurveyField objects
    """
    PROPERTIES         = ["ra", "dec", "width", "height"]
    SIDE_PROPERTIES    = []
    DERIVED_PROPERTIES = [] 

    def __init__(self, ra, dec, width=7., height=7., max_stepsize=5, 
                 empty=False):
        """
        """
        self.__build__()
        if empty:
            return
        self.create(ra, dec, width=width, height=height, 
                    max_stepsize=max_stepsize)

    def create(self, ra, dec, width=7., height=7., max_stepsize=5):
        """
        """
        self._properties["ra"] = ra
        self._properties["dec"] = dec
        self._properties["width"] = float(width)
        self._properties["height"] = float(height)
                         
        self._properties["max_stepsize"] = max_stepsize

        #self.__update__()

    # =========== #
    # = Binning = #
    # =========== #
    def coord_in_field(self, ra, dec):
        """
        Check whether coordinates are in the field
        Returns bool if (ra, dec) floats, np.ndarray of bools if (ra, dec) 
        lists or np.ndarrays

        TODO:
        Test various cases of iterables that may break the method
        """
        ra = copy(ra)
        dec = copy(dec)

        single_val = False
        if type(ra) is list:
            ra = np.array(ra)
        elif type(ra) is not np.ndarray:
            # Assume it is a float
            ra = np.array([ra])
            single_val = True

        if type(dec) is list:
            dec = np.array(dec)
        elif type(dec) is not np.ndarray:
            # Assume it is a float
            dec = np.array([dec])
            single_val = True

        if len(ra) != len(dec):
            raise ValueError('ra and dec must be of same length')

        ra -= self.ra
        ra1, dec1 = rot_xz_sph(ra, dec, -self.dec)
        
        out = np.ones(ra1.shape, dtype=bool)
        out[dec1 > self.height/2.] = False
        out[dec1 < -self.height/2.] = False
        out[ra1*np.cos(dec1*_d2r) > self.width/2.] = False
        out[ra1*np.cos(dec1*_d2r) < -self.width/2.] = False
        
        if single_val:
            return out[0]
        return out

    # ========================== #
    # = Utilities for plotting = #
    # ========================== #
    def boundary(self, steps=None, max_stepsize=None, edge=1e-6):
        """
        Return boundary of the field; used for drawing polygons.
        If steps is None, max_stepsize is used to automatically determine
        the appropriate step size.
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        if steps is None:
            steps = self._determine_steps(max_stepsize=max_stepsize)

        dec1 = np.ones(steps) * (self.dec + self.height/2)
        ra1 = self.ra + (np.linspace(-self.width/2, self.width/2, steps)
                         / np.cos((self.dec + self.height/2)*_d2r))
        
        dec2 = np.linspace(self.dec + self.height/2, self.dec - self.height/2, steps)
        ra2 = self.ra + self.width/2/np.cos(dec2*_d2r)

        dec3 = np.ones(steps) * (self.dec - self.height/2)
        ra3 = self.ra + (np.linspace(self.width/2, -self.width/2, steps)
                         / np.cos((self.dec - self.height/2)*_d2r))
    
        dec4 = np.linspace(self.dec - self.height/2, self.dec + self.height/2, steps)
        ra4 = self.ra - self.width/2/np.cos(dec4*_d2r)

        ra = ((np.concatenate((ra1, ra2, ra3, ra4)) + 180) % 360 ) - 180
        dec = np.concatenate((dec1, dec2, dec3, dec4))

        return ra, dec
        
    def _determine_steps(self, max_stepsize=None):
        """
        """
        if max_stepsize is None:
            max_stepsize = self.max_stepsize

        return np.ceil(max(self.height/max_stepsize, 
                           self.width/max_stepsize)) + 1

    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def ra(self):
        """RA of field center"""
        return self._properties["ra"]

    @property
    def dec(self):
        """Dec of field center"""
        return self._properties["dec"]

    @property
    def width(self):
        """field width"""
        return self._properties["width"]

    @property
    def height(self):
        """field height"""
        return self._properties["height"]

    @property
    def max_stepsize(self):
        """maximum stepsize for boundary in degrees"""
        return self._properties["max_stepsize"]

    # # --------------------
    # # - Derived Properties
    # @property
    # def nbins(self):
    #     """number of bins"""
    #     return hp.nside2npix(self._properties["nside"])

