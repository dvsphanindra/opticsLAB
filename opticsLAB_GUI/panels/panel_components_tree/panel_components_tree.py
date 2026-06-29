"""
Components Tree Panel for OpticsLAB.
Displays optical system components and light rays in a tree hierarchy widget.
Simple and clean code for updating and selecting elements in the tree.
"""
import wx
from panel_components_tree_GUI import MyPanel_panel_components_tree as MyPanel_components_tree_GUI
from opticsLAB_support import TREE_CATEGORY_LABELS, is_template_name


# Component tree panel class for displaying system hierarchy
class ComponentsTreePanel(MyPanel_components_tree_GUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self._init_tree()

    # Initializes tree widget icons and structure
    def _init_tree(self):
        tree = self.treeCtrl_projectComponents
        tree.DeleteAllItems()
        self.il = wx.ImageList(16, 16)
        
        folder_art = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16))
        open_art = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16))
        file_art = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16))
        
        self.il.Add(folder_art)
        self.il.Add(open_art)
        self.il.Add(file_art)
        
        tree.AssignImageList(self.il)
        self.update_tree()

    # Redraws the tree with current workspace components and light rays
    def update_tree(self):
        tree = self.treeCtrl_projectComponents
        tree.Freeze()
        tree.DeleteAllItems()

        proj_name = self.frame.project_info.get("name", "Optics System Layout")
        self.root = tree.AddRoot(proj_name, image=0, selImage=1)

        proj_node = tree.AppendItem(self.root, "[project]", image=0, selImage=1)
        tree.SetItemData(proj_node, "[project]")

        comps_node = tree.AppendItem(self.root, "[[components]]", image=0, selImage=1)
        tree.SetItemData(comps_node, "[[components]]")

        if self.frame.active_components:
            for name, comp in self.frame.active_components.items():
                item = tree.AppendItem(comps_node, name, image=2)
                tree.SetItemData(item, name)
                
                if hasattr(comp, "get_Rays") and callable(comp.get_Rays):
                    try:
                        ray_list = comp.get_Rays()
                        for idx, ray in enumerate(ray_list, 1):
                            ray_title = f"Ray {idx}"
                            ray_item = tree.AppendItem(item, ray_title, image=2)
                            tree.SetItemData(ray_item, (name, idx - 1))
                    except Exception:
                        pass

        tree.ExpandAll()
        tree.Thaw()

    # When user clicks an item in the tree control
    def m_treeCtrl1OnTreeSelChanged(self, event):
        item = event.GetItem()
        if not item.IsOk():
            self.frame.show_project_properties()
            return

        tree = self.treeCtrl_projectComponents
        label = tree.GetItemText(item)
        data = tree.GetItemData(item)
        
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            self.frame.GetStatusBar().SetStatusText(f"Selected component: {label}", 0)

        if label == "[project]" or data == "[project]":
            self.frame.show_project_properties()
            return

        if isinstance(data, tuple) and len(data) == 2:
            parent_comp_name, ray_idx = data
            if hasattr(self.frame, "show_ray_properties"):
                self.frame.show_ray_properties(parent_comp_name, ray_idx)
            return

        if label in TREE_CATEGORY_LABELS or label.startswith("Traced Segment"):
            self.frame.show_project_properties()
            return

        comp_name = data or label
        if isinstance(comp_name, str):
            if is_template_name(comp_name) or comp_name in self.frame.active_components:
                self.frame.show_component_properties(comp_name)
            else:
                self.frame.show_project_properties()
        else:
            self.frame.show_project_properties()
