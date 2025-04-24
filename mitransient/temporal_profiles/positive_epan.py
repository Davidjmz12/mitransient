import mitsuba as mi
import drjit as dr

class PosEpanProfile(mi.TemporalProfile):
    def __init__(self, props: mi.Properties):
        mi.TemporalProfile.__init__(self, props)
        self.range = props.get('range', 1.0)
        self.shift = props.get('shift', 1.0)

        assert self.range > 0, "Mean must be positive"
        assert self.shift > 0, "Shift must be positive"
        assert self.shift >= self.range, "Shift must be greater than or equal to range to be a valid Positive Epanechnikov profile"

        props.mark_queried('range')
        props.mark_queried('shift')

    def to_string(self) -> str:
        return f"PosEpan[range = {self.range}, shift = {self.shift}]"


    def sample_delay(self, si, sample1):
        """ 
        Sample a delay from the positive Epanechnikov distribution.
        Extracted from: https://stats.stackexchange.com/questions/6643/what-is-the-closed-form-solution-for-the-inverse-cdf-for-epanechnikov 
        """
        return 2*self.range*dr.sin(1/3*dr.asin(2*sample1.x-1)) + self.shift


    def eval_delay(self, delay, si):

        return dr.maximum(3/(4*self.range) * (1 - dr.power((delay - self.shift)/self.range, 2)), 0.0)
    
mi.register_temporal_profile("PosEpanTP", lambda props: PosEpanProfile(props))