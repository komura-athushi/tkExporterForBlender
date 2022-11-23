# tkExporterForBlender

# 最初に
Takayama様、この場を借りてお礼申し上げます。
<br>
<br>大変参考にさせて頂きました。
<br>https://qiita.com/kenyoshi17/items/b93bbba6451e3c6017e5

# 更新履歴
 **11/20&nbsp;&nbsp;ver.1.0.0**
  <br>&nbsp;&nbsp;tkmファイルの出力、アルベドファイルの取得及びdds変換出力実装(単一メッシュ、単一マテリアル、ボーンなしのみ対応)
<br>
 **11/22&nbsp;&nbsp;ver.1.1.0**
  <br>&nbsp;&nbsp;スキンウェイト・スキンインデックスも出力できるように(動作未検証)
<br>
 **11/23&nbsp;&nbsp;ver.1.2.0**
  <br>&nbsp;&nbsp;tksファイル出力実装(動作未検証)
     

# 概要
非公式Blender版tkExporterです。
Blender3.3.1にて動作確認済みです。

# インストール方法
詳しくは「アドオン　インストール」
<br>1.&nbsp;設定→プリファレンス
<br>![1](https://user-images.githubusercontent.com/44657623/202902685-123d81df-5561-4e91-8251-205606a1d19d.png)
<br>2.&nbsp;アドオン→インストール→tkExporter.py→アドオンをインストール
<br>![2](https://user-images.githubusercontent.com/44657623/202902789-0c5857bb-2c65-4123-ba87-ccc682e84f0c.png)
<br>3.&nbsp;tkExporterに✓
<br>![3](https://user-images.githubusercontent.com/44657623/202902856-b194fb85-ad2a-487b-91e9-c2de8b073ef0.png)

# tkmファイル出力
**三角形ポリゴンしか出力できません**
<br>四角形→三角形にする方法はこちらを参照
<br>https://www.matatabi-ux.com/entry/2019/09/05/100000
<br><br>
**シェーダーエディターで、アルベドテクスチャのラベル名をalbedoに設定してください。**
<br>![4](https://user-images.githubusercontent.com/44657623/202903175-8986e331-61f4-4f9b-98ea-b3214c57adc8.png)
<br><br>
**アルベドテクスチャのdds変換出力を行いたい場合は、makefile、mk.bat、texconv.exeファイルをblender.exeがあるフォルダにコピーしてください。**
<br>![5](https://user-images.githubusercontent.com/44657623/202903461-e0485e01-c978-42fa-910a-a77068ee66f0.png)
<br><br>
1.&nbsp;tkmファイルに出力したい**メッシュオブジェクト**を選択
<br>![6](https://user-images.githubusercontent.com/44657623/202903646-7edabb2d-8976-4bb3-a3e3-8ddec51cb3ed.png)
<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createTkm
<br>![7](https://user-images.githubusercontent.com/44657623/202903877-d500505a-b454-425c-9c36-96f8e9995bac.png)
<br>3.&nbsp;ファイルパスを指定して、createTkm
<br>![8](https://user-images.githubusercontent.com/44657623/202904033-0e1a9589-85ff-4f5c-a03a-8b6a0a32aebb.png)

# tksファイル出力
1.&nbsp;tksファイルに出力したい**アーマチュアオブジェクト**を選択
<br>![9](https://user-images.githubusercontent.com/44657623/203451472-adcddb27-0e22-4bcd-9b22-aa4f2256857c.png)
<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createSkeleton
<br>![10](https://user-images.githubusercontent.com/44657623/203451565-507c5056-17e1-4b39-80ad-417ae7317715.png)
<br>3.&nbsp;ファイルパスを指定してcreateSkeleton
<br>![11](https://user-images.githubusercontent.com/44657623/203451713-518cb6a0-f277-4a95-99f7-0747a1510a28.png)


