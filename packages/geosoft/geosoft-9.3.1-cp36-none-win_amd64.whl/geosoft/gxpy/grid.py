"""
Geosoft grids and image handling, including all
`supported file formats <https://geosoftgxdev.atlassian.net/wiki/display/GXDEV92/Grid+File+Name+Decorations>`_

:Classes:

    ============= ====================================================
    :class:`Grid` grid, which can be in memory or created from a file _
    ============= ====================================================

.. seealso:: :class:`geosoft.gxapi.GXIMG`, :class:`geosoft.gxapi.GXIMU`

.. note::

    Regression tests provide usage examples:     
    `Tests <https://github.com/GeosoftInc/gxpy/blob/master/geosoft/gxpy/tests/test_grid.py>`_
    
"""
import os
import numpy as np
import math

import geosoft
import geosoft.gxapi as gxapi
from . import gx as gx
from . import coordinate_system as gxcs
from . import vv as gxvv
from . import utility as gxu
from . import agg as gxagg
from . import geometry as gxgm
from . import map as gxmap

__version__ = geosoft.__version__


def _t(s):
    return geosoft.gxpy.system.translate(s)


class GridException(Exception):
    """
    Exceptions from :mod:`geosoft.gxpy.grid`.

    .. versionadded:: 9.1
    """
    pass


def name_parts(name):
    """
    Return folder, undecorated file name + ext, file root, ext, decorations.

    If extension is not specified, ".grd" assumed

    For example:

    .. code::

        >>> import geosoft.gxpy.grid as gxgrd
        >>> namep = gxgrd.name_parts("f:/someFolder/name.grd(GRD;TYPE=SHORT)")
        >>> print(namep)
        ('f:/someFolder/','name.grd','name','.grd','(GRD;TYPE=SHORT)')

    .. versionadded:: 9.1
    """

    path = os.path.abspath(name)
    fn = os.path.dirname(path)
    root, ext = os.path.splitext(os.path.basename(path))

    if '(' in ext:
        ext, dec = ext.split('(')
        if ')' in dec:
            dec = dec.split(')')[0]
    else:
        dec = ''

    if not ext:
        if (not dec) or (dec[:3].upper() == 'GRD'):
            ext = '.grd.'
    name = root + ext

    return fn, name, root, ext, dec


def decorate_name(name, decorations=''):
    """
    Properly decorate a grid name.

    :param name:        file name
    :param decorations: file decorations, semicolon delimited
    :returns:           decorated file name

    .. versionadded:: 9.1
    """

    root, ext = os.path.splitext(name)
    dec = decorations.strip()
    if dec:
        d = decorations.lstrip('(')
        end = d.rfind(')')
        if end != -1:
            d = d[:end]
        ext = ext.split('(')[0]
        return '{}{}({})'.format(root, ext, d)

    else:
        if ext.lower() == '.grd':
            return '{}{}(GRD)'.format(root, ext)
        else:
            return name


def delete_files(file_name):
    """
    Delete all files associates with this grid name.

    :param file_name: name of the grid file

    .. versionadded:: 9.2
    """

    if file_name is not None:

        fn = name_parts(file_name)
        file_name = os.path.join(fn[0], fn[1])
        ext = fn[3]
        gxu.delete_file(file_name)
        gxu.delete_file(file_name + '.gi')
        gxu.delete_file(file_name + '.xml')

        # remove shaded files associated with this grid
        file_s = os.path.join(fn[0], fn[1].replace('.', '_')) + '_s.grd'
        gxu.delete_file(file_s)
        gxu.delete_file(file_s + '.gi')
        gxu.delete_file(file_s + '.xml')

        # hgd files
        if ext == '.hgd':
            for i in range(16):
                gxu.delete_file(file_name + str(i))


def _transform_color_int_to_rgba(np_values):
    np_values[np_values == gxapi.iDUMMY] = 0
    a = (np.right_shift(np_values, 24) & 0xFF).astype(np.uint8)
    b = (np.right_shift(np_values, 16) & 0xFF).astype(np.uint8)
    g = (np.right_shift(np_values, 8) & 0xFF).astype(np.uint8)
    r = (np_values & 0xFF).astype(np.uint8)
    # the values for color grids actually do not contain alphas but just
    # 0 or 1 to indicate if the color is valid or not
    a[a > 0] = 255
    return np.array([r, g, b, a]).transpose()


# constants
FILE_READ = 0          #:
FILE_READWRITE = 1     #: file exists, but can change properties
FILE_NEW = 2           #:


