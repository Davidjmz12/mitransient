import mitsuba as mi
import drjit as dr

class TransientBSDF(mi.BSDF):
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
        self.temporal_profile = props.get('temporal-profile')
        if self.temporal_profile is None:
            raise Exception("No temporal profile specified")
        
        # Set flags equal to 'bsdf'
        self.m_components = self.bsdf.m_components
        self.m_flags = self.bsdf.m_flags

    def sample(self, ctx, si, sample1, sample2, active = True):
        return self.bsdf.sample(ctx, si, sample1, sample2, active)

    def eval(self, ctx, si, wo, active):
        return self.bsdf.eval(ctx, si, wo, active)

    def pdf(self, ctx, si, wo, active):
        return self.bsdf.pdf(ctx, si, wo, active)

    def temporal_delay(self, si, random_sample, sample_data, active):
        return dr.select(active, self.temporal_profile.temporal_delay(si, random_sample), 0)
    
    def traverse(self, cb):
        cb.put_parameter('temporal-profile', self.temporal_profile, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('bsdf', self.bsdf, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys=None):
        raise NotImplementedError("Not implemented yet...")

    def to_string(self):
        return f"TransientBSDF[bsdf = {self.bsdf}], [temporal-profile = {self.temporal_profile}]"

mi.register_bsdf("TransientBSDF", lambda props: TransientBSDF(props))