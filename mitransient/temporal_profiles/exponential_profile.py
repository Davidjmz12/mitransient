import mitsuba as mi
from mitransient.temporal_profiles.common import TemporalProfile
import drjit as dr

class ExponentialProfile(TemporalProfile):
    def __init__(self, mean:float):
        super().__init__()
        self.mean = mean

    def to_string(self) -> str:
        return f"ExponentialProfile[mean = {self.mean}]"

    @staticmethod
    def create(props: mi.Properties) -> TemporalProfile:
        props.mark_queried('mean')
        mean = float(props.get('mean', 0.0))

        if mean < 0.0:
            raise ValueError(f"ExponentialProfile mean is negative: {mean}")
        return ExponentialProfile(mean)

    def temporal_delay(self, si:mi.SurfaceInteraction3f, sample1:mi.Point2f) -> mi.Float:
        return mi.Float(-1.0)/mi.Float(self.mean)*dr.log(mi.Float(1)-sample1.x)