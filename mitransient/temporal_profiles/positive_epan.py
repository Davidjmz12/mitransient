import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class PosEpanProfile(mi.TemporalProfile):
    def __init__(self, props: mi.Properties):
        r"""

        .. temporalprofile-positive_epan:

        Positive Epanechnikov Temporal Profile (:monosp:`PosEpanTP`)
        -------------------------------------------------

        A temporal profile that represents a positive Epanechnikov distribution in light transport. 
        This profile is characterized by a range and a shift parameter, which define the deviation and 
        mean of the distribution, respectively. The positive Epanechnikov distribution is a
        "bounded" gaussian-like distribution easy to sample from.

        .. pluginparameters::
            * - range
                - |TransientTexture|
                - The range (deviation) of the distribution, represented as a transient texture.
                This allows for spatially varying ranges across the surface.
                It must be strictly positive.
            * - shift
                - |TransientTexture|
                - The shift (mean) of the distribution, represented as a transient texture.
                This allows for spatially varying shifts across the surface.
                It must be non-negative and greater than or equal to the range to ensure positivity of delays.

        """
        mi.TemporalProfile.__init__(self, props)
        
        def check_range(value):
            dr.assert_true(value > 0, "Range must be positive for PosEpanProfile")
        def check_shift(value):
            dr.assert_true(value >= 0, "Shift must be non-negative for PosEpanProfile")

        self.range = TransientTexture(props, "range", check_range)
        self.shift = TransientTexture(props, "shift", check_shift)


    def to_string(self) -> str:
        return f"PosEpan[range = {self.range}, shift = {self.shift}]"

    def sample_delay(self, si, sample1):
        """ 
        Sample a delay from the positive Epanechnikov distribution.
        Extracted from: https://stats.stackexchange.com/questions/6643/what-is-the-closed-form-solution-for-the-inverse-cdf-for-epanechnikov 
        """
        range_value = self.range.eval_1(si)
        shift_value = self.shift.eval_1(si)

        dr.assert_true(shift_value >= range_value, "Shift value must be greater than or equal to range for PosEpanProfile") 

        return 2*range_value*dr.sin(1/3*dr.asin(2*sample1-1)) + shift_value

    def eval_delay(self, delay, si):
        range_value = self.range.eval_1(si)
        shift_value = self.shift.eval_1(si)

        dr.assert_true(shift_value >= range_value, "Shift value must be greater than or equal to range for PosEpanProfile") 
        
        pdf = 3/(4*range_value) * (1 - dr.power((delay - shift_value)/range_value, 2))
        return dr.minimum(dr.maximum(pdf, 0.0), 1.0)
    
mi.register_temporal_profile("PosEpanTP", lambda props: PosEpanProfile(props))