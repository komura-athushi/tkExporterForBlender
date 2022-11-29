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
            #todo Blenderにパネルを追加して設定できるようにしたい
            #シャドウキャスターフラグ
            target.write(struct.pack("<?", 0))
            #シャドウレシーバーフラグ
            target.write(struct.pack("<?", 0))

            #それぞれのデータ
            #todo Blenderにパネルを追加して設定できるようにしたい
            #intデータ
            target.write(struct.pack("<i", 0))
            #floatデータ
            target.write(struct.pack("<i", 0))
            #charデータ
            target.write(struct.pack("<i", 0))
            #Vector3データ
            target.write(struct.pack("<i", 0))
            
            #ここから各オブジェクトの情報
            for obj in colle.all_objects:
                name = obj.name
                #ドット以下削除
                if isDeleteDot:
                    name = deleteAfterDot(name)
                #エンコード(バイト文字列に変換)
                name = name.encode("shift_jis")

                target.write(struct.pack("<B", len(name)))#名前の長さ
                target.write(name + b"\0")#オブジェクトの名前
                target.write(struct.pack("<i", 0))#親の番号(実際には親ではなくコレクションだが、とりあえず0番を入れとく)

                #オブジェクトのワールド行列を取得
                objMat = copy.deepcopy(obj.matrix_world)

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
                #todo Blenderにパネルを追加して設定できるようにしたい
                #シャドウキャスターフラグ
                target.write(struct.pack("<?", 0))
                #シャドウレシーバーフラグ
                target.write(struct.pack("<?", 0))

                #それぞれのデータ
                #todo Blenderにパネルを追加して設定できるようにしたい
                #intデータ
                target.write(struct.pack("<i", 0))
                #floatデータ
                target.write(struct.pack("<i", 0))
                #charデータ
                target.write(struct.pack("<i", 0))
                #Vector3データ
                target.write(struct.pack("<i", 0))
                
        return