import mitsuba as mi
from mitransient.temporal_profiles.common import TemporalProfile


class ConstantProfile(TemporalProfile):
    def __init__(self, delay:float):
        super().__init__()
        self.delay = delay

    def to_string(self) -> str:
        return f"ConstantProfile[delay = {self.delay}]"

    @staticmethod
    def create(props: mi.Properties) -> TemporalProfile:
        props.mark_queried('delay')
        delay = float(props.get('delay', 0.0))
        return ConstantProfile(delay)

    def temporal_delay(self, si:mi.SurfaceInteraction3f, sample1:mi.Point2f) -> mi.Float:
        return mi.Float(self.delay)