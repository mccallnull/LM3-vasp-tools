# VASP의 INCAR 파일을 읽어줌
# 지금은 POTIM만 parser에 들어감.

from pathlib import Path

from ..model.incar_tags import INCAR

def _parse_incar_line(line: str, data: dict) -> None:
    """Parse a single line of VASP INCAR/"""

    fields = line.replace("=", " ").split()

    if not fields:
        return

    if fields[0] == "POTIM":
        data["potim"] = float(fields[1])
    elif fields[0] == "ML_OUTBLOCK":
        data["ml_outblock"] = int(fields[1])

    # 이후 더 필요한 tag는 여기 추가


def read_incar(filename: Path) -> INCAR:

    data = {
        "potim": None,
        "ml_outblock": 1,
    }

    with open(filename, "r") as f:
        for line in f:
            _parse_incar_line(line, data)

    _validate_data(data)

    return INCAR(
        potim=data["potim"],
        ml_outblock=data["ml_outblock"]
    )

def _validate_data(data: dict) -> None:

    if data["potim"] is None:
        raise ValueError("No POTIM in INCAR!!")
