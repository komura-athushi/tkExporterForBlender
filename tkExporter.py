import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils

import sys
# 読み込み元のディレクトリパスを取得
addon_dirpath = os.path.dirname(__file__)
addon_dirpath += "/tkExporter_sub"
# 読み込み元のディレクトリパスをシステムパスに追加
sys.path += [addon_dirpath]

import tkmExporter
import tksExporter

#アドオン(スクリプト)の詳細？
bl_info = {
    "name": "tkExporter",
    #説明。-
    "description": "Informal tkExporter for Blender.\
    Good luck and make an tkmExporter.",
    "author": "komura",
    "version": (1, 2, 0, 0),
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
        self.layout.operator("tkexporter.skeleton")

#tkmファイル出力
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

    def print_data(self,message):
        self.report({'INFO'}, str(message))

    def invoke(self, context, event):
        self.tkm = tkmExporter.TkExporter_Tkm()
        if self.tkm.invoke(context.object) == False:
            self.print_data("Please select Mesh object!")
            return {'FINISHED'}
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
        #編集モードに切り替える
        #bpy.ops.object.mode_set(mode='EDIT')
        #オブジェクトモードに切り替える
        bpy.ops.object.mode_set(mode='OBJECT')
        #メッシュデータを取得
        mesh = context.object.data
        self.tkm.execute(mesh,self.filepath)
        self.print_data("Finished making tkm file.")
        return {'FINISHED'}

#スケルトン出力オペレーション
class TkExporter_OT_Skeleton(bpy.types.Operator):
    
    bl_idname = "tkexporter.skeleton"
    bl_label = "createSkeleton"
    
    filename_ext = ".tks"

    #ダイアログから受け取ったファイル名を入れておく変数(?)。
    filepath : StringProperty(
        name="Tks_FilePath",
        description="Filepath used for exporting the file",
        default = "untitled.tks",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    def print_data(self,message):
        self.report({'INFO'}, str(message))

    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        self.tks = tksExporter.TkExporter_Skeleton()
        armature = context.object
        #Armatureオブジェクト選択時以外は何もしないため、リターン。
        if self.tks.invoke(armature) == False:
            self.report({'INFO'}, "Please select Armature object!")
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
        return {'RUNNING_MODAL'}

    #invokeの後に呼ばれる関数
    def execute(self, context):
        #編集モードに切り替える 
        bpy.ops.object.mode_set(mode='EDIT')
        #オブジェクトモードに切り替える
        #bpy.ops.object.mode_set(mode='OBJECT')
        arm = context.object.data
        con = context
        self.tks.execute(arm, self.filepath,context.object.matrix_world)
    
        #self.tks.execute(armature=arm, filepath=self.filepath, world_matrix=context.object.matrix_world)
        self.print_data("Finished making skeleton file.")
        return{'FINISHED'}

#各クラスの配列
classes = {
    TkExporter_PT_Panel,
    TkExporter_OT_Tkm,
    TkExporter_OT_Skeleton
}

#クラスをblenderに追加していきます
def register():
    for c in classes:
        bpy.utils.register_class(c)

#クラスをblenderから外します。
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
