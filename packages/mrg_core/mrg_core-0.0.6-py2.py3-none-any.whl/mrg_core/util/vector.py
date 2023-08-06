"""
mots_vector.py
MOTS 3D vector routines

Meteoroid Orbit and Trajectory Software (MOTS)

Contact: geert@barentsen.be

:Authors:

    Geert Barentsen    (ESA/RSSD/MRG);
    Jorge Diaz del Rio (ODC Space);
    Detlef Koschny     (ESA/RSSD/MRG); and
    Jonathan McAuliffe (ESA/RSSD/MRG)

:Version:

   -MRG Toolkit version 0.1.4 -- 2016-09-30 (JDR)

      Corrected bug in linefit routine.  An exception is raised when
      the line cannot be fitted.  Added the corresponding documentation.

   -MRG Toolkit version 0.1.3 -- 2016-09-16 (JDR)

      Updates to adhere to MRG coding standards.
      Updated vector_angle to add case for zero vector input.
      Added logging module.

   -MRG Toolkit version 0.1.2 -- 2016-08-03 (DVK)

      Replaced pylab with numpy in import section.

   -MRG Toolkit version 0.1.1 -- 2015-10-07 (DVK)

      Updated ``RunTimeError`` with ``RuntimeErro`` before line fitting
      failure message.

"""

import itertools
import logging
from math import acos

from numpy import array, dot, cross, arccos, arcsin
from numpy import degrees, append
from numpy.linalg import norm
from scipy.optimize import leastsq
#  from numpy.linalg.linalg import lstsq  # can this on be used instead?


def normalize(v_in):
    """
    Normalize a vector array to the unit vector.

    Extended summary
    ----------------
    Find the unit vector along a double precision 3-dimensional array.

    Parameters
    ----------
    v_in : double precision 3-array
       is an arbitrary double precision, 3-dimensional vector.  ``v_in`` may
       be the zero vector.

    Returns
    -------
    numpy.array
       Unit vector in the direction of ``v_in``.  If ``v_in`` represents the
       zero vector, then ``normalize`` will also return the zero vector.

    Examples
    --------
        >>> normalize(array([0.500, 0.000, 0.000]))
        array([ 1.000, 0.000, 0.000])
        >>> normalize(array([0.000, 0.000, 0.000]))
        array([ 0.000, 0.000, 0.000])

    Notes
    -----
       Despite what is says in the documentation, this routine does not
       check for the number of dimensions of the input array.

    """
    magnitude = norm(v_in)
    if magnitude != 0:
        return v_in / magnitude
    else:
        return v_in


def project_point_on_line(point, line):
    """
    Orthogonal projection of point m on line p+Rq

    Parameters
    ----------
    point : 3-array

    line : 2x3-array

    Returns
    -------
    array
       3-dimensional vector to projected point.

    Examples
    --------
        >>> project_point_on_line([0.5,0.5,0.0], [[0.0,0.0,0.0], [1.0,0.0,0.0]])
        array([ 0.5,  0. ,  0. ])
        >>> project_point_on_line([-0.5,-0.5,0.0], [[0.0,0.0,0.0], [1.0,0.0,0.0]])
        array([-0.5,  0. ,  0. ])
        >>> project_point_on_line([1.0,0.0,0.0], [[0.0,0.0,0.0], [1.0,1.0,0.0]])
        array([ 0.5,  0.5,  0. ])

    """
    point = array(point)
    pos = array(line[0])
    vec = array(line[1])

    #
    # Calculate the orthogonal projection of the point onto the line
    # defined by the point 'pos' and the direction 'vec'
    #
    projection = pos + vec * (dot((point-pos), vec) / dot(vec, vec))

    return projection


