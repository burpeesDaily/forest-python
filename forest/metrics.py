# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Metrics model to measure tree performance."""

import numpy as np

from typing import Dict, List, Union


class Counter:
    """An incrementing and decrementing counter metric."""

    def __init__(self) -> None:
        self._count = 0

    def increase(self, n: int = 1) -> None:
        """Increment the counter.

        Parameters
        ----------
        n: `int`
            The count to be increased.
        """
        self._count += n

    def decrease(self, n: int = 1) -> None:
        """Decrement the counter.

        Parameters
        ----------
        n: `int`
            The count to be decreased.
        """
        self._count -= n

    @property
    def count(self) -> int:
        """Return the current count."""
        return self._count


class Histogram:
    """A metric which calculates the distribution of a value."""

    def __init__(self) -> None:
        self._values: List[int] = list()

    def update(self, value: int) -> None:
        """Add a recorded value.

        Parameters
        ----------
        value: `int`
            value to be updated
        """
        self._values.append(value)

    def report(self) -> Dict:
        """Return the histogram report."""
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
                "99": np.percentile(array, 99),
            },
        }


MetricType = Union[Counter, Histogram]
"""Alias for the supported metric types."""


class MetricRegistry:
    """A registry for metric instances."""

    def __init__(self) -> None:
        self._registry: Dict[str, MetricType] = dict()

    def register(self, name: str, metric: MetricType) -> None:
        """Given a metric, register it under the given name.

        Parameters
        ----------
        name: `str`
            The name of the metric

        metric: `MetricType`
            The type of the metric
        """
        self._registry[name] = metric

    def get_metric(self, name: str) -> MetricType:
        """Return the metric by the given name.

        Parameters
        ----------
        name: `str`
            The name of the metric

        Returns
        -------
        `MetricType`
            The metric instance by the given name.
        """
        return self._registry[name]
