"""
Component List Panel for OpticsLAB.
Simple code for adding, removing, duplicating, and reordering optical components in the active list.
"""
import copy
import wx
from panel_component_GUI import MyPanel_tree
from opticsLAB_support import component_z_value, next_unique_name, remove_visual, template_base_name


# Component panel class for managing active components in the listbox
class ComponentPanel(MyPanel_tree):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent

    # When user clicks on an item in the component listbox
    def listBox_lst_componentsOnListBox(self, event):
        idx = self.listBox_lst_components.GetSelection()
        if idx != wx.NOT_FOUND:
            item_name = self.listBox_lst_components.GetString(idx)
            self.frame.show_component_properties(item_name)
        else:
            self.frame.show_project_properties()

    # Alias handler for active list selection
    def OnActiveListSelect(self, event):
        self.listBox_lst_componentsOnListBox(event)

    # When user clicks the Remove button
    def m_button_remove_componentOnButtonClick(self, event):
        idx = self.listBox_lst_components.GetSelection()
        if idx == wx.NOT_FOUND:
            return
            
        name = self.listBox_lst_components.GetString(idx)
        self.listBox_lst_components.Delete(idx)

        # Remove component from active dictionaries and delete visual 3D object
        comp_obj = self.frame.active_components.pop(name, None)
        remove_visual(comp_obj)
        self.frame.active_component_configs.pop(name, None)

        if self.frame.panel_simulation.canvas_obj:
            self.frame.panel_simulation.canvas_obj.canvas.update()
        
        self.frame.panel_components_tree.update_tree()
        self.frame.show_project_properties()
        self.frame.GetStatusBar().SetStatusText(f"Removed component: {name}", 0)
        self.frame.run_simulation(user_initiated=False)

    # When user clicks the Duplicate button
    def m_button_Duplicate_componentOnButtonClick(self, event):
        idx = self.listBox_lst_components.GetSelection()
        if idx == wx.NOT_FOUND:
            return
            
        name = self.listBox_lst_components.GetString(idx)
        config = self.frame.active_component_configs.get(name)
        if config is None:
            return

        # Make a copy of component configuration and give it a new name
        duplicate = copy.deepcopy(config)
        base_title = template_base_name(name)
        unique_name = next_unique_name(base_title, self.frame.active_components)
        duplicate["name"] = unique_name
        
        comp_obj = self.frame.active_components.get(name)
        z_val = float(component_z_value(comp_obj) + 1.5)

        raw_center = duplicate.get("center", [0.0, 0.0, 0.0])
        if hasattr(raw_center, "coordinates"):
            raw_center = raw_center.coordinates
        elif hasattr(raw_center, "tolist"):
            raw_center = raw_center.tolist()
            
        try:
            duplicate["center"] = [float(raw_center[0]), float(raw_center[1]), z_val]
        except Exception:
            duplicate["center"] = [0.0, 0.0, z_val]

        self.frame.update_component_instance(unique_name, duplicate)

    # Moves an item up or down in the listbox order
    def _move_item(self, direction):
        idx = self.listBox_lst_components.GetSelection()
        count = self.listBox_lst_components.GetCount()
        
        if idx == wx.NOT_FOUND:
            return
        if direction == -1 and idx <= 0:
            return
        if direction == 1 and idx >= count - 1:
            return

        name = self.listBox_lst_components.GetString(idx)
        self.listBox_lst_components.Delete(idx)
        new_idx = idx + direction
        self.listBox_lst_components.Insert(name, new_idx)
        self.listBox_lst_components.SetSelection(new_idx)
        self.frame.sync_component_order_from_listbox()
        self.frame.run_simulation(user_initiated=False)

    # When user clicks Move Up button
    def m_button_upOnButtonClick(self, event):
        self._move_item(-1)

    # When user clicks Move Down button
    def m_button_downOnButtonClick(self, event):
        self._move_item(1)
