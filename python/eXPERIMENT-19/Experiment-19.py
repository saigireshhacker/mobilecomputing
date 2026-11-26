
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)

N, AREA = 8, 200.0
Pt, PL0, n, sigma, d0, SENS = 20.0, 40.0, 3.0, 4.0, 1.0, -85.0

pos = rng.uniform(0, AREA, (N, 2))

D = np.linalg.norm(pos[:, None] - pos[None], axis=2)

R = Pt - PL0 - 10 * n * np.log10(np.maximum(D, d0) / d0) + rng.normal(0, sigma, (N, N))

R = np.triu(R, 1)
R = R + R.T

np.fill_diagonal(R, np.nan)

A = (R >= SENS).astype(int)

print("RSSI Matrix (dBm):")
print(np.round(R, 1))

print("Average Degree:", A.sum() / N)

seen, stack = {0}, [0]

while stack:
    u = stack.pop()

    for v in np.where(A[u])[0]:
        if v not in seen:
            seen.add(v)
            stack.append(v)

print("Connected:", len(seen) == N)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

iu = np.triu_indices(N, 1)

ax[0].scatter(D[iu], R[iu])
ax[0].axhline(SENS, color='r', ls='--')
ax[0].set_xlabel('Distance (m)')
ax[0].set_ylabel('RSSI (dBm)')
ax[0].set_title('RSSI vs Distance')

for i in range(N):
    for j in range(i + 1, N):
        if A[i, j]:
            ax[1].plot(*zip(pos[i], pos[j]), 'g-', lw=0.8)

ax[1].scatter(pos[:, 0], pos[:, 1], color='blue')

for i in range(N):
    ax[1].text(pos[i, 0], pos[i, 1], str(i))

ax[1].set_xlabel('X Position (m)')
ax[1].set_ylabel('Y Position (m)')
ax[1].set_title('Wireless Network Connectivity')
ax[1].set_xlim(0, AREA)
ax[1].set_ylim(0, AREA)

plt.tight_layout()
plt.show()