def project_point_on_plane(point, plane):
    """

    Project a double precision 3-dimensional point onto a plane defined by a
    3-dimensional point and a 3-dimensional vector normal to the plane.

    Parameters
    ----------
    point : 3-array

    plane : 2x3-array
       is an 2x3-dimensional array that contains the definition of the plane as
       follows: plane[0] is an arbitary 3-dimensional point of the plane, and
       plane[1] is the normal 3-dimensional vector to the plane.

    Returns
    -------
    array
       3-dimensional vector to projected point.

    Examples
    --------
        >>> project_point_on_plane(array([0.0,1.0,0.0]), [array([0.0,0.0,0.0]),
            array([0.0,1.0,0.0])])
        array([ 0.,  0.,  0.])
        >>> project_point_on_plane(array([1.0,1.0,0.0]), [array([0.0,0.0,0.0]),
            array([0.0,1.0,0.0])])
        array([ 1.,  0.,  0.])

    """
    # Compute distance between point and plane
    distance = dot(plane[1], point - plane[0])
    # Projection is distance*normal away
    return array(point - distance * plane[1])


def project_line_on_plane(line, plane):
    """
    Project a line onto a plane.

    Parameters
    ----------
    line : 2x3-array
       line[0] -- point
       line[1] -- direction

    plane : 2x3-array
       plane[0] -- point
       plane[1] -- normal

    Returns
    -------
    array
       2x3-dimensional array representing the projected line onto the plane.

    Examples
    --------
        >>> project_line_on_plane([array([0.0,1.0,0.0]), array([0.0,0.0,1.0])], \
                                  [array([0.0,0.0,0.0]), array([0.0,1.0,0.0])])
        [array([ 0.,  0.,  0.]), array([ 0.,  0.,  1.])]
    """
    #
    # Compute the projection of the two points that define the line
    # onto the input plane. These points are given by the 3-dimensional
    # input vector named 'point' from the line "object" and the end
    # point of the direction vector.
    #
    projected_origin = project_point_on_plane(line[0], plane)
    projected_end = project_point_on_plane(line[0] + line[1], plane)
    return [projected_origin, projected_end-projected_origin]


def shortest_vector(point, line):
    """
    Shortest vector between a point and a line.

    Parameters
    ----------
    point : numpy.array
       3-dimensional float precision vector defining a point in Cartesian
       coordinates.

    line : numpy.array
       2x3-dimensional float precision array defining a line. The first
       component of the array defines a in 3-dimensional point in Cartesian
       coordinates, while the second component corresponds to the line
       direction vector.

    Returns
    -------
    numpy.array
       3-dimensional float precision array containing the shortest vector
       between the input ``point`` and the input ``line``.

    Examples
    --------
    >>> shortest_vector([2.0, 2.0, 2.0], [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        array([ 0.0,  0.0,  0.0])
    >>> shortest_vector([1.0, 0.0, 0.0], [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        array([-0.5,  0.5,  0. ])
    """
    projected = project_point_on_line(point, line)
    s_vector = projected - point
    return s_vector


def vector_angle(vector1, vector2):
    """
    Angular separation between two 3-dimensional vectors.


    Find the separation angle in degrees between two double precision,
    3-dimensional vectors.  This angle is defined as zero if either
    vector is zero.

    Parameters
    ----------
    vector1 : 3-array
       is an arbitrary double precision, 3-dimensional vector.  `vector1` may
       be the zero vector.
    vector2 : 3-array
       is an arbitrary double precision, 3-dimensional vector.  `vector2` may
       be the zero vector.

    Returns
    -------
    float
       Angular separation between `vector1` and `vector2`, in degrees.  If
       either vector is zero, the angular separation is defined as zero.

    Notes
    -----
        Despite saying that the input should be 3-dimensional vectors,
        the routine does not check for the dimensions, therefore it
        is only required that both vectors have the **SAME** dimensions.

    """

    if norm(vector1) == 0.000 or norm(vector2) == 0.000:

        return 0.000

    else:

        angle = arccos(dot(vector1, vector2) / (norm(vector1) * norm(vector2)))
        return degrees(angle)


