from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from colorfield.fields import ColorField

# align
TOP = 0
MIDDLE = 1
BOTTOM = 2

# fit
FILL = 'fill'
CONTAIN = 'contain'
COVER = 'cover'
NONE = 'none'
SCALE_DOWN = 'scale-down'

# anchor
NORTH = 'center top'
NORTH_EAST = 'right top'
EAST = 'right center'
SOUTH_EAST = 'right bottom'
SOUTH = 'center bottom'
SOUTH_WEST = 'left bottom'
WEST = 'left center'
NORTH_WEST = 'left top'
CENTER = 'center center'


class LasagnaPlugin(CMSPlugin):
    '''Lasagna container'''

    name = models.CharField(
        _('name'), max_length=400, default='', blank=True
    )

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = _('Lasagna')
        verbose_name_plural = _('Lasagna')


class ColorLayerPlugin(CMSPlugin):
    '''Color layer'''

    color = ColorField(
        _('color'), null=False,
    )

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = _('Color layer')
        verbose_name_plural = _('Color layer')


class OpacityModifierPlugin(CMSPlugin):
    '''Sets the opacity of its children'''

    opacity = models.PositiveSmallIntegerField(
        _('opacity (%)'),
        validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return _('%(opacity)d%%') % {
            'opacity': self.opacity
        }

    class Meta:
        verbose_name = _('Opacity modifier')
        verbose_name_plural = _('Opacity modifiers')


class VerticalAlignmentModifierPlugin(CMSPlugin):
    '''sets the vertical alignment of its children'''

    ALIGN_LABELS = {
        TOP: _('top'),
        MIDDLE: _('middle'),
        BOTTOM: _('bottom'),
    }

    ALIGN_CHOICES = (
        (TOP, ALIGN_LABELS[TOP]),
        (MIDDLE, ALIGN_LABELS[MIDDLE]),
        (BOTTOM, ALIGN_LABELS[BOTTOM]),
    )

    alignment = models.PositiveSmallIntegerField(
        _('alignment'), choices=ALIGN_CHOICES, default=TOP
    )

    def __str__(self):
        return str(self.ALIGN_LABELS[self.alignment])

    class Meta:
        verbose_name = _('Vertical alignment modifier')
        verbose_name_plural = _('Vertical alignment modifiers')


class ImageAnchorModifierPlugin(CMSPlugin):
    '''fixes the anchor of an image'''

    ANCHOR_LABELS = {
        NORTH: _('North'),
        NORTH_EAST: _('North-east'),
        EAST: _('East'),
        SOUTH_EAST: _('South-east'),
        SOUTH: _('South'),
        SOUTH_WEST: _('South-west'),
        WEST: _('West'),
        NORTH_WEST: _('North-west'),
        CENTER: _('Middle'),
    }

    ANCHOR_CHOICHES = (
        (NORTH, ANCHOR_LABELS[NORTH]),
        (NORTH_EAST, ANCHOR_LABELS[NORTH_EAST]),
        (EAST, ANCHOR_LABELS[EAST]),
        (SOUTH_EAST, ANCHOR_LABELS[SOUTH_EAST]),
        (SOUTH, ANCHOR_LABELS[SOUTH]),
        (SOUTH_WEST, ANCHOR_LABELS[SOUTH_WEST]),
        (WEST, ANCHOR_LABELS[WEST]),
        (NORTH_WEST, ANCHOR_LABELS[NORTH_WEST]),
        (CENTER, ANCHOR_LABELS[CENTER]),
    )

    FIT_LABELS = {
        FILL: _('Fill the container'),
        CONTAIN: _('Fit into the container'),
        COVER: _('Fill the container and maintain the aspect ratio'),
        NONE: _("Don't resize"),
        SCALE_DOWN: _('Scale down to fit into the container'),
    }

    FIT_CHOICES = (
        (FILL, FIT_LABELS[FILL]),
        (CONTAIN, FIT_LABELS[CONTAIN]),
        (COVER, FIT_LABELS[COVER]),
        (NONE, FIT_LABELS[NONE]),
        (SCALE_DOWN, FIT_LABELS[SCALE_DOWN]),
    )

    anchor_point = models.CharField(
        _('anchor point'),
        max_length=15,
        choices=ANCHOR_CHOICHES,
        default=CENTER, blank=False
    )

    object_fit = models.CharField(
        _('resize'),
        max_length=10,
        choices=FIT_CHOICES,
        default=COVER, blank=False
    )

    def __str__(self):
        if self.anchor_point:
            return str(self.ANCHOR_LABELS[self.anchor_point])
        return None

    class Meta:
        verbose_name = _('Image anchor modifier')
        verbose_name_plural = _('Image anchor modifiers')
