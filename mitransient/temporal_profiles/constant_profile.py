import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class ConstantProfile(mi.TemporalProfile):
    def __init__(self, props:mi.Properties):
        mi.TemporalProfile.__init__(self, props)
        
        self.delay = TransientTexture(props, "delay")

    def to_string(self) -> str:
        return f"ConstantProfile[delay = {self.delay}]"

    def sample_delay(self, si:mi.SurfaceInteraction3f, sample1):
        delay_value = self.delay.eval_1(si)
        dr.assert_true(delay_value >= 0, "Delay must be non-negative for ConstantProfile")
        dr.print("\n{foo}",
         "A PyTree containing an array",
         foo={ 'a' : delay_value, }, limit=1000)
        return delay_value

    def eval_delay(self, delay, si):
        prop = self.delay.pdf_spectrum(si)
        return dr.select(delay == self.delay.eval_1(si), 
                         1.0, 
                         0.0)* prop

mi.register_temporal_profile("ConstantTP", lambda props: ConstantProfile(props))