# -*- coding: utf-8 -*-

"""
This example shows how to compute a traveltime grid using an Eikonal solver
and to plot it.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""

import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import pickle
try:
    from fteikpy import Eikonal
except ImportError:
    import sys
    sys.path.append("../")
    from fteikpy import Eikonal


if __name__ == "__main__":
    # Parameters
    source = ( 0., 5000. )
    marmousi = pickle.load(open("marmousi.pickle", "rb"))
    nz, nx = marmousi.shape
    dz, dx = 10., 10.
    
    # Compute traveltimes using a 2D Eikonal solver
    eik = Eikonal(marmousi, grid_size = (dz, dx), n_sweep = 2)
    eik.smooth(10)
    tt = eik.solve(source)
    
    # Plot velocity model and isochrones
    fig = plt.figure(figsize = (10, 3.5), facecolor = "white")
    fig.patch.set_alpha(0.)
    ax1 = fig.add_subplot(1, 1, 1)
    
    ax = eik.xaxis
    az = eik.zaxis
    cax = ax1.contourf(ax, az, eik.velocity_model/1e3, 100, cmap = "jet")
    tt.plot(n_levels = 30, axes = ax1, cont_kws = dict(colors = "black", linewidths = 1))
    
    ax1.set_title("Marmousi")
    ax1.set_xlabel("X (m)")
    ax1.set_ylabel("Depth (m)")
    ax1.invert_yaxis()
    
    cb = fig.colorbar(cax)
    cb.set_label("P-wave velocity (km/s)")
    
    fig.tight_layout()
    plt.show()