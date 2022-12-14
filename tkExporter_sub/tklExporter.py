import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils


TKL_VERSION = 100

#ドット以下を無視する関数
def deleteAfterDot(name):
    index = 0
    for c in name:
        if c == ".":
            return name[0:index]
        index += 1
    
    return name

#レベル出力オペレーション
class TkExporter_Level():    
    #レベル出力をやる関数
    def execute(self, context,filepath,isDeleteDot):
        colle = context.collection
        with open(filepath, "wb") as target:

            #tklのバージョンを出力
            target.write(struct.pack("<i", TKL_VERSION))
            #オブジェクトの総数を出力。(一番最初は無視されるので1プラス)
            target.write(struct.pack("<i", len(colle.all_objects) + 1))

            #一番最初の無視される用ダミー
            target.write(struct.pack("<B", 0))#名前の長さ
            target.write(struct.pack("<B", 0))#ヌル文字
            target.write(struct.pack("<i", -1))#親の番号(親無しの意)
            for i in range(3*4*2):
                target.write(struct.pack("<f", 0))#行列(どうせ無視されるの)

            #シャドウフラグの調整
            #シャドウキャスターフラグ
            target.write(struct.pack("<?", 0))
            #シャドウレシーバーフラグ
            target.write(struct.pack("<?", 0))

            #それぞれのデータ
            #intデータ
            target.write(struct.pack("<i", 0))
            #floatデータ
            target.write(struct.pack("<i", 0))
            #charデータ
            target.write(struct.pack("<i", 0))
            #Vector3データ
            target.write(struct.pack("<i", 0))
            
            #ここから各オブジェクトの情報
            for obj_data in colle.all_objects:
                name = obj_data.name
                #ドット以下削除
                if isDeleteDot:
                    name = deleteAfterDot(name)
                #エンコード(バイト文字列に変換)
                name_jis = name.encode("shift_jis")

                target.write(struct.pack("<B", len(name_jis)))#名前の長さ
                target.write(name_jis + b"\0")#オブジェクトの名前
                target.write(struct.pack("<i", 0))#親の番号(実際には親ではなくコレクションだが、とりあえず0番を入れとく)

                #オブジェクトのワールド行列を取得
                objMat = copy.deepcopy(obj_data.matrix_world)

                objMat.transpose()#転置する。blenderは列優先。tkは行優先です。

                for vec3 in objMat:
                    for i , m in enumerate(vec3):
                        if i != 3:
                            target.write( struct.pack("<f", m) )
                
                #逆行列
                objMat.invert()
                for vec3 in objMat:
                    for i , m in enumerate(vec3):
                        if i != 3:
                            target.write( struct.pack("<f", m) )
                

                #シャドウフラグの調整
                #シャドウキャスターフラグ
                if obj_data.isShadowCaster:
                    target.write(struct.pack("<?", 1))
                else:
                    target.write(struct.pack("<?", 0))
                #シャドウレシーバーフラグ
                if obj_data.isShadowReceiver:
                    target.write(struct.pack("<?", 1))
                else:
                    target.write(struct.pack("<?", 0))

                #それぞれのデータ
                #todo Blenderにパネルを追加して設定できるようにしたい

                #for obj in bpy.data.objects:
                obj = bpy.data.objects.get(name)

                param_list = []
                key_list = ["Int","Float","Char","Vector"]
                for i in range(0,len(key_list)):
                    param_list.append([])
                for key,value in obj.items():
                    index = 0
                    for i in key_list:
                        if i in key:
                            param_list[index].append(value)
                        index += 1
            
                for index in range(0,len(param_list)):
                    params = param_list[index]
                    target.write(struct.pack("<i", len(params)))
                    param_type = key_list[index]
                    
                    for param in params:
                        print(type(param))
                        #intデータ
                        if param_type == "Int":
                            target.write(struct.pack("<i", param))
                        #floatデータ
                        if param_type == "Float":
                            target.write(struct.pack("<f", param))
                        #charデータ
                        if param_type == "Char":
                            print(len(param))
                            target.write(struct.pack("<B", len(param)))#名前の長さ
                            target.write(param.encode("shift_jis") + b"\0")
                        #Vector3データ
                        if param_type == "Vector":
                            for i in param:
                                target.write(struct.pack("<f", i))
                
        return
