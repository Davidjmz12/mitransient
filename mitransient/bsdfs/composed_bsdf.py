import mitsuba as mi
import drjit as dr
import numpy as np

class ComposedBSDF(mi.BSDF):
    def __init__(self, props):
        mi.BSDF.__init__(self, props)

        self.tp1 = props.get("temporal-profile-1")
        self.tp2 = props.get("temporal-profile-2")
        self.bsdf1 = props.get("bsdf-1")
        self.bsdf2 = props.get("bsdf-2")

        self.prob = props.get("probability", 0.5)

        assert 0 <= self.prob <= 1, "Probability must be between 0 and 1"

        assert self.tp1 is not None and self.tp2 is not None, "Both temporal profiles must be provided"
        assert self.bsdf1 is not None and self.bsdf2 is not None, "Both BSDFs must be provided"

        assert self.bsdf1.m_flags == self.bsdf2.m_flags, "Both BSDFs must have the same flags"
        assert self.bsdf1.m_components == self.bsdf2.m_components, "Both BSDFs must have the same components"

        self.m_flags = self.bsdf1.m_flags
        self.m_components = self.bsdf1.m_components
        
    def sample_t(self, ctx, si, sample1, sample2, active):

        selected_r  = (sample1 <= self.prob) & active

        bs, value1 = self.bsdf1.sample(ctx, si, sample1, sample2, active)
        _, value2 = self.bsdf2.sample(ctx, si, sample1, sample2, active)

        selected_value = dr.select(selected_r, value1, value2)

        delay = dr.select(selected_r,
                          self.tp1.sample_delay(si, sample1),
                          self.tp2.sample_delay(si, sample1))
        
        return bs, selected_value, delay


    def eval_t(self, ctx, si, wo, t, active):
        return self.bsdf1.eval(ctx, si, wo, active)*self.tp1.eval_delay(t, si)*(self.prob) + \
                self.bsdf2.eval(ctx, si, wo, active)*self.tp2.eval_delay(t, si)*(1-self.prob)

    def pdf_t(self, ctx, si, wo, t, active):
        return self.bsdf1.pdf(ctx, si, wo, active)*self.tp1.eval_delay(t, si)*(self.prob) + \
               self.bsdf2.pdf(ctx, si, wo, active)*self.tp2.eval_delay(t, si)*(1-self.prob)
    
    def traverse(self, cb):
        cb.put_parameter('temporal-profile-1', self.tp1, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('temporal-profile-2', self.tp2, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('bsdf-1', self.bsdf1, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('bsdf-2', self.bsdf2, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('probability', self.prob, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys):
        raise NotImplementedError("Not implemented yet...")

    def to_string(self):
        return f"ComposedBSDF[tp1 = {self.tp1}, tp2 = {self.tp2}, bsdf1 = {self.bsdf1}, bsdf2 = {self.bsdf2}, prob = {self.prob}]"

mi.register_bsdf("ComposedBSDF", lambda props: ComposedBSDF(props))