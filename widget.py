from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Widget import MultiSelectionWidget
from AccessControl import ClassSecurityInfo

class ReadOnlyStringWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro' : "widgets/readonlystring",  
        })

    security = ClassSecurityInfo()


class AccommodationsGrantedMultiSelectionWidget(MultiSelectionWidget):
    _properties = MultiSelectionWidget._properties.copy()
    _properties.update({
        'macro' : 'accommodationsgrantedmultiselection',
        'format' : 'checkbox',
        })

    security = ClassSecurityInfo()
