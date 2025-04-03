import mitsuba as mi
import drjit as dr
from mitransient.temporal_profiles.constant_profile import ConstantProfile

class ChlorophyllBSDF(mi.BSDF):
    def __init__(self, props):
        mi.BSDF.__init__(self, props)

        self.color_red = mi.load_string(
            '''"<bsdf version='2.0.0' type='diffuse'>
                <rgb name="reflectance" value="0.570068, 0.0430135, 0.0443706"/>
            </bsdf>"'''
        )
        self.color_red_delay = 3.0

        self.color_green = mi.load_string(
            '''"<bsdf version='2.0.0' type='diffuse'>
                <rgb name="reflectance" value="0.105421, 0.37798, 0.076425"/>
            </bsdf>"''')
        self.color_green_delay = 0.0

        self.green_prob = 0.8
        # Set the BSDF flags
        self.m_flags = mi.BSDFFlags.DiffuseReflection | mi.BSDFFlags.FrontSide
        self.m_components = [self.m_flags]


    def sample(self, ctx, si, sample1, sample2, active):

        selected_r  = (sample1 <= self.green_prob) & active

        bs, red_value = self.color_red.sample(ctx, si, sample1, sample2, active)
        _, green_value = self.color_green.sample(ctx, si, sample1, sample2, active)
        
        bs.sampled_component = dr.select(selected_r, 1, 2)
        selected_value = dr.select(selected_r, green_value, red_value)

        return bs, selected_value

    def temporal_delay(self, si, random_sample, sample_data, active):
        
        delay = dr.select(sample_data.sampled_component==1,
                          self.color_green_delay,
                          self.color_red_delay)
       
        return delay

    # def eval(self, ctx, si, wo, active):
    #     return self.color_red.eval(ctx, si, wo, active)
    # def pdf(self, ctx, si, wo, active):
    #     return self.color_red.pdf(ctx, si, wo, active)
    # def eval_pdf(self, ctx, si, wo, active):
    #     return self.color_red.eval_pdf(ctx, si, wo, active)

    # def eval(self, ctx, si, wo, active):
    #     return self.color_green.eval(ctx, si, wo, active)
    # def pdf(self, ctx, si, wo, active):
    #     return self.color_green.pdf(ctx, si, wo, active)
    # def eval_pdf(self, ctx, si, wo, active):
    #     return self.color_green.eval_pdf(ctx, si, wo, active)

    def eval(self, ctx, si, wo, active):
        return  self.color_green.eval(ctx, si, wo, active)*(self.green_prob) + \
                self.color_red.eval(ctx, si, wo, active)*(1-self.green_prob)


    def pdf(self, ctx, si, wo, active):
        return  self.color_green.pdf(ctx, si, wo, active)*(self.green_prob) + \
                self.color_red.pdf(ctx, si, wo, active)*(1-self.green_prob)

    def eval_pdf(self, ctx, si, wo, active):
        return self.eval(ctx, si, wo, active), self.pdf(ctx, si, wo, active)

    def traverse(self, callback):
        pass

    def parameters_changed(self, keys):
        pass

    def to_string(self):
        return ""
mi.register_bsdf("ChlorophyllBSDF", lambda props: ChlorophyllBSDF(props))