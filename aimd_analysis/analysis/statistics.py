# Single AIMD run으로부터 얻은 profile에 대해 통계분석
# NVT의 경우: potential E, kinetic E, total E, temperature
# NPT의 경우: NVT 물리량들 + pressure, volume
# (lattice constants는 아직 구현 안됨: XDATCAR reader 필요)

import numpy as np
from typing import Optional

from ..model.md_profile import MDProfile
from ..model.quantity_statistics import QuantityStatistics


# MDProfile의 시계열 quantity에 대한 통계량들 계산
def compute_statistics(profile: MDProfile) -> None:

    if profile.stats:
        profile.stats.clear()

    profile.stats["Epot"] = _build_statistics(profile.Epot)
    profile.stats["Ekin"] = _build_statistics(profile.Ekin)
    profile.stats["Etot"] = _build_statistics(profile.Etot)
    profile.stats["T_md"] = _build_statistics(profile.T_md)
    profile.stats["P_md"] = _build_statistics(profile.P_md)

    if profile.has_variable_cell:
        profile.stats["V_md"] = _build_statistics(profile.V_md)
        profile.stats["lat_a"] = _build_statistics(profile.lat_a)
        profile.stats["lat_b"] = _build_statistics(profile.lat_b)
        profile.stats["lat_c"] = _build_statistics(profile.lat_c)
        profile.stats["lat_alp"] = _build_statistics(profile.lat_alp)
        profile.stats["lat_bet"] = _build_statistics(profile.lat_bet)
        profile.stats["lat_gam"] = _build_statistics(profile.lat_gam)


def _build_statistics(data: Optional[np.ndarray]) -> Optional[QuantityStatistics]:

    if data is None:
        return None

    return QuantityStatistics(
        mean=np.mean(data),
        std=np.std(data),

        min=np.min(data),
        max=np.max(data),
    )


# MDProfile 통계 요약 (raw MDProfile, sliced MDProfile 모두 가능.)
def summary(profile: MDProfile, verbose: bool = False) -> None:

    if not profile.stats:
        raise RuntimeError(
            "Statistics have not been computed. "
            "Call compute_statistics(profile) first."
        )

    print("=" * 50)
    print("MD Summary")
    print("=" * 50)

    print(f"Step range      : {profile.step[0]} -> {profile.step[-1]}")
    print(f"Number of steps : {profile.nsteps}")

    if profile.dt is not None:
        print(f"Time step        : {profile.dt:.4f} fs")
        print(f"Start in absolute: {profile.start_time:.4f} fs")
        print(f"End in absolute  : {profile.end_time:.4f} fs")
        print(f"Start in elapsed : {profile.elapsed_time[0]:.4f} fs")
        print(f"End in elapsed   : {profile.elapsed_time[-1]:.4f} fs")
        if verbose and (profile.parent is not None):
            name = profile.parent.operation or "raw"
            print(f"Parent: {name}")
            print(f"Start in parent  : {profile.parent_time[0]:.4f} fs")
            print(f"End in parent    : {profile.parent_time[-1]:.4f} fs")
        print(f"Duration        : {profile.duration:.4f} fs")

    print()

    _print_statistics("Potential Energy (eV)", profile.stats["Epot"])
    _print_statistics("Kinetic Energy (eV)", profile.stats["Ekin"])
    _print_statistics("Total Energy (eV)", profile.stats["Etot"])
    _print_statistics("Temperature (K)", profile.stats["T_md"])
    _print_statistics("Pressure (kBar)", profile.stats["P_md"])

    if profile.has_variable_cell:
        _print_statistics("Volume (A^3)", profile.stats["V_md"])
        _print_statistics("a (A)", profile.stats["lat_a"])
        _print_statistics("b (A)", profile.stats["lat_b"])
        _print_statistics("c (A)", profile.stats["lat_c"])
        _print_statistics("alpha (deg.)", profile.stats["lat_alp"])
        _print_statistics("beta (deg.)", profile.stats["lat_bet"])
        _print_statistics("gamma (deg.)", profile.stats["lat_gam"])

    print("=" * 50)


def _print_statistics(title: str, stats: QuantityStatistics) -> None:

    if stats is None:
        print(f"{title}")
        print("    Not available")
        print()
        return

    print(title)
    print(f"    Mean : {stats.mean:12.6f}")
    print(f"    Std  : {stats.std:12.6f}")
    print()


# Slice하여 새로운 MDProfile 생성 (equilibration 자르기, block average 등에 사용)
def slice_profile(
    profile: MDProfile,
    start: int = 0,
    stop: Optional[int] = None,
) -> MDProfile:

    return MDProfile(
        parent=profile,
        operation="slice",

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
        stride=profile.stride,
        first_step=profile.step[start],
    )


def _slice_optional(
    arr: Optional[np.ndarray],
    start: int,
    stop: int,
) -> Optional[np.ndarray]:

    if arr is None:
        return None
    return arr[start:stop]


# Block average: 시간은 block마다 시작과 끝의 평균값 이용
def block_average(
    profile: MDProfile,
    block_size: int,
) -> MDProfile:

    if block_size < 1:
        raise ValueError("block_size must be positive.")

    if block_size > profile.nsteps:
        raise ValueError("block_size is larger than the trajectory length.")

    return MDProfile(
        parent=profile,
        operation="block_average",

        Epot=_block_average_array(profile.Epot, block_size),
        Ekin=_block_average_array(profile.Ekin, block_size),
        Etot=_block_average_array(profile.Etot, block_size),
        T_md=_block_average_array(profile.T_md, block_size),
        P_md=_block_average_array(profile.P_md, block_size),

        V_md=_block_average_array(profile.V_md, block_size),
        lat_a=_block_average_array(profile.lat_a, block_size),
        lat_b=_block_average_array(profile.lat_b, block_size),
        lat_c=_block_average_array(profile.lat_c, block_size),
        lat_alp=_block_average_array(profile.lat_alp, block_size),
        lat_bet=_block_average_array(profile.lat_bet, block_size),
        lat_gam=_block_average_array(profile.lat_gam, block_size),

        dt=profile.dt,
        stride=profile.stride * block_size,
        first_step = profile.step[block_size // 2],
    )


def _block_average_array(arr: Optional[np.ndarray], block_size: int) -> Optional[np.ndarray]:

    if arr is None:
        return None

    if block_size == 1:
        return arr.copy()

    nblock = len(arr) // block_size
    arr = arr[: nblock * block_size]
    arr = arr.reshape(nblock, block_size)
    return np.mean(arr, axis=1)