class Grid(gxgm.Geometry):
    """
    Grid and image class.

    :Constructors:

        ======================= ============================================
        :meth:`open`            open an existing grid/image
        :meth:`new`             create a new grid/image
        :meth:`copy`            create a copy
        :meth:`index_window`    create a windowed grid based on grid indexes
        :meth:`from_data_array` create a new grid from a 2d data array
        ======================= ============================================

    A grid instance supports iteration that yields (x, y, z, grid_value) by points along rows.
    For example, the following prints the x, y, z, grid_value of every non-dummy point in a grid:

    .. code::

        import geosoft.gxpy.grid as gxgrd

        with gxgrd.Grid.open('some.grd') ad g:
            for x, y, z, v in g:
                if v is not None:
                    print(x, y, z, v)

    Specific grid cell values can be indexed (null grid values are None):

    .. code::

        import geosoft.gxpy.grid as gxgrd

        with gxgrd.Grid.open('some.grd') as g:
            for ix in range(g.nx):
                for iy in range(g.ny):
                    x, y, z, v = g[ix, iy]
                    if v is not None:
                        print(x, y, z, v)

    .. versionadded:: 9.1

    .. versionchanged:: 9.2.1 added iterator support
    """

    _delete_files = False
    _file_name = None

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.__del__()

    def __del__(self):
        if hasattr(self, '_close'):
            self._close()

    def _close(self, pop=True):

        if hasattr(self, '_open'):
            if self._open:

                if self._delete_files:

                    self._img = None
                    delete_files(self._file_name)
                    self._metadata_changed = False

                elif self._hgd:
                    # an HGD memory grid was made, save it to an HGD file
                    gxapi.GXHGD.h_create_img(self._img, decorate_name(self._file_name, 'HGD'))

                if self._metadata_changed:
                    with open(self._file_name + '.xml', 'w+') as f:
                        f.write(gxu.xml_from_dict(self._metadata))
                    gxapi.GXIMG.sync(self._file_name)

                if pop:
                    gx.pop_resource(self._open)
                self._open = None
                self._img = None
                self._buffer_np = None
                self._buffer_x = None
                self._buffer_y = None
                self._cs = None
                self._gxpg = None

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __str__(self):
        if self._file_name is None:
            return '__memory__'
        else:
            return self.file_name_decorated

    def __init__(self, file_name=None, dtype=None, mode=None, kx=1, dim=None, overwrite=False, **kwargs):

        self._delete_files = False
        self._readonly = False
        self._decoration = ''

        # When working with very large grids (gigabyte+), the
        # file system cannot always keep up with closing/caching and re-opening the
        # grid. Though this is actually a system problem, we deal with this problem by attempting
        # to open a grid three times before raising an error.

        # rebuild a clean file name
        self._hgd = False
        if (file_name is None) or (len(file_name.strip()) == 0):
            self._file_name = None
        else:
            path, file_name, root, ext, self._decoration = name_parts(file_name)
            self._file_name = os.path.join(path, file_name)

            if mode == FILE_NEW:
                # special case - HGD file, must work with a memory grid, save to HGD at end
                if ext.lower() == '.hgd':
                    self._hgd = True

        if 'name' not in kwargs:
            if file_name:
                kwargs['name'] = os.path.splitext(file_name)[0]
            else:
                kwargs['name'] = '_grid_'
        super().__init__(**kwargs)

        self._metadata = None
        self._metadata_changed = False
        self._metadata_root = ''
        self._img = None
        self._buffered_row = None
        self._buffer_np = None
        self._buffered_xy = None
        self._buffer_x = None
        self._buffer_y = None
        self._cs = None
        self._gxpg = None

        gxtype = gxu.gx_dtype(dtype)
        if self._file_name is None:
            self._img = gxapi.GXIMG.create(gxtype, kx, dim[0], dim[1])

        elif mode == FILE_NEW:
            if not overwrite:
                if os.path.isfile(self.file_name):
                    raise GridException(_t('Cannot overwrite existing grid {}'.format(self.file_name)))
            if self._hgd:
                # for HGD grids, make a memory grid, which will be saved to an HGD on closing
                self._img = gxapi.GXIMG.create(gxtype, kx, dim[0], dim[1])
            else:
                self._img = gxapi.GXIMG.create_new_file(gxtype,
                                                        kx, dim[0], dim[1],
                                                        self.file_name_decorated)

        elif mode == FILE_READ:
            self._img = gxapi.GXIMG.create_file(gxtype,
                                                self.file_name_decorated,
                                                gxapi.IMG_FILE_READONLY)
            self._readonly = True

        else:
            self._img = gxapi.GXIMG.create_file(gxtype,
                                                self.file_name_decorated,
                                                gxapi.IMG_FILE_READORWRITE)

        self._next = 0
        self._next_row = 0
        self._next_col = 0
        self._gxtype = self._img.e_type()
        self._dtype = gxu.dtype_gx(self._gxtype)
        self._dummy = gxu.gx_dummy(self._dtype)
        self._is_int = gxu.is_int(self._gxtype)
        self._cos_rot = 1.0
        self._sin_rot = 0.0
        self.rot = self.rot

        self._open = gx.track_resource(self.__class__.__name__, self._file_name)

    @classmethod
    def open(cls, file_name, dtype=None, mode=None):
        """
        Open an existing grid file.

        :param file_name:   name of the grid file (see `supported file formats <https://geosoftgxdev.atlassian.net/wiki/display/GXDEV92/Grid+File+Name+Decorations>`_)
        :param dtype:       numpy data type, None for the grid native type.  If not the same as the native
                            type a memory grid is created in the new type.
        :param mode:        open mode:

            =================  ================================================
            FILE_READ          only read the file, properties cannot be changed
            FILE_READWRITE     grid stays the same, but properties may change
            =================  ================================================

        .. versionadded:: 9.1
        """

        if mode is None:
            mode = FILE_READ
        grd = cls(file_name, dtype=None, mode=mode)

        if (dtype is not None) and (grd.dtype != dtype):
            grdm = cls.copy(grd, dtype=dtype)
            grd.close()
            return grdm
        else:
            return grd

    @classmethod
    def new(cls, file_name=None, properties=None, overwrite=False):
        """
        Create a new grid file.

        :param file_name:   name of the grid file, None or '' for a memory grid. See
         `supported file formats <https://geosoftgxdev.atlassian.net/wiki/display/GXDEV92/Grid+File+Name+Decorations>`_)
        :param properties:  dictionary of grid properties, see :meth:`properties`
        :param overwrite:   True to overwrite existing file

        .. versionadded:: 9.1
        """

        if properties is None:
            raise GridException(_t("Missing properties dictionary."))

        # set basic grid properties
        dtype = properties.get('dtype', None)
        if dtype is None:
            dtype = np.float64
        nx = properties.get('nx', 0)
        ny = properties.get('ny', 0)
        if (nx <= 0) or (ny <= 0):
            raise GridException(_t('Grid dimension ({},{}) must be > 0').format(nx, ny))

        grd = cls(file_name, dtype=dtype, mode=FILE_NEW, dim=(nx, ny), overwrite=overwrite)
        grd.set_properties(properties)

        return grd

    def __iter__(self):
        return self

    def __next__(self):
        if self._next >= self.nx * self.ny:
            self._next = 0
            raise StopIteration
        else:
            v = self.__getitem__(self._next)
            self._next += 1
            return v

    def __getitem__(self, item):

        if isinstance(item, int):
            ix = item % self.nx
            iy = item // self.nx
        else:
            ix, iy = item

        x, y, z = self.xyz((ix, iy))

        if self._buffered_row != iy:
            self._buffered_row = iy
            self._buffer_np = self.read_row(self._buffered_row).np

        v = self._buffer_np[ix]
        if self._is_int:
            v = int(v)
            if v == gxapi.iDUMMY:
                v = None
        elif np.isnan(v):
            v = None
        else:
            v = float(v)
        return x, y, z, v

    def gxpg(self):
        """Get a `geosoft.gxapi.GXPG` instance for the grid."""
        if self._gxpg is None:
            self._gxpg = self._img.geth_pg()
        return self._gxpg

    def get_value(self, x, y):
        """
        Return a grid value at a point as a float.  For scalar data the point value will
        be interpolated between neighbors.  For color data the nearest value is returned
        as a color int.
        
        :param x: X location on the grid plane 
        :param y: Y location on the grid plane
        :returns: grid value, or None if outside of grid area
        
        """
        return gxu.dummy_none(self.gximg.get_z(x, y))

    @classmethod
    def copy(cls, grd, file_name=None, dtype=None, overwrite=False):
        """
        Create a new Grid instance as a copy of an existing grid.

        :param grd:         :class:`Grid` instance to save as a new grid, or a grid file name
        :param file_name:   name of the new grid (file with optional decorations), default is in memory
        :param dtype:       numpy data type, None to use type of the parent grid
        :param overwrite:   True to overwrite if the file exists, False to not overwrite.

        .. versionadded:: 9.2
        """

        if not isinstance(grd, Grid):
            grd = Grid.open(grd, mode=FILE_READ)
            close_grid = True
        else:
            close_grid = False

        p = grd.properties()
        if dtype:
            p['dtype'] = dtype

        if file_name is not None:
            path0, base_file0, root0, ext0, dec0 = name_parts(grd.file_name_decorated)
            path1, base_file1, root1, ext1, dec1 = name_parts(file_name)
            if not ext1:
                ext1 = ext0
            if (ext1 == ext0) and not dec1:
                dec1 = dec0
            file_name = decorate_name(os.path.join(path1, root1) + ext1, dec1)

        copy = Grid.new(file_name, p, overwrite=overwrite)
        grd._img.copy(copy._img)

        if close_grid:
            grd.close()

        return copy

    @classmethod
    def index_window(cls, grd, name=None, x0=0, y0=0, nx=None, ny=None, overwrite=False):
        """
        Create a windowed instance of a grid.
        
        :param grd:         :class:`Grid` instance
        :param name:        name for the windowed_grid, default is constructed from input grid
        :param x0:          integer index of the first X point
        :param y0:          integer index of the first Y point
        :param nx:          number of points in x
        :param ny:          number of points in y
        :param overwrite:   True to overwrite existing file, default is False

        .. versionadded:: 9.2
        """

        gnx = grd.nx
        gny = grd.ny
        if nx is None:
            nx = gnx - x0
        if ny is None:
            ny = gny - y0
        mx = x0 + nx
        my = y0 + ny
        if ((x0 >= gnx) or (y0 >= gny) or
                (x0 < 0) or (y0 < 0) or
                (nx <= 0) or (ny <= 0) or
                (mx > gnx) or (my > gny)):
            raise GridException(_t('Window x0,y0,mx,my({},{},{},{}) out of bounds ({},{})').
                                format(x0, y0, mx, my, gnx, gny))

        if name is None:
            path, file_name, root, ext, dec = name_parts(grd.file_name_decorated)
            name = '{}_({},{})({},{}){}'.format(root, x0, y0, nx, ny, ext)
            name = decorate_name(name, dec)
            overwrite = True

        # create new grid
        p = grd.properties()
        p['nx'] = nx
        p['ny'] = ny
        if grd.rot == 0.0:
            p['x0'] = grd.x0 + grd.dx * x0
            p['y0'] = grd.y0 + grd.dy * y0
        else:
            dx = grd.dx * x0
            dy = grd.dy * y0
            cos, sin = grd.rotation_cos_sine
            p['x0'] = grd.x0 - dx * cos - dy * sin
            p['y0'] = grd.y0 - dy * cos + dx * sin

        window_grid = cls.new(name, p, overwrite=overwrite)
        source_pager = grd.gxpg()
        window_pager = window_grid.gxpg()
        window_pager.copy_subset(source_pager, 0, 0, y0, x0, ny, nx)

        return window_grid

    @classmethod
    def from_data_array(cls, data, file_name, properties=None):
        """
        Create grid from a 2D numpy array.

        :param data:        2D numpy data array, ot a 2d list.  Must be 2D.
        :param file_name:   name of the file
        :param properties:  grid properties as a dictionary
        :returns:           :class:`Grid` instance

        .. versionadded:: 9.1
        """

        if type(data) is not np.ndarray:
            data = np.array(data)
        ny, nx = data.shape
        if properties is None:
            properties = {}
        properties['nx'] = nx
        properties['ny'] = ny
        properties['dtype'] = data.dtype
        grd = cls.new(file_name, properties=properties)
        grd.write_rows(data)
        return grd

    @property
    def rotation_cos_sine(self):
        """
        Returns grid rotation (cosine, sine).

        .. versionadded:: 9.3.1
        """
        return self._cos_rot, self._sin_rot

    def delete_files(self, delete=True):
        """
        Delete the files associated with this grid when deleting the grid object.
        Note that files are not deleted until all references to this object are
        deleted and garbage collection is performed.

        :param delete: set to False to reverse a previous delete request

        .. versionadded:: 9.1
        """
        self._delete_files = delete

    def close(self):
        """close the grid and release all instance resources."""
        self._close()

    @property
    def dummy_value(self):
        """ Return the grid data dummy value."""
        return self._dummy

    @property
    def gximg(self):
        """ The `geosoft.gxapi.GXIMG` instance handle."""
        return self._img

    def _init_metadata(self):
        if not self._metadata:
            self._metadata = gxu.geosoft_metadata(self._file_name)
        self._metadata_root = tuple(self._metadata.items())[0][0]

    @property
    def metadata(self):
        """
        Return the grid metadata as a dictionary.  Can be set, in which case
        the dictionary items passed will be added to, or replace existing metadata.
        
        .. seealso::
            `Geosoft metadata schema <https://geosoftgxdev.atlassian.net/wiki/display/GXDEV92/Geosoft+Metadata+Schema>`_     

        .. versionadded:: 9.2
        """
        self._init_metadata()
        return self._metadata[self._metadata_root]

    @metadata.setter
    def metadata(self, meta):
        self._init_metadata()
        self._metadata[self._metadata_root] = gxu.merge_dict(self._metadata[self._metadata_root], meta)
        self._metadata_changed = True

    @property
    def unit_of_measure(self):
        """
        Units of measurement (a string) for the grid data, can be set.
        
        .. versionadded:: 9.2
        """
        try:
            uom = self.metadata['geosoft']['dataset']['geo:unitofmeasurement']['#text']
        except (KeyError, TypeError):
            uom = ''
        return uom

    @unit_of_measure.setter
    def unit_of_measure(self, uom):
        self.metadata = {'geosoft': {'dataset': {'geo:unitofmeasurement': {'#text': str(uom)}}}}
        self.metadata = {'geosoft': {'dataset':
                             {'geo:unitofmeasurement':{'@xmlns:geo': 'http://www.geosoft.com/schema/geo'}}}}

    @property
    def dtype(self):
        """
        numpy data type for the grid

        .. versionadded:: 9.2
        """
        return self._dtype

    @property
    def gxtype(self):
        """
        Geosoft data type for the grid

        .. versionadded:: 9.2
        """
        return self._gxtype

    @property
    def is_int(self):
        """ returns True if base grid type is integer, which includes color integers"""
        return self._is_int

    @property
    def nx(self):
        """
        grid x dimension (number of columns)

        .. versionadded:: 9.2
        """
        return self._img.nx()

    @property
    def ny(self):
        """
        grid y dimension (number of rows)

        .. versionadded:: 9.2
        """
        return self._img.ny()

    @property
    def x0(self):
        """
        grid origin x location in the plane coordinate system

        .. versionadded:: 9.2
        """
        return self._img.query_double(gxapi.IMG_QUERY_rXO)

    @property
    def y0(self):
        """
        grid origin y location in the plane coordinate system

        .. versionadded:: 9.2
        """
        return self._img.query_double(gxapi.IMG_QUERY_rYO)

    @property
    def dx(self):
        """
        separation between grid points in the grid x direction

        .. versionadded:: 9.2
        """
        return self._img.query_double(gxapi.IMG_QUERY_rDX)

    @property
    def dy(self):
        """
        separation between grid points in the grid y direction

        .. versionadded:: 9.2
        """
        return self._img.query_double(gxapi.IMG_QUERY_rDY)

    @property
    def rot(self):
        """
        grid rotation angle, degrees azimuth
        
        Note that grid rotations in the gxapi GXIMG are degrees clockwise, which is the opposite of
        degree azimuth, used here.  All horizontal plane angles in the Python gxpy module are degrees
        azimuth for consistency.

        .. versionadded:: 9.2
        """
        return -self._img.query_double(gxapi.IMG_QUERY_rROT)

    @property
    def is_color(self):
        """ returns True if grid contains colors. is_int will also be True"""
        return bool(self._img.is_colour())

    @property
    def file_name(self):
        """
        grid file name without decorations

        .. versionadded:: 9.2
        """
        return self._file_name

    @property
    def file_name_decorated(self):
        """
        grid file name with decorations

        .. versionadded:: 9.2
        """
        return decorate_name(self.file_name, self._decoration)

    @property
    def name(self):
        """
        Grid name, usually the file name without path or extension.
        
        .. versionadded:: 9.2
        """
        basename = os.path.basename(self.file_name)
        return os.path.splitext(basename)[0]

    @property
    def gridtype(self):
        """
        grid type (ie. 'GRD' or 'HGD')

        .. versionadded:: 9.2
        """
        _, _, _, ext, dec = name_parts(self._file_name)
        if len(dec) > 0:
            return dec.split(';')[0]
        else:
            return ext[1:].upper()

    @property
    def decoration(self):
        """
        grid descriptive decoration

        .. versionadded:: 9.2
        """
        return self._decoration

    @property
    def coordinate_system(self):
        """
        grid coordinate system as a :class:`geosoft.gxpy.coordinate_system.Coordinate_system` instance.

        Can be set from any :class:`geosoft.gxpy.coordinate_system.Coordinate_system` constructor.

        .. versionadded:: 9.2

        .. versionchanged:: 9.3
            added ability to set directly
        """
        if self._cs is None:
            self._cs = gxcs.Coordinate_system()
            self._img.get_ipj(self._cs.gxipj)
        return self._cs

    @coordinate_system.setter
    def coordinate_system(self, cs):
        self._cs = gxcs.Coordinate_system(cs)
        self._img.set_ipj(self._cs.gxipj)

    def properties(self):
        """
        Get the grid properties dictionary

        :returns: dictionary of all grid properties

        .. versionadded:: 9.1
        """

        properties = {'nx': self.nx,
                      'ny': self.ny,
                      'x0': self.x0,
                      'y0': self.y0,
                      'dx': self.dx,
                      'dy': self.dy,
                      'rot': self.rot,
                      'is_color': self.is_color,
                      'dtype': self.dtype,
                      'file_name': self.file_name,
                      'gridtype': self.gridtype,
                      'decoration': self._decoration,
                      'coordinate_system': self.coordinate_system}

        return properties

    @x0.setter
    def x0(self, v):
        self._img.set_info(self.dx, self.dy, v, self.y0, -self.rot)

    @y0.setter
    def y0(self, v):
        self._img.set_info(self.dx, self.dy, self.x0, v, -self.rot)

    @dx.setter
    def dx(self, v):
        self._img.set_info(v, self.dy, self.x0, self.y0, -self.rot)

    @dy.setter
    def dy(self, v):
        self._img.set_info(self.dx, v, self.x0, self.y0, -self.rot)

    @rot.setter
    def rot(self, v):
        self._img.set_info(self.dx, self.dy, self.x0, self.y0, -v)
        self._cos_rot = math.cos(math.radians(v))
        self._sin_rot = math.sin(math.radians(v))

    def set_properties(self, properties):
        """
        Set grid properties from a properties dict.  Settable property keys are:

            ==================== ============================================
            'x0'                 grid X origin location (default 0.0)
            'y0'                 grid Y origin location (0.0)
            'dx'                 grid X point separation (1.0)
            'dy'                 grid Y point separation (1.0)
            'rot'                grid rotation angle in degrees azimuth (0.0)
            'coordinate_system'  coordinate system (unchanged)
            ==================== ============================================

        Not all keys need be passed, though typically one will get the properties from
        the grid and modify those that need to change and pass the properties back.

        :param properties: properties dictionary

        .. versionadded:: 9.1
        """

        if self._readonly:
            raise GridException(_t('{} opened as read-only, cannot set properties.').format(self.file_name_decorated))

        dx = properties.get('dx', 1.0)
        dy = properties.get('dy', dx)
        self._img.set_info(dx, dy,
                           properties.get('x0', 0.0),
                           properties.get('y0', 0.0),
                           -properties.get('rot', 0.0))
        self.rot = self.rot  # calculates cos and sin
        cs = properties.get('coordinate_system', None)
        if cs is not None:
            if not isinstance(cs, gxcs.Coordinate_system):
                cs = gxcs.Coordinate_system(cs)
            self._img.set_ipj(cs.gxipj)

    def write_rows(self, data, ix0=0, iy0=0, order=1):
        """
        Write data to a grid by rows.

        :param data:    array of data to write
        :param ix0:     grid X index of first point
        :param iy0:     grid Y index of first point, top index if writing rows top to bottom
        :param order:   1: bottom to top; -1: top to bottom

        .. versionadded:: 9.1
        """

        ny, nx = data.shape
        iy = iy0
        dtype = self._dtype
        for i in range(ny):
            self._img.write_y(iy, ix0, 0, gxvv.GXvv(data[i, :], dtype=dtype).gxvv)
            iy += order

    def read_row(self, row=None, start=0, length=0):
        """

        :param row:     row to read, if not specified the next row is read starting from row 0
        :param start:   the first point in the row, default is 0
        :param length:  number of points to read, the default is to the end of the row.
        :return:        :class:`geosoft.gxvv.GXvv` instance

        .. versionadded:: 9.1
        """

        if row is None:
            row = self._next_row
        self._next_row = row + 1

        if row >= self.ny:
            raise GridException(_t('Attempt to read row {} past the last row {}'.format(row, self.ny)))
        vv = gxvv.GXvv(dtype=self._dtype)
        self._img.read_y(row, start, length, vv.gxvv)

        return vv

    def read_column(self, column=None, start=0, length=0):
        """

        :param column:  column to read, if not specified the next column is read starting from column 0
        :param start:   the first point in the column, default is 0
        :param length:  number of points to read, the default is to the end of the col.
        :return:        :class:`geosoft.gxvv.GXvv` instance

        .. versionadded:: 9.1
        """

        if column is None:
            column = self._next_col
        if column >= self.nx:
            raise GridException(_t('Attempt to read column {} past the last column {}'.format(column, self.ny)))
        self._next_col = column + 1
        vv = gxvv.GXvv(dtype=self._dtype)
        self._img.read_x(column, start, length, vv.gxvv)

        return vv

    @staticmethod
    def name_parts(name):
        """
        .. deprecated:: 9.2 use gxpy.grid.name_parts()
        """
        return name_parts(name)

    @staticmethod
    def decorate_name(name, decorations=''):
        """
        .. deprecated:: 9.2 use gxpy.grid.name_parts()
        """
        return decorate_name(name, decorations)

    def indexWindow(self, name, x0=0, y0=0, nx=None, ny=None):
        """
        .. deprecated:: 9.2 gxpy.Grid.index_window()
        """
        return self.index_window(self, name, x0, y0, nx, ny, overwrite=True)

    def extent_2d(self):
        """
        Return the 2D extent of the grid on the grid plane
        :returns:(min_x, min_y, max_x, max_y)

        .. versionadded:: 9.2
        """
        width = (self.nx - 1) * self.dx
        height = (self.ny - 1) * self.dy
        xy0 = (self.x0, self.y0)
        xy1 = (self.x0 + width * self._cos_rot, self.y0 - width * self._sin_rot)
        xy2 = (xy1[0] + height * self._sin_rot, xy1[1] + height * self._cos_rot)
        xy3 = (self.x0 + height * self._sin_rot, self.y0 + height * self._cos_rot)

        return min(xy0[0], xy1[0], xy2[0], xy3[0]), \
               min(xy0[1], xy1[1], xy2[1], xy3[1]), \
               max(xy0[0], xy1[0], xy2[0], xy3[0]), \
               max(xy0[1], xy1[1], xy2[1], xy3[1])

    def extent_cell_2d(self):
        """
        Return the 2D cell extent of the grid on the grid plane
        :returns:(min_x, min_y, max_x, max_y)

        .. versionadded:: 9.3.1
        """

        def rotate(x, y):
            x -= self.x0
            y -= self.y0
            _x = x * self._cos_rot + y * self._sin_rot
            _y = -x * self._sin_rot + y * self._cos_rot
            return _x + self.x0, _y + self.y0

        x0 = self.x0 - self.dx / 2.
        x1 = x0 + self.nx * self.dx
        y0 = self.y0 - self.dy / 2.
        y1 = y0 + self.ny * self.dy
        if self.rot != 0.:
            xy0 = rotate(x0, y0)
            xy1 = rotate(x1, y0)
            xy2 = rotate(x1, y1)
            xy3 = rotate(x0, y1)
            min_x = min(xy0[0], xy1[0], xy2[0], xy3[0])
            min_y = min(xy0[1], xy1[1], xy2[1], xy3[1])
            max_x = max(xy0[0], xy1[0], xy2[0], xy3[0])
            max_y = max(xy0[1], xy1[1], xy2[1], xy3[1])
            return min_x, min_y, max_x, max_y
        else:
            return x0, y0, x1, y1

    def extent_3d(self):
        """
        Return the 3D extent of the grid in the base coordinate system.

        :returns: (min_x, min_y, min_z, max_x, max_y, max_z)

        .. versionadded:: 9.2
        """

        ex2d = self.extent_2d()
        cs = self.coordinate_system
        xyz0 = cs.xyz_from_oriented((ex2d[0], ex2d[1], 0.0))
        xyz1 = cs.xyz_from_oriented((ex2d[2], ex2d[1], 0.0))
        xyz2 = cs.xyz_from_oriented((ex2d[2], ex2d[3], 0.0))
        xyz3 = cs.xyz_from_oriented((ex2d[0], ex2d[3], 0.0))

        min_x = min(xyz0[0], xyz1[0], xyz2[0], xyz3[0])
        min_y = min(xyz0[1], xyz1[1], xyz2[1], xyz3[1])
        min_z = min(xyz0[2], xyz1[2], xyz2[2], xyz3[2])
        max_x = max(xyz0[0], xyz1[0], xyz2[0], xyz3[0])
        max_y = max(xyz0[1], xyz1[1], xyz2[1], xyz3[1])
        max_z = max(xyz0[2], xyz1[2], xyz2[2], xyz3[2])
        return min_x, min_y, min_z, max_x, max_y, max_z

    def extent_cell_3d(self):
        """
        Return the 3D cell extent of the grid in the base coordinate system.

        :returns: (min_x, min_y, min_z, max_x, max_y, max_z)

        .. versionadded:: 9.3.1
        """

        ex2d = self.extent_cell_2d()
        cs = self.coordinate_system
        xyz0 = cs.xyz_from_oriented((ex2d[0], ex2d[1], 0.0))
        xyz1 = cs.xyz_from_oriented((ex2d[2], ex2d[1], 0.0))
        xyz2 = cs.xyz_from_oriented((ex2d[2], ex2d[3], 0.0))
        xyz3 = cs.xyz_from_oriented((ex2d[0], ex2d[3], 0.0))

        min_x = min(xyz0[0], xyz1[0], xyz2[0], xyz3[0])
        min_y = min(xyz0[1], xyz1[1], xyz2[1], xyz3[1])
        min_z = min(xyz0[2], xyz1[2], xyz2[2], xyz3[2])
        max_x = max(xyz0[0], xyz1[0], xyz2[0], xyz3[0])
        max_y = max(xyz0[1], xyz1[1], xyz2[1], xyz3[1])
        max_z = max(xyz0[2], xyz1[2], xyz2[2], xyz3[2])
        return min_x, min_y, min_z, max_x, max_y, max_z

    @property
    def extent(self):
        """
        Grid cell extent as `geosoft.gxpy.geometry.Point2`.

        .. versionadded:: 9.3.1
        """
        return gxgm.Point2((self.extent_cell_3d()), coordinate_system=self.coordinate_system)

    def np(self):
        """
        Return a numpy array of grid values.

        :returns: numpy array shape (nx, ny) or (nx, ny, 4) containing RGBA bytes in case of color grids

        .. versionadded:: 9.3.1
        """

        nx = self.nx
        ny = self.ny
        if self.is_color:
            data = np.zeros((ny, nx, 4), np.dtype(np.uint8))
        else:
            data = np.zeros((ny, nx), dtype=self._dtype)
        if self.gximg.query_kx() == -1:
            for i in range(self.nx):
                column = self.read_column(i).np
                if self.is_color:
                    column = _transform_color_int_to_rgba(column)
                data[:, i] = column
        else:
            for i in range(self.ny):
                row = self.read_row(i).np
                if self.is_color:
                    row = _transform_color_int_to_rgba(row)
                data[i, :] = row

        return data

    def xyzv(self):
        """
        Return a numpy float array of (x, y, z, v) grid points.

        x, y, z) is the location of each grid point in 3D space and v is the grid value at that location.
        Dummies will be numpy.nan.

        :returns: numpy array shape (nx, ny, 4)

        .. versionadded:: 9.2
        """

        nx = self.nx
        ny = self.ny
        dx = self.dx
        dy = self.dy
        cs = self.coordinate_system
        xyzv = np.zeros((ny, nx, 4))
        xyzv[:, :, 0:2] = np.mgrid[0: (nx - 0.5) * dx: dx, 0: (ny - 0.5) * dy: dy].swapaxes(0, 2)

        if self.rot != 0.:
            x = xyzv[:, :, 0]
            cosx = x * self._cos_rot
            sinx = x * self._sin_rot
            y = xyzv[:, :, 1]
            cosy = y * self._cos_rot
            siny = y * self._sin_rot
            xyzv[:, :, 0] = cosx + siny
            xyzv[:, :, 1] = cosy - sinx

        xyzv += (self.x0, self.y0, 0, 0)

        if cs.is_oriented:
            xyzv[:, :, :3] = cs.xyz_from_oriented(xyzv[:, :, :3].reshape((-1, 3))).reshape((ny, nx, 3))

        if self.gximg.query_kx() == -1:
            for i in range(self.nx):
                xyzv[:, i, 3] = self.read_column(i).np
        else:
            for i in range(self.ny):
                xyzv[i, :, 3] = self.read_row(i).np

        return xyzv

    def xyz(self, item):
        """
        Returns the (x, y, z) location of an indexed point in the grid.

        :param item: tuple (ix, iy) grid point, or the point number counting by row
        :return: tuple (x, y, z) location

        .. versionadded:: 9.2.1
        """

        if isinstance(item, int):
            ix = item % self.nx
            iy = item // self.nx
        else:
            ix, iy = item

        if self._buffered_xy != iy:
            self._buffered_xy = iy
            self._buffer_x = np.arange(self.nx, dtype=np.float64)
            self._buffer_x *= self.dx
            self._buffer_y = np.zeros(self.nx, dtype=np.float64)
            self._buffer_y += iy * self.dy

            if self.rot != 0.:
                rx = self._buffer_x * self._cos_rot + self._buffer_y * self._sin_rot
                self._buffer_y *= self._buffer_y * self._cos_rot
                self._buffer_y -= self._buffer_x * self._sin_rot
                self._buffer_x = rx

            self._buffer_x += self.x0
            self._buffer_y += self.y0

        ggx = self._buffer_x[ix]
        ggy = self._buffer_y[ix]
        ggz = 0.

        if self.coordinate_system.is_oriented:
            ggx, ggy, ggz = self.coordinate_system.xyz_from_oriented((ggx, ggy, ggz))

        return ggx, ggy, ggz

    def image_file(self, image_file_name=None, image_type=gxmap.RASTER_FORMAT_PNG, pix_width=None,
                   shade=False, color_map=None, contour=None, display_area=None):
        """
        Save as a georeferenced image file.

        :param image_file_name:  image file name. The extension should be consistent with the image_type.
                            If not specified a temporary PNG file is created.
        :param image_type:  image type, one ot the RASTER_FORMAT constants in `geosoft.gxpy.map`.
        :param pix_width:   desired image width in pixels, default is the width of the aggregate base layer
        :param shade:       `True` to add shading effect
        :param color_map:   `geosoft.gxpy.group.Color_map` instance, or a colour ramp file name,
                            default is user's default
        :param contour:     colour contour interval if colours need to break at exact levels
        :param display_area:    `geosoft.gxpy.geometry.Point2` instance, which defines the desired display
                                area. The display area coordinate system can be different from the grid.
        :return:            image file name.

        .. seealso:: `geosoft.gxpy.grid.image_file`, which creates an image directly from a grid file.

        .. Note:: This method saves the grid as a temporary file from which an aggregate and image are
            created. If the grid already exists as a grid file it is more efficient to call
            `geosoft.gxpy.grid.image_file`.

        .. versionadded:: 9.3.1
        """

        temp_grid = gx.gx().temp_file('grd')
        try:
            with Grid.copy(self, temp_grid) as g:
                temp_decorated = g.file_name_decorated
            imagefile = image_file(temp_decorated,
                                   image_file=image_file_name,
                                   image_type=image_type,
                                   pix_width=pix_width,
                                   shade=shade,
                                   color_map=color_map,
                                   contour=contour,
                                   display_area=display_area)
        finally:
            delete_files(temp_grid)

        return imagefile


