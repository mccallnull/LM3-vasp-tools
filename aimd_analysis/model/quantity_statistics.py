from dataclasses import dataclass


@dataclass
class QuantityStatistics:

    mean: float
    std: float

    min: float
    max: float
