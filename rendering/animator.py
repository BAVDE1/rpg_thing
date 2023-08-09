

class Animator:
    def __init__(self, current_texture_obj, idle_ss, **one_time_ss):
        """ ss - sprite sheets - must be lists of two objects - [0]: original image, [1]: sprite sheet """
        self.texture_obj = current_texture_obj
        self.idle_ss = idle_ss
        if one_time_ss:
            self.one_time_ss = {ss[0]: ss[1] for ss in one_time_ss}

