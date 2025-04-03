import mitsuba as mi
from mitransient.temporal_profiles.common import TemporalProfile
import drjit as dr

class GaussianProfile(TemporalProfile):
    def __init__(self, mean:float, sd:float):
        super().__init__()
        self.mean = mean
        self.sd = sd

    def to_string(self) -> str:
        return f"GaussianProfile[mean = {self.mean}, sd = {self.sd}]"

    @staticmethod
    def create(props: mi.Properties) -> TemporalProfile:
        props.mark_queried('mean')
        props.mark_queried('sd')
        mean = float(props.get('mean', 0.0))
        sd = float(props.get('sd', 1.0))

        if sd < 0.0:
            raise RuntimeError('sd must be positive')
        return GaussianProfile(mean, sd)

    def temporal_delay(self, si:mi.SurfaceInteraction3f, sample1:mi.Point2f) -> mi.Float:

        # Following the Box-Muller transform, sample a N(0,1) from two independent uniform U(0,1) samples

        return dr.maximum(
            dr.sqrt(mi.Float(-2) * dr.log(sample1.x))*dr.cos(mi.Float(2) * mi.Float(dr.pi) * sample1.y) * mi.Float(self.sd) + mi.Float(self.mean),
            mi.Float(0)
        )