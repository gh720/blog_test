from PIL import Image, ImageDraw, ImageFilter, ImageColor
import random
import tempfile
import math
import numpy


from blend_modes import blend_modes

from django.conf import settings


class ddot(dict):
    def __init__(self, *args, **kwargs):
        super(ddot, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self

    @classmethod
    def recursive_walk(cls, d):
        self = cls(d)
        for key, value in self.items():
            if type(value) is dict:
                self[key] = cls.recursive_walk(value)
        return self

class Point(ddot):
    def __init__(self, x, y):
        super().__init__(x=x,y=y)

    def copy(self):
        return Point(self['x'],self['y'])

    def __hash__(self):
        return (self['x'],self['y']).__hash__()

    def __iter__(self):
        yield self['x']
        yield self['y']

    @classmethod
    def fromdict(cls, dict):
        return cls(dict['x'], dict['y'])



class Segment(ddot):
    def __init__(self, start:Point, end:Point, turn, length, pos, charge, total_length):
        super().__init__(start=start,end=end, turn=turn, length=length, pos=pos, charge=charge, total_length=total_length)

    # def __hash__(self):
    #     return (self['start'],self['end']).__hash__()

    # def __iter__(self):
    #     yield self['start']
    #     yield self['end']


def pdiff(start,end):
  return Point(end.x- start.x, end.y- start.y)

def psum(p1,p2):
  return Point(p1.x+p2.x, p1.y+p2.y)

def project(v:Point, angle, scale) -> Point:
    """
    Rotate vector v(dx,dy) by angle(radians) a counterclockwise
    """
    vv = Point(0,0)
    sa = math.sin(angle)*scale
    ca = math.cos(angle)*scale

    vv.x = ca * v.x  - sa * v.y 
    vv.y = sa * v.x  + ca * v.y 
    return vv 

def random_displace(pt1,pt2,scale,angle):
  d = pdiff(pt1,pt2)
  dd = project(d, angle, scale)
  return psum(pt1, dd)

def sign(v):
  return -(v<0) or +(v>0)

def plen(v):
    l = math.sqrt(v.x * v.x + v.y * v.y)
    return l

def pnorm(v):
    l = plen(v)
    return Point(v.x/l, v.y/l), l


class lightning_c:

    def __init__(self, start,end, **kwargs):
        args = dict(**kwargs)
        self.start=start
        self.end=end
        self.distance = plen(pdiff(self.start,self.end))
        self.branches = []

        self.min_charge = 0.1
        self.branch_node_ratio = 4
        self.max_level=1
        self.max_branches=100
        self.max_branch_charge=6
        self.max_branch_scale=0.6
        self.dissipation_rate=.99/30
        self.__dict__.update(kwargs)

    def pround(self,pt):
        _pt=Point(round(pt.x,4), round(pt.y,4))
        return _pt

    def create_bolt(self, start, end):
        segments=[]
        d = pdiff(start, end)
        dx = -d.y
        dy = d.x
        norm,length = pnorm(Point(dx,dy))

        ilen = int(length)
        array= list(range(ilen))

        margin=3
        positions=list(map(lambda v: v/ilen, range(margin+1)))
        del array[:margin+1]
        for i in range(int(length/self.branch_node_ratio)):
            ai = random.randint(0,len(array)-1)
            n = array[ai]
            lower = max(0,ai-margin)
            upper = min(len(array)-1,ai+margin)
            slice_len = upper+1-lower
            for j in range(slice_len):
                array[lower+j]=array[-slice_len+j]
            del array[-slice_len:]
            if not len(array):
                break
            positions.append(n/ilen)
            # positions.append(random.random())
        positions.sort()

        sway=320
        jaggedness=1/sway

        pp  = start
        prev_disp = 0
        disp = 0

        prev_angle =None
        prev_pt=None
        total_length=0
        for i in range(1,len(positions)):
            pos = positions[i]
            scale = (length*jaggedness) * (pos-positions[i-1])
            envelope =  20 * (1-pos) if pos > 0.95 else 1
            disp = (0.5 - random.random())*2 * sway
            disp -= (disp - prev_disp) * ( 1- scale)
            pt = Point(0,0)
            pt.x = d.x * pos
            pt.y = d.y * pos
            pt.x += norm.x * disp
            pt.y += norm.y * disp
            pt.x += start.x
            pt.y += start.y

            dd = pdiff(pp, pt)
            seg_length = plen(dd)
            angle = math.atan2(dd.y, dd.x) # from vertical axis
            turn = 0 if prev_angle==None else angle - prev_angle
            total_length+=seg_length
            segments.append(Segment(self.pround(pp), self.pround(pt), turn, seg_length, pos, charge=0
                                    , total_length=total_length))
            prev_angle = angle
            pp = pt
            prev_disp=disp
        return segments

    def create_branches(self, start, end, initial_charge, level=0):
        if level > self.max_level:
            return
        segments = self.create_bolt(start, end)
        self.branches.append(segments)
        # sseg = sorted(_segments, key=lambda v: -v.turn * v.length)

        d = pdiff(start,end)
        path_len = plen(d)

        max_branches=self.max_branches
        charge=initial_charge
        for i in range(len(segments)):
            v = segments[i]
            v.charge = charge
            if not (abs(v.turn) > 0.6 and v.length > 10
                    and (abs(v.turn) * v.length > .6*10*1.2) # not branching
                    ):
                charge = max(0, charge - v.length * self.dissipation_rate)
                if charge==0:
                    break
                continue
            if max_branches <= 0:
                break
            max_branches -= 1

            branch_distance= min(self.max_branch_scale * self.distance, path_len * (1-v.pos))
            de = pdiff(v.start, end)
            main_angle = math.atan2(de.y, de.x)
            angle =  - sign(v.turn) * (min(80, max(20, 15 + (12 + random.random()* (48-12)))) / 180 * math.pi)
            # scale= (0.2 + 0.5 * random.random())
            scale =1
            # distance = branch_distance * scale
            dd = pdiff(v.start, end)
            pt = project(dd, angle, scale)
            pt.x += v.start.x
            pt.y += v.start.y
            branch_charge = min(self.max_branch_charge, charge) * (0.1 + random.random() * .4) # diverge no more than ... of the charge
            charge -= branch_charge
            v.charge = charge
            self.create_branches(v.start, pt, branch_charge, level+1)
            if charge <=0 :
                break
            # if charge < self.min_charge:
            #     break


def draw_segments(draw, segments, color):
    for seg in segments:
        log_charge = min(5, math.log(1+seg.charge))
        width = int(math.floor(log_charge))
        # color = LIGHTBLUE
        if width==0:
            width=1
            color = tuple([ *[ int((0.7 + log_charge*0.3) * v) for v in color[:3] ], color[3]])
        # draw.line([seg.start.x,seg.start.y,seg.end.x, seg.end.y], width = width, fill=color)
        draw.line([seg.start.y,seg.start.x,seg.end.y, seg.end.x], width = width, fill=color)

def save_image(image):
    if image.mode!='RGB':
        image = image.convert('RGB')
    tmp_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False, dir='.', suffix='.jpg')

    image.save(tmp_file)
    tmp_file.close()

