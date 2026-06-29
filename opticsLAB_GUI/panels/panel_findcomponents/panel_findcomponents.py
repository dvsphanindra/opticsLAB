"""
Search and Find Dialog for OpticsLAB components.
Allows searching active optical elements and preset templates cleanly.
Simple multi-line code without complex inline filtering.
"""
import wx
from panel_findcomponentsGUI import MyDialog_search_components_GUI


# Search dialog class for filtering components and presets
class ComponentSearchDialog(MyDialog_search_components_GUI):
    def __init__(self, parent, active_list, preset_list):
        super().__init__(parent)
        self.active_list = active_list
        self.preset_list = preset_list
        self.selected_item = None
        self.m_searchCtrl1.SetHint("Type component name (e.g. lens, mirror, ray)...")
        self.populate_list("")

    # When user types in the search search control box
    def m_searchCtrl1OnText(self, event):
        search_text = self.m_searchCtrl1.GetValue()
        self.populate_list(search_text)

    # When user double-clicks an item in the search listbox
    def m_listBox1OnListBoxDClick(self, event):
        self._confirm_selection(event)

    # When user clicks the OK button
    def m_sdbSizer1OKOnButtonClick(self, event):
        self._confirm_selection(event)

    # Filters active items and presets based on search query
    def populate_list(self, query):
        query_clean = query.strip().lower()
        self.m_listBox1.Clear()
        
        filtered_active = []
        if query_clean:
            for item in self.active_list:
                if query_clean in item.lower():
                    filtered_active.append(item)
        else:
            filtered_active = self.active_list

        filtered_preset = []
        if query_clean:
            for item in self.preset_list:
                if query_clean in item.lower():
                    filtered_preset.append(item)
        else:
            filtered_preset = self.preset_list

        if len(filtered_active) > 0:
            self.m_listBox1.Append("=== ACTIVE SCENE COMPONENTS ===")
            for item in filtered_active:
                self.m_listBox1.Append(item)

        if len(filtered_preset) > 0:
            self.m_listBox1.Append("=== AVAILABLE PRESET TEMPLATES ===")
            for item in filtered_preset:
                self.m_listBox1.Append(item)

        if self.m_listBox1.GetCount() > 1:
            self.m_listBox1.SetSelection(1)

    # Confirms selected component and closes dialog modal
    def _confirm_selection(self, event):
        selected_text = self.m_listBox1.GetStringSelection()
        
        if selected_text != "":
            if not selected_text.startswith("==="):
                self.selected_item = selected_text
                self.EndModal(wx.ID_OK)
                return

        if hasattr(event, "GetEventType"):
            if event.GetEventType() == wx.EVT_BUTTON.typeId:
                self.EndModal(wx.ID_CANCEL)

    # Display modal dialog and return result
    def ShowModal(self):
        result = super().ShowModal()
        if result == wx.ID_OK:
            if self.selected_item is None:
                selected_text = self.m_listBox1.GetStringSelection()
                if selected_text != "":
                    if not selected_text.startswith("==="):
                        self.selected_item = selected_text
        return result
