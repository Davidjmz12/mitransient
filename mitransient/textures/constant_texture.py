import mitsuba as mi

class ConstantTexture(mi.Texture):
    r"""
    
    .. texture-constant:

    Constant Texture (:monosp:`ConstantTexture`)
    -------------------------------------------------

    A simple texture that returns a constant value across the entire surface.
    .. pluginparameters::
        * - value
            - |float|
            - The constant value to be returned by the texture. Default is 0.0.
    """
    def __init__(self, props:mi.Properties, name: str):
        mi.Texture.__init__(self, props)
        self.value = props.get(name, 0.0)
        props.mark_queried(name)
    
    def eval_1(self, si, active = True):
        return mi.Float(self.value)

    def to_string(self) -> str:
        return f"ConstantTexture[delay = {self.value}]"