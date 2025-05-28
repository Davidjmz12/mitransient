import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class ExponentialProfile(mi.TemporalProfile):
    def __init__(self, props: mi.Properties):
        mi.TemporalProfile.__init__(self, props)

        self.lambd = TransientTexture(props, "lambda")


    def to_string(self) -> str:
        return f"ExponentialProfile[lambda = {self.lambd}]"

    def sample_delay(self, si, sample1):
        lambda_value = self.lambd.eval_1(si)
        return mi.Float(-1.0)/mi.Float(lambda_value)*dr.log(mi.Float(1)-sample1)
    
    def eval_delay(self, delay, si):
        lambda_value = self.lambd.eval_1(si)
        prop = self.lambd.pdf_spectrum(si)
        return mi.Float(lambda_value)*dr.exp(-mi.Float(delay)*mi.Float(lambda_value)) * prop
    
mi.register_temporal_profile("ExponentialTP", lambda props: ExponentialProfile(props))