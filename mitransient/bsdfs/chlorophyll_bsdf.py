import mitsuba as mi
import drjit as dr

class ChlorophyllBSDF(mi.BSDF):
    def __init__(self, props):
        mi.BSDF.__init__(self, props)

        self.color_red = mi.load_string(
            '''"<bsdf version='2.0.0' type='diffuse'>
                <rgb name="reflectance" value="0.570068, 0.0430135, 0.0443706"/>
            </bsdf>"'''
        )
        
        self.color_red_delay = props.get('red-delay', None)
        assert self.color_red_delay is not None, "red-delay must be specified"
        props.mark_queried('red-delay')

        self.color_green = mi.load_string(
            '''"<bsdf version='2.0.0' type='diffuse'>
                <rgb name="reflectance" value="0.105421, 0.37798, 0.076425"/>
            </bsdf>"''')
        
        self.color_green_delay = props.get('green-delay', None)
        assert self.color_green_delay is not None, "green-delay must be specified"
        props.mark_queried('green-delay')

        self.green_prob = props.get('green-prob', 0.5)
        assert self.green_prob is not None, "green-prob must be specified"
        assert self.green_prob >= 0 and self.green_prob <= 1, "green-prob must be between 0 and 1"
        props.mark_queried('green-prob')


        # Set the BSDF flags
        self.m_flags = mi.BSDFFlags.DiffuseReflection
        self.m_components = [self.m_flags]


    def sample_t(self, ctx, si, sample1, sample2, active):

        selected_r  = (sample1 <= self.green_prob) & active

        bs, red_value = self.color_red.sample(ctx, si, sample1, sample2, active)
        _, green_value = self.color_green.sample(ctx, si, sample1, sample2, active)
        
        bs.sampled_component = dr.select(selected_r, 1, 2)
        selected_value = dr.select(selected_r, green_value, red_value)

        delay = dr.select(selected_r, 
                          self.color_green_delay.sample_delay(si, sample1), 
                          self.color_red_delay.sample_delay(si, sample1))

        return bs, selected_value, delay

    def eval_t(self, ctx, si, wo, t, active):
        return  self.color_green.eval(ctx, si, wo, active)*self.color_green_delay.eval_delay(t, si)*(self.green_prob) + \
                self.color_red.eval(ctx, si, wo, active)*self.color_red_delay.eval_delay(t, si)*(1-self.green_prob)


    def pdf_t(self, ctx, si, wo, t, active):
        return  self.color_green.pdf(ctx, si, wo, active)*self.color_green_delay.eval_delay(t, si)*(self.green_prob) + \
                self.color_red.pdf(ctx, si, wo, active)*self.color_red_delay.eval_delay(t, si)*(1-self.green_prob)
    
    def traverse(self, cb):
        cb.put_parameter('green-delay', self.temporal_profile, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('red-delay', self.temporal_profile, mi.ParamFlags.NonDifferentiable)
        cb.put_parameter('green-prob', self.bsdf, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys):
        raise NotImplementedError("Not implemented yet...")

    def to_string(self):
        return f"ChlorophyllBSDF[red-delay = {self.color_red_delay}, green-delay = {self.color_green_delay}, green-prob = {self.green_prob}]"

mi.register_bsdf("ChlorophyllBSDF", lambda props: ChlorophyllBSDF(props))