# grid utilities
def array_locations(properties):
    """
    Create an array of (x,y,z) points for a grid defined by properties
    :param properties:  grid properties
    :returns:           array of points, shaped (ny, nx, 3)

    .. versionadded:: 9.1
    """

    with Grid.new(properties=properties) as g:
        return g.xyzv()[:, :, :3]


def gridMosaic(*args, **kwargs):
    """
    .. deprecated:: 9.2 use :py:method: grid_mosaic
    """
    return grid_mosaic(*args, **kwargs)


def grid_mosaic(mosaic,  grid_list, type_decorate='', report=None):
    """
    Combine a set of grids into a single grid.  Raises an error if the resulting grid is too large.

    :param mosaic:          name of the output grid, returned.  Decorate with '(HGD)' to get an HGD
    :param  grid_list:        list of input grid names
    :param type_decorate:  decoration for input grids if not default
    :param report:          string reporting function, report=print to print progress
    :returns:               :class`Grid` instance, must be closed with a call to close().

    .. versionadded:: 9.1
    """

    def props(gn, repro=None):
        with Grid.open(gn) as gg:
            if repro:
                gg.gximg.create_projected2(repro[0], repro[1])
            return gg.properties()

    def dimension(glist):

        def dimg(_gd, _rep=None):
            prp = props(_gd, _rep)
            _x0 = prp.get('x0')
            _y0 = prp.get('y0')
            _xm = _x0 + (prp.get('nx') - 1) * prp.get('dx')
            _ym = _y0 + (prp.get('ny') - 1) * prp.get('dy')
            _ipj = prp.get('coordinate_system').gxipj
            cell = prp.get('dx')
            return _x0, _y0, _xm, _ym, (_ipj, cell)

        def ndim(_x0, _xm, _dx):
            return int((_xm - _x0 + _dx / 2.0) / _dx) + 1

        dx0, dy0, dxm, dym, drepro = dimg(glist[0])
        for gd in glist[1:]:
            xx0, yy0, xxm, yym, r = dimg(gd, drepro)
            if xx0 < dx0:
                dx0 = xx0
            if yy0 < dy0:
                dy0 = yy0
            if xxm > dxm:
                dxm = xxm
            if yym > dym:
                dym = yym

        # calculate new grid dimension
        _p = props(glist[0])
        nnx = ndim(dx0, dxm, _p.get('dx'))
        nny = ndim(dy0, dym, _p.get('dy'))

        return dx0, dy0, nnx, nny, dxm, dym

    def locate(_x0, _y0, _p):

        _dx = _p.get('dx')
        _dy = _p.get('dy')
        dsx = round((p.get('x0') - _x0) / _dx)
        dsy = round((p.get('y0') - _y0) / _dy)

        return dsx, dsy

    def paste(gn, _mpg):
        with Grid.open(gn) as _g:
            _p = _g.properties()
            _nx = _p.get('nx')
            _ny = _p.get('ny')
            gpg = _g.gxpg()
            destx, desty = locate(x0, y0, _p)
            if report:
                report('    +{} nx,ny({},{})'.format(_g, _nx, _ny))
                report('     Copy ({},{}) -> ({},{}) of ({},{})'.format(_nx, _ny, destx, desty, mnx, mny))
            _mpg.copy_subset(gpg, desty, destx, 0, 0, _ny, _nx)
            return

    if len(grid_list) == 0:
        raise GridException(_t('At least one grid is required'))

    # create list of grids, all matching on coordinate system of first grid
    grids = []
    for i in range(len(grid_list)):
        grids.append(decorate_name(grid_list[i], type_decorate))

    # output grid
    x0, y0, nx, ny, xm, ym = dimension(grids)
    p = props(grids[0])
    p['x0'] = x0
    p['y0'] = y0
    p['nx'] = nx
    p['ny'] = ny
    if report is not None:
        report('')
        report('Mosaic: dim({},{}) x({},{}) y({},{}), cell({})...'.format(nx, ny, x0, xm, y0, ym, p.get('dx')))
    master = Grid.new(mosaic, p)
    if report:
        report('Memory image ready ({}) dim({},{}) x0,y0({},{})'.format(master, master.nx, master.ny,
                                                                        master.x0, master.y0))

    # paste grids onto master
    mnx = master.nx
    mny = master.ny
    mpg = master.gxpg()
    for g in grids:
        paste(g, mpg)

    if report:
        report('Mosaic completed: {}'.format(mosaic))

    return master


