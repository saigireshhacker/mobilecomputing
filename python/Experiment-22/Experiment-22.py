
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate(seed=7, T=300, base=45.0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)

    lat = base + 15 * np.sin(2 * np.pi * t / 120) + rng.gamma(2.0, 3.0, T)

    for h in (80, 160, 240):
        lat[h:h + 3] += 120

    lat[rng.random(T) < 0.01] = np.nan

    return pd.Series(lat, index=t, name='latency_ms')


def from_ping(path):
    vals = [
        float(m.group(1))
        for l in open(path)
        if (m := re.search(r'time=([\d.]+)', l))
    ]

    return pd.Series(vals, name='latency_ms')


s = simulate()

# To use actual ping data:
# s = from_ping('ping.log')

roll = s.rolling(10, min_periods=1)

print(f"Mean   = {s.mean():.1f} ms")
print(f"Median = {s.median():.1f} ms")
print(f"P95    = {s.quantile(0.95):.1f} ms")
print(f"Jitter = {s.diff().abs().mean():.1f} ms")
print(f"Loss   = {100 * s.isna().mean():.1f} %")

plt.figure(figsize=(9, 4))

plt.plot(s.index, s, lw=0.6, label='Latency sample')
plt.plot(roll.mean(), 'r', label='10 s moving average')

plt.xlabel('Time (s)')
plt.ylabel('Latency (ms)')
plt.legend()
plt.title('Latency Trend')

plt.grid(True)
plt.tight_layout()

plt.savefig('latency.png', dpi=150)

plt.show()
