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
    def __init__(self, hue, sat=100, lum=50, alpha=100, vals=HUE_VALS, names=HUE_NAMES):
        self._vals = vals
        self._names = names
        if hue in ['black', 'white', 'grey', 'gray'] or sat == 0:
            self._h, self._s = 0, 0
            if hue == 'black':
                self._l = 0
            elif hue == 'white':
                self._l = 100
            else:
                self._l = lum
        else:
            if type(hue) is int:
                self._h = hue
            else:
                self._h = vals[names.index(hue)]
            self._s, self._l = sat, lum
        self._a = alpha

    def get_selector(self):
        """Return color component for selector: <h>[<s>][-<l>][-<a>a]"""
        s = str(self._s) if self._s < 100 else ""
        l = "-"+str(self._l) if self._l != 50 else ""
        a = '-{:.2f}a'.format(self._a) if self._a < 100 else ""
        if self._s == 0:
            s = ""
            if self._l == 0:
                h = 'black'
            elif self._l == 100:
                h = 'white'
            else:
                h = 'gray'
        else:
            h = self._names[self._vals.index(self._h)]
        return h+s+l+a

    def __str__(self):
        if self._a < 100:
            return 'hsla({:d}, {:d}%, {:d}%, {:.2f})'.format(self._h, self._s, self._l, self._a/100)
        return 'hsl({:d}, {:d}%, {:d}%)'.format(self._h, self._s, self._l)
