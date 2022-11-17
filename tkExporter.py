import copy
import struct
import os

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils

#アドオン(スクリプト)の詳細？
bl_info = {
    "name": "tkExporter",
    #説明。
    "description": "Informal tkExporter for Blender.\
    Good luck and make an tkmExporter.",
    "author": "komura",
    "version": (1, 0, 0, 0),
    "blender": (3, 3, 1),
    "category": "Properties",
    "location": "Window",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

#オブジェクトプロパティにパネルを追加する
class TkExporter_PT_Panel(bpy.types.Panel):
    bl_label = "TkExporter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    def draw(self, context):
        self.layout.operator("tkexporter.tkm")

#tkmファイルを出力したい
class TkExporter_OT_Tkm(bpy.types.Operator):
    #ID
    bl_idname = "tkexporter.tkm"
    #パネルに表示されるテキスト
    bl_label = "createTkm"

    #ファイル拡張子
    filename_ext = ".tkm"

    #ダイアログから受け取ったファイル名を入れておく変数(?)。
    
    filepath : StringProperty(
        name="Tkm_FilePath",                                #プロパティ
        description="Filepath used for exporting the file", #説明文
        default = "untitled.tkm",                           #デフォルト
        maxlen=1024,                                        #長さ
        subtype='FILE_PATH',                                #サブタイプ
    )

    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        mesh = context.object
        
        #選択されたオブジェクトがMESH以外なら
        #処理を終了させる
        if mesh.type != "MESH":
            self.report({'INFO'}, "Please select Armature object.")
            return{'FINISHED'}

        
        #デフォルトの文字列を設定する。
        blend_filepath = context.blend_data.filepath
        if not blend_filepath:
            blend_filepath = "untitled"
        else:
            blend_filepath = os.path.splitext(blend_filepath)[0]

        self.filepath = blend_filepath + self.filename_ext

        #ファイルダイアログを開く。
        #ダイアログが閉じたとき、execute()を呼んでくれるらしい。
        context.window_manager.fileselect_add(self)

        #ここはRUNNING_MODALで固定？
        return {'RUNNING_MODAL'}
  
    #invokeの後に呼ばれる関数
    def execute(self, context):

        print("pushed")
        return{'FINISHED'}
  
#各クラスの配列
classes = {
    TkExporter_PT_Panel,
    TkExporter_OT_Tkm
}

#クラスをblenderに追加していきます
def register():
    for c in classes:
        bpy.utils.register_class(c)

#クラスをblenderから外します。
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
