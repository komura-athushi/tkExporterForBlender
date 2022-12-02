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
import tkaExporter
import tklExporter

#アドオン(スクリプト)の詳細？
bl_info = {
    "name": "tkExporter",
    #説明。-
    "description": "Informal tkExporter for Blender.\
    Good luck and make an tkmExporter.",
    "author": "komura",
    "version": (1, 5, 2, 0),
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
        self.layout.operator("tkExporter.animation")
        self.layout.operator("tkExporter.level")

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

    isOutputAllMeshOnCollection : BoolProperty(
        name="Output all mesh on Collection.",
        description="If it's true, it Output all mesh on Collection.",
        default=False,
    )

    def print_data(self,message):
        self.report({'INFO'}, str(message))

    def invoke(self, context, event):
        self.tkm = tkmExporter.TkExporter_Tkm()

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

        self.meshs = []
        self.armature = None
        self.bones = {}

        #選択したメッシュオブジェクトをtkmとして出力する
        if self.isOutputAllMeshOnCollection == False:
            #選択されたオブジェクトがメッシュでなければ
            if context.object.type != "MESH":
                self.report({'INFO'}, "Please select Mesh object!")
                return{'FINISHED'}
            #メッシュなら
            else:
                self.meshs.append(context.object)
        #Collection直下のメッシュオブジェクトをtkmとして出力する
        else:
            #コレクションを取得
            collection = context.collection
            #コレクションのオブジェクトを検索
            for children in collection.all_objects:
                #メッシュタイプなら
                if children.type == "MESH":
                    #配列に追加
                    self.meshs.append(children)
            if len(self.meshs) == 0:
                self.report({'INFO'}, "There is no Mesh object!")
                return{'FINISHED'}


        #コレクションを取得
        collection = context.collection
        #コレクションのオブジェクトを検索
        for children in collection.all_objects:
            #アーマチュアタイプなら
            if children.type == "ARMATURE":
                self.armature = children

        #アーマチュアが見つからなければ
        if self.armature == None:
            self.tkm.execute(self.meshs,self.filepath,self.bones)
            self.print_data("Finished making tkm file.")
            return {'FINISHED'}

        # 他のオブジェクトに操作を適用しないよう全てのオブジェクトを走査する
        for ob in bpy.context.scene.objects:
            # 非選択状態に設定する
            ob.select_set(False)

        selectob = bpy.data.objects.get(self.armature.name)
        # 変更オブジェクトをアクティブに変更する
        bpy.context.view_layer.objects.active = selectob
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        edit_bones = list(self.armature.data.edit_bones)
        bone_number = 0
        for bone in edit_bones: 
            #ボーンの名前をキー、番号を値とする辞書を作成
            self.bones[bone.name] = bone_number
            bone_number += 1
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        #tkmファイル出力
        self.tkm.execute(self.meshs,self.filepath,self.bones)
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
        self.print_data("Finished making skeleton file.")
        return{'FINISHED'}

#アニメーション出力オペレーション
class TkExporter_OT_Animation(bpy.types.Operator):
    
    bl_idname = "tkexporter.animation"
    bl_label = "createAnimation"
    
    filename_ext = ".tka"

    #ダイアログから受け取ったファイル名を入れておく変数(?)。
    filepath : StringProperty(
        name="Tka_FilePath",
        description="Filepath used for exporting the file",
        default = "untitled.tka",
        maxlen=1024,
        subtype='FILE_PATH',
    )
    
    def print_data(self,message):
        self.report({'INFO'}, str(message))

    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        self.tka = tkaExporter.TkExporter_Animation()
        armature = context.object

        if self.tka.invoke(context, event) == False:
            self.print_data("Please select Armature object, or The armature don't has animations")
            return{'FINISHED'}

        #デフォルトの文字列を設定する。
        blend_filepath = context.blend_data.filepath
        if not blend_filepath:
            blend_filepath = "untitled"
        else:
            blend_filepath = os.path.splitext(blend_filepath)[0] + "_" + armature.animation_data.action.name

        self.filepath = blend_filepath + self.filename_ext

        #ファイルダイアログを開く。
        #ダイアログが閉じたとき、execute()を呼んでくれるらしい。
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}
    
    
    #アニメーション出力をやる関数
    def execute(self, context):
        #エディットモードとポーズモードでボーンの並びが違うので
        #エディットモード基準のインデックスを使うために名前のリストを作る
        bpy.ops.object.mode_set(mode='EDIT')
        bone_name_list = [b.name for b in context.object.data.edit_bones]
        bpy.ops.object.mode_set(mode='POSE')
        pose_bones = context.object.pose.bones
        self.tka.execute(context, self.filepath, bone_name_list, pose_bones)
        self.print_data("Finished making animation file.")
        return {'FINISHED'}

#レベル出力オペレーション
class TkExporter_OT_Level(bpy.types.Operator):

    bl_idname = "tkexporter.level"
    bl_label = "createLevel"
    
    filename_ext = ".tkl"

    #ダイアログから受け取ったファイル名を入れておく変数(?)。
    filepath : StringProperty(
        name="Tkl_FilePath",
        description="Filepath used for exporting the file",
        default = "untitled.tkl",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    #blenderは名前の重複を許さないので、出力時に任意で名前のドット(.)以下を削除します。
    #ファイルダイアログが開いたときに左側にDelete name after the dot.というチェックボックスがあるので
    #それにチェックを入れると削除が有効になります。
    #例：Box.001 => Box
    #    Box.0.1 => Box
    #    Box_1.001 => Box_1
    isDeleteDot : BoolProperty(
        name="Delete name after the dot.",
        description="If it's true, it delete name after the dot.",
        default=False,
    )

    def print_data(self,message):
        self.report({'INFO'}, str(message))

    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
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
    
    
    #レベル出力をやる関数
    def execute(self, context):
        self.tkl = tklExporter.TkExporter_Level()
        self.tkl.execute(context, self.filepath,self.isDeleteDot)
        self.print_data("Finished making level file.")
        return {'FINISHED'}

#各クラスの配列
classes = {
    TkExporter_PT_Panel,
    TkExporter_OT_Tkm,
    TkExporter_OT_Skeleton,
    TkExporter_OT_Animation,
    TkExporter_OT_Level
}

#クラスをblenderに追加していきます
def register():
    for c in classes:
        bpy.utils.register_class(c)

#クラスをblenderから外します。
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
