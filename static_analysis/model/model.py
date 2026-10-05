from dataclasses import dataclass


@dataclass
class StaticOutcar:
    """Summary of a static VASP OUTCAR.

    Attributes
    ----------
    energy : float
        Final total energy in eV.
    volume : float
        Final cell volume in Angstrom^3.
    external_pressure : float
        Final external pressure in kbar.
    encut : float
        Plane-wave cutoff energy in eV.
    """

    energy: float
    volume: float
    external_pressure: float
    encut: float
