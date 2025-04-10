import mitsuba as mi
from mitransient.temporal_profiles.common import TemporalProfile


class ConstantTextureProfile(TemporalProfile):
    def __init__(self, texture:mi.Texture):
        super().__init__()
        self.texture = texture

    def to_string(self) -> str:
        return f"ConstantTextureProfile[texture = {self.texture}]"

    @staticmethod
    def create(props: mi.Properties) -> TemporalProfile:
        props.mark_queried('delay-texture')

        texture = props.get('delay-texture')
        return ConstantTextureProfile(texture)

    def sample_delay(self, si, sample1):
        return self.texture.eval_1(si)
    
    def eval_delay(self, delay, si):
        raise NotImplementedError("eval_delay not implemented for ConstantTextureProfile")