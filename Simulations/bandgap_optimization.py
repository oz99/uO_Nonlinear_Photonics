import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

num_bands = 8
resolution = 32
# Define the lattice constant for the Kagome lattice
lattice_constant = 1

# Define the basis vectors for the hexagonal lattice structure
basis1=mp.Vector3(math.sqrt(3)/2 * lattice_constant, 0.5 * lattice_constant)
basis2=mp.Vector3(0, lattice_constant)

geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
                              basis1=basis1,
                              basis2=basis2)

# Define the sites in the Kagome lattice
geometry = [
    mp.Cylinder(0.252, center=mp.Vector3(0, 0), material=mp.Medium(epsilon=12)),
    mp.Cylinder(0.252, center=mp.Vector3(basis1.x/2, basis1.y/2), material=mp.Medium(epsilon=12)),
    mp.Cylinder(0.252, center=mp.Vector3(basis2.x/2, basis2.y/2), material=mp.Medium(epsilon=12))
]

# Define the k-points
k_points = [
    mp.Vector3(),                          # Gamma
    mp.Vector3(0.5, 0),                    # M
    mp.Vector3(1./3 * lattice_constant, 1./3 * lattice_constant), # K
    mp.Vector3(),                          # Gamma
]

k_points = mp.interpolate(4, k_points)

ms = mpb.ModeSolver(
    geometry=geometry,
    geometry_lattice=geometry_lattice,
    k_points=k_points,
    resolution=resolution,
    num_bands=num_bands
)
ms.run_tm(mpb.output_at_kpoint(mp.Vector3(-1./3, 1./3), mpb.fix_efield_phase,
          mpb.output_efield_z))
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

#The following portion of the code is used to maximize the TM bandgap. Ensure that the geometry matches the structure your calculating

""" def first_tm_gap(r):
    ms.geometry = [mp.Cylinder(r, center=mp.Vector3(0, 0), material=mp.Medium(epsilon=12)),
    mp.Cylinder(r, center=mp.Vector3(basis1.x/2, basis1.y/2), material=mp.Medium(epsilon=12)),
    mp.Cylinder(r, center=mp.Vector3(basis2.x/2, basis2.y/2), material=mp.Medium(epsilon=12))]
    ms.run_te()
    return -1 * ms.retrieve_gap(1) # return the gap from TM band 1 to TM band 2

ms.num_bands = 2
ms.mesh_size = 14

result = minimize_scalar(first_tm_gap, method='bounded', bounds=[0.1, 0.5], options={'xatol': 0.1})
print("radius at maximum: {}".format(result.x))
print("gap size at maximum: {}".format(result.fun * -1))  """


## Plot the bandstructure


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
