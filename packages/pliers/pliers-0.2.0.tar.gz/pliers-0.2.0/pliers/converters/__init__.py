''' The `Converter` hierarchy contains Transformer classes that take a `Stim`
of one type as input and return a `Stim` of a different type as output.
'''

from .api import (WitTranscriptionConverter,
                  IBMSpeechAPIConverter)
from .base import Converter, get_converter
from .google import GoogleVisionAPITextConverter, GoogleSpeechAPIConverter
from .image import TesseractConverter
from .iterators import (VideoFrameIterator, VideoFrameCollectionIterator,
                        ComplexTextIterator)
from .multistep import VideoToTextConverter, VideoToComplexTextConverter
from .video import VideoToAudioConverter

__all__ = [
    'WitTranscriptionConverter',
    'GoogleSpeechAPIConverter',
    'IBMSpeechAPIConverter',
    'GoogleVisionAPITextConverter',
    'TesseractConverter',
    'VideoFrameIterator',
    'VideoFrameCollectionIterator',
    'ComplexTextIterator',
    'VideoToTextConverter',
    'VideoToComplexTextConverter',
    'VideoToAudioConverter',
    'Converter',
    'get_converter'
]
