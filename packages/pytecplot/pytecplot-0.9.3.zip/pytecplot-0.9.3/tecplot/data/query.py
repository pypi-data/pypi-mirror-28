from collections import namedtuple
from ctypes import c_double

from ..tecutil import _tecutil, Index, IndexSet, lock
from .. import layout
from ..constant import *
from ..exception import *


@lock()
def probe_at_position(x, y, z=None, nearest=False, starting_cell=None,
                      starting_zone=None, zones=None, dataset=None, frame=None):
    """Returns field values at a point in space.

    .. note::

        The position is taken according to the axis assignments of the `Frame`
        which may be any of the associated variables in the `Dataset` and not
        necessarily ``(X, Y, Z)``. See: `Cartesian3DFieldAxis.variable`.

    Parameters:
        x,y,z (`float`, *z* is optional): position to probe for field values.
        nearest (`bool`): Returns the values at the nearest node to the given
            position. Probe position must be inside the volume of the data
            being queried, otherwise this will return `None`.
        starting_cell (3-`tuple` of `integers <int>`, optional):
            The ``(i,j,k)``-index of the cell to start looking for the given
            position. This must be used with ``starting_zone``.
        starting_zone (`Zone <data_access>`, optional): The first zone to start
            searching. This is required only when ``starting_cell`` is
            specified.
        zones (`list` of `Zones <data_access>`, optional): Limits the search to
            the given zones. `None` implies searching all zones. (default:
            `None`)
        dataset (`Dataset`, optional): The `Dataset` to probe. (defaults to
            the active `Dataset`.)
        frame (`Frame`, optional): The `Frame` which determines the spatial
            variable assignment ``(X,Y,Z)``. (defaults to the active `Frame`.)

    Returns:
        `namedtuple <collections.namedtuple>`: ``(data, cell, zone)``:

            ``data`` (`list` of `floats <float>`)
                The values of each variable in the dataset at the given
                position.
            ``cell`` (3-`tuple` of `integers <int>`)
                ``(i,j,k)`` of the cell containing the given position.
            ``zone`` (`Zone <data_access>`)
                Zone containing the given position

    .. note:: Returns `None` if the position can't be probed.

        This method will return `None` if the position is outside the volume
        of the data being queried. This means one should capture the results
        in a single variable and test it against `None` before proceeding::

            result = tp.data.query.probe_at_position(1.0, 2.0, 3.0)
            if result is None:
                print('probe failed.')
            else:
                data, cell, zone = result

        Additionally, with Tecplot 360 versions 2018 R1 and later, this
        function will raise an exception if Tecplot 360 was interrupted via the
        GUI during the probe operation.
    """
    if __debug__:
        if frame and dataset and frame.dataset != dataset:
            msg = ('Dataset must be attached to the input Frame: {} != {}'.
                   format(repr(frame.dataset), repr(dataset)))
            raise TecplotValueError(msg)
        if (starting_cell is None) ^ (starting_zone is None):
            msg = 'starting_cell option requires an associated starting_zone'
            raise TecplotLogicError(msg)

    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    with frame.activated():
        if starting_cell is None:
            start_with_local_cell = False
            i, j, k = 0, 0, 0
            starting_zone_index = 0
        else:
            start_with_local_cell = True
            i, j, k = (x+1 for x in starting_cell)
            starting_zone_index = starting_zone.index

        allocd = []
        if zones is not None:
            zones = IndexSet(*zones)
            allocd.append(zones)

        data = (max(3, dataset.num_variables)*c_double)()

        try:
            result = _tecutil.ProbeAtPosition(
                x, y, z or 0,
                i, j, k,
                IJKPlanes.Volume.value,
                starting_zone_index+1,
                start_with_local_cell,
                data,
                zones,
                z is not None,
                False,
                nearest)
            success, i, j, k, plane, zone_index = result
        except TecplotSystemError as e:
            if 'Assertion' in str(e):
                raise
            success = False

        if not success:
            try:
                if _tecutil.InterruptCheck():
                    raise TecplotInterruptError()
            except AttributeError:
                pass  # InterruptCheck added to TecUtilChecked in SDK 2018.1
            return None

        cell = (Index(i-1), Index(j-1), Index(k-1))
        zone_index = Index(zone_index-1)

        for a in allocd:
            a.dealloc()

        probe_return_tuple = namedtuple('probe_return_tuple', ['data', 'cell', 'zone'])
        return probe_return_tuple(data[:], cell, dataset.zone(zone_index))
