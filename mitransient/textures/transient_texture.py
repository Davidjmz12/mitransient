import mitsuba as mi
import drjit as dr

from mitransient.textures.constant_texture import ConstantTexture

class TransientTexture(mi.Texture):
    def __init__(self, props:mi.Properties, name: str):
        mi.Texture.__init__(self, props)
        
        if props.has_property(name):
            if props.type(name) == mi.Properties.Type.Object:
                self.texture = props.get(name)
                self.prop = 1/dr.prod(self.texture.resolution())
            elif props.type(name) == mi.Properties.Type.Float:
                self.texture = ConstantTexture(props, name)
                self.prop = 1
            else:
                raise ValueError(f"TransientTexture: `{name}` must be a float or a texture")
            props.mark_queried(name)
        else:
            raise ValueError(f"TransientTexture: `{name}` property must be specified")
        
    def eval_1(self, si, active = True):
        return self.texture.eval_1(si, active)

    def pdf_spectrum(self, si, active = True):
        return dr.select(active, self.prop, 0.0)

    def to_string(self) -> str:
        return f"TransientTexture[texture = {self.texture}]"
    