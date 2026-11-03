import sys

x = [float(v) for v in sys.argv[1:]]  # Per-UE throughput values

n = len(x)

J = sum(x)**2 / (n * sum(v*v for v in x))

print(f"Total = {sum(x):.2f}   Jain index = {J:.3f}")
