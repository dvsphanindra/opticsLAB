"""
Project workspace directory browser tree panel for OpticsLAB.
Browses files and directories directly without using background threads.
All threading concepts have been removed for straightforward synchronous operations.
"""
import json
import os
import wx
from panel_project_folder_tree_GUI import MyPanel_panel_components_tree as MyPanel_project_folder_tree_GUI
from opticsLAB_support import load_toml


class ProjectFolderTreePanel(MyPanel_project_folder_tree_GUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.populate_tree()

    def load_directory(self, path):
        self.current_dir = path
        self.populate_tree()

    def clear_directory(self):
        self.current_dir = None
        tree = self.treeCtrl_projectDirectory
        tree.DeleteAllItems()
        self.root = tree.AddRoot("(No Folder Opened)", image=0, selImage=0)

    # Scans the workspace folder directly and displays files in the tree view
    def populate_tree(self):
        tree = self.treeCtrl_projectDirectory
        tree.DeleteAllItems()
        self.il = wx.ImageList(16, 16)
        for art in (wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE):
            self.il.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, (16, 16)))
        tree.AssignImageList(self.il)

        if not self.current_dir:
            self.root = tree.AddRoot("(No Folder Opened)", image=0, selImage=0)
            return

        self.root = tree.AddRoot(os.path.basename(self.current_dir) or "Project Folder", image=0, selImage=1)
        tree.SetItemData(self.root, self.current_dir)
        
        # Scan folders and build tree nodes directly in main thread
        nodes = self._scan_directory_structure(self.current_dir, 0)
        self._populate_nodes_gui(self.root, nodes)
        try: self.treeCtrl_projectDirectory.Expand(self.root)
        except Exception: pass

    # Reads files and folders up to 2 subfolders deep
    def _scan_directory_structure(self, path, depth):
        if depth > 2: return []
        try: items = sorted(os.listdir(path))
        except OSError: return []

        nodes = []
        for item in items:
            if item.startswith(".") or item == "__pycache__": continue
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            sub_nodes = self._scan_directory_structure(full_path, depth + 1) if is_dir else []
            nodes.append((item, full_path, is_dir, sub_nodes))
        return nodes

    # Adds scanned folder items into the GUI tree widget
    def _populate_nodes_gui(self, parent_node, nodes):
        tree = self.treeCtrl_projectDirectory
        for item, full_path, is_dir, sub_nodes in nodes:
            node = tree.AppendItem(parent_node, item, image=0 if is_dir else 2, selImage=1 if is_dir else 2)
            tree.SetItemData(node, full_path)
            if is_dir and sub_nodes:
                self._populate_nodes_gui(node, sub_nodes)

    # When user clicks a file in the tree, load it directly
    def treeCtrl_projectDirectoryOnTreeSelChanged(self, event):
        item = event.GetItem()
        if not item.IsOk() or item == self.root: return

        full_path = self.treeCtrl_projectDirectory.GetItemData(item)
        if not full_path or not os.path.isfile(full_path) or not full_path.lower().endswith((".json", ".toml")):
            return

        # Load project file content directly
        raw, p_path = self._read_project_file(full_path)
        if hasattr(self.frame, "load_project_data"):
            self.frame.load_project_data(raw, p_path)

    # Reads json or toml project configuration file from disk
    def _read_project_file(self, full_path):
        if full_path.endswith(".json"):
            with open(full_path, "r", encoding="utf-8") as h: raw = json.load(h)
        else:
            raw = load_toml(full_path)
        return raw, full_path
