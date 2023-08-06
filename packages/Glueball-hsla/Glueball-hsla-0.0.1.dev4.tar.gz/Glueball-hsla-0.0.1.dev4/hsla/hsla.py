"""A human-friendly system for HSLA colors in HTML"""

HUE_VALS = range(0, 360, 10)
HUE_NAMES = (
    'red',          # shadows HTML color name
    'scarlet',
    'tangerine',
    'carrot',
    'amber',
    'maize',
    'yellow',       # shadows HTML color name
    'apple',
    'springbud',
    'inchworm',
    'pistacho',
    'harlequin',
    'lime',         # shadows HTML color name
    'emerald',
    'malachite',
    'cadmium',
    'jade',
    'opal',
    'cyan',         # shadows HTML color name
    'cerulean',
    'police',
    'cobalt',
    'sapphire',
    'phthalo',
    'blue',         # shadows HTML color name
    'majorelle',
    'lilac',
    'mauve',
    'wisteria',
    'phlox',
    'magenta',      # shadows HTML color name
    'rose',
    'candy',
    'cerise',
    'raspberry',
    'amaranth',
)
HUES = dict(zip(HUE_NAMES, HUE_VALS))


class Hsla:
    """Generates CSS hsl(a) color value as string representation.
    Depends on the HUES dictionary to produce human friendly names.

    Colors 'black', 'white' and 'gray' have a hue and saturation of 0.
    A luminisity of 0 defaults to 'black' and 100 to 'white'; anything in between is treated as `gray`.

    suffix      The suffix attribute for use in selectors: <hue>[<sat>][-<lum>][-<alpha>a]
    _h          Hue - The value (0 to 360)
    _s          Saturation - The percentage as a value 0-100, defaults to 100
    _l          Luminosity - The percentage as a value 0-100, defaults to 50
    _a          Alpha - Value 0-100 translates to 0.0 to 1.0
    """
    def __init__(self, hue_name, sat=100, lum=50, alpha=100, hue_dict=HUES):
        if hue_name == 'black' or lum == 0:
            self._h = 0
            self._s = 0
            self._l = 0
            self.suffix = 'black'
        elif hue_name == 'white' or lum == 100:
            self._h = 0
            self._s = 0
            self._l = 100
            self.suffix = 'white'
        elif hue_name in ['grey', 'gray']:
            self._h = 0
            self._s = 0
            self._l = lum
            self.suffix = 'gray'
            if lum != 50:
                self.suffix = self.suffix + "-" + str(lum)
        else:
            self._h = hue_dict[hue_name]
            self._s = sat
            self._l = lum
            self.suffix = hue_name
            if sat != 100:
                self.suffix = self.suffix + str(sat)
            if lum != 50:
                self.suffix = self.suffix + "-" + str(lum)

        self._a = alpha
        if alpha != 100:
            self.suffix = self.suffix + "-" + str(alpha) + "a"

    def __str__(self):
        if self._a < 100:
            return 'hsla({:d}, {:d}%, {:d}%, {:.2f})'.format(self._h, self._s, self._l, self._a/100)
        return 'hsl({:d}, {:d}%, {:d}%)'.format(self._h, self._s, self._l)
