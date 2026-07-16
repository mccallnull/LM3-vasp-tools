from dataclasses import dataclass
from dataclasses import field
from typing import Dict, Optional
import numpy as np

from .quantity_statistics import QuantityStatistics


@dataclass
class MDProfile:

    # 어떤 profile로부터 유도된 프로파일이라면....
    parent: Optional["MDProfile"] = field(
        default=None,
        repr=False,
    )

    operation: Optional[str] = field(default=None)

    # NVT에서 기본적으로 추출할 것들.
    step: np.ndarray = field(default=None)
    Epot: np.ndarray = field(default=None)
    Ekin: np.ndarray = field(default=None)
    Etot: np.ndarray = field(default=None)
    T_md: np.ndarray = field(default=None)

    # NPT라면, 이것들도 추가로 추출할 것.
    P_md: Optional[np.ndarray] = field(default=None)
    V_md: Optional[np.ndarray] = field(default=None)
    lat_a: Optional[np.ndarray] = field(default=None)
    lat_b: Optional[np.ndarray] = field(default=None)
    lat_c: Optional[np.ndarray] = field(default=None)
    lat_alp: Optional[np.ndarray] = field(default=None)
    lat_bet: Optional[np.ndarray] = field(default=None)
    lat_gam: Optional[np.ndarray] = field(default=None)

    # 실제 timestep (in fs) --> 실제 시간을 쓰려면, step * dt 를 하도록. (INCAR reading 필요.)
    dt: Optional[float] = field(default=None)

    # 추출한 것들의 통계자료
    stats: Dict[str, QuantityStatistics] = field(
        default_factory=dict
    )

    # 다른 유도 properties(추출하는 것들로부터 계산되는 것들)는 여기.
    @property
    def nsteps(self):
        if self.step is None:
            return 0
        return len(self.step)

    @property
    def time(self):
        if self.dt is None:
            return None
        return (self.step - 1) * self.dt

    @property
    def start_time(self):
        if self.dt is None:
            return None
        return self.time[0]

    @property
    def end_time(self):
        if self.dt is None:
            return None
        return self.time[-1]

    @property
    def duration(self):
        if self.dt is None:
            return None
        return self.end_time - self.start_time

    @property
    def elapsed_time(self):
        if self.dt is None:
            return None
        return self.time - self.time[0]

    @property
    def parent_time(self):
        if self.parent is None or self.dt is None:
            return None

        return self.time - self.parent.start_time

    @property
    def has_pressure(self): # NPT인지를 판가름할 때 편할 듯.
        return self.P_md is not None
