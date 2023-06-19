import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt

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
    mp.Cylinder(0.29, center=mp.Vector3(0, 0), material=mp.Medium(epsilon=11.9)),
    mp.Cylinder(0.29, center=mp.Vector3(basis1.x/2, basis1.y/2), material=mp.Medium(epsilon=11.9)),
    mp.Cylinder(0.29, center=mp.Vector3(basis2.x/2, basis2.y/2), material=mp.Medium(epsilon=11.9))
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


# let's assume we are interested in the first band
band_index = 1

for i in range(len(k_points)):
    k_point = k_points[i]
    band_freq = tm_freqs[i][band_index-1]  # adjust for 0-based indexing
    group_velocity = ms.get_group_velocity_band(band_index, k_point)
    
    # Calculate group index
    n_g = band_freq / group_velocity
    print(f"Group index for TM band {band_index} at k-point {i+1}: {n_g}")

# Repeat the calculation for TE bands
ms.run_te()
te_freqs = ms.all_freqs

for i in range(len(k_points)):
    k_point = k_points[i]
    band_freq = te_freqs[i][band_index-1]  # adjust for 0-based indexing
    group_velocity = ms.get_group_velocity_band(band_index, k_point)
    
    # Calculate group index
    n_g = band_freq / group_velocity
    print(f"Group index for TE band {band_index} at k-point {i+1}: {n_g}")
