# VASP 결과 중 REPORT 파일을 읽어줌
# 이 스크립트는 TI를 활용한 purely harmonic system에 대한 것 (즉, 특수상황)

from pathlib import Path
import numpy as np
from typing import Dict, List

from ..model.md_profile import MDProfile


def _parse_report_line_pureHO(line: str, data: Dict[str, List[float]]) -> None:
    """Parse a single line of VASP REPORT."""

    line = line.replace(">", "")
    fields = line.split()

    if not fields:
        return

    if fields[0] == "e_b":
        data["Ekin"].append(float(fields[3]))

    elif fields[0] == "e_ti":
        data["Epot"].append(float(fields[1]))

    elif fields[0] == "tmprt":
        data["T_md"].append(float(fields[2]))

    # 나중에 NPT 확장은 여기 추가
    #
    # elif fields[0] == "...":
    #     data["P_md"].append(...)
    #
    # elif fields[0] == "...":
    #     data["V_md"].append(...)


def read_report_pureHO(filename: Path, verbose: bool = False) -> MDProfile:

    data = {
        "Epot": [],
        "Ekin": [],
        "T_md": [],
    }

    with open(filename, "r") as f:
        for line in f:
            _parse_report_line_pureHO(line, data)

    if verbose:
        _print_loaded_data(data)

    _validate_data(data)

    epot = np.asarray(data["Epot"])
    ekin = np.asarray(data["Ekin"])
    temp = np.asarray(data["T_md"])

    return MDProfile(
        Epot=epot,
        Ekin=ekin,
        Etot=epot + ekin,
        T_md=temp,
    )

def _validate_data(data: Dict[str, List[float]]) -> None:

    n = len(data["Epot"])

    if len(data["Ekin"]) != n:
        raise ValueError("Different data length!!")

    if len(data["T_md"]) != n:
        raise ValueError("Different data length!!")


def _print_loaded_data(data: Dict[str, List[float]]) -> None:

    for key, value in data.items():
        print(f"{key:6s}: {len(value)}")
