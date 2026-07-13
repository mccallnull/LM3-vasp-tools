# Single AIMD run으로부터 얻은 profile에 대해 통계분석
# NVT의 경우: potential E, kinetic E, total E, temperature
# NPT의 경우: NVT 물리량들 + pressure, volume
# (lattice constants는 아직 구현 안됨: XDATCAR reader 필요)

import numpy as np

from ..model.md_profile import MDProfile


def summary(profile: MDProfile):

    print("=" * 50)
    print("MD Summary")
    print("=" * 50)

    print(f"Number of steps : {profile.nsteps}")

    if profile.dt is not None:
        print(f"Time step       : {profile.dt:.4f} fs")
        print(f"Duration        : {profile.duration:.4f} fs")

    print()

    _print_statistics("Potential Energy (eV)", profile.Epot)
    _print_statistics("Kinetic Energy (eV)", profile.Ekin)
    _print_statistics("Total Energy (eV)", profile.Etot)
    _print_statistics("Temperature (K)", profile.T_md)

    if profile.has_pressure:
        print()
        _print_statistics("Pressure (kBar)", profile.P_md)
        _print_statistics("Volume (A^3)", profile.V_md)

    print("=" * 50)


def _print_statistics(title: str, data):

    print(title)
    print(f"    Mean : {np.mean(data):12.6f}")
    print(f"    Std  : {np.std(data):12.6f}")
    print()