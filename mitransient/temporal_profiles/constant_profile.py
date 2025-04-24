import mitsuba as mi
import drjit as dr

class ConstantProfile(mi.TemporalProfile):
    def __init__(self, props):
        mi.TemporalProfile.__init__(self, props)
        self.delay = props.get('delay', 0.0)
        props.mark_queried('delay')

    def to_string(self) -> str:
        return f"ConstantProfile[delay = {self.delay}]"

    def sample_delay(self, si, sample1):
        return mi.Float(self.delay)

    def eval_delay(self, delay, si):
        return dr.select(delay == self.delay, 1.0, 0.0)

mi.register_temporal_profile("ConstantTP", lambda props: ConstantProfile(props))