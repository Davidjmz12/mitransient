import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class ConstantProfile(mi.TemporalProfile):
    def __init__(self, props:mi.Properties):
        mi.TemporalProfile.__init__(self, props)
        
        def check_delay(value):
            dr.assert_true(value >= 0, "Delay must be non-negative for ConstantProfile")

        self.delay = TransientTexture(props, "delay", check_delay)

    def to_string(self) -> str:
        return f"ConstantProfile[delay = {self.delay}]"

    def sample_delay(self, si:mi.SurfaceInteraction3f, sample1):
        delay_value = self.delay.eval_1(si)
        return delay_value

    def eval_delay(self, delay, si):
        return dr.select(delay == self.delay.eval_1(si), 
                         1.0, 
                         0.0)

mi.register_temporal_profile("ConstantTP", lambda props: ConstantProfile(props))