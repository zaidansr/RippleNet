"""Synthetic research components; no trained financial forecasting model."""

from .simulation import Config, Event, GroundTruth, Observations, Simulation, paired_worlds, simulate

__all__ = ["Config", "Event", "GroundTruth", "Observations", "Simulation", "paired_worlds", "simulate"]
