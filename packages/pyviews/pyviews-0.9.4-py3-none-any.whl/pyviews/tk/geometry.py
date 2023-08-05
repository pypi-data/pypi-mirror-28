from pyviews.core.xml import XmlNode
from pyviews.core.node import Node
from pyviews.core.parsing import parse_attributes

class Geometry:
    def __init__(self, **args):
        self._args = args if args else {}

    def set(self, key, value):
        self._args[key] = value

    def apply(self, widget):
        pass

    def forget(self, widget):
        pass

class GridGeometry(Geometry):
    def apply(self, widget):
        widget.grid(**self._args)

    def forget(self, widget):
        widget.grid_forget()

class PackGeometry(Geometry):
    def apply(self, widget):
        widget.pack(**self._args)

    def forget(self, widget):
        widget.pack_forget()

class PlaceGeometry(Geometry):
    def apply(self, widget):
        widget.place(**self._args)

    def forget(self, widget):
        widget.place_forget()

class LayoutSetup(Node):
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._master = master
        self._args = {}
        self._index = None

    def set_attr(self, key, value):
        if key == 'index':
            self._index = value
        else:
            self._args[key] = value

    def apply(self):
        pass

class Row(LayoutSetup):
    def apply(self):
        self._master.grid_rowconfigure(self._index, **self._args)

class Column(LayoutSetup):
    def apply(self):
        self._master.grid_columnconfigure(self._index, **self._args)

def apply_layout(layout: LayoutSetup):
    parse_attributes(layout)
    layout.apply()
