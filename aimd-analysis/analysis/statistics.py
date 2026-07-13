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
        _print_statistics("a (A)", profile.lat_a)
        _print_statistics("b (A)", profile.lat_b)
        _print_statistics("c (A)", profile.lat_c)
        _print_statistics("alpha (deg.)", profile.lat_alp)
        _print_statistics("beta (deg.)", profile.lat_bet)
        _print_statistics("gamma (deg.)", profile.lat_gam)

    print("=" * 50)


def _print_statistics(title: str, data):

    print(title)
    print(f"    Mean : {np.mean(data):12.6f}")
    print(f"    Std  : {np.std(data):12.6f}")
    print()


def slice_profile(
    profile: MDProfile,
    start: int = 0,
    stop: int | None = None,
) -> MDProfile:

    return MDProfile(
        step=profile.step[start:stop],
        Epot=profile.Epot[start:stop],
        Ekin=profile.Ekin[start:stop],
        Etot=profile.Etot[start:stop],
        T_md=profile.T_md[start:stop],

        P_md=_slice_optional(profile.P_md, start, stop),
        V_md=_slice_optional(profile.V_md, start, stop),
        lat_a=_slice_optional(profile.lat_a, start, stop),
        lat_b=_slice_optional(profile.lat_b, start, stop),
        lat_c=_slice_optional(profile.lat_c, start, stop),
        lat_alp=_slice_optional(profile.lat_alp, start, stop),
        lat_bet=_slice_optional(profile.lat_bet, start, stop),
        lat_gam=_slice_optional(profile.lat_gam, start, stop),

        dt=profile.dt,
    )


def _slice_optional(arr, start, stop):
    if arr is None:
        return None
    return arr[start:stop]