"""Unit tests for the metrics module."""

import pytest

from forest import metrics


def test_counter():
    """Test counter."""
    counter = metrics.Counter()

    counter.increase()
    assert counter.count == 1

    counter.increase(10)
    assert counter.count == 11

    counter.decrease()
    assert counter.count == 10

    counter.decrease(11)
    assert counter.count == -1


def test_histogram():
    """Test histogram."""
    histogram = metrics.Histogram()

    for value in range(0, 10):
        histogram.update(value=value)

    result = histogram.report()

    assert result["min"] == 0
    assert result["max"] == 9
    assert result["medium"] == pytest.approx(4.5)
    assert result["mean"] == pytest.approx(4.5)
    assert result["stdDev"] == pytest.approx(2.8, 0.1)
    assert result["percentile"]["75"] == pytest.approx(6.75)
    assert result["percentile"]["95"] == pytest.approx(8.5, 0.1)
    assert result["percentile"]["99"] == pytest.approx(9, 0.1)


def test_registry():
    """Test metrics registry."""
    counter = metrics.Counter()
    histogram = metrics.Histogram()
    registry = metrics.MetricsRegistry()
    registry.register("counter", counter)
    registry.register("histogram", histogram)

    assert registry.get_metric("counter") is counter
    assert registry.get_metric("histogram") is histogram
