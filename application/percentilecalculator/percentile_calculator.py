class PercentileCalculator:
    """Computes percentile ranks for labeled stat values against the input cohort."""

    def calculate(self, entries: dict[str, float | int]) -> dict[str, int]:
        if not entries:
            return {}

        values = [float(value) for value in entries.values()]
        population_size = len(values)

        return {
            label: self._percentile_rank(float(stat), values, population_size)
            for label, stat in entries.items()
        }

    @staticmethod
    def _percentile_rank(value: float, population: list[float], size: int) -> int:
        rank = sum(1 for v in population if v <= value)
        return round(rank / size * 100)
