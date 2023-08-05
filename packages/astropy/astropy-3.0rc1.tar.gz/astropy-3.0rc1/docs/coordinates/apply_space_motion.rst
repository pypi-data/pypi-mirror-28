.. include:: references.txt

.. _astropy-coordinates-apply-space-motion:

Accounting for space motion
***************************

The |SkyCoord| object supports updating the position of a source given its space
motion and a time or time difference to evaluate the new position at. This is
done using the :meth:`~astropy.coordinates.SkyCoord.apply_space_motion` method.
As an example, first we'll create a |SkyCoord| object with a specified
``obstime``::

    >>> import astropy.units as u
    >>> from astropy.time import Time
    >>> from astropy.coordinates import SkyCoord
    >>> c = SkyCoord(l=10*u.degree, b=45*u.degree, distance=100*u.pc,
    ...              pm_l_cosb=34*u.mas/u.yr, pm_b=-117*u.mas/u.yr,
    ...              frame='galactic',
    ...              obstime=Time('1988-12-18 05:11:23.5'))

We can now find the position at some other time, taking the space motion into
account. We can either specify the time difference between the observation time
and the desired time::

    >>> c.apply_space_motion(dt=10. * u.year) # doctest: +FLOAT_CMP
    <SkyCoord (Galactic): (l, b, distance) in (deg, deg, pc)
        ( 10.00013356,  44.999675,  99.99999994)
     (pm_l_cosb, pm_b, radial_velocity) in (mas / yr, mas / yr, km / s)
        ( 33.99980714, -117.00005604,  0.00034117)>
    >>> c.apply_space_motion(dt=-10. * u.year) # doctest: +FLOAT_CMP
    <SkyCoord (Galactic): (l, b, distance) in (deg, deg, pc)
        ( 9.99986643,  45.000325,  100.00000006)
     (pm_l_cosb, pm_b, radial_velocity) in (mas / yr, mas / yr, km / s)
        ( 34.00019286, -116.99994395, -0.00034117)>

Or, we can specify the new time to evaluate the position at::

    >>> c.apply_space_motion(new_obstime=Time('2017-12-18 01:12:07.3')) # doctest: +FLOAT_CMP
    <SkyCoord (Galactic): (l, b, distance) in (deg, deg, pc)
        ( 10.00038732,  44.99905754,  99.99999985)
     (pm_l_cosb, pm_b, radial_velocity) in (mas / yr, mas / yr, km / s)
        ( 33.99944073, -117.00016248,  0.00098937)>

If the |SkyCoord| object has no specified radial velocity (RV), the RV is
assumed to be 0. The new position of the source is determined assuming the
source moves in a straight line with constant velocity in an inertial frame.
There are no plans to support more complex evolution (e.g. non-inertial
frames or more complex evolution), as that is out of scope for the Astropy core
(although it may well be in-scope for a variety of affiliated packages).
