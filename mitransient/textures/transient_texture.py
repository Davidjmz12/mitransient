import mitsuba as mi
import drjit as dr

from mitransient.textures.constant_texture import ConstantTexture

class TransientTexture(mi.Texture):
    r"""
    
    .. texture-transient:

    Transient Texture (:monosp:`TransientTexture`)
    -------------------------------------------------

    A wrapper class that allows the use of either a constant float value or a texture as input for transient properties.
    This class ensures that the input value adheres to specified constraints through a user-defined checking function.

    .. pluginparameters::
        * - name
            - |string|
            - The name of the property to be used as the texture or constant value.
            This property can either be a float or a texture.
            If it is a float, it will be wrapped in a ConstantTexture.
        * - check_func
            - |function|
            - A user-defined function that takes a float value as input and raises an error if the value does not meet the required constraints.
            This function is called whenever the texture is evaluated to ensure that the value is valid.
            This ensures that the texture values are always valid according to the specified constraints.
    """
    def __init__(self, props:mi.Properties, name: str, check_func):
        mi.Texture.__init__(self, props)
        
        self.check_func = check_func

        if props.has_property(name):
            if props.type(name) == mi.Properties.Type.Object:
                self.texture = props.get(name)
            elif props.type(name) == mi.Properties.Type.Float:
                self.texture = ConstantTexture(props, name)
            else:
                raise ValueError(f"TransientTexture: `{name}` must be a float or a texture")
            props.mark_queried(name)
        else:
            raise ValueError(f"TransientTexture: `{name}` property must be specified")
        
    def eval_1(self, si, active = True):
        value = self.texture.eval_1(si, active)
        self.check_func(value)

        return dr.select(active, value, 0.0)

    def to_string(self) -> str:
        return f"TransientTexture[texture = {self.texture}]"
    