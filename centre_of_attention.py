class Central_Pixels_Finder(object):
    def __init__(self, data, w, h):
        self.pixels = data
        self.width = w
        self.height = h

    def central_pixels(self, colour):
        w, h = self.width, self.height
        dst = [min(w, h)] * (w * h)
        for i in range(h):
            for j in range(w):
                k = i * w + j
                dst[k] = 0 if self.pixels[k] != colour \
                    else 1 if (i == 0 or j == 0) \
                    else min(dst[k - 1], dst[k - w]) + 1
        m = 0
        for i in range(h - 1, -1, -1):
            for j in range(w - 1, -1, -1):
                k = i * w + j
                dst[k] = min(dst[k], 1 if (i == h - 1 or j == w - 1) \
                    else min(dst[k + 1], dst[k + w]) + 1)
                m = max(m, dst[k])
        return [] if m == 0 else [k for k in range(w * h) if dst[k] == m]

image = Central_Pixels_Finder([1, 1, 4, 4, 4, 4, 2, 2, 2, 2,
                               1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                               1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                               1, 1, 1, 1, 1, 3, 2, 2, 2, 2,
                               1, 1, 1, 1, 1, 3, 3, 3, 2, 2,
                               1, 1, 1, 1, 1, 1, 3, 3, 3, 3], 10, 6)

print(image.central_pixels(1))
print(image.central_pixels(2))
print(image.central_pixels(3))
print(image.central_pixels(4))
print(image.central_pixels(5))
