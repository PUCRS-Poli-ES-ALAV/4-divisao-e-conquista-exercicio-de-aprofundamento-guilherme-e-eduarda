import random
import time
from typing import List, Tuple, Dict, Any


def maxVal1(A: List[int]) -> Tuple[int, int]:
    n = len(A)
    if n == 0:
        raise ValueError("Vetor vazio")
    maxv = A[0]
    it = 0
    for i in range(1, n):
        it += 1
        if A[i] > maxv:
            maxv = A[i]
    return maxv, it


def merge(A: List[int], l: int, m: int, r: int, aux: List[int]) -> int:
    i, j, k = l, m + 1, l
    comps = 0
    while i <= m and j <= r:
        comps += 1
        if A[i] <= A[j]:
            aux[k] = A[i]
            i += 1
        else:
            aux[k] = A[j]
            j += 1
        k += 1
    while i <= m:
        aux[k] = A[i]
        i += 1
        k += 1
    while j <= r:
        aux[k] = A[j]
        j += 1
        k += 1
    A[l:r + 1] = aux[l:r + 1]
    return comps


def _merge_sort_rec(A: List[int], l: int, r: int, aux: List[int]) -> int:
    if l >= r:
        return 0
    m = (l + r) // 2
    c1 = _merge_sort_rec(A, l, m, aux)
    c2 = _merge_sort_rec(A, m + 1, r, aux)
    c3 = merge(A, l, m, r, aux)
    return c1 + c2 + c3


def merge_sort(A: List[int]) -> Tuple[List[int], int]:
    if len(A) <= 1:
        return A, 0
    aux = [0] * len(A)
    comps = _merge_sort_rec(A, 0, len(A) - 1, aux)
    return A, comps


def maxVal2(A: List[int], init: int, end: int, counter: List[int]) -> int:
    counter[0] += 1
    if end - init <= 1:
        ai = A[init]
        aj = A[end]
        return ai if ai >= aj else aj
    m = (init + end) // 2
    v1 = maxVal2(A, init, m, counter)
    v2 = maxVal2(A, m + 1, end, counter)
    return v1 if v1 >= v2 else v2


def gera_vetor_aleatorio(n: int, rng: random.Random) -> List[int]:
    return [rng.randint(-10**9, 10**9) for _ in range(n)]


def testa_maxVal1_e_merge_sort(sizes: List[int], seed: int = 42) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    resultados = []
    for n in sizes:
        A = gera_vetor_aleatorio(n, rng)

        t0 = time.perf_counter()
        max1, it1 = maxVal1(A)
        t1 = time.perf_counter()

        B = A.copy()
        t2 = time.perf_counter()
        B_sorted, comps = merge_sort(B)
        t3 = time.perf_counter()

        resultados.append({
            "n": n,
            "maxVal1": {
                "max": max1,
                "iteracoes": it1,
                "tempo_segundos": t1 - t0
            },
            "merge_sort": {
                "comparacoes_chave": comps,
                "tempo_segundos": t3 - t2
            }
        })
    return resultados


def testa_maxVal2(sizes: List[int], seed: int = 42) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    resultados = []
    for n in sizes:
        A = gera_vetor_aleatorio(n, rng)
        counter = [0]

        t0 = time.perf_counter()
        max_algo = maxVal2(A, 0, n - 1, counter)
        t1 = time.perf_counter()

        resultados.append({
            "n": n,
            "max": max_algo,
            "iteracoes": counter[0],
            "tempo_segundos": t1 - t0
        })
    return resultados


if __name__ == "__main__":
    sizes = [32, 2048, 1048576]

    res_a = testa_maxVal1_e_merge_sort(sizes)
    for r in res_a:
        print(r)

    res_b = testa_maxVal2(sizes)
    for r in res_b:
        print(r)