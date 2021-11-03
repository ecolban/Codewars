def drain_fill(a: list[int], left_retainer: int = 0, right_retainer: int = 0) -> list[int]:
    water = [0] * len(a)
    # Assume at first that water flows down and right, but not left
    for i, h in enumerate(reversed(a), start=1):
        right_retainer = 0 if h == 0 else max(right_retainer, h)
        water[len(a) - i] = right_retainer - h
    # Then assume it can also flow down and left...
    for i, h in enumerate(a):
        left_retainer = 0 if h == 0 else max(left_retainer, h)
        water[i] = min(water[i], left_retainer - h)
    return water
