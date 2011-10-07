from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from Products.Archetypes.atapi import *
from zope.interface import implements, Interface
from zope.component import adapts, provideAdapter

from Products.FacultyStaffDirectory.interfaces.person import IPerson
from Products.OfficeHoursExtender import OfficeHoursExtenderMF as _
from Products.OfficeHoursExtender.interfaces import IOfficeHoursExtenderLayer

# Any field you tack on must have ExtensionField as its first subclass:
class _LinesExtensionField(ExtensionField, LinesField):
    pass


class PersonExtender(object):
    """Adapter that adds a Mobile Phone field to Person.
    
    You could also change or delete existing fields (though you might violate assumptions made in other code). To do that, implement ISchemaModifier instead of ISchemaExtender.
    """
    adapts(IPerson)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IOfficeHoursExtenderLayer
    
    _fields = [
            _LinesExtensionField('officeHours',
                required=False,
                searchable=True,
                schemata="Office Hours",
                widget=LinesWidget(
                    label=_(u"FSDOfficeHoursExtender_label_OfficeHours", default=u"Office Hours"),
                    description=_(u"FSDOfficeHoursExtender_description_OfficeHours", default=u"Demo field added by the OfficeHoursExtender product."),
                    i18n_domain='FSDOfficeHoursExtender',
                )
            )
        ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self._fields


# # Optional stuff to tack on more methods to Person (after you adapt it to IYuppie, anyway):
# 
# class IYuppie(Interface):
#     """A Yuppie is any person who eats tofu and has a mobile phone."""
#     
#     def textMessage(self, spam):
#         """Text message some spam to the yuppie's mobile phone."""
# 
# 
# class YuppieAdapter(object):
#     """Adapt Persons to Yuppies."""
#     adapts(IPerson)
#     implements(IYuppie)
#     
#     def __init__(self, context):
#         self.context = context  # Phillip Weitershausen says this is canonical.
#     
#     def textMessage(self, spam):
#         print "I just texted %s to the yuppie's mobile phone at %s!" % (spam, self.context.getMobilePhone())
# 
# provideAdapter(YuppieAdapter)  # This should be in ZCML. Yuck.
