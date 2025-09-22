import mitsuba as mi

class Separable(mi.BSDF):
    """
    Class to represent a BSDF with a temporal delay profile.
    """

    def __init__(self, props):
        # Init the parent
        mi.BSDF.__init__(self, props)
        # Read the bsdf
        if not props.has_property("bsdf"):
            raise Exception("No bsdf specified")
        else:
            self.bsdf = props.get('bsdf')

        # Read the temporal profile
        self.tp = props.get('tp')
        if self.tp is None:
            raise Exception("No temporal profile specified")
        
        # Set flags equal to 'bsdf'
        self.m_components = self.bsdf.m_components
        self.m_flags = self.bsdf.m_flags

    def sample_t(self, ctx, si, sample1, sample2, active):

        bs, value = self.bsdf.sample(ctx, si, sample1, sample2, active)

        bs.pdf *= self.tp.eval_delay(sample1, si)

        delay = self.tp.sample_delay(si, sample1)
        
        return bs, value, delay

    def eval_t(self, ctx, si, wo, t, active):
        return self.bsdf.eval(ctx, si, wo, active)*self.tp.eval_delay(t, si)

    def pdf_t(self, ctx, si, wo, t, active):
        return  self.bsdf.pdf(ctx, si, wo, active)*self.tp.eval_delay(t, si)
    
    
    def traverse(self, cb):
        cb.put_parameter('tp', self.tp, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('bsdf', self.bsdf, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys=None):
        raise NotImplementedError("Not implemented yet...")

    def to_string(self):
        return f"Separable[bsdf = {self.bsdf}, tp = {self.tp}]"

mi.register_bsdf("Separable", lambda props: Separable(props))