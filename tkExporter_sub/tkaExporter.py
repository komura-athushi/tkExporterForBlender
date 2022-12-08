import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils


#アニメーション出力オペレーション
class TkExporter_Animation():
    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        armature = context.object
        
        #Armatureオブジェクト選択時以外は何もしないため、リターン。
        if armature.type != "ARMATURE":
           return False
        #アニメーションが無いため、リターン
        if (armature.animation_data is None) or (armature.animation_data.action is None):
           return False
        return True
    
    
    #アニメーション出力をやる関数
    def execute(self, context,filepath,bone_name_list,pose_bones):
        
        with open(filepath, "wb") as target:
            
            scene = context.scene
            armar = context.object

            #キーフレームの数を出力
            target.write(struct.pack("<I", (scene.frame_end - scene.frame_start) * len(pose_bones)))

            time = 0#経過時間を入れとく変数
            spf = 1 / scene.render.fps#フレームあたりの秒数

             #アニメーションイベント数を出力
            eventcount = len(armar.animation_data.action.pose_markers)
            target.write(struct.pack("<I", eventcount))
            #アニメーションイヴェントの出力
            for event in armar.animation_data.action.pose_markers:
                fr = spf * event.frame
                #ｲｳﾞｪﾝﾄﾉｵｺﾙｼﾞｶﾝ(ﾋﾞｮｳ)
                target.write( struct.pack("<f", fr) )
                #イヴェント名の出力
                target.write( struct.pack("<i", len(event.name)) )
                target.write(event.name.encode()+b"\0")

            for frame in range(scene.frame_start , scene.frame_end+1):
                scene.frame_set(frame)    

                for bone in pose_bones:
                    #ボーンのインデックスを出力
                    target.write( struct.pack("<I", bone_name_list.index(bone.name)) )
                    
                    #秒数を出力
                    target.write( struct.pack("<f", time) )

                    #ボーンの行列を出力
                    matrix = copy.deepcopy(bone.matrix)

                    #アーマチュアオブジェクトのワールド行列をかけてボーンの行列をワールド基準にする。
                    matrix = context.object.matrix_world @ matrix

                    #Yアップに変換
                    #matrix = transToYUp(matrix)

                    if not bone.parent is None:
                        #親の逆行列をかけて自分の座標系にする。親もワールド基準に直すのを忘れない。
                        invMat = copy.deepcopy(context.object.matrix_world @ bone.parent.matrix)
                        invMat.invert()
                        #列優先なのでこの順番
                        matrix = invMat @ matrix
                        del invMat

                    matrix.transpose()#転置する。blenderは列優先。tkEngineは行優先です。

                    for vec3 in matrix:
                        for i , m in enumerate(vec3):
                            if i != 3:
                                target.write( struct.pack("<f", m) )
                
                #1フレームあたりの秒数をプラス
                time += spf
