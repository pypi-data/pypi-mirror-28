"""Test GammaProcess."""
# flake8: noqa
import pytest

from stochastic.continuous import GammaProcess


def test_gamma_process_init(t, mean_fixture, variance_fixture, rate_fixture, scale_fixture):
    first_params = bool(mean_fixture) + bool(variance_fixture)
    second_params = bool(rate_fixture) + bool(scale_fixture)
    all_params = first_params + second_params
    if all_params != 2 or (first_params != 2 and second_params != 2):
        with pytest.raises((TypeError, ValueError)):
            instance = GammaProcess(t, mean_fixture, variance_fixture, rate_fixture, scale_fixture)
    else:
        instance = GammaProcess(t, mean_fixture, variance_fixture, rate_fixture, scale_fixture)
        assert isinstance(repr(instance), str)
        assert isinstance(str(instance), str)

def test_gamma_process_str_repr(t, mean, variance):
    instance = GammaProcess(t, mean, variance)
    assert isinstance(repr(instance), str)
    assert isinstance(str(instance), str)

def test_gamma_process_sample(t, mean, variance, n, zero, threshold):
    instance = GammaProcess(t, mean, variance)
    s = instance.sample(n, zero)
    assert len(s) == n + int(zero)

def test_gamma_process_sample_at(t, mean, variance, times, threshold):
    instance = GammaProcess(t, mean, variance)
    s = instance.sample_at(times)
    assert len(s) == len(times)
