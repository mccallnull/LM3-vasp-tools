# VASP의 INCAR 파일을 읽어줌
# 지금은 POTIM만 parser에 들어감.

from pathlib import Path
import numpy as np

from ..model.incar_tags import INCARtags

def _parse_report_line_incar(line: str, data: dict):
    """Parse a single line of VASP INCAR/"""

    fields = line.replace("=", " ").split()

    if not fields:
        return
    
    if fields[0] == "POTIM":
        data["potim"].append(int(fields[1]))

    # 이후 더 필요한 tag는 여기 추가


def read_incar(filename: Path) -> INCARtags:

    data = {
        "potim": float,
    }

    with filename.open("r") as f:
        for line in f:
            _parse_report_line_incar(line, data)

    _validate_data(data)

    return INCARtags(
        potim=data["potim"],
    )

def _validate_data(data):

    if data["potim"] == None:
        raise ValueError("No POTIM in INCAR!!")