def make_glow(image):
    blurred_images = []
    for i in [4, 8, 16]:
        blurred_images.append(image.filter(ImageFilter.GaussianBlur(radius=i)))
    b_image1 = numpy.array(image).astype(float)
    b_images = []
    for b_image in blurred_images:
        b_images.append(numpy.array(b_image).astype(float))

    composite_image_numpy = b_image1
    opacity = 1

    for b_image in b_images:
        composite_image_numpy = blend_modes.addition(composite_image_numpy, b_image, opacity)

    composite_image_8 = numpy.uint8(composite_image_numpy)
    composite_image = Image.fromarray(composite_image_8)
    return composite_image


def image_to_blend(image):
    np_image = numpy.array(image)  # Inputs to blend_modes need to be numpy arrays.
    image_float = np_image.astype(float)  # Inputs to blend_modes need to be floats.
    return image_float

def image_from_blend(image):
    blended_img = numpy.uint8(image)
    blended_img_raw = Image.fromarray(blended_img)
    return blended_img_raw

def load_image(file):
    image = Image.open(file)  # RGBA image
    return image

def generate_lightning_logo():
    image1 = generate_lightning_image((256, 256))
    logo_file_path = "%s/%s" % (settings.AUXILIARY_RESOURCES, 'logo_letters.png')
    image2 = load_image(logo_file_path)
    image = blend_modes.addition(image_to_blend(image1), image_to_blend(image2), opacity=1)
    # save_image(image_from_blend(image))
    return image_from_blend(image)


def generate_lightning_image(size):
    WHITE = (255, 255, 255, 255)
    BLACK = (0,0,0, 255)
    BLUE = "#0000ff"
    LIGHTBLUE = (0xaa,0xaa,0xff, 0xff)
    LIGHTRED = (0xff,0xaa,0xaa, 0xff)
    RED = (0xff,0x88, 0x88, 0xff)
    BLACK_TRANS=(0,0,0,0)

    colors = [ ImageColor.getrgb(v) for v in 'white red green blue cyan magenta'.split()]

    seed = None
    # seed = 12641
    if not seed:
        seed = random.randint(0,100000)
    random.seed(seed)

    size = size or (600,600)

    start_point = Point(10,int(size[1]/2))
    end_point = Point(size[0]-10,int(size[1]/2))

    max_level=5
    max_branches=100

    # segments = create_bolt(start_point, end_point, 1)

    image_mode='RGBA'
    image = Image.new(image_mode, size, BLACK)
    draw = ImageDraw.Draw(image)

    # image.paste(BLACK, [0, 0, image.size[0], image.size[1]]) # this is somehow crucial
    # blur doesn't work on transparent colors ?

    lightning = lightning_c(start_point, end_point, max_level=max_level, max_branches=max_branches,
                            max_branch_charge=20, dissipation_rate=.99 / 30)
    lightning.create_branches(start_point, end_point, 100)

    for segments in lightning.branches:
        draw_segments(draw, segments, LIGHTBLUE)

    surf = None
    composite_image = make_glow(image)
    return composite_image