def plane_vector_angle(normal, vector):
    """
    Compute the angle between a plane and a vector.

    Parameters
    ----------
    normal : numpy.array
       3-dimensional vector normal to the plane
    vector : numpy.array
       is an arbitrary double precision 3-dimensional vector.

    Returns
    -------
    float
       The angle between a plane and a vector in degrees.

    Examples
    --------
        >>> plane_vector_angle([1,0,0], [1,0,0])
        90.0
        >>> plane_vector_angle([1,0,0], [-20,0,0])
        -90.0
        >>> round(plane_vector_angle([1,0,0], [1,1,0]))
        45.0
        >>> round(plane_vector_angle([0,1,0], [-1,0,0]))
        0.0
    """
    # BUG: Crashes if normal = [0.0, 0.0, 0.0] or vector = [0.0, 0.0, 0.0]
    mydot = dot(normal, vector)
    return degrees(arcsin(mydot / (norm(normal) * norm(vector))))


def skew_distance(pnt_1, dir_1, pnt_2, dir_2):
    """
    Distance between 2 skewed (non-parallel) lines in 3D
    (checked 07 Aug 2014, dvk - needs numpy arrays as input)

    Input:
    p1 -- numpy array ([x, y, z]) of point on line 1
    q1 -- numpy array ([r, s, t]) of direction vector of line 1
    p2 -- numpy array ([x, y, z]) of point on line 2
    q2 -- numpy array ([r, s, t]) of direction vector of line2

    :return: The closest distance between the two lines.
    :rtype: float
    """

    #
    # A common normal vector of the lines is the cross product of
    # the direction vectors of the lines.
    #
    cnv = cross(dir_1, dir_2)

    #
    # It may be normed to a unit vector by dividing it by its length
    # which is distinct from 0 because of the non-parallelity.
    #
    # By projecting (dot product) the difference vector between the
    # two points of the lines on the unit common normal vector, we
    # obtain a vector whose length is the distance between the two
    # lines.
    #
    distance = norm(dot(pnt_2-pnt_1, cnv)) / norm(cnv)

    return distance


def plane_normal(vectors):
    """
    Weighted averaged normal of a plane going through a set of vectors.

    Parameters
    ----------
    vectors : numpy.array
       3xN-dimensional float precision array containing N 3-dimensional
       Cartesian vectors.

    Returns
    -------
    numpy.array
       The normal vector [x,y,z] of the fitted plane

    Examples
    --------
        >>> plane_normal ([[1.0,0.0,0.0], [0.0,1.0,0.0]])
        array([ 0.,  0.,  1.])
        >>> plane_normal ([[1,2,3], [2,4,6]])
        array([ 0.,  0.,  0.])
        >>> plane_normal ([[2,-6,-3], [4,3,-1]])
        array([ 0.42857143, -0.28571429,  0.85714286])
        >>> plane_normal ([[2.0,-6.0,-3.0], [4.0,3.0,-1.0]])
        array([ 0.42857143, -0.28571429,  0.85714286])
        >>> plane_normal ([[2,-6,-3], [4,3,-1], [4,3,-1]])
        array([ 0.42857143, -0.28571429,  0.85714286])
    """

    #
    # Initialize the output variable to zero
    #
    avgnormal = array([0.000, 0.000, 0.000])

    #
    # For each combination of two input vectors, without repetition
    #
    for vector_duple in itertools.combinations(vectors, 2):

        #
        # Obtain the normalized normal vector to the plane defined by the two
        # input vectors contained in this duple.
        #
        normal = normalize(cross(vector_duple[0], vector_duple[1]))

        #
        # Obtain the weighting factor. This averaging weight factor is the
        # inverse cosine of the scalar vector product (i.e. the angle between
        # the two input vectors). Round the dot product in order to avoid
        # rounding errors that may lead to a value greater than 1.0.
        #
        weight = acos(round(dot(normalize(vector_duple[0]),
                                normalize(vector_duple[1])), 15))

        #
        # Compute the weighted normal vector for the plane defined by the two
        # input vectors, and add it to the current averaged weighted normal
        # vector.
        #
        avgnormal += normal * weight

    #
    # Normalize the weighted average plane normal vector. The final result is
    # the mean normal vector to the plane defined by all the combinations
    # of two non-parallel input vectors.
    #
    avgnormal = normalize(avgnormal)

    return avgnormal


