import copy
import struct
import os

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils

#アドオンの詳細
bl_info = {
    "name": "tkExporter",
    #注意：descriptionは1行目以外すべて野本晟矢による加筆です。
    "description": "Informal tkExporter for Blender.\
AnimationEvent mo shuturyoku dekiru kamo shirehen wa!\
Marker you no tukatte yarun yakedo... ma, yo wakaran kattara \
yamaP ni nan demo keyte na! wai mo yo wakaran nen.\
Teka, marker saisho wa global ni natten no honma nazo yawa.\
Sono hen Marker tukau yakara wa key tuke ya.\
Nishitemo honma Blender you natta yona, wai wa saisho tomadottan yakedo,\
korekara hajimeru hitora ni totte wa wakari yasuku natteru to omou wa!\
Kore kara wa blender no jidai yade! Hahasi kawaru kedo StarWars no jedai tte \
Sengoku Jidai no Jidai kara kiteru rashi de.Shinjiru ka shinji nai kawa anata shidai ya!\
Konnani kaite mo blender de hyouji sare hen noga honma kanashie wa.\
Ma, betuni kinisee hen kedona!Kono sourse code ijiru yakara ga itehattara \
kitto zenbu yonde kureru yaro, sonai na yatu zettai Hentai ni kimatte harukara na!\
Blender min mot huete hoshi na.show me 3DSMAX toka Maya toka irahen nen onedan takai dake \
yade, annan ni toushi surugurai nara Blender ni toushi shita houga 100by mashi yawa.",
    "author": "kbc18b13",
    "version": (1, 0, 0, 0),
    "blender": (2, 80, 2),
    "category": "Properties",
    "location": "Window",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

#列優先行列をYアップに変換する(なので転置前に使ってね！)
#戻り値として変換後の行列を返す
def transToYUp(matrix):
    #ZUpをYUpに変えるための回転行列
    rotMat = mathutils.Matrix([ [1, 0,0,0],\
                                [0, 0,1,0],\
                                [0,-1,0,0],\
                                [0, 0,0,1]])
    matrix = rotMat @ matrix
    return matrix

#オブジェクトプロパティに追加されるパネル
class TkExporter_PT_Panel(bpy.types.Panel):
    bl_label = "TkExporter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    def draw(self, context):
        self.layout.operator("tkexporter.skeleton")
        self.layout.operator("tkexporter.animation")
        self.layout.operator("tkexporter.level")


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
    
    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        armature = context.object
        
        #Armatureオブジェクト選択時以外は何もしないため、リターン。
        if armature.type != "ARMATURE":
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
        
        return {'RUNNING_MODAL'}
    
    
    #スケルトン出力をやる関数
    def execute(self, context):
        
        with open(self.filepath, "wb") as target:
            
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = list(context.object.data.edit_bones)
            
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
                boneMat = context.object.matrix_world @ boneMat

                #Yアップに変換
                boneMat = transToYUp(boneMat)

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
                
        self.report({'INFO'}, "Finished making skeleton file.")
        return {'FINISHED'}


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
    
    #ボタンを押すとexecuteの前に呼ばれる関数。
    def invoke(self, context, event):
        armature = context.object
        
        #Armatureオブジェクト選択時以外は何もしないため、リターン。
        if armature.type != "ARMATURE":
            self.report({'INFO'}, "Please select Armature object.")
            return{'FINISHED'}

        #アニメーションが無いため、リターン
        if (armature.animation_data is None) or (armature.animation_data.action is None):
            self.report({'INFO'}, "The armature don't has animations")
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
        
        with open(self.filepath, "wb") as target:
            
            scene = context.scene
            armar = context.object

            #エディットモードとポーズモードでボーンの並びが違うので
            #エディットモード基準のインデックスを使うために名前のリストを作る
            bpy.ops.object.mode_set(mode='EDIT')
            bone_name_list = [b.name for b in context.object.data.edit_bones]

            bpy.ops.object.mode_set(mode='POSE')
            pose_bones = context.object.pose.bones

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
                    matrix = transToYUp(matrix)

                    if not bone.parent is None:
                        #親の逆行列をかけて自分の座標系にする。親もワールド基準に直すのを忘れない。
                        invMat = copy.deepcopy(transToYUp(context.object.matrix_world @ bone.parent.matrix))
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
                
        self.report({'INFO'}, "Finished making animation file.")
        return {'FINISHED'}

#ドット以下を無視する関数
def deleteAfterDot(name):
    index = 0
    for c in name:
        if c == ".":
            return name[0:index]
        index += 1
    
    return name



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
        colle = context.collection
        with open(self.filepath, "wb") as target:

            #オブジェクトの総数を出力。(一番最初は無視されるので1プラス)
            target.write(struct.pack("<I", len(colle.all_objects) + 1))

            #一番最初の無視される用ダミー
            target.write(struct.pack("<B", 0))#名前の長さ
            target.write(struct.pack("<B", 0))#ヌル文字
            target.write(struct.pack("<i", -1))#親の番号(親無しの意)
            for i in range(3*4*2):
                target.write(struct.pack("<f", 0))#行列(どうせ無視されるの)
            
            #ここから各オブジェクトの情報
            for obj in colle.all_objects:
                name = obj.name
                #ドット以下削除
                if self.isDeleteDot:
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
                
        self.report({'INFO'}, "Finished making level file.")
        return {'FINISHED'}
                



classes = {
    TkExporter_PT_Panel,
    TkExporter_OT_Skeleton,
    TkExporter_OT_Animation,
    TkExporter_OT_Level
}

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

