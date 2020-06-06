# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import (
    EnumProperty, FloatVectorProperty,
    IntProperty, IntVectorProperty, BoolProperty)

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvListInputNode(bpy.types.Node, SverchCustomTreeNode):
    ''' Creta a float or int List '''
    bl_idname = 'SvListInputNode'
    bl_label = 'List Input'
    bl_icon = 'OUTLINER_OB_EMPTY'
    sv_icon = 'SV_LIST_INPUT'

    defaults = [0 for i in range(32)]
    to3d: BoolProperty(name='to3d', description='show in 3d panel', default=True)

    int_: IntProperty(
        name='int_', description='integer number', default=1, min=1, max=128, update=updateNode)

    v_int: IntProperty(
        name='int_', description='integer number', default=1, min=1, max=10, update=updateNode)

    int_list: IntVectorProperty(
        name='int_list', description="Integer list", default=defaults, size=32,update=updateNode)
    int_list1: IntVectorProperty(
        name='int_list1', description="Integer list", default=defaults, size=32,update=updateNode)
    int_list2: IntVectorProperty(
        name='int_list2', description="Integer list", default=defaults, size=32,update=updateNode)
    int_list3: IntVectorProperty(
        name='int_list3', description="Integer list", default=defaults, size=32,update=updateNode)

    float_list: FloatVectorProperty(
        name='float_list', description="Float list", default=defaults, size=32, update=updateNode)

    vector_list: FloatVectorProperty(
        name='vector_list', description="Vector list", default=defaults, size=32, update=updateNode)

    def changeMode(self, context):
        if self.mode == 'vector':
            if 'Vector List' not in self.outputs:
                self.outputs.remove(self.outputs[0])
                self.outputs.new('SvVerticesSocket', 'Vector List')
                return
        else:
            if 'List' not in self.outputs:
                self.outputs.remove(self.outputs[0])
                self.outputs.new('SvStringsSocket', 'List')
                return

    modes = [
        ("int_list", "Int", "Integer", "", 1),
        ("float_list", "Float", "Float", "", 2),
        ("vector", "Vector", "Vector", "", 3)]

    mode: EnumProperty(items=modes, default='int_list', update=changeMode)

    def sv_init(self, context):
        self.outputs.new('SvStringsSocket', "List")

    def draw_buttons(self, context, layout):
        if self.mode == 'vector':
            layout.prop(self, "v_int", text="List Length")
        else:
            layout.prop(self, "int_", text="List Length")

        layout.prop(self, "mode", expand=True)

        if self.mode == 'vector':
            col = layout.column(align=False)
            for i in range(self.v_int):
                row = col.row(align=True)
                for j in range(3):
                    row.prop(self, 'vector_list', index=i*3+j, text='XYZ'[j])
        elif self.mode == 'int_list':
            col = layout.column(align=True)
            k = 0
            lists = 'int_list', 'int_list1', 'int_list2', 'int_list3'
            for i in range(self.int_//32):
                for t in range(32):
                    col.prop(self, lists[i], index=t, text=str(k))
                    k += 1
            for t in range(self.int_%32):
                col.prop(self, lists[self.int_//32], index=t, text=str(k))
                k += 1
        else:
            col = layout.column(align=True)
            for i in range(self.int_):
                col.prop(self, self.mode, index=i, text=str(i))


    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'to3d', text='to3d')

    @property
    def draw_3dpanel(self):
        return False if not self.outputs[0].is_linked or not self.to3d else True

    def draw_buttons_3dpanel(self, layout):
        layout.row(align=True).label(text=self.label or self.name)

        if self.mode == 'vector':
            colum_list = layout.column(align=True)
            for i in range(self.v_int):
                row = colum_list.row(align=True)
                for j in range(3):
                    row.prop(self, 'vector_list', index=i*3+j, text='XYZ'[j]+(self.label if self.label else self.name))
        else:
            colum_list = layout.column(align=True)
            for i in range(self.int_):
                row = colum_list.row(align=True)
                row.prop(self, self.mode, index=i, text=str(i)+(self.label if self.label else self.name))
                row.scale_x = 0.8

    def process(self):
        if self.outputs[0].is_linked:
            if self.mode == 'int_list':
                data = []
                lists = self.int_list, self.int_list1, self.int_list2, self.int_list3
                for i in range(self.int_//32):
                    data.extend(list(lists[i][:32]))
                data.extend(list(lists[self.int_//32][:self.int_%32]))
                data = [data]
            elif self.mode == 'float_list':
                data = [list(self.float_list[:self.int_])]
            elif self.mode == 'vector':
                c = self.v_int*3
                v_l = list(self.vector_list)
                data = [list(zip(v_l[0:c:3], v_l[1:c:3], v_l[2:c:3]))]
            self.outputs[0].sv_set(data)


def register():
    bpy.utils.register_class(SvListInputNode)


def unregister():
    bpy.utils.unregister_class(SvListInputNode)