def linefit(xyz_array, maxiterations=8000):
    """
    Fits a line in 3D through a set of points using the least squares
    method.

    Parameters
    ----------
    xyz_array : numpy.array
       3xN-dimensional float precision array containing N 3-dimensional
       vectors, in Cartesian coordinates [x, y, z] that define a line in 3D.

    maxiterations : int
       Maximum number of calls for the optimization process when calling to
       the function ``linefit_residuals``. By default, the maximum number
       of iterations is 8,000.

    Returns
    -------
    numpy.array
       3x2-dimensional float precision array containing the fitted 3D line
       defined as a 3-dimensional point in Cartesian coordinates and a
       3-dimensional direction vector, also in Cartesian coordinates. The
       units of these vectors are the same as the units the input array
       are given in.

    Raises
    ------
    RuntimeError
       If the line fitting algorithm failed.

    Examples
    --------
    >>> linefit([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        [array([ 1.,  2.,  3.]), array([ 3.,  3.,  3.])]
    >>> linefit([[0.0,0.0,0.0], [1.0,1.0,1.0], [2.0,2.0,2.0]])
        [array([ 0.,  0.,  0.]), array([ 2.,  2.,  2.])]
    >>> linefit([[2.0,2.0,2.0], [1.0,1.0,1.0], [0.0,0.0,0.0]])
        [array([ 2.,  2.,  2.]), array([-2., -2., -2.])]
    """
    # Due to the implementation of scipy leastsq, there must be as many
    # arguments as parameters
    if len(xyz_array) < 3:
        tmp = append(xyz_array, xyz_array, axis=0)
        xyz_array = append(xyz_array, tmp, axis=0)
    elif len(xyz_array) < 6:
        xyz_array = append(xyz_array, xyz_array, axis=0)
    start_vel = array(xyz_array[-1]) - array(xyz_array[0])
    start = append(array(xyz_array[0]), start_vel)

    # Added the following in V3.x, 14 Aug 2014
    try:
        plsq = leastsq(linefit_residuals, start, args=xyz_array,
                       maxfev=maxiterations)
    except RuntimeError:

        #
        # Log the error message and raise again the same exception.
        #
        logging.error("Line fitting failed, skip this meteor.")
        raise

    state = [plsq[0][0:3], plsq[0][3:6]]
    return state


def linefit_residuals(line, xyz_array):
    """
    Helper function for the ``linefit`` routine that evaluates a 3D linear
    fit and returns the residual errors.

    Parameters
    ----------
    line: numpy.array
       6-dimensional float precision array that defines a 3-dimensional
       line, where the first 3 Cartesian coordinates define a ``point`` in
       3-D space, and the last 3 Cartesian coordinates define the line
       direction from the original ``point``.

    xyz_array : numpy.array
       Nx3-dimensional float precision array that contains N 3-dimensional
       points for which the residual error to the input ``line`` will
       be computed.

    Returns
    -------
    numpy.array
       N-dimensional float precision array that contains the residual errors
       for each of the N 3-dimensional points contained in the ``xyz_array``
       with respect to the 3-dimensional input ``line``.

    Examples
    --------
    >>> line = [0.0, 0.0, 0.0, 2.0, 2.0, 0.0]
    >>> linefit_residuals(line, [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        array([0.0, 1.0])
    >>> linefit_residuals(line, [[0.0, 0.0, 1.0], [2.0, 0.0, 0.0]])
        array([1.0, 1.414214])

    """
    residuals = []
    for xyz in xyz_array:
        vec = shortest_vector(xyz, [array(line[0:3]), array(line[3:6])])
        residuals.append(norm(vec))
    return residuals