def gridBool(*args, **kwargs):
    """
    .. deprecated:: 9.2 use grid_bool
    """
    return grid_bool(*args, **kwargs)


def grid_bool(g1, g2, joined_grid, opt=1, size=3, olap=1):
    """

    :param g1:          Grids to merge
    :param g2:
    :param joined_grid: joined output grid name, overwritten if it exists
    :param opt:         logic to use on overlap points, default 1 (OR):

        === ============================================
        0   AND, both grids must have valid value
        1   OR, either grid has a valid value
        2   XOR, same as OR, except overlap is dummied
        === ============================================

    :param size:    size of the output grid, default is minimum size

        === ==========================================
        0   minimum size - dummy regions clipped
        1   size to grid 1
        2   size to grid 2
        3   size to maximum including both grids
        === ==========================================

    :param olap:    what to do with overlapping valid points, default uses grid 1

        === ==========================================
        0   average points
        1   use grid 1
        2   use grid 2
        === ==========================================

    :returns:       `Grid` instance of the merged output grid, must be closed with a call to close().

    .. versionadded:: 9.1
    """

    close_g1 = close_g2 = False
    if isinstance(g1, str):
        g1 = Grid.open(g1)
        close_g1 = True
    if isinstance(g2, str):
        g2 = Grid.open(g2)
        close_g2 = True

    gxapi.GXIMU.grid_bool(g1.gximg, g2.gximg, joined_grid, opt, size, olap)

    if close_g1:
        g1.close()
    if close_g2:
        g2.close()

    return Grid.open(joined_grid)


