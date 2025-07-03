import mitsuba as mi

class ConstantTexture(mi.Texture):
    def __init__(self, props:mi.Properties, name: str):
        mi.Texture.__init__(self, props)
        self.value = props.get(name, 0.0)
        props.mark_queried(name)
    
    def eval_1(self, si, active = True):
        return mi.Float(self.value)

    def to_string(self) -> str:
        return f"ConstantTexture[delay = {self.value}]"