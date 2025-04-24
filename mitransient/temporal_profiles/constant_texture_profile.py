import mitsuba as mi

class ConstantTextureProfile(mi.TemporalProfile):
    def __init__(self, texture:mi.Texture):
        super().__init__()
        self.texture = texture

    def to_string(self) -> str:
        return f"ConstantTextureProfile[texture = {self.texture}]"

    def sample_delay(self, si, sample1):
        return self.texture.eval_1(si)
    
    def eval_delay(self, delay, si):
        raise NotImplementedError("eval_delay not implemented for ConstantTextureProfile")
    
mi.register_temporal_profile("constant-texture", lambda props: ConstantTextureProfile(props))