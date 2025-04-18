import mitsuba as mi

class TemporalProfile(mi.Object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create(props: mi.Properties) -> "TemporalProfile":
        raise NotImplementedError("\"create\" method must be implemented in subclass")

    def sample_delay(self, si:mi.SurfaceInteraction3f, sample1:mi.Point2f) -> mi.Float:
        raise NotImplementedError("\"sample_delay\" method must be implemented in subclass")
    
    def eval_delay(self, delay:mi.Float) -> mi.Float:
        raise NotImplementedError("\"eval_delay\" method must be implemented in subclass")

    def to_string(self) -> str:
        raise NotImplementedError("\"to_string\" method must be implemented in subclass")

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()