import mitsuba as mi
import drjit as dr

class ExponentialProfile(mi.TemporalProfile):
    def __init__(self, props: mi.Properties):
        mi.TemporalProfile.__init__(self, props)
        self._lambda = props.get('lambda', 1.0)
        props.mark_queried('lambda')

    def to_string(self) -> str:
        return f"ExponentialProfile[lambda = {self.lambd}]"

    def sample_delay(self, si, sample1):
        return mi.Float(-1.0)/mi.Float(self.lambd)*dr.log(mi.Float(1)-sample1.x)
    
    def eval_delay(self, delay, si):
        return mi.Float(self.lambd)*dr.exp(-mi.Float(delay)*mi.Float(self.lambd))
    
mi.register_temporal_profile("ExponentialTP", lambda props: ExponentialProfile(props))