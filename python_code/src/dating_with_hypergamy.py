from itertools import groupby


def guys_alone_from_group(men, women):
    men.sort(reverse=True)  # men with highest rating first
    women.sort()  # women with highest rating last
    loner_men = []
    for k, g in groupby(men):
        # Remove women who are not interested in men with look level k or less:
        while women and (women[-1] > k or k < 8 and women[-1] + 2 > k):
            women.pop()
        # Get the men with look level k
        k_men = list(g)
        # Match each man with look level k with a woman as long as there are enough women
        for m in k_men:
            if women:
                women.pop()
            else:
                loner_men.append(m)
        # Match each Chad with a second woman as long as there are enough women
        if k >= 8:
            for _ in k_men:
                if women:
                    women.pop()
    return list(reversed(loner_men))
