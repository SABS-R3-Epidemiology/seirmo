import numpy as np
import seircpp

F = seircpp.SEIRModelFactory()
a = F.gillespieSEIR()

N = 56286961
times = np.linspace(0, 100, 100000, dtype=np.float64)

arr = a.simulate(
    np.array(
        [48719236,21325,7158681,387719,
        0.055/N, 0.2, 0.1613],
        dtype=np.float64),
    times)

