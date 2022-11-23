import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils

#スケルトン出力オペレーション
class TkExporter_Skeleton():
    
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
    
    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, armature):
        #Armatureオブジェクト選択時以外は何もしないため、リターン。
        if armature.type != "ARMATURE":
            return False
        return True
    
    
    #スケルトン出力をやる関数
    def execute(self,armature,filepath,matrix_world):
        
        with open(filepath, "wb") as target:
            edit_bones = list(armature.edit_bones)
            
            #骨の数を出力
            target.write( struct.pack("<i", len(edit_bones) ) )
            
            for bone in edit_bones:
                
                #骨の名前を出力
                target.write( struct.pack("<B", len(bone.name) ) )
                target.write( bone.name.encode() + b"\0")
                
                #親ボーンのインデックスを出力
                parent = bone.parent
                if parent is None:
                    target.write( struct.pack("<i", -1) )
                else:
                    target.write( struct.pack("<i", edit_bones.index(parent)) )
                #バインドポーズ
                boneMat = copy.deepcopy(bone.matrix)
                #アーマチュアオブジェクトのワールド行列をかけてボーンの行列をワールド基準にする。
                boneMat = matrix_world @ boneMat

                boneMat.transpose()#転置する。blenderは列優先。tkは行優先です。
                for vec3 in boneMat:
                    for i , m in enumerate(vec3):
                        if i != 3:
                            target.write( struct.pack("<f", m) )
                
                #バインドポーズの逆行列
                boneMat.invert()
                for vec3 in boneMat:
                    for i , m in enumerate(vec3):
                        if i != 3:
                            target.write( struct.pack("<f", m) )
