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

    def temporal_delay(self, si:mi.SurfaceInteraction3f, sample1:mi.Point2f) -> mi.Float:
        delay = self.texture.eval_1(si)
        return delay