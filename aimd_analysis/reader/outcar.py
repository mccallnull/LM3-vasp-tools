# VASP 결과 중 OUTCAR 파일을 읽어줌
# 현재는 NVT 전용 (이후 NPT까지 커버하도록 확장.)

from pathlib import Path
import numpy as np

from ..model.md_profile import MDProfile


def _parse_outcar_line(line: str, data: dict) -> None:
    """Parse a single line of VASP OUTCAR."""

    line = line.replace("=", " = ")
    fields = line.split()

    if not fields:
        return
    #여기서부터가 핵심적으로 바꿔야 할 부분(수정됨.)
    if len(fields) >= 3 and fields[0] == "POTIM":
        data["dt"] = float(fields[2])

    elif len(fields) >= 3 and fields[0] == "ISIF":
        data["isif"] = int(fields[2])
        data["_variable_cell"] = data["isif"] in (3,4)

    elif len(fields) >= 4 and fields[1:3] == ["Ionic", "step"]:
        data["_in_ionic_steps"] = True

    elif data["_in_ionic_steps"]:
        if data["_reading_lattice"]:
            data["_lattice_buffer"].append(
                [float(x) for x in fields[:3]]
            )

            if len(data["_lattice_buffer"]) == 3:
                data["lat_vecs"].append(data["_lattice_buffer"])
                data["_lattice_buffer"] = []
                data["_reading_lattice"] = False

        elif len(fields) >= 5 and fields[1] == "ion-electron":
            data["Epot"].append(float(fields[4]))

        elif len(fields) >= 5 and fields[2] == "EKIN":
            data["_ekin"] = float(fields[4])

        elif len(fields) >= 6 and fields[2] == "EKIN_LAT":
            data["_ekin_lat"] = float(fields[4])

            data["Ekin"].append(data["_ekin"] + data["_ekin_lat"])
            data["T_md"].append(float(fields[6]))

        elif len(fields) >= 5 and fields[:2] == ["total", "pressure"]:
            data["P_md"].append(float(fields[3]))

        elif len(fields) >= 5 and fields[:3] == ["volume", "of", "cell"] and data["_variable_cell"]:
            data["V_md"].append(float(fields[4]))

        elif fields[:3] == ["direct", "lattice", "vectors"] and data["_variable_cell"]:
            data["_reading_lattice"] = True
            data["_lattice_buffer"] = []


def read_outcar(filename: Path, verbose: bool = False) -> MDProfile:

    data = {
        "Epot": [],
        "Ekin": [],
        "T_md": [],
        "P_md": [],
        "V_md": [],
        "lat_vecs": [],
        "dt": None,
        "isif": None,

        "_ekin": None,
        "_ekin_lat": None,
        "_in_ionic_steps": False,
        "_reading_lattice": False,
        "_lattice_buffer": [],
        "_variable_cell": False,
    }

    with open(filename, "r") as f:
        for line in f:
            _parse_outcar_line(line, data)

    if verbose:
        _print_loaded_data(data)

    _validate_data(data)

    epot = np.asarray(data["Epot"])
    ekin = np.asarray(data["Ekin"])
    temperature = np.asarray(data["T_md"])
    pressure = np.asarray(data["P_md"])

    volume = (
        np.asarray(data["V_md"])
        if data["_variable_cell"]
        else None
    )

    lat_vecs = (
        np.asarray(data["lat_vecs"])
        if data["_variable_cell"]
        else None
    )

    return MDProfile(
        Epot=epot,
        Ekin=ekin,
        Etot=epot + ekin,
        T_md=temperature,
        dt=data["dt"],
        stride=1,
        P_md=pressure,
        V_md=volume,
        lat_vecs=lat_vecs
    )

def _validate_data(data: dict) -> None:

    n = len(data["Epot"])

    if len(data["Ekin"]) != n:
        raise ValueError("Different data length!!")

    if len(data["T_md"]) != n:
        raise ValueError("Different data length!!")

    if len(data["P_md"]) != n:
        raise ValueError("Different data length!!")

    if data["_variable_cell"]:

        if len(data["V_md"]) != n:
            raise ValueError("Different data length!!")

        if len(data["lat_vecs"]) != n:
            raise ValueError("Different data length!!")


def _print_loaded_data(data: dict) -> None:

    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key:6s}: {len(value)}")
        else:
            print(f"{key:6s}: {value}")
