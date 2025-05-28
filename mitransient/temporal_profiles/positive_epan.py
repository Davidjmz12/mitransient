import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class PosEpanProfile(mi.TemporalProfile):
    def __init__(self, props: mi.Properties):
        mi.TemporalProfile.__init__(self, props)
        
        self.range = TransientTexture(props, "range")
        self.shift = TransientTexture(props, "shift")


    def to_string(self) -> str:
        return f"PosEpan[range = {self.range}, shift = {self.shift}]"

    def sample_delay(self, si, sample1):
        """ 
        Sample a delay from the positive Epanechnikov distribution.
        Extracted from: https://stats.stackexchange.com/questions/6643/what-is-the-closed-form-solution-for-the-inverse-cdf-for-epanechnikov 
        """
        range_value = self.range.eval_1(si)
        dr.assert_true(range_value > 0, "Range must be positive for PosEpanProfile")
        shift_value = self.shift.eval_1(si)
        dr.assert_true(shift_value >= 0, "Shift must be non-negative for PosEpanProfile")
        dr.assert_true(shift_value >= range_value, "Delay must be greater than or equal to shift for PosEpanProfile") 

        return 2*range_value*dr.sin(1/3*dr.asin(2*sample1-1)) + shift_value

    def eval_delay(self, delay, si):
        range_value = self.range.eval_1(si)
        dr.assert_true(range_value > 0, "Range must be positive for PosEpanProfile")
        shift_value = self.shift.eval_1(si)
        dr.assert_true(shift_value >= 0, "Shift must be non-negative for PosEpanProfile")
        dr.assert_true(shift_value >= range_value, "Delay must be greater than or equal to shift for PosEpanProfile") 

        prop = dr.min(self.range.pdf_spectrum(si), self.shift.pdf_spectrum(si)) 
        pdf = 3/(4*range_value) * (1 - dr.power((delay - shift_value)/range_value, 2)) * prop
        return dr.maximum(pdf, 0.0)
    
mi.register_temporal_profile("PosEpanTP", lambda props: PosEpanProfile(props))