## HSLA colors for HTML

With CSS3 the hsl(a) color values were introduced. These have had cross browser 
support since early 2011, yet see only limited use.

Possibly because the existing `#ff1ab3` hex-style colors offer the same palet and 
were always supported across browsers. With universal browser support for hsla, 
the time is overdue to challenge this.

This library offers a naming system for selectors and a python Hsla class 
to manage colors for use in CSS generators.

## Why use hsl(a) colors?

+ Hex colors offer no opacity, necessitating a partial switch to rgba or hsla 
colors anyways (this may change with the CSS4 spec).
+ Graphical designers are used to working with hsla, as it is the color picker 
in applications such as Sketch.
+ It makes it easier to reason about colors: a lower luminosity means a darker color; 
a higher saturation means more vibrant.

It also opens the door to more uniform, expansive and unambiguous naming of color 
selectors. The existing "semantic" approaches do not work well in most cases and 
give the designer non-descriptive class names such as `color-secondary` or bastardly 
descriptions as `color-primary-darker`. Descriptive solutions are often limited in 
scope (`darkest-blue` *will we also need a darkest-darkest blue?*) and fall short of 
giving a proper representation (`near-white` *how near?*)

## About hues

It is easy to see that color `hsla(30, 100%, 50%, 0.7)` is a vibrant color, 
light neither dark and with 70% opacity. It is less clear or "human-friendly" 
to find out what hue 30 is supposed to represent. Spoiler: it's an orangy hue.

This library contains a well-thought-out system to address various hues by name. 
The following were the considerations:
 
 + A named hue for every 10 steps on the hue scale, resulting in 36 hues;
 + When the hues match a HTML color for 100% saturation and 50% luminosity, the 
 HTML color is used for the hue (0: `red`, 60 `yellow`, 120: `lime`, 180: `cyan`, 240: `blue` 
 & 300 `magenta`)
 + For the other names, the HTML color names are avoided to prevent ambiguity and confusion.
 + All other names are single-words and do not contain other color names, again to be 
 unambiguous (no "cornflower blue")
 + The names were chosen to be broadly recognized and memorable, often the colors of 
 minerals, plants, etc.

## Getting started

### Creating hsla colors

The hue names and integer values in the naming sytem combine to create more than 345 million 
colors. Here is how you would create: 
+ a dark orange/red
+ a muted & light lila/blue
+ a black with 60% opacity:
 
```python
from hsla import Hsla

color1 = Hsla('scarlet', lum=18)
color2 = Hsla('majorelle', 40, 80)
color3 = Hsla('black', alpha=60)
```
Suppose we want to use the colors we created for genetating CSS selectors and values. 

```python
# The hsl representation is used with alpha=100
print(color1)  
# 'hsl(10, 100%, 18%)'

color1.suffix  
# 'scarlet-18'

print(color2)  
# 'hsl(250, 40%, 80%)

color2.suffix  
# 'majorelle40-80'

print(color3)  
# 'hsla(0, 0, 0, 0.6)'

color3.suffix  
# 'black-60a'
```

Notice that for the selectors, the saturation value is directly attached to the hue. 
The luminosity and alpha values by a hyphen and the latter has an 'a' suffixed. All 
values other than than the hue are optional. They default to:

+ `100` for saturation (`0` for black, white and gray)
+ `50` for luminosity (`0` for black, `100` for white and gray lies in between)
+ `100` for alpha

More formally: `<hue>[<sat>][-<lum>][-<alpha>a]`

### Generate a palet

The code below uses a catesian product of hues, saturations and luminosities to quickly 
generate a color palet. Bear in mind that this method is exponential with the value count, 
so you may end up generating many colors.

```python
colors = [Hsla(*hsl) for hsl in itertools.product(list(HUES)[::3], (100, 60), (92, 70, 50, 25))]
``` 

Notice that we take every 3rd value from the keys of the HUES dictionary (=12) **x** 
2 saturation values **x** 4 luminosities to get a palet of 96 colors and shades. We may 
also want to generate gray in muliple luminosities and black & white in various opacities:

```python
# Grays from various luminosities
grays = [Hsla('gray', lum=l) for l in (98, 95, 90, 80, 50, 65, 35, 20, 10, 5)]

# Blacks and whites from various alpha values
black_white = [Hsla(h, alpha=a) for h in ['black', 'white'] for a in (100, 80, 60, 40, 20, 10, 5)]
```

We now have a perfectly usable palet for use in a CSS generator such as Glueball.

```python
palet = colors + grays + black_white

palet[51].suffix
# cobalt60-70
```

### Hsla in your project

This method above may be suitable to create a palet for a versatile framework or 
for flexibility early in the development phase. 

It is just as easy to create the colors individually for your project, or you can 
forego the Hsla class altogether and only use the method to create consistent and readable 
names throughout your projects.

