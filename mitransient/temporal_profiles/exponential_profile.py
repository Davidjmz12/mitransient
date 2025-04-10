import mitsuba as mi
from mitransient.temporal_profiles.common import TemporalProfile
import drjit as dr

class ExponentialProfile(TemporalProfile):
    def __init__(self, lambd:float):
        super().__init__()
        self.lambd = lambd

    def to_string(self) -> str:
        return f"ExponentialProfile[mean = {self.lambd}]"

    @staticmethod
    def create(props: mi.Properties) -> TemporalProfile:
        props.mark_queried('mean')
        mean = float(props.get('mean', 0.0))

        if mean < 0.0:
            raise ValueError(f"ExponentialProfile mean is negative: {mean}")
        return ExponentialProfile(mean)

    def sample_delay(self, si, sample1):
        return mi.Float(-1.0)/mi.Float(self.lambd)*dr.log(mi.Float(1)-sample1.x)
    
    def eval_delay(self, delay, si):
        return mi.Float(self.lambd)*dr.exp(-mi.Float(delay)*mi.Float(self.lambd))