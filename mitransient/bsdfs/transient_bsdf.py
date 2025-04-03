import mitsuba as mi
import drjit as dr
from mitransient.temporal_profiles.constant_profile import ConstantProfile
from mitransient.temporal_profiles.constant_texture_profile import ConstantTextureProfile
from mitransient.temporal_profiles.gaussian_profile import GaussianProfile
from mitransient.temporal_profiles.exponential_profile import ExponentialProfile

def read_temporal_profile_(props):
    """
    Function that returns a temporal delay given by the properties' dictionary.

    """

    type_delay = props["temporal-profile"]

    map_type_delay = {
        "constant": ConstantProfile,
        "gaussian": GaussianProfile,
        "exponential": ExponentialProfile,
        "constant-texture": ConstantTextureProfile
    }

    if type_delay in map_type_delay:
        return map_type_delay[type_delay].create(props)
    else:
        raise Exception("Unknown delay profiling type")


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
        if not props.has_property('temporal-profile'):
            self.temporal_profile = ConstantProfile(0)
        else:
            self.temporal_profile = read_temporal_profile_(props)

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