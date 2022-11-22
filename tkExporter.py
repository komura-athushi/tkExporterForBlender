import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils

#アドオン(スクリプト)の詳細？
bl_info = {
    "name": "tkExporter",
    #説明。-
    "description": "Informal tkExporter for Blender.\
    Good luck and make an tkmExporter.",
    "author": "komura",
    "version": (1, 1, 0, 0),
    "blender": (3, 3, 1),
    "category": "Properties",
    "location": "Window",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

ALBEDO_TEXTURE = "albedo"

class Vertex:
    def __init__(self):
        self.position = [0.0,0.0,0.0]
        self.normal = [0.0,0.0,0.0]
        self.uv = [0.0,0.0]
        self.skin_indexs = [0,0,0,0]
        self.skin_weights = [0.0,0.0,0.0,0.0]

#オブジェクトプロパティにパネルを追加する
class TkExporter_PT_Panel(bpy.types.Panel):
    bl_label = "TkExporter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    def draw(self, context):
        self.layout.operator("tkexporter.tkm")

#tkmファイルを出力する
#todo 重複した頂点バッファも違うものとして登録してしまっているので修正したい
class TkExporter_OT_Tkm(bpy.types.Operator):
    #ID
    bl_idname = "tkexporter.tkm"
    #パネルに表示されるテキスト
    bl_label = "createTkm"

    #ファイル拡張子
    filename_ext = ".tkm"

    #tkmファイルのバージョン
    TKM_VERSION = 100

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
  
    def build_vertex_and_index(self,mesh):
        #頂点バッファ
        self.vertices = {}
        #インデックスバッファ
        self.indices = []

        uv_layer = mesh.uv_layers.active.data

        self.print_data("uvの数は")
        self.print_data(len(uv_layer))

        #ポリゴン回す
        for poly in mesh.polygons:
            #ポリゴンが三角形なら
            if poly.loop_total == 3:
                #loopを回す
                for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                    self.add_vertex_and_index(mesh, poly, uv_layer, loop_index)
    
    def add_vertex_and_index(self,mesh,poly,uv_layer,loop_index):
        #頂点インデックスを取得
        vertex_index = mesh.loops[loop_index].vertex_index
        vertex_index = int(vertex_index)
        vertex_index = int(loop_index)
        '''
        #既にインデックスバッファにインデックスが追加済みなら
        if vertex_index in self.indices:
            #インデックスバッファにインデックスだけ追加してスルー。
            self.indices.append(vertex_index)
            return
        '''
        #インデックスバッファにインデックスを追加
        self.indices.append(vertex_index)
        vertex = Vertex()
        v = mesh.vertices[mesh.loops[loop_index].vertex_index]
                    
        vertex_position = v.co
        vertex_normal = v.normal

        vertex.position[0] = vertex_position[0]
        vertex.position[1] = vertex_position[1]
        vertex.position[2] = vertex_position[2]
        vertex.normal[0] = vertex_normal[0]
        vertex.normal[1] = vertex_normal[1]
        vertex.normal[2] = vertex_normal[2]
        vertex.uv[0] = uv_layer[loop_index].uv[0]
        vertex.uv[1] = uv_layer[loop_index].uv[1]

        #スキンインデックスとスキンウェイト
        for i in range(0,len(v.groups)):
            #4つのスキン？までしか対応してません
            if i > 3:
                break
            vg = v.groups[i]
            vertex.skin_indexs[i] = vg.group
            vertex.skin_weights[i] = vg.weight

        self.vertices[vertex_index] = vertex

    def get_texture_filepath(self,mesh):
        #テクスチャ
        self.textures = {}

        #マテリアルを取得
        mat = mesh.materials[0]
        #ノードツリーを取得
        node_tree = mat.node_tree
        #ノードの配列？を取得
        nodes = node_tree.nodes
        #ノードを回す。
        for node in nodes:
            #ラベル名がalbedoなら
            if node.label == ALBEDO_TEXTURE:
                #画像の絶対パスを入れる
                self.textures[ALBEDO_TEXTURE] = node.image.filepath_from_user()
            
    def write_file(self):
        #ファイルオープン
        with open(self.filepath, "wb") as target:
            #tkmのバージョンを出力
            target.write( struct.pack("<B",  self.TKM_VERSION))
            #フラットシェーディング
            target.write(struct.pack("<B",0))
            #メッシュパーツの数を出力(今は1で)
            target.write(struct.pack("<H",1))
            #マテリアルの数を出力(今は1で)
            target.write(struct.pack("<I",1))
            #頂点数を出力
            target.write(struct.pack("<I",len(self.indices)))
            index_size = 0
            #インデックスバッファのバイトサイズを出力
            #インデックスバッファのサイズが65536より小さいなら2byte
            if len(self.indices) < 65536:
                index_size = 2
            else:
                index_size = 4
            target.write(struct.pack("<B",index_size))
            #パディング(0を3回出力)
            target.write(struct.pack("<B",0))
            target.write(struct.pack("<B",0))
            target.write(struct.pack("<B",0))
            #マテリアル情報を出力(アルベド、法線マップ、スペキュラ、リフレクション、屈折)
            #ファイル名を、文字列の長さと文字列をそれぞれ出力
            #アルベド
            if ALBEDO_TEXTURE in self.textures:
                texture_name = self.textures[ALBEDO_TEXTURE]
                texture_name = texture_name.split("\\")
                texture_name = texture_name[-1]
                target.write(struct.pack("<I",len(texture_name)))
                target.write(texture_name.encode()+b"\0")
            else:
                target.write(struct.pack("<I",0))
            
            #法線、スペキュラ、リフレクション、屈折
            target.write(struct.pack("<I",0))
            target.write(struct.pack("<I",0))
            target.write(struct.pack("<I",0))
            target.write(struct.pack("<I",0))
            #頂点バッファを出力
            for i in range(0,len(self.indices)):
                vertex = self.vertices[i]
                #座標
                for vec in vertex.position:
                    target.write(struct.pack("f",vec))
                #法線
                for vec in vertex.normal:
                    target.write(struct.pack("f",vec))
                #UV
                for vec in vertex.uv:
                    target.write(struct.pack("f",vec))
                #ボーンウェイト
                for vec in vertex.skin_weights:
                    target.write(struct.pack("f",vec))
                #スキンインデックス
                for vec in vertex.skin_indexs:
                    target.write(struct.pack("h",vec))

            #ポリゴン数を出力
            polygon_index = len(self.indices) / 3
            target.write(struct.pack("<i", int(polygon_index)))
            #インデックスバッファを出力(今は2byte)
            for index in self.indices:
                if index_size == 2:
                    target.write(struct.pack("<H", index+1))
                else:
                    target.write(struct.pack("<I", index+1))

    def output_dds_texture(self):
        self.print_data("カレンドディレクトリは")
        self.print_data(os.getcwd())
        cmd_file = "mk.bat"   #.batファイルへのパス
        filepath = self.filepath
        number = filepath.rfind('\\')
        filepath = filepath[:number]
        for i in self.textures:
            command = cmd_file
            command += " " + self.textures[i].replace('/', '\\')
            command += " " + filepath.replace('/', '\\')
            os.system(command)

    #invokeの後に呼ばれる関数
    def execute(self, context):
        #編集モードに切り替える
        #bpy.ops.object.mode_set(mode='EDIT')
        #オブジェクトモードに切り替える
        bpy.ops.object.mode_set(mode='OBJECT')

        #メッシュデータを取得
        mesh = context.object.data

        #メッシュデータ4つの配列
        #mesh.vertices 3つの頂点
        #mesh.edges 1つの辺
        #mesh.loops 単一の頂点とエッジ
        #mesh.polygons  ポリゴン(loopsへの参照)
        

        #struct.pac()
        #バイトコードとして解釈する
        #int                i
        #unsignd int        I
        #unsigned char      B(文字の長さとか)
        #short              h
        #unsigned short     H
        #float              f
        #文字列     .encode()+b"\0"(ヌル文字)

        #頂点バッファとインデックスバッファを構築
        self.build_vertex_and_index(mesh)
        #テクスチャのファイルパスを取得
        self.get_texture_filepath(mesh)
        #tkmファイル書き出し
        self.write_file()
        #ddsファイル作成
        self.output_dds_texture()

        
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
