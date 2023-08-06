"""Specific data provider for Netherlands (nl)."""

from mimesis.builtins.base import BaseSpecProvider


class NetherlandsSpecProvider(BaseSpecProvider):
    """Class that provides special data for Netherlands (nl)."""

    class Meta:
        """The name of the provider."""

        name = 'netherlands_provider'

    def bsn(self) -> str:
        """Generate a random, but valid ``Burgerservicenummer``.

        :returns: Random BSN.

        :Example:
            255159705
        """
        def _is_valid_bsn(number: str) -> bool:
            total = 0
            multiplier = 9

            for char in number:
                multiplier = -multiplier if multiplier == 1 else multiplier
                total += int(char) * multiplier
                multiplier -= 1

            result = total % 11 == 0
            return result

        a, b = (100000000, 999999999)
        sample = str(self.random.randint(a, b))

        while not _is_valid_bsn(sample):
            sample = str(self.random.randint(a, b))

        return sample
