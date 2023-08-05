# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for intersecting B |eacute| zier curves via geometric methods.

As a convention, the functions defined here with a leading underscore
(e.g. :func:`_bbox_intersect`) have a special meaning.

Each of these functions have a Cython speedup with the exact same
interface which calls out to a Fortran implementation. The speedup
will be used if the extension can be built. The name **without** the
leading underscore will be surfaced as the actual interface (e.g.
``bbox_intersect``) whether that is the pure Python implementation
or the speedup.

.. |eacute| unicode:: U+000E9 .. LATIN SMALL LETTER E WITH ACUTE
   :trim:
"""


import atexit
import itertools

import numpy as np
import six

from bezier import _curve_helpers
from bezier import _helpers
from bezier import _intersection_helpers
try:
    from bezier import _curve_intersection_speedup
except ImportError:  # pragma: NO COVER
    _curve_intersection_speedup = None


# Set the threshold for exponent at half the bits available,
# this way one round of Newton's method can finish the job
# by squaring the error.
_ERROR_VAL = 0.5**26
_MAX_INTERSECT_SUBDIVISIONS = 20
_MAX_CANDIDATES = 64
_SEGMENTS_PARALLEL = 'Line segments parallel.'
_TOO_MANY_TEMPLATE = (
    'The number of candidate intersections is too high.\n'
    '{:d} candidate pairs.')
_NO_CONVERGE_TEMPLATE = (
    'Curve intersection failed to converge to approximately linear '
    'subdivisions after {:d} iterations.')
# Allow wiggle room for ``s`` and ``t`` computed during segment
# intersection. Any over- or under-shooting will (hopefully) be
# resolved in the Newton refinement step. If it isn't resolved, the
# call to _wiggle_interval() will fail the intersection.
_WIGGLE_START = -2.0**(-16)
_WIGGLE_END = 1.0 - _WIGGLE_START
# Number of bits allowed in ``add_intersection()`` to consider two
# intersections to be "identical".
_SIMILAR_ULPS = 1


def _bbox_intersect(nodes1, nodes2):
    r"""Bounding box intersection predicate.

    .. note::

       There is also a Fortran implementation of this function, which
       will be used if it can be built.

    Determines if the bounding box of two sets of control points
    intersects in :math:`\mathbf{R}^2` with non-trivial
    intersection (i.e. tangent bounding boxes are insufficient).

    .. note::

       Though we assume (and the code relies on this fact) that
       the nodes are two-dimensional, we don't check it.

    Args:
        nodes1 (numpy.ndarray): Set of control points for a
            B |eacute| zier shape.
        nodes2 (numpy.ndarray): Set of control points for a
            B |eacute| zier shape.

    Returns:
        int: Enum from ``BoxIntersectionType`` indicating the type of
        bounding box intersection.
    """
    left1, right1, bottom1, top1 = _helpers.bbox(nodes1)
    left2, right2, bottom2, top2 = _helpers.bbox(nodes2)

    if (right2 < left1 or right1 < left2 or
            top2 < bottom1 or top1 < bottom2):
        return BoxIntersectionType.DISJOINT

    if (right2 == left1 or right1 == left2 or
            top2 == bottom1 or top1 == bottom2):
        return BoxIntersectionType.TANGENT
    else:
        return BoxIntersectionType.INTERSECTION


def linearization_error(nodes):
    r"""Compute the maximum error of a linear approximation.

    .. note::

       There is also a Fortran implementation of this function, which
       will be used if it can be built.

    .. note::

       This is a helper for :class:`.Linearization`, which is used during the
       curve-curve intersection process.

    We use the line

    .. math::

       L(s) = v_0 (1 - s) + v_n s

    and compute a bound on the maximum error

    .. math::

       \max_{s \in \left[0, 1\right]} \|B(s) - L(s)\|_2.

    Rather than computing the actual maximum (a tight bound), we
    use an upper bound via the remainder from Lagrange interpolation
    in each component. This leaves us with :math:`\frac{s(s - 1)}{2!}`
    times the second derivative in each component.

    The second derivative curve is degree :math:`d = n - 2` and
    is given by

    .. math::

       B''(s) = n(n - 1) \sum_{j = 0}^{d} \binom{d}{j} s^j
       (1 - s)^{d - j} \cdot \Delta^2 v_j

    Due to this form (and the convex combination property of
    B |eacute| zier Curves) we know each component of the second derivative
    will be bounded by the maximum of that component among the
    :math:`\Delta^2 v_j`.

    For example, the curve

    .. math::

       B(s) = \left[\begin{array}{c} 0 \\ 0 \end{array}\right] (1 - s)^2
           + \left[\begin{array}{c} 3 \\ 1 \end{array}\right] 2s(1 - s)
           + \left[\begin{array}{c} 9 \\ -2 \end{array}\right] s^2

    has
    :math:`B''(s) \equiv \left[\begin{array}{c} 6 \\ -8 \end{array}\right]`
    which has norm :math:`10` everywhere, hence the maximum error is

    .. math::

       \left.\frac{s(1 - s)}{2!} \cdot 10\right|_{s = \frac{1}{2}}
          = \frac{5}{4}.

    .. image:: images/linearization_error.png
       :align: center

    .. testsetup:: linearization-error, linearization-error-fail

       import numpy as np
       import bezier
       from bezier._geometric_intersection import linearization_error

    .. doctest:: linearization-error

       >>> nodes = np.asfortranarray([
       ...     [0.0,  0.0],
       ...     [3.0,  1.0],
       ...     [9.0, -2.0],
       ... ])
       >>> linearization_error(nodes)
       1.25

    .. testcleanup:: linearization-error

       import make_images
       make_images.linearization_error(nodes)

    As a **non-example**, consider a "pathological" set of control points:

    .. math::

       B(s) = \left[\begin{array}{c} 0 \\ 0 \end{array}\right] (1 - s)^3
           + \left[\begin{array}{c} 5 \\ 12 \end{array}\right] 3s(1 - s)^2
           + \left[\begin{array}{c} 10 \\ 24 \end{array}\right] 3s^2(1 - s)
           + \left[\begin{array}{c} 30 \\ 72 \end{array}\right] s^3

    By construction, this lies on the line :math:`y = \frac{12x}{5}`, but
    the parametrization is cubic:
    :math:`12 \cdot x(s) = 5 \cdot y(s) = 180s(s^2 + 1)`. Hence, the fact
    that the curve is a line is not accounted for and we take the worse
    case among the nodes in:

    .. math::

       B''(s) = 3 \cdot 2 \cdot \left(
           \left[\begin{array}{c} 0 \\ 0 \end{array}\right] (1 - s)
           + \left[\begin{array}{c} 15 \\ 36 \end{array}\right] s\right)

    which gives a nonzero maximum error:

    .. doctest:: linearization-error-fail

       >>> nodes = np.asfortranarray([
       ...     [ 0.0,  0.0],
       ...     [ 5.0, 12.0],
       ...     [10.0, 24.0],
       ...     [30.0, 72.0],
       ... ])
       >>> linearization_error(nodes)
       29.25

    Though it may seem that ``0`` is a more appropriate answer, consider
    the **goal** of this function. We seek to linearize curves and then
    intersect the linear approximations. Then the :math:`s`-values from
    the line-line intersection is lifted back to the curves. Thus
    the error :math:`\|B(s) - L(s)\|_2` is more relevant than the
    underyling algebraic curve containing :math:`B(s)`.

    .. note::

       It may be more appropriate to use a **relative** linearization error
       rather than the **absolute** error provided here. It's unclear if
       the domain :math:`\left[0, 1\right]` means the error is **already**
       adequately scaled or if the error should be scaled by the arc
       length of the curve or the (easier-to-compute) length of the line.

    Args:
        nodes (numpy.ndarray): Nodes of a curve.

    Returns:
        float: The maximum error between the curve and the
        linear approximation.
    """
    num_nodes, _ = nodes.shape
    degree = num_nodes - 1
    if degree == 1:
        return 0.0

    second_deriv = nodes[:-2, :] - 2.0 * nodes[1:-1, :] + nodes[2:, :]
    worst_case = np.max(np.abs(second_deriv), axis=0)

    # max_{0 <= s <= 1} s(1 - s)/2 = 1/8 = 0.125
    multiplier = 0.125 * degree * (degree - 1)
    # NOTE: worst_case is 1D due to np.max(), so this is the vector norm.
    return multiplier * np.linalg.norm(worst_case, ord=2)


def segment_intersection(start0, end0, start1, end1):
    r"""Determine the intersection of two line segments.

    Assumes each line is parametric

    .. math::

       \begin{alignat*}{2}
        L_0(s) &= S_0 (1 - s) + E_0 s &&= S_0 + s \Delta_0 \\
        L_1(t) &= S_1 (1 - t) + E_1 t &&= S_1 + t \Delta_1.
       \end{alignat*}

    To solve :math:`S_0 + s \Delta_0 = S_1 + t \Delta_1`, we use the
    cross product:

    .. math::

       \left(S_0 + s \Delta_0\right) \times \Delta_1 =
           \left(S_1 + t \Delta_1\right) \times \Delta_1 \Longrightarrow
       s \left(\Delta_0 \times \Delta_1\right) =
           \left(S_1 - S_0\right) \times \Delta_1.

    Similarly

    .. math::

       \Delta_0 \times \left(S_0 + s \Delta_0\right) =
           \Delta_0 \times \left(S_1 + t \Delta_1\right) \Longrightarrow
       \left(S_1 - S_0\right) \times \Delta_0 =
           \Delta_0 \times \left(S_0 - S_1\right) =
           t \left(\Delta_0 \times \Delta_1\right).

    .. note::

       Since our points are in :math:`\mathbf{R}^2`, the "traditional"
       cross product in :math:`\mathbf{R}^3` will always point in the
       :math:`z` direction, so in the above we mean the :math:`z`
       component of the cross product, rather than the entire vector.

    For example, the diagonal lines

    .. math::

       \begin{align*}
        L_0(s) &= \left[\begin{array}{c} 0 \\ 0 \end{array}\right] (1 - s) +
                  \left[\begin{array}{c} 2 \\ 2 \end{array}\right] s \\
        L_1(t) &= \left[\begin{array}{c} -1 \\ 2 \end{array}\right] (1 - t) +
                  \left[\begin{array}{c} 1 \\ 0 \end{array}\right] t
       \end{align*}

    intersect at :math:`L_0\left(\frac{1}{4}\right) =
    L_1\left(\frac{3}{4}\right) =
    \frac{1}{2} \left[\begin{array}{c} 1 \\ 1 \end{array}\right]`.

    .. image:: images/segment_intersection1.png
       :align: center

    .. testsetup:: segment-intersection1, segment-intersection2

       import numpy as np
       from bezier._geometric_intersection import segment_intersection

    .. doctest:: segment-intersection1
       :options: +NORMALIZE_WHITESPACE

       >>> start0 = np.asfortranarray([[0.0, 0.0]])
       >>> end0 = np.asfortranarray([[2.0, 2.0]])
       >>> start1 = np.asfortranarray([[-1.0, 2.0]])
       >>> end1 = np.asfortranarray([[1.0, 0.0]])
       >>> s, t, _ = segment_intersection(start0, end0, start1, end1)
       >>> s
       0.25
       >>> t
       0.75

    .. testcleanup:: segment-intersection1

       import make_images
       make_images.segment_intersection1(start0, end0, start1, end1, s)

    Taking the parallel (but different) lines

    .. math::

       \begin{align*}
        L_0(s) &= \left[\begin{array}{c} 1 \\ 0 \end{array}\right] (1 - s) +
                  \left[\begin{array}{c} 0 \\ 1 \end{array}\right] s \\
        L_1(t) &= \left[\begin{array}{c} -1 \\ 3 \end{array}\right] (1 - t) +
                  \left[\begin{array}{c} 3 \\ -1 \end{array}\right] t
       \end{align*}

    we should be able to determine that the lines don't intersect, but
    this function is not meant for that check:

    .. image:: images/segment_intersection2.png
       :align: center

    .. doctest:: segment-intersection2
       :options: +NORMALIZE_WHITESPACE

       >>> start0 = np.asfortranarray([[1.0, 0.0]])
       >>> end0 = np.asfortranarray([[0.0, 1.0]])
       >>> start1 = np.asfortranarray([[-1.0, 3.0]])
       >>> end1 = np.asfortranarray([[3.0, -1.0]])
       >>> _, _, success = segment_intersection(start0, end0, start1, end1)
       >>> success
       False

    .. testcleanup:: segment-intersection2

       import make_images
       make_images.segment_intersection2(start0, end0, start1, end1)

    Instead, we use :func:`parallel_different`:

    .. testsetup:: segment-intersection2-continued

       import numpy as np
       from bezier._geometric_intersection import parallel_different

       start0 = np.asfortranarray([[1.0, 0.0]])
       end0 = np.asfortranarray([[0.0, 1.0]])
       start1 = np.asfortranarray([[-1.0, 3.0]])
       end1 = np.asfortranarray([[3.0, -1.0]])

    .. doctest:: segment-intersection2-continued

       >>> parallel_different(start0, end0, start1, end1)
       True

    .. note::

       There is also a Fortran implementation of this function, which
       will be used if it can be built.

    Args:
        start0 (numpy.ndarray): A 1x2 NumPy array that is the start
            vector :math:`S_0` of the parametric line :math:`L_0(s)`.
        end0 (numpy.ndarray): A 1x2 NumPy array that is the end
            vector :math:`E_0` of the parametric line :math:`L_0(s)`.
        start1 (numpy.ndarray): A 1x2 NumPy array that is the start
            vector :math:`S_1` of the parametric line :math:`L_1(s)`.
        end1 (numpy.ndarray): A 1x2 NumPy array that is the end
            vector :math:`E_1` of the parametric line :math:`L_1(s)`.

    Returns:
        Tuple[float, float, bool]: Pair of :math:`s_{\ast}` and
        :math:`t_{\ast}` such that the lines intersect:
        :math:`L_0\left(s_{\ast}\right) = L_1\left(t_{\ast}\right)` and then
        a boolean indicating if an intersection was found.
    """
    delta0 = end0 - start0
    delta1 = end1 - start1
    cross_d0_d1 = _helpers.cross_product(delta0, delta1)
    if cross_d0_d1 == 0.0:
        return None, None, False
    else:
        start_delta = start1 - start0
        s = _helpers.cross_product(start_delta, delta1) / cross_d0_d1
        t = _helpers.cross_product(start_delta, delta0) / cross_d0_d1
        return s, t, True


def parallel_different(start0, end0, start1, end1):
    r"""Checks if two parallel lines ever meet.

    Meant as a back-up when :func:`segment_intersection` fails.

    .. note::

       This function assumes but never verifies that the lines
       are parallel.

    In the case that the segments are parallel and lie on the **exact**
    same line, finding a unique intersection is not possible. However, if
    they are parallel but on **different** lines, then there is a
    **guarantee** of no intersection.

    In :func:`segment_intersection`, we utilized the normal form of the
    lines (via the cross product):

    .. math::

       \begin{align*}
       L_0(s) \times \Delta_0 &\equiv S_0 \times \Delta_0 \\
       L_1(t) \times \Delta_1 &\equiv S_1 \times \Delta_1
       \end{align*}

    So, we can detect if :math:`S_1` is on the first line by
    checking if

    .. math::

       S_0 \times \Delta_0 \stackrel{?}{=} S_1 \times \Delta_0.

    If it is not on the first line, then we are done, the
    segments don't meet:

    .. image:: images/parallel_different1.png
       :align: center

    .. testsetup:: parallel-different1, parallel-different2

       import numpy as np
       from bezier._geometric_intersection import parallel_different

    .. doctest:: parallel-different1

       >>> # Line: y = 1
       >>> start0 = np.asfortranarray([[0.0, 1.0]])
       >>> end0 = np.asfortranarray([[1.0, 1.0]])
       >>> # Vertical shift up: y = 2
       >>> start1 = np.asfortranarray([[-1.0, 2.0]])
       >>> end1 = np.asfortranarray([[3.0, 2.0]])
       >>> parallel_different(start0, end0, start1, end1)
       True

    .. testcleanup:: parallel-different1

       import make_images
       make_images.helper_parallel_different(
           start0, end0, start1, end1, 'parallel_different1.png')

    If :math:`S_1` **is** on the first line, we want to check that
    :math:`S_1` and :math:`E_1` define parameters outside of
    :math:`\left[0, 1\right]`. To compute these parameters:

    .. math::

       L_1(t) = S_0 + s_{\ast} \Delta_0 \Longrightarrow
           s_{\ast} = \frac{\Delta_0^T \left(
               L_1(t) - S_0\right)}{\Delta_0^T \Delta_0}.

    For example, the intervals :math:`\left[0, 1\right]` and
    :math:`\left[\frac{3}{2}, 2\right]` (via
    :math:`S_1 = S_0 + \frac{3}{2} \Delta_0` and
    :math:`E_1 = S_0 + 2 \Delta_0`) correspond to segments that
    don't meet:

    .. image:: images/parallel_different2.png
       :align: center

    .. doctest:: parallel-different2

       >>> start0 = np.asfortranarray([[1.0, 0.0]])
       >>> delta0 = np.asfortranarray([[2.0, -1.0]])
       >>> end0 = start0 + 1.0 * delta0
       >>> start1 = start0 + 1.5 * delta0
       >>> end1 = start0 + 2.0 * delta0
       >>> parallel_different(start0, end0, start1, end1)
       True

    .. testcleanup:: parallel-different2

       import make_images
       make_images.helper_parallel_different(
           start0, end0, start1, end1, 'parallel_different2.png')

    but if the intervals overlap, like :math:`\left[0, 1\right]` and
    :math:`\left[-1, \frac{1}{2}\right]`, the segments meet:

    .. image:: images/parallel_different3.png
       :align: center

    .. testsetup:: parallel-different3, parallel-different4

       import numpy as np
       from bezier._geometric_intersection import parallel_different

       start0 = np.asfortranarray([[1.0, 0.0]])
       delta0 = np.asfortranarray([[2.0, -1.0]])
       end0 = start0 + 1.0 * delta0

    .. doctest:: parallel-different3

       >>> start1 = start0 - 1.0 * delta0
       >>> end1 = start0 + 0.5 * delta0
       >>> parallel_different(start0, end0, start1, end1)
       False

    .. testcleanup:: parallel-different3

       import make_images
       make_images.helper_parallel_different(
           start0, end0, start1, end1, 'parallel_different3.png')

    Similarly, if the second interval completely contains the first,
    the segments meet:

    .. image:: images/parallel_different4.png
       :align: center

    .. doctest:: parallel-different4

       >>> start1 = start0 + 3.0 * delta0
       >>> end1 = start0 - 2.0 * delta0
       >>> parallel_different(start0, end0, start1, end1)
       False

    .. testcleanup:: parallel-different4

       import make_images
       make_images.helper_parallel_different(
           start0, end0, start1, end1, 'parallel_different4.png')

    .. note::

       This function doesn't currently allow wiggle room around the
       desired value, i.e. the two values must be bitwise identical.
       However, the most "correct" version of this function likely
       should allow for some round off.

    .. note::

       There is also a Fortran implementation of this function, which
       will be used if it can be built.

    Args:
        start0 (numpy.ndarray): A 1x2 NumPy array that is the start
            vector :math:`S_0` of the parametric line :math:`L_0(s)`.
        end0 (numpy.ndarray): A 1x2 NumPy array that is the end
            vector :math:`E_0` of the parametric line :math:`L_0(s)`.
        start1 (numpy.ndarray): A 1x2 NumPy array that is the start
            vector :math:`S_1` of the parametric line :math:`L_1(s)`.
        end1 (numpy.ndarray): A 1x2 NumPy array that is the end
            vector :math:`E_1` of the parametric line :math:`L_1(s)`.

    Returns:
        bool: Indicating if the lines are different.
    """
    delta0 = end0 - start0
    line0_const = _helpers.cross_product(start0, delta0)
    start1_against = _helpers.cross_product(start1, delta0)
    if line0_const != start1_against:
        return True

    # Each array is 1x2 (i.e. a row vector), we want the vector dot product.
    norm0_sq = np.vdot(delta0[0, :], delta0[0, :])
    start_numer = np.vdot((start1 - start0)[0, :], delta0[0, :])
    #      0 <= start_numer / norm0_sq <= 1
    # <==> 0 <= start_numer            <= norm0_sq
    if _helpers.in_interval(start_numer, 0.0, norm0_sq):
        return False

    end_numer = np.vdot((end1 - start0)[0, :], delta0[0, :])
    #      0 <= end_numer / norm0_sq <= 1
    # <==> 0 <= end_numer            <= norm0_sq
    if _helpers.in_interval(end_numer, 0.0, norm0_sq):
        return False

    # We know neither the start or end parameters are in [0, 1], but
    # they may contain [0, 1] between them.
    min_val, max_val = sorted([start_numer, end_numer])
    # So we make sure that 0 isn't between them.
    return not _helpers.in_interval(0.0, min_val, max_val)


def wiggle_pair(s_val, t_val):
    """Coerce two parameter values into the unit interval.

    Returns:
        Tuple[float, float]: Pair of ``(s_val, t_val)`` with each potentially
        rounded into the unit interval (if close enough).

    Raises:
        ValueError: If one of the values falls outside the unit interval
            (with wiggle room).
    """
    new_s, success_s = _helpers.wiggle_interval(s_val)
    new_t, success_t = _helpers.wiggle_interval(t_val)
    if not (success_s and success_t):
        raise ValueError(
            'At least one value outside of unit interval', s_val, t_val)

    return new_s, new_t


def from_linearized(first, second, intersections):
    """Determine curve-curve intersection from pair of linearizations.

    If there is an intersection along the segments, adds that intersection
    to ``intersections``. Otherwise, returns without doing anything.

    Args:
        first (Linearization): First curve being intersected.
        second (Linearization): Second curve being intersected.
        intersections (list): A list of existing intersections.

    Raises:
        NotImplementedError: If the segment intersection fails.
    """
    s, t, success = segment_intersection(
        first.start_node, first.end_node, second.start_node, second.end_node)
    if success:
        if first.error == 0.0 and not _helpers.in_interval(s, 0.0, 1.0):
            return
        if second.error == 0.0 and not _helpers.in_interval(t, 0.0, 1.0):
            return
        if not _helpers.in_interval(s, _WIGGLE_START, _WIGGLE_END):
            return
        if not _helpers.in_interval(t, _WIGGLE_START, _WIGGLE_END):
            return
    else:
        # Handle special case where the curves are actually lines.
        if first.error == 0.0 and second.error == 0.0:
            if parallel_different(
                    first.start_node, first.end_node,
                    second.start_node, second.end_node):
                return
        else:
            bbox_int = bbox_intersect(
                first.curve.original_nodes, second.curve.original_nodes)
            if bbox_int == BoxIntersectionType.DISJOINT:
                return

        raise NotImplementedError(_SEGMENTS_PARALLEL)

    # Now, promote `s` and `t` onto the original curves.
    orig_s = (1 - s) * first.curve.start + s * first.curve.end
    orig_t = (1 - t) * second.curve.start + t * second.curve.end
    # Perform one step of Newton iteration to refine the computed
    # values of s and t.
    refined_s, refined_t = _intersection_helpers.newton_refine(
        orig_s, first.curve.original_nodes,
        orig_t, second.curve.original_nodes)
    refined_s, refined_t = wiggle_pair(refined_s, refined_t)
    add_intersection(refined_s, refined_t, intersections)


def add_intersection(s, t, intersections):
    """Adds an intersection to list of ``intersections``.

    .. note::

       This is a helper for :func:`from_linearized` and :func:`endpoint_check`.
       These functions are used (directly or indirectly) by
       :func:`_all_intersections` exclusively, and that function has a
       Fortran equivalent.

    Accounts for repeated points at curve endpoints. If the
    intersection has already been found, does nothing.

    Args:
        s (float): The first parameter in an intersection.
        t (float): The second parameter in an intersection.
        intersections (list): List of existing intersections.
    """
    for existing_s, existing_t in intersections:
        if (_helpers.ulps_away(
                existing_s, s, num_bits=_SIMILAR_ULPS) and
                _helpers.ulps_away(
                    existing_t, t, num_bits=_SIMILAR_ULPS)):
            return

    intersections.append((s, t))


def endpoint_check(
        first, node_first, s, second, node_second, t, intersections):
    r"""Check if curve endpoints are identical.

    .. note::

       This is a helper for :func:`tangent_bbox_intersection`. These
       functions are used (directly or indirectly) by
       :func:`_all_intersections` exclusively, and that function has a
       Fortran equivalent.

    Args:
        first (SubdividedCurve): First curve being intersected (assumed in
            :math:\mathbf{R}^2`).
        node_first (numpy.ndarray): ``1x2`` array, one of the endpoints
            of ``first``.
        s (float): The parameter corresponding to ``node_first``, so
             expected to be one of ``0.0`` or ``1.0``.
        second (SubdividedCurve): Second curve being intersected (assumed in
            :math:\mathbf{R}^2`).
        node_second (numpy.ndarray): ``1x2`` array, one of the endpoints
            of ``second``.
        t (float): The parameter corresponding to ``node_second``, so
             expected to be one of ``0.0`` or ``1.0``.
        intersections (list): A list of already encountered
            intersections. If these curves intersect at their tangeny,
            then those intersections will be added to this list.
    """
    if _helpers.vector_close(node_first, node_second):
        orig_s = (1 - s) * first.start + s * first.end
        orig_t = (1 - t) * second.start + t * second.end
        add_intersection(orig_s, orig_t, intersections)


def tangent_bbox_intersection(first, second, intersections):
    r"""Check if two curves with tangent bounding boxes intersect.

    .. note::

       This is a helper for :func:`intersect_one_round`. These
       functions are used (directly or indirectly) by
       :func:`_all_intersections` exclusively, and that function has a
       Fortran equivalent.

    If the bounding boxes are tangent, intersection can
    only occur along that tangency.

    If the curve is **not** a line, the **only** way the curve can touch
    the bounding box is at the endpoints. To see this, consider the
    component

    .. math::

       x(s) = \sum_j W_j x_j.

    Since :math:`W_j > 0` for :math:`s \in \left(0, 1\right)`, if there
    is some :math:`k` with :math:`x_k < M = \max x_j`, then for any
    interior :math:`s`

    .. math::

       x(s) < \sum_j W_j M = M.

    If all :math:`x_j = M`, then :math:`B(s)` falls on the line
    :math:`x = M`. (A similar argument holds for the other three
    component-extrema types.)

    .. note::

       This function assumes callers will not pass curves that can be
       linearized / are linear. In :func:`_all_intersections`, curves
       are pre-processed to do any linearization before the
       subdivision / intersection process begins.

    Args:
        first (SubdividedCurve): First curve being intersected (assumed in
            :math:\mathbf{R}^2`).
        second (SubdividedCurve): Second curve being intersected (assumed in
            :math:\mathbf{R}^2`).
        intersections (list): A list of already encountered
            intersections. If these curves intersect at their tangeny,
            then those intersections will be added to this list.
    """
    node_first1 = np.asfortranarray([
        [first.nodes[0, 0], first.nodes[0, 1]],
    ])
    node_first2 = np.asfortranarray([
        [first.nodes[-1, 0], first.nodes[-1, 1]],
    ])
    node_second1 = np.asfortranarray([
        [second.nodes[0, 0], second.nodes[0, 1]],
    ])
    node_second2 = np.asfortranarray([
        [second.nodes[-1, 0], second.nodes[-1, 1]],
    ])

    endpoint_check(
        first, node_first1, 0.0, second, node_second1, 0.0, intersections)
    endpoint_check(
        first, node_first1, 0.0, second, node_second2, 1.0, intersections)
    endpoint_check(
        first, node_first2, 1.0, second, node_second1, 0.0, intersections)
    endpoint_check(
        first, node_first2, 1.0, second, node_second2, 1.0, intersections)


def bbox_line_intersect(nodes, line_start, line_end):
    r"""Determine intersection of a bounding box and a line.

    We do this by first checking if either the start or end node of the
    segment are contained in the bounding box. If they aren't, then
    checks if the line segment intersects any of the four sides of the
    bounding box.

    .. note::

       This function is "half-finished". It makes no distinction between
       "tangent" intersections of the box and segment and other types
       of intersection. However, the distinction is worthwhile, so this
       function should be "upgraded" at some point.

    Args:
        nodes (numpy.ndarray): Points (Nx2) that determine a bounding box.
        line_start (numpy.ndarray): Beginning of a line segment (1x2).
        line_end (numpy.ndarray): End of a line segment (1x2).

    Returns:
        int: Enum from ``BoxIntersectionType`` indicating the type of
        bounding box intersection.
    """
    left, right, bottom, top = _helpers.bbox(nodes)

    if (_helpers.in_interval(line_start[0, 0], left, right) and
            _helpers.in_interval(line_start[0, 1], bottom, top)):
        return BoxIntersectionType.INTERSECTION
    if (_helpers.in_interval(line_end[0, 0], left, right) and
            _helpers.in_interval(line_end[0, 1], bottom, top)):
        return BoxIntersectionType.INTERSECTION

    # NOTE: We allow ``segment_intersection`` to fail below (i.e.
    #       ``success=False``). At first, this may appear to "ignore"
    #       some potential intersections of parallel lines. However,
    #       no intersections will be missed. If parallel lines don't
    #       overlap, then there is nothing to miss. If they do overlap,
    #       then either the segment will have endpoints on the box (already
    #       covered by the checks above) or the segment will contain an
    #       entire side of the box, which will force it to intersect the 3
    #       edges that meet at the two ends of those sides. The parallel
    #       edge will be skipped, but the other two will be covered.

    # Bottom Edge
    s_bottom, t_bottom, success = segment_intersection(
        np.asfortranarray([[left, bottom]]),
        np.asfortranarray([[right, bottom]]),
        line_start, line_end)
    if (success and _helpers.in_interval(s_bottom, 0.0, 1.0) and
            _helpers.in_interval(t_bottom, 0.0, 1.0)):
        return BoxIntersectionType.INTERSECTION
    # Right Edge
    s_right, t_right, success = segment_intersection(
        np.asfortranarray([[right, bottom]]),
        np.asfortranarray([[right, top]]),
        line_start, line_end)
    if (success and _helpers.in_interval(s_right, 0.0, 1.0) and
            _helpers.in_interval(t_right, 0.0, 1.0)):
        return BoxIntersectionType.INTERSECTION
    # Top Edge
    s_top, t_top, success = segment_intersection(
        np.asfortranarray([[right, top]]),
        np.asfortranarray([[left, top]]),
        line_start, line_end)
    if (success and _helpers.in_interval(s_top, 0.0, 1.0) and
            _helpers.in_interval(t_top, 0.0, 1.0)):
        return BoxIntersectionType.INTERSECTION
    # NOTE: We skip the "last" edge. This is because any curve
    #       that doesn't have an endpoint on a curve must cross
    #       at least two, so we will have already covered such curves
    #       in one of the branches above.

    return BoxIntersectionType.DISJOINT


def intersect_one_round(candidates, intersections):
    """Perform one step of the intersection process.

    .. note::

       This is a helper for :func:`_all_intersections` and that function
       has a Fortran equivalent.

    Checks if the bounding boxes of each pair in ``candidates``
    intersect. If the bounding boxes do not intersect, the pair
    is discarded. Otherwise, the pair is "accepted". Then we
    attempt to linearize each curve in an "accepted" pair and
    track the overall linearization error for every curve
    encountered.

    Args:
        candidates (Union[list, itertools.chain]): An iterable of
            pairs of curves (or linearized curves).
        intersections (list): A list of already encountered
            intersections. If any intersections can be readily determined
            during this round of subdivision, then they will be added
            to this list.

    Returns:
        list: Returns a list of the next round of ``candidates``.
    """
    next_candidates = []

    # NOTE: In the below we replace ``isinstance(a, B)`` with
    #       ``a.__class__ is B``, which is a 3-3.5x speedup.
    for first, second in candidates:
        if first.__class__ is Linearization:
            if second.__class__ is Linearization:
                # If both ``first`` and ``second`` are linearizations, then
                # we can intersect them immediately.
                from_linearized(first, second, intersections)
                continue
            else:
                bbox_int = bbox_line_intersect(
                    second.nodes, first.start_node, first.end_node)
        else:
            if second.__class__ is Linearization:
                bbox_int = bbox_line_intersect(
                    first.nodes, second.start_node, second.end_node)
            else:
                bbox_int = bbox_intersect(first.nodes, second.nodes)

        if bbox_int == BoxIntersectionType.DISJOINT:
            continue
        elif bbox_int == BoxIntersectionType.TANGENT:
            tangent_bbox_intersection(first, second, intersections)
            continue

        # If we haven't ``continue``-d, add the accepted pair.
        # NOTE: This may be a wasted computation, e.g. if ``first``
        #       or ``second`` occur in multiple accepted pairs (the caller
        #       only passes one pair at a time). However, in practice
        #       the number of such pairs will be small so this cost
        #       will be low.
        lin1 = six.moves.map(Linearization.from_shape, first.subdivide())
        lin2 = six.moves.map(Linearization.from_shape, second.subdivide())
        next_candidates.extend(itertools.product(lin1, lin2))

    return next_candidates


def _all_intersections(nodes_first, nodes_second):
    r"""Find the points of intersection among a pair of curves.

    .. note::

       There is also a Fortran implementation of this function, which
       will be used if it can be built.

    .. note::

       This assumes both curves are in :math:`\mathbf{R}^2`, but does not
       **explicitly** check this. However, functions used here will fail if
       that assumption fails, e.g. :func:`bbox_intersect` and
       :func:`newton_refine() <._intersection_helpers._newton_refine>`.

    Args:
        nodes_first (numpy.ndarray): Control points of a curve to be
            intersected with ``nodes_second``.
        nodes_second (numpy.ndarray): Control points of a curve to be
            intersected with ``nodes_first``.

    Returns:
        numpy.ndarray: ``Nx2`` array of intersection parameters.
        Each row contains a pair of values :math:`s` and :math:`t`
        (each in :math:`\left[0, 1\right]`) such that the curves
        intersect: :math:`B_1(s) = B_2(t)`.

    Raises:
        ValueError: If the subdivision iteration does not terminate
            before exhausting the maximum number of subdivisions.
        NotImplementedError: If the subdivision process picks up too
            many candidate pairs. This typically indicates tangent
            curves or coincident curves.
    """
    curve_first = SubdividedCurve(nodes_first, nodes_first)
    curve_second = SubdividedCurve(nodes_second, nodes_second)
    candidates = [
        (
            Linearization.from_shape(curve_first),
            Linearization.from_shape(curve_second),
        ),
    ]
    intersections = []
    for _ in six.moves.xrange(_MAX_INTERSECT_SUBDIVISIONS):
        candidates = intersect_one_round(candidates, intersections)
        if len(candidates) > _MAX_CANDIDATES:
            msg = _TOO_MANY_TEMPLATE.format(len(candidates))
            raise NotImplementedError(msg)

        # If none of the candidate pairs have been accepted, then there are
        # no more intersections to find.
        if not candidates:
            if intersections:
                return np.asfortranarray(intersections)
            else:
                return np.empty((0, 2), order='F')

    msg = _NO_CONVERGE_TEMPLATE.format(_MAX_INTERSECT_SUBDIVISIONS)
    raise ValueError(msg)


class BoxIntersectionType(object):  # pylint: disable=too-few-public-methods
    """Enum representing all possible bounding box intersections.

    .. note::

       This class would be more "correct" as an ``enum.Enum``, but it we keep
       the values integers to make interfacing with Fortran easier.
    """

    INTERSECTION = 0
    """Bounding boxes overlap with positive area."""
    TANGENT = 1
    """Bounding boxes are tangent but do not overlap."""
    DISJOINT = 2
    """Bounding boxes do not intersect or touch."""


class SubdividedCurve(object):  # pylint: disable=too-few-public-methods
    """A data wrapper for a B |eacute| zier curve

    To be used for intersection algorithm via repeated subdivision,
    where the ``start`` and ``end`` parameters must be tracked.

    Args:
        nodes (numpy.ndarray): The control points of the current
            subdivided curve
        original_nodes (numpy.ndarray): The control points of the original
            curve used to define the current one (before subdivision began).
        start (Optional[float]): The start parameter after subdivision.
        end (Optional[float]): The start parameter after subdivision.
    """

    __slots__ = ('nodes', 'original_nodes', 'start', 'end')

    def __init__(self, nodes, original_nodes, start=0.0, end=1.0):
        self.nodes = nodes
        self.original_nodes = original_nodes
        self.start = start
        self.end = end

    @property
    def __dict__(self):
        """dict: Dictionary of current subdivided curve's property namespace.

        This is just a stand-in property for the usual ``__dict__``. This
        class defines ``__slots__`` so by default would not provide a
        ``__dict__``.

        This also means that the current object can't be modified by the
        returned dictionary.
        """
        return {
            'nodes': self.nodes,
            'original_nodes': self.original_nodes,
            'start': self.start,
            'end': self.end,
        }

    def subdivide(self):
        """Split the curve into a left and right half.

        See :meth:`.Curve.subdivide` for more information.

        Returns:
            Tuple[SubdividedCurve, SubdividedCurve]: The left and right
            sub-curves.
        """
        left_nodes, right_nodes = _curve_helpers.subdivide_nodes(self.nodes)
        midpoint = 0.5 * (self.start + self.end)
        left = SubdividedCurve(
            left_nodes, self.original_nodes,
            start=self.start, end=midpoint)
        right = SubdividedCurve(
            right_nodes, self.original_nodes,
            start=midpoint, end=self.end)
        return left, right


class Linearization(object):
    """A linearization of a curve.

    This class is provided as a stand-in for a curve, so it
    provides a similar interface.

    Args:
        curve (SubdividedCurve): A curve that is linearized.
        error (float): The linearization error. Expected to have been
            computed via :func:`linearization_error`.
    """

    __slots__ = ('curve', 'error', 'start_node', 'end_node')

    def __init__(self, curve, error):
        self.curve = curve
        """SubdividedCurve: The curve that this linearization approximates."""
        self.error = error
        """float: The linearization error for the linearized curve."""
        self.start_node = np.asfortranarray([
            [curve.nodes[0, 0], curve.nodes[0, 1]],
        ])
        """numpy.ndarray: The start vector of this linearization."""
        self.end_node = np.asfortranarray([
            [curve.nodes[-1, 0], curve.nodes[-1, 1]],
        ])
        """numpy.ndarray: The end vector of this linearization."""

    @property
    def __dict__(self):
        """dict: Dictionary of current linearization's property namespace.

        This is just a stand-in property for the usual ``__dict__``. This
        class defines ``__slots__`` so by default would not provide a
        ``__dict__``.

        This also means that the current object can't be modified by the
        returned dictionary.
        """
        return {
            'curve': self.curve,
            'error': self.error,
            'start_node': self.start_node,
            'end_node': self.end_node,
        }

    def subdivide(self):
        """Do-nothing method to match the :class:`.Curve` interface.

        Returns:
            Tuple[~bezier._geometric_intersection.Linearization]: List of all
            subdivided parts, which is just the current object.
        """
        return self,

    @classmethod
    def from_shape(cls, shape):
        """Try to linearize a curve (or an already linearized curve).

        Args:
            shape (Union[SubdividedCurve, \
            ~bezier._geometric_intersection.Linearization]): A curve or an
                already linearized curve.

        Returns:
            Union[SubdividedCurve, \
            ~bezier._geometric_intersection.Linearization]: The
            (potentially linearized) curve.
        """
        # NOTE: In the below we replace ``isinstance(a, B)`` with
        #       ``a.__class__ is B``, which is a 3-3.5x speedup.
        if shape.__class__ is cls:
            return shape
        else:
            error = linearization_error(shape.nodes)
            if error < _ERROR_VAL:
                linearized = cls(shape, error)
                return linearized
            else:
                return shape


# pylint: disable=invalid-name
if _curve_intersection_speedup is None:  # pragma: NO COVER
    bbox_intersect = _bbox_intersect
    all_intersections = _all_intersections
else:
    bbox_intersect = _curve_intersection_speedup.bbox_intersect
    all_intersections = _curve_intersection_speedup.all_intersections
    atexit.register(
        _curve_intersection_speedup.free_curve_intersections_workspace)
# pylint: enable=invalid-name
