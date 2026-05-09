from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionOption:
    name: str
    expected_error: float
    harm_risk: float = 0.0
    falsehood_risk: float = 0.0
    governance_risk: float = 0.0
    notes: str = ""

    def total_risk(self) -> float:
        values = [
            self.expected_error,
            self.harm_risk,
            self.falsehood_risk,
            self.governance_risk,
        ]

        for value in values:
            if value < 0:
                raise ValueError("Risk values must be non-negative.")

        return sum(values)


def choose_min_expected_error(options):
    """Choose the option with the lowest combined expected risk.

    Truthkind rule:
    This is a governance helper, not an oracle.
    Human authority remains final.
    """

    options = list(options)

    if not options:
        raise ValueError("At least one decision option is required.")

    return min(options, key=lambda option: (option.total_risk(), option.name))
