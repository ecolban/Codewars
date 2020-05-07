def square_sums_row(n):
    sqrs = {i * i for i in range(2, int((2 * n) ** 0.5) + 1)}
    succs = {i: {j for j in range(1, n + 1) if i + j in sqrs and i != j} for i in range(1, n + 1)}
    chosen = set()
    done = False

    def helper(last, k, res):
        nonlocal done
        chosen.add(last)
        res.append(last)
        k += 1
        if k < n:
            for i in succs[last]:
                if i not in chosen:
                    helper(i, k, res)
                if done: break
            if not done:
                x = res.pop(-1)
                chosen.remove(x)
                k -= 1
        else:
            done = True
        return res

    return next((res for i in range(1, n + 1) for res in (helper(i, 0, []),) if res), None)


if __name__ == "__main__":
    print(square_sums_row(60))
