import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Author: Ozan Oner
# Photonic crystal slab consisting of a Kagome lattice of air
# holes in a finite_thickness dielectric slab, optionally with a
# substrate on one side of the slab. 

# For similar case using triangular lattice see the paper: S. G. Johnson,
# S. Fan, P. R. Villeneuve, J. D. Joannopoulos, L. A. Kolodziejski,
# "Guided modes in photonic crystal slabs," PRB 60, 5751 (August
# 1999).

# Note that this structure has mirror symmetry throught the z=0 plane,
# and we are looking at k_vectors in the xy plane only.  Thus, we can
# break up the modes into even and odd (analogous to TE and TM), using
# the run_zeven and run_zodd functions.

h = 0.5  # the thickness of the slab .. Note that this should be changed to represent a 220nm thick Si slab
eps = 12.0  # the dielectric constant of the slab
loweps = 1.0  # the dielectric constant of the substrate
r = 0.29  # the radius of the holes with respect to the lattice constance r/a = 0.29, 
# the r=0.29 above is the experimental value of our Si Kagome sample 
supercell_h = 4  # height of the supercell
lattice_constant = 1 #Normalized lattice constant // Note the lattice constant is defined as a in litterature

# Define the basis vectors for the hexagonal lattice structure
basis1=mp.Vector3(math.sqrt(3)/2 * lattice_constant, 0.5 * lattice_constant)
basis2=mp.Vector3(0, lattice_constant)

# Kagome lattice with vertical supercell:
geometry_lattice = mp.Lattice(
    size=mp.Vector3(1, 1, supercell_h),
    basis1=mp.Vector3(math.sqrt(3)/2 * lattice_constant, 0.5 * lattice_constant, 0.5),
    basis2=mp.Vector3(0, lattice_constant, -0.5),
)

geometry = [
    mp.Block(
        material=mp.Medium(epsilon=loweps),
        center=mp.Vector3(z=0.25 * supercell_h),
        size=mp.Vector3(mp.inf, mp.inf, 0.5 * supercell_h),
    ),
    mp.Block(material=mp.Medium(epsilon=eps), size=mp.Vector3(mp.inf, mp.inf, h)),
    mp.Cylinder(r, center=mp.Vector3(0, 0), material=mp.air, height=supercell_h),
    mp.Cylinder(r, center=mp.Vector3(basis1.x/2, basis1.y/2), material=mp.air, height=supercell_h),
    mp.Cylinder(r, center=mp.Vector3(basis2.x/2, basis2.y/2), material=mp.air, height=supercell_h),
]

# Define the k-points
k_points = [
    mp.Vector3(),                          # Gamma
    mp.Vector3(0.5, 0),                    # M
    mp.Vector3(1./3 * lattice_constant, 1./3 * lattice_constant), # K
    mp.Vector3(),                          # Gamma
]

k_points = mp.interpolate(4, k_points)

resolution = mp.Vector3(32, 32, 16)
num_bands = 9

ms = mpb.ModeSolver(
    geometry_lattice=geometry_lattice,
    geometry=geometry,
    resolution=resolution,
    num_bands=num_bands,
    k_points=k_points,
)

ms.run_tm()
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

fig, ax = plt.subplots()
x = range(len(tm_freqs))
# Plot bands
# Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
    ax.scatter([xz]*len(tmz), tmz, color='blue')
    ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
ax.plot(tm_freqs, color='blue')
ax.plot(te_freqs, color='red')
ax.set_ylim([0, 1])
ax.set_xlim([x[0], x[-1]])

# Plot gaps
for gap in tm_gaps:
    if gap[0] > 1:
        ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)

for gap in te_gaps:
    if gap[0] > 1:
        ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)


# Plot labels
ax.text(12, 0.04, 'TM bands', color='blue', size=15)
ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

points_in_between = (len(tm_freqs) - 4) / 3
tick_locs = [i*points_in_between+i for i in range(4)]
tick_labs = ['Γ', 'X', 'M', 'Γ']
ax.set_xticks(tick_locs)
ax.set_xticklabels(tick_labs, size=16)
ax.set_ylabel('frequency (c/a)', size=16)
ax.grid(True)
plt.savefig('bandstructure_plot.png')
plt.show()


""" def main():
    # Run even and odd bands, outputting fields only at the K point:
    if loweps == 1.0:
        # we only have even/odd classification for symmetric structure
        ms.run_zeven(mpb.output_at_kpoint(K, mpb.output_hfield_z))
        ms.run_zodd(mpb.output_at_kpoint(K, mpb.output_dfield_z))
    else:
        ms.run(mpb.output_at_kpoint(K, mpb.output_hfield_z), mpb.display_zparities)

    ms.display_eigensolver_stats()


if __name__ == "__main__":
    main() """
