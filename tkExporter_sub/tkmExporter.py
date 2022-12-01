import copy
import struct
import os
import re
import pathlib

import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty
import mathutils


ALBEDO_TEXTURE = "albedo"

class Vertex:
    def __init__(self):
        self.position = [0.0,0.0,0.0]
        self.normal = [0.0,0.0,0.0]
        self.uv = [0.0,0.0]
        self.skin_indexs = [0,0,0,0]
        self.skin_weights = [0.0,0.0,0.0,0.0]

class UVVertex:
    def __init__(self):
        self.index = 0
        self.uv = [0.0,0.0]

class Mesh:
    def __init__(self):
        return
    
    def build_vertex_and_index(self,mesh,matrix_world,bones):
        #頂点バッファ
        self.vertices = {}
        #インデックスバッファ
        self.indices = {}
        #UV頂点バッファ
        self.uv_vertices = {}

        vertex_groups = mesh.vertex_groups
        for vg in vertex_groups:
            print(vg.name)
            print(vg.index)
        print(vertex_groups[0])

        #マテリアルの数だけ
        self.num_material = len(mesh.data.materials)
        for i in range(0,self.num_material):
            self.indices[i] = []
        uv_layer = mesh.data.uv_layers.active.data
        #最大のインデックス
        self.max_index = len(mesh.data.vertices)
        #ポリゴン回す
        for poly in mesh.data.polygons:
            #ポリゴンが三角形なら
            if poly.loop_total == 3:
                #loopを回す
                for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                    self.add_vertex_and_index(mesh, poly, uv_layer, loop_index,matrix_world,bones)
    
    def add_vertex_and_index(self,mesh,poly,uv_layer,loop_index,matrix_world,bones):
        #頂点インデックスを取得
        vertex_index = mesh.data.loops[loop_index].vertex_index
        #頂点バッファの番号
        vertex_index = int(vertex_index)
        #vertex_index = int(loop_index)
        #マテリアルID
        material_index = poly.material_index
        
        #UV座標
        vertex_uv = [0.0,0.0]
        vertex_uv[0] = uv_layer[loop_index].uv[0]
        vertex_uv[1] = uv_layer[loop_index].uv[1]

        #既にUV頂点バッファにインデックスが既に存在していたら
        if vertex_index in self.uv_vertices:
            for uv_vertex in self.uv_vertices[vertex_index]:
                #UVが一致していたら
                if vertex_uv[0] == uv_vertex.uv[0] and vertex_uv[1] == uv_vertex.uv[1]:
                    #インデックスバッファにインデックスを追加して終わり
                    self.indices[material_index].append(uv_vertex.index)
                    return

            #一致するUV頂点が存在しなければ
            uv_vertex = UVVertex()
            #最大インデックス値を設定
            uv_vertex.index = self.max_index
            uv_vertex.uv = vertex_uv
            #UV頂点を追加
            self.uv_vertices[vertex_index].append(uv_vertex)
            #最大インデックスを+1
            self.max_index += 1
            #インデックスを設定
            vertex_index = uv_vertex.index
        #UV頂点バッファにインデックスが存在していなければ
        else:
            uv_vertex = UVVertex()
            #頂点バッファのインデックスを設定
            uv_vertex.index = vertex_index
            uv_vertex.uv = vertex_uv
            #新しく辞書にキーを追加
            self.uv_vertices[vertex_index] = []
            self.uv_vertices[vertex_index].append(uv_vertex)
        
        #インデックスバッファにインデックスを追加
        self.indices[material_index].append(vertex_index)
        vertex = Vertex()
        v = mesh.data.vertices[mesh.data.loops[loop_index].vertex_index]

        #頂点ローカル座標にワールド行列を適用
        vertex_position = matrix_world @ v.co
        #vertex_position = v.co
        vertex_normal = v.normal

        vertex.position[0] = vertex_position[0]
        vertex.position[1] = vertex_position[1]
        vertex.position[2] = vertex_position[2]
        vertex.normal[0] = vertex_normal[0]
        vertex.normal[1] = vertex_normal[1]
        vertex.normal[2] = vertex_normal[2]
        vertex.uv[0] = uv_layer[loop_index].uv[0]
        vertex.uv[1] = uv_layer[loop_index].uv[1]

        if len(bones) != 0:
            #スキンインデックスとスキンウェイト
            for i in range(0,len(v.groups)):
                #4つのスキン？までしか対応してません
                if i > 3:
                    break
                vge = v.groups[i]
                vertex_groups = mesh.vertex_groups
                for vg in vertex_groups:
                    if vg.index == vge.group:
                        vertex.skin_indexs[i] = bones[vg.name]
                        vertex.skin_weights[i] = vge.weight
            

        self.vertices[vertex_index] = vertex
    
    def get_texture_filepath(self,mesh):
        #テクスチャ
        self.textures = {}

        index = 0
        for mat in mesh.data.materials:
            self.textures[index] = {}
            #ノードツリーを取得
            node_tree = mat.node_tree
            #ノードの配列？を取得
            nodes = node_tree.nodes
            #ノードを回す。
            for node in nodes:
                #ラベル名がalbedoなら
                if node.label == ALBEDO_TEXTURE:
                    #画像の絶対パスを入れる
                    self.textures[index][ALBEDO_TEXTURE] = node.image.filepath_from_user()
            index += 1

