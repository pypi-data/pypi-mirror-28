''' The `Filter` hierarchy contains Transformer classes that take a `Stim`
of one type as input and return a `Stim` of the same type as output (but with
some changes to its data).
'''

from .image import (ImageCroppingFilter,
                    PillowImageFilter)
from .text import (WordStemmingFilter,
                   TokenizingFilter,
                   TokenRemovalFilter,
                   PunctuationRemovalFilter)
from .video import FrameSamplingFilter


__all__ = [
    'ImageCroppingFilter',
    'PillowImageFilter',
    'WordStemmingFilter',
    'TokenizingFilter',
    'TokenRemovalFilter',
    'PunctuationRemovalFilter',
    'FrameSamplingFilter'
]
