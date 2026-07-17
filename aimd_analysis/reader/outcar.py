# VASP 결과 중 OUTCAR 파일을 읽어줌
# 현재는 NVT 전용 (이후 NPT까지 커버하도록 확장.)

from pathlib import Path
import numpy as np

from ..model.md_profile import MDProfile


def _parse_outcar_line(line: str, data: dict) -> None:
    """Parse a single line of VASP REPORT."""

    line = line.replace("=", " = ")
    fields = line.split()

    if not fields:
        return
    #여기서부터가 핵심적으로 바꿔야 할 부분(수정됨.)
    if len(fields) >= 4 and fields[1:3] == ["Ionic", "step"]:
        data["step"].append(int(fields[3]))

    elif len(fields) >= 5 and fields[1] == "ion-electron":
        data["Epot"].append(float(fields[4]))

    elif len(fields) >= 5 and fields[2] == "EKIN":
        data["_ekin"] = float(fields[4])

    elif len(fields) >= 6 and fields[2] == "EKIN_LAT":
        data["_ekin_lat"] = float(fields[4])

        data["Ekin"].append(data["_ekin"] + data["_ekin_lat"])
        data["T_md"].append(float(fields[6]))

    elif len(fields) >= 3 and fields[0] == "POTIM":
        data["dt"] = float(fields[2])
    #바꿔야 할 부분 끝.

    # 나중에 NPT 확장은 여기 추가
    #
    # elif fields[0] == "...":
    #     data["P_md"].append(...)
    #
    # elif fields[0] == "...":
    #     data["V_md"].append(...)


def read_outcar(filename: Path, verbose: bool = False) -> MDProfile:

    data = {
        "step": [],
        "Epot": [],
        "Ekin": [],
        "T_md": [],
        "dt": None,

        "_ekin": None,
        "_ekin_lat": None,
    }

    with open(filename, "r") as f:
        for line in f:
            _parse_outcar_line(line, data)

    if verbose:
        _print_loaded_data(data)

    _validate_data(data)

    step_ = np.asarray(data["step"])
    epot = np.asarray(data["Epot"])
    ekin = np.asarray(data["Ekin"])
    temp = np.asarray(data["T_md"])
    dt = data["dt"]

    return MDProfile(
        step=step_,
        Epot=epot,
        Ekin=ekin,
        Etot=epot + ekin,
        T_md=temp,
        dt=dt,
    )

def _validate_data(data: dict) -> None:

    n = len(data["step"])

    if len(data["Epot"]) != n:
        raise ValueError("Different data length!!")

    if len(data["Ekin"]) != n:
        raise ValueError("Different data length!!")

    if len(data["T_md"]) != n:
        raise ValueError("Different data length!!")


def _print_loaded_data(data: dict) -> None:

    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key:6s}: {len(value)}")
        else:
            print(f"{key:6s}: {value}")
