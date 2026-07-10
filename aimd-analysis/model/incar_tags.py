from dataclasses import dataclass
from dataclasses import field

@dataclass
class INCARtags:

    # 일단 지금은 POTIM만 추출. 나중에 필요시 하나하나 넣을 것.
    potim: float = field(default=None)