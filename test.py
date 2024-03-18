import numpy as np
import matplotlib.pyplot as plt

RESOLUTION = 256  # Resolution of the generated noise image
SIZE = 9  # Number of octaves for multi-frequency noise
MAP_SIZE = 16  # Size of the map (adjust as needed)
SEA_LEVEL = 10
HEIGHT_PEAK = 128
TROUGH_PEAK = -128 # Negative number else 0

def perlin(x, y, seed=None):
    # permutation table
    if seed: np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    # coordinates of the top-left
    xi, yi = x.astype(int), y.astype(int)
    # internal coordinates
    xf, yf = x - xi, y - yi
    # fade factors
    u, v = fade(xf), fade(yf)
    # noise components
    n00 = gradient(p[p[xi % 256] + yi % 256], xf, yf)
    n01 = gradient(p[p[xi % 256] + (yi + 1) % 256], xf, yf - 1)
    n11 = gradient(p[p[(xi + 1) % 256] + (yi + 1) % 256], xf - 1, yf - 1)
    n10 = gradient(p[p[(xi + 1) % 256] + yi % 256], xf - 1, yf)
    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)

def lerp(a, b, x):
    "linear interpolation"
    return a + x * (b - a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h, x, y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y

def get_island(map: np.ndarray,
               size: float = 1, sea_level: float = -100, max_size: int = 100000):

    try:    
        max_index = np.unravel_index(np.argmax(map), map.shape)
        unsearched_indexes = [max_index]
        searched_indexes = list()

        while unsearched_indexes:
            row, col = unsearched_indexes[-1]
            for y in range(row - 1, row + 3):
                for x in range(col - 1, col + 3):
                    if (y, x) in searched_indexes:
                        pass
                    elif map[y, x] > map[max_index] * (1 - size):
                        unsearched_indexes.append((y, x))
            searched_indexes.append(unsearched_indexes.pop())
            if len(searched_indexes) > 1000: size = 0.9
        return searched_indexes
    except IndexError:
        for row in range(map.shape[0]):
            for col in range(map.shape[1]):
                if (row, col) in searched_indexes:
                    map[row, col] = 0
        get_island(map)




# Generate noise at multiple frequencies and add them up
island_generated = False

while not island_generated:
    try:
        map = np.zeros((RESOLUTION, RESOLUTION))
        for i in range(SIZE):
            freq = 2**i
            lin = np.linspace(0, freq * MAP_SIZE, RESOLUTION, endpoint=False)
            x, y = np.meshgrid(lin, lin)
            map += perlin(x, y) / freq

        print("Perlin noise generated")

        # Normalize the result
        map = (HEIGHT_PEAK - TROUGH_PEAK) * (map - np.min(map)) / (np.max(map) - np.min(map)) + TROUGH_PEAK

        # island = get_island(map)
                
        # for row in range(map.shape[0]):
        #     for col in range(map.shape[1]):
        #         if (row, col) not in island:
        #             map[row, col] = 0
        island_generated = True
    except:
        print("retrying")
        pass

# lowestx = 0
# highestx = 0
# for y in p:
#     for x in y:
#         if x > highestx: highestx = x
#         if x < lowestx:  lowestx  = x

# print(highestx, lowestx)

# Display the noise pattern with Viridis colormap
plt.imshow(map, origin='upper', cmap='viridis')
plt.show()
