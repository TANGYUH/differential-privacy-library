"""
Core utilities for DP transformers.
"""
from diffprivlib.mechanisms.base import DPMachine


class DPTransformer(DPMachine):
    """
    Base class for DP transformers. DP Transformers are simple wrappers for DP Mechanisms to allow mechanisms to be used
    with data types and structures outside their scope.
    """
    def __init__(self, parent):
        if not isinstance(parent, DPMachine):
            raise TypeError("Data transformer must take a DPMachine as input")

        self.parent = parent

    def pre_transform(self, value):
        """
        Transforms the input data to be ingested by the differential privacy mechanism.

        :param value: Input value to be transformed.
        :type value: `float` or `string`
        :return: Transformed input value.
        :rtype: `float` or `string`
        """
        return value

    def post_transform(self, value):
        """
        Transforms the output of the differential privacy mechanism to resemble the input data.

        :param value: Mechanism output to be transformed.
        :type value: `float` or `string`
        :return: Transformed output value.
        :rtype: `float` or `string`
        """
        return value

    def set_epsilon(self, epsilon):
        """
        Sets the value of epsilon to be used by the mechanism.

        :param epsilon: Epsilon value for differential privacy.
        :type epsilon: `float`
        :return: self
        :rtype: :class:`.DPMachine`
        """
        self.parent.set_epsilon(epsilon)
        return self

    def set_epsilon_delta(self, epsilon, delta):
        """
        Set the privacy parameters epsilon and delta for the mechanism.

        Epsilon must be non-negative, epsilon >= 0. Delta must be on the unit interval, 0 <= delta <= 1. At least
        one or epsilon and delta must be non-zero.

        Pure (strict) differential privacy is given when delta = 0. Approximate (relaxed) differential privacy is given
        when delta > 0.

        :param epsilon: Epsilon value of the mechanism.
        :type epsilon: `float`
        :param delta: Delta value of the mechanism.
        :type delta: `float`
        :return: self
        :rtype: :class:`.DPMachine`
        """
        self.parent.set_epsilon_delta(epsilon, delta)
        return self

    def randomise(self, value):
        """
        Randomise the given value using the :class:`.DPMachine`.

        :param value: Value to be randomised.
        :type value: `float` or `string`
        :return: Randomised value, same type as value.
        :rtype: `float` or `string`
        """
        transformed_value = self.pre_transform(value)
        noisy_value = self.parent.randomise(transformed_value)
        output_value = self.post_transform(noisy_value)
        return output_value