#tkmファイルを出力する
#todo 重複した頂点バッファも違うものとして登録してしまっているので修正したい
#todo tkm最適化を行うようにする
class TkExporter_Tkm():
    #tkmファイルのバージョン
    TKM_VERSION = 100
            
    def write_file(self,filepath):
        #ファイルオープン
        with open(filepath, "wb") as target:
            #tkmのバージョンを出力
            target.write( struct.pack("<B",  self.TKM_VERSION))
            #フラットシェーディング
            target.write(struct.pack("<B",0))
            #メッシュパーツの数を出力
            target.write(struct.pack("<H",len(self.meshs)))
            
            for mesh in self.meshs:
                #マテリアルの数を出力(今は1で)
                target.write(struct.pack("<I",mesh.num_material))
                #頂点数を出力
                target.write(struct.pack("<I",len(mesh.vertices)))
                index_size = 2
                #インデックスバッファのバイトサイズを出力
                #インデックスバッファのサイズが65536より小さいなら2byte
                for i in range(0,mesh.num_material):
                    if len(mesh.indices[i]) > 65536:
                        index_size = 4
                target.write(struct.pack("<B",index_size))
                #パディング(0を3回出力)
                target.write(struct.pack("<B",0))
                target.write(struct.pack("<B",0))
                target.write(struct.pack("<B",0))

                #マテリアル情報を出力(アルベド、法線マップ、スペキュラ、リフレクション、屈折)
                #ファイル名を、文字列の長さと文字列をそれぞれ出力
                #アルベド
                for i in range(0,mesh.num_material):
                    textures = mesh.textures[i]
                    if ALBEDO_TEXTURE in textures:
                        texture_name = textures[ALBEDO_TEXTURE]
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
                for i in range(0,len(mesh.vertices)):
                    vertex = mesh.vertices[i]
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

                #各マテリアルごとのインデックスバッファを出力
                for i in range(0,mesh.num_material):
                    indices = mesh.indices[i]
                    #ポリゴン数を出力
                    polygon_index = len(indices) / 3
                    target.write(struct.pack("<i", int(polygon_index)))
                    #インデックスバッファを出力(今は2byte)
                    for index in indices:
                        if index_size == 2:
                            target.write(struct.pack("<H", index+1))
                        else:
                            target.write(struct.pack("<I", index+1))

    def output_dds_texture(self,filepath):
        cmd_file = "mk.bat"   #.batファイルへのパス
        number = filepath.rfind('\\')
        filepath = filepath[:number]

        for mesh in self.meshs:
            for textures in mesh.textures.values():
                for i in textures:
                    command = cmd_file
                    command += " " + textures[i].replace('/', '\\')
                    command += " " + filepath.replace('/', '\\')
                    os.system(command)

    #invokeの後に呼ばれる関数
    def execute(self, mesh_datas,filepath,bones):
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

        self.meshs = []
        for ms in mesh_datas:
            mesh = Mesh()
            mesh.build_vertex_and_index(ms,ms.matrix_world,bones)
            mesh.get_texture_filepath(ms)
            self.meshs.append(mesh)

        #tkmファイル書き出し
        self.write_file(filepath)
        #ddsファイル作成
        self.output_dds_texture(filepath)
        
        return