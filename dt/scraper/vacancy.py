from dataclasses import dataclass


@dataclass(frozen=True)
class IVacancy:
    """Represents a job vacancy with detailed information."""

    title: str
    link: str
    company: str
    location: str
    description: str
