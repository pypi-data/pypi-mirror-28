## Interface to the Litho1.0 Earth model

Provides a simple, fast, interface to the litho1.0 model (Pasyanos et al, 2014) using the `stripack` spherical meshing / interpolation toolkit. It is a convenient replacement for the `access_litho` tool supplied with the data and considerably faster when computing values at lots of points.

This initial "release" provides layer depths for any (lon, lat) point on the Earth's surface.

Todo: add the interface to provide the material properties for any (lat,lon,depth)

## Litho 1.0

Pasyanos, M.E., T.G. Masters, G. Laske, and Z. Ma (2014). LITHO1.0: An updated crust and lithospheric model of the Earth, J. Geophys. Res., 119 (3), 2153-2173, DOI: 10.1002/2013JB010626..

Cover your eyes, then read the [litho 1.0 home page](http://igppweb.ucsd.edu/~gabi/litho1.0.html)

## Stripy

(A modified / extended form of): [STRIPACK](https://people.sc.fsu.edu/~jburkardt/f_src/stripack/stripack.html) is a FORTRAN90 library which carries out some computational geometry tasks on the unit sphere in 3D, by Robert Renka. The [python interface to stripack](https://github.com/jswhit/stripack) is provided by Jeff Whitaker 