def figure_map(grid_file, map_file=None, shade=True, color_map=None, contour=None, **kwargs):
    """
    Create a map figure from a grid file.

    :param grid_file:   grid file name
    :param map_file:    name of the map file, if `None` a default map is created.
    :param shade:       `True` to add shading effect
    :param color_map:   `geosoft.gxpy.group.Color_map` instance, or a colour ramp file name, default is user's default
    :param contour:     colour contour interval if colours need to break at exact levels
    :param kwargs:      passed to  `geosoft.gxpy.agg.Aggregate_image.figure_map` and `geosoft.gxpy.map.Map.new`
    :return:            `geosoft.gxpy.map.Map` instance

    .. versionadded:: 9.3
    """

    with gxagg.Aggregate_image.new(grid_file, shade=shade, color_map=color_map, contour=contour) as agg:
        return agg.figure_map(file_name=map_file, **kwargs)


def image_file(grid_file, image_file=None, image_type=gxmap.RASTER_FORMAT_PNG, pix_width=None,
                  shade=True, color_map=None, contour=None, display_area=None):
    """
    Save a grid file grid as a georeferenced image file.

    :param grid_file:   grid file name
    :param image_file:  image file name. The extension should be consistent with the image_type.
                        If not specified a temporary PNG file is created.
    :param image_type:  image type, one ot the RASTER_FORMAT constants in `geosoft.gxpy.map`.
    :param pix_width:   desired image width in pixels, default is the width of the aggregate base layer
    :param shade:       `True` to add shading effect
    :param color_map:   `geosoft.gxpy.group.Color_map` instance, or a colour ramp file name, default is user's default
    :param contour:     colour contour interval if colours need to break at exact levels
    :param display_area:    `geosoft.gxpy.geometry.Point2` instance, which defines the desired display
                            area. The display area coordinate system can be different from the grid.
    :return:            image file name.

    .. versionadded:: 9.3.1
    """

    with gxagg.Aggregate_image.new(grid_file, shade=shade, color_map=color_map, contour=contour) as agg:
        return agg.image_file(image_file, image_type=image_type, pix_width=pix_width, display_area=display_area)
