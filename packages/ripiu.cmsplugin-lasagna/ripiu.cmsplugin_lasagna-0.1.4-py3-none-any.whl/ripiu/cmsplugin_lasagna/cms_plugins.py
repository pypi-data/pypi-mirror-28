from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import __version__
from .models import (
    BOTTOM, MIDDLE, TOP, ColorLayerPlugin, ImageAnchorModifierPlugin,
    LasagnaPlugin, OpacityModifierPlugin, VerticalAlignmentModifierPlugin
)


@plugin_pool.register_plugin
class LasagnaPluginPublisher(CMSPluginBase):
    model = LasagnaPlugin
    name = _('Lasagna')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_lasagna/lasagna.html'
    allow_children = True
    child_classes = [
        'TextPlugin',
        'FilerImagePlugin',
        'ColorLayerPluginPublisher',
        'ImageAnchorModifierPluginPublisher',
        'OpacityModifierPluginPublisher',
        'VerticalAlignmentModifierPluginPublisher',
    ]

    def render(self, context, instance, placeholder):
        context = super(LasagnaPluginPublisher, self).render(
            context, instance, placeholder
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'version': __version__,
        })
        return context


@plugin_pool.register_plugin
class ColorLayerPluginPublisher(CMSPluginBase):
    model = ColorLayerPlugin
    name = _('Color layer')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_lasagna/color.html'
    allow_children = False
    require_parent = True
    parent_classes = [
        'LasagnaPluginPublisher',
        'OpacityModifierPluginPublisher',
        'VerticalAlignmentModifierPluginPublisher',
    ]

    def render(self, context, instance, placeholder):
        context = super(ColorLayerPluginPublisher, self).render(
            context, instance, placeholder
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'color': instance.color,
        })
        return context


@plugin_pool.register_plugin
class OpacityModifierPluginPublisher(CMSPluginBase):
    model = OpacityModifierPlugin
    name = _('Opacity modifier')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_lasagna/opacity.html'
    allow_children = True
    require_parent = True
    parent_classes = [
        'LasagnaPluginPublisher',
        'OpacityModifierPluginPublisher',
        'VerticalAlignmentModifierPluginPublisher',
    ]

    def render(self, context, instance, placeholder):
        context = super(OpacityModifierPluginPublisher, self).render(
            context, instance, placeholder
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'opacity': instance.opacity / 100,
        })
        return context


@plugin_pool.register_plugin
class VerticalAlignmentModifierPluginPublisher(CMSPluginBase):
    model = VerticalAlignmentModifierPlugin
    name = _('Vertical alignment modifier')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_lasagna/valign.html'
    allow_children = True
    require_parent = True
    parent_classes = [
        'LasagnaPluginPublisher',
        'OpacityModifierPluginPublisher',
        'VerticalAlignmentModifierPluginPublisher',
    ]

    ALIGN_CHOICES = {
        TOP: 'flex-start',
        MIDDLE: 'center',
        BOTTOM: 'flex-end',
    }

    def render(self, context, instance, placeholder):
        context = super(VerticalAlignmentModifierPluginPublisher, self).render(
            context, instance, placeholder
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'valign': self.ALIGN_CHOICES[instance.alignment],
        })
        return context


@plugin_pool.register_plugin
class ImageAnchorModifierPluginPublisher(CMSPluginBase):
    model = ImageAnchorModifierPlugin
    name = _('Image anchor modifier')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_lasagna/anchor.html'
    allow_children = True
    child_classes = [
        'FilerImagePlugin',
        'FilerSvgImagePlugin'
    ]
    require_parent = True
    parent_classes = [
        'LasagnaPluginPublisher',
        'OpacityModifierPluginPublisher',
        'VerticalAlignmentModifierPluginPublisher',
    ]

    def render(self, context, instance, placeholder):
        context = super(ImageAnchorModifierPluginPublisher, self).render(
            context, instance, placeholder
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'anchor': instance.anchor_point,
            'fit': instance.object_fit,
        })
        return context
