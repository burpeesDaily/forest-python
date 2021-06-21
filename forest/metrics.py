# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Metrics model to measure tree performance."""

import numpy as np

from typing import Dict, List, Union


class Counter:

    def __init__(self) -> None:
        self._count = 0

    def increase(self, n: int = 1) -> None:
        self._count += n

    def decrease(self, n: int = 1) -> None:
        self._count -= n

    @property
    def count(self) -> int:
        return self._count


class Histogram:

    def __init__(self) -> None:
        self._values: List[int] = list()

    def update(self, value: int) -> None:
        self._values.append(value)

    def report(self) -> Dict:
        array = np.array(self._values)
        return {
            "min": array.min(),
            "max": array.max(),
            "medium": np.median(array),
            "mean": array.mean(),
            "stdDev": array.std(),
            "percentile": {
                "75": np.percentile(array, 75),
                "95": np.percentile(array, 95),
                "99": np.percentile(array, 99)
            }
        }


MetricType = Union[Counter, Histogram]


class MetricsRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, MetricType] = dict()

    def register(self, name: str, metric: MetricType) -> None:
        self._registry[name] = metric

    def get_metric(self, key: str) -> MetricType:
        return self._registry[key]
