from pathlib import Path

from ..model.model import StaticOutcar


def read_static_outcar(path: str) -> StaticOutcar:
    """Read a static VASP OUTCAR."""

    path = Path(path)

    encut = None
    volume = None
    external_pressure = None
    energy = None

    with path.open("r") as f:
        for line in f:

            if "ENCUT" in line:
                encut = float(line.split()[2])

            if "volume of cell" in line:
                volume = float(line.split(":")[-1].strip())

            if "external pressure" in line:
                external_pressure = float(line.replace("=", " = ").split()[3])

            if "free  energy   TOTEN" in line:
                energy = float(line.split("=")[1].split()[0])

    # validation
    if encut is None:
        raise ValueError(f"ENCUT was not found in {path}")

    if volume is None:
        raise ValueError(f"Cell volume was not found in {path}")

    if external_pressure is None:
        raise ValueError(f"External pressure was not found in {path}")

    if energy is None:
        raise ValueError(f"TOTEN was not found in {path}")


    return StaticOutcar(
        energy=energy,
        volume=volume,
        external_pressure=external_pressure,
        encut=encut,
    )
