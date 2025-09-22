import mitsuba as mi
import drjit as dr

class Composed(mi.BSDF):
    r"""

    .. bsdf-composed:

    Composed BSDF (:monosp:`Composed`)
    -------------------------------------------------

    A transient BSDF model that composes two other transient BSDFs, mixing their contributions based on a specified weight.

    .. pluginparameters::

        * - bsdf-1
            - |bsdf|
            - The first BSDF to be mixed.
        * - bsdf-2
            - |bsdf|
            - The second BSDF to be mixed.
        * - weight
            - |float|
            - The mixing weight for the first BSDF. Must be in the range [0, 1]. The weight for the second BSDF is implicitly (1 - weight).
    
    """

    def __init__(self, props):

        mi.BSDF.__init__(self, props)

        self.bsdf1 = props.get("bsdf-1", None)
        self.bsdf2 = props.get("bsdf-2", None)

        self.weight = props.get("weight", 0.5)

        assert 0 <= self.weight <= 1, "Probability must be between 0 and 1"

        assert self.bsdf1 is not None and self.bsdf2 is not None, "Both BSDFs must be provided"

        assert self.bsdf1.m_flags == self.bsdf2.m_flags, "Both BSDFs must have the same flags"
        assert self.bsdf1.m_components == self.bsdf2.m_components, "Both BSDFs must have the same components"

        self.m_flags = self.bsdf1.m_flags
        self.m_components = self.bsdf1.m_components
        
    def sample_t(self, ctx, si, sample1, sample2, active):

        selected_r  = (sample1 <= self.weight) & active

        bs, value1, delay_1 = self.bsdf1.sample_t(ctx, si, sample1, sample2, active)
        _, value2, delay_2 = self.bsdf2.sample_t(ctx, si, sample1, sample2, active)

        selected_value = dr.select(selected_r, value1, value2)
        
        delay = dr.select(selected_r, delay_1, delay_2)
        
        bs.pdf = self.pdf_t(ctx, si, bs.wo, delay, active)

        return bs, selected_value, delay


    def eval_t(self, ctx, si, wo, t, active):
        return self.bsdf1.eval_t(ctx, si, wo, t, active)*(self.weight) + \
                self.bsdf2.eval_t(ctx, si, wo, t, active)*(1-self.weight)

    def pdf_t(self, ctx, si, wo, t, active):
        return self.bsdf1.pdf_t(ctx, si, wo, t, active)*(self.weight) + \
               self.bsdf2.pdf_t(ctx, si, wo, t, active)*(1-self.weight)
    
    def traverse(self, cb):
        cb.put_parameter('bsdf-1', self.bsdf1, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('bsdf-2', self.bsdf2, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('weight', self.weight, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys):
        raise NotImplementedError("Not implemented yet...")

    def to_string(self):
        return f"Composed[bsdf1 = {self.bsdf1}, bsdf2 = {self.bsdf2}, weight = {self.weight}]"

mi.register_bsdf("Composed", lambda props: Composed(props))