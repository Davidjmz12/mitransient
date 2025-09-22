import mitsuba as mi
import drjit as dr
from mitransient.textures.transient_texture import TransientTexture

class ExponentialProfile(mi.TemporalProfile):
    r"""

    .. temporalprofile-exponential:
    
    Exponential Temporal Profile (:monosp:`ExponentialTP`)
    -------------------------------------------------

    A temporal profile that represents an exponential decay in light transport. 
    This profile is characterized by a decay rate (lambda), which defines how quickly the intensity of
    light interactions decreases over time.

    .. pluginparameters::
        * - lambda
            - |TransientTexture|
            - The decay rate, represented as a transient texture.
            This allows for spatially varying decay rates across the surface.
            It must be strictly positive.
    """
    def __init__(self, props: mi.Properties):
        mi.TemporalProfile.__init__(self, props)

        def check_lambda(value):
            dr.assert_true(value > 0, "Lambda must be positive for ExponentialProfile")

        self.lambd = TransientTexture(props, "lambda", check_lambda)


    def to_string(self) -> str:
        return f"ExponentialProfile[lambda = {self.lambd}]"

    def sample_delay(self, si, sample1):
        lambda_value = self.lambd.eval_1(si)
        return mi.Float(-1.0)/mi.Float(lambda_value)*dr.log(mi.Float(1)-sample1)
    
    def eval_delay(self, delay, si):
        lambda_value = self.lambd.eval_1(si)
        return mi.Float(lambda_value)*dr.exp(-mi.Float(delay)*mi.Float(lambda_value))
    
mi.register_temporal_profile("ExponentialTP", lambda props: ExponentialProfile(props))