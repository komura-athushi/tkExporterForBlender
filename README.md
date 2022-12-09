# tkExporterForBlender

# 最初に
Takayama様、この場を借りてお礼申し上げます。
<br>
<br>大変参考にさせて頂きました。
<br>https://qiita.com/kenyoshi17/items/b93bbba6451e3c6017e5

# 概要
非公式Blender版tkExporterです。
Blender3.3.1にて動作確認済みです。

# インストール方法

<br>1.&nbsp;「右クリックで管理者として実行してね.bat」を右クリックで管理者として実行
<br>![16](https://user-images.githubusercontent.com/44657623/203994330-492e4351-8184-4bb7-a836-181cefdffd92.png)
<br>2.&nbsp;Blenderのaddonsフォルダに「tkExporter_sub」フォルダが出来ていることを確認
<br>![17](https://user-images.githubusercontent.com/44657623/203994647-fb462026-15f4-464f-9bc6-c95630e195a8.png)
<br>詳しくは「アドオン　インストール」
<br>3.&nbsp;設定→プリファレンス
<br>![1](https://user-images.githubusercontent.com/44657623/202902685-123d81df-5561-4e91-8251-205606a1d19d.png)
<br>4.&nbsp;アドオン→インストール→tkExporter.py→アドオンをインストール
<br>![2](https://user-images.githubusercontent.com/44657623/202902789-0c5857bb-2c65-4123-ba87-ccc682e84f0c.png)
<br>5.&nbsp;tkExporterに✓
<br>![3](https://user-images.githubusercontent.com/44657623/202902856-b194fb85-ad2a-487b-91e9-c2de8b073ef0.png)

# OSL(OpenShadingLanguage)の使用方法
<br>**OSLとは**
<br>→Blenderで使用可能なシェーディング言語です。
<br>
<br>1.&nbsp;レンダープロパティ→レンダーエンジンを「**Cycles**」→デバイスを「**CPU**」→**Open Shading Languageに✓**
<br>![24](https://user-images.githubusercontent.com/44657623/205442630-01441c30-aa76-4044-86b0-1019678dea35.png)
<br>2.&nbsp;シェーダーエディター→追加→スクリプト→スクリプト
<br>![25](https://user-images.githubusercontent.com/44657623/205442717-89e4a108-8253-44e9-b1dc-3377c10aa947.png)
<br>3.&nbsp;外部→ファイルブラウザを開く
<br>![26](https://user-images.githubusercontent.com/44657623/205442757-adf811b9-a7b0-4757-af11-a9cc2150d533.png)
<br>4.&nbsp;tkExporterForBlender/shader/test.oslを選択
<br>![27](https://user-images.githubusercontent.com/44657623/205442801-8629d1df-0066-451d-9d7a-830f2ea637d4.png)
<br>5.&nbsp;以下のようにノードを繋いでください。
<br>![28](https://user-images.githubusercontent.com/44657623/206435933-cdb4783b-3681-4b2d-8fa6-269b9f159431.png)
<br>![29](https://user-images.githubusercontent.com/44657623/206436662-de88545f-423b-42e2-ac1b-6b48724e8bae.png)

<br>6.&nbsp;シェーディングを「**レンダー**」に
<br>![30](https://user-images.githubusercontent.com/44657623/205444034-77432cab-8bbe-456b-a789-efe6fe818709.png)
<br>![33](https://user-images.githubusercontent.com/44657623/206437076-b995e07b-d44a-41fb-a6a8-111cc55a6dcb.png)
<br>各パラメータを弄れば、以下のようにモデルがライティングされます。
<br>![31](https://user-images.githubusercontent.com/44657623/206435741-9648b8b0-cd40-41a9-87bb-d22aafa48f46.png)
<br>![34](https://user-images.githubusercontent.com/44657623/206437582-52d126aa-0d9d-4b37-a628-d8ed9c2ba15f.png)








# tkmファイル出力
**三角形ポリゴンしか出力できません**
<br>四角形→三角形にする方法はこちらを参照
<br>https://www.matatabi-ux.com/entry/2019/09/05/100000
<br><br>
**シェーダーエディターで、**アルベドマップのラベル名をalbedo**、**法線マップのラベル名をnormal**、**スペキュラマップのラベル名をspecular**、**リフレクションマップのラベル名をreflection**、**屈折マップのラベル名をrefraction**に設定してください。**
<br>![4](https://user-images.githubusercontent.com/44657623/202903175-8986e331-61f4-4f9b-98ea-b3214c57adc8.png)
<br><br>
**アルベドテクスチャのdds変換出力を行いたい場合は、makefile、mk.bat、texconv.exeファイルをblender.exeがあるフォルダにコピーしてください。**
<br>**テクスチャのファイルパスに空白が含まれていると(例:3D Objects)、dds出力に失敗します。**
<br>![5](https://user-images.githubusercontent.com/44657623/202903461-e0485e01-c978-42fa-910a-a77068ee66f0.png)
<br><br>
1.&nbsp;tkmファイルに出力したい**メッシュオブジェクト**を選択or**Collection**を選択
<br>![6](https://user-images.githubusercontent.com/44657623/202903646-7edabb2d-8976-4bb3-a3e3-8ddec51cb3ed.png)
<br>![21](https://user-images.githubusercontent.com/44657623/204788193-7d41ea03-761b-4f4d-9ab6-1c043efd62d7.png)

<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createTkm
<br>![7](https://user-images.githubusercontent.com/44657623/202903877-d500505a-b454-425c-9c36-96f8e9995bac.png)
<br>3.&nbsp;ファイルパスを指定して、createTkm
<br>(Output all mesh on Collectionに✓を入れると、**選択したCollection上に存在する全てのMesh**を対象にtkmファイルを出力します、✓を入れなければ**選択したMeshオブジェクト**(1つ)をtkmファイルとして出力します)
<br>![23](https://user-images.githubusercontent.com/44657623/204789146-f12b44d2-7cae-4537-b80e-cc32da0b4f10.png)
# tksファイル出力
1.&nbsp;tksファイルに出力したい**アーマチュアオブジェクト**を選択
<br>![9](https://user-images.githubusercontent.com/44657623/203451472-adcddb27-0e22-4bcd-9b22-aa4f2256857c.png)
<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createSkeleton
<br>![10](https://user-images.githubusercontent.com/44657623/203451565-507c5056-17e1-4b39-80ad-417ae7317715.png)
<br>3.&nbsp;ファイルパスを指定してcreateSkeleton(tkmと同じファイル名にしてください)
<br>![11](https://user-images.githubusercontent.com/44657623/203451713-518cb6a0-f277-4a95-99f7-0747a1510a28.png)

# tkaファイル出力
**タイムラインエディタで開始フレームと終了フレームを設定する。**
<br>![12](https://user-images.githubusercontent.com/44657623/203992635-5fc5a1a0-d92a-4915-9ac9-344a36d1fa93.png)
<br><br>
**アニメーションを作る際にポーズマーカーを設定しておくと、アニメーションイベントとして出力します。**
<br><br>
**頂点ウェイトを編集した後などは3Dビューポート→メッシュ→ウェイト→すべてを正規化、を行わないと、Blenderでは大丈夫でもゲーム内ではおかしなアニメーションになることがあります。**
<br><br>
1.&nbsp;tkaファイルに出力したい**アーマチュアオブジェクト**を選択
<br>![13](https://user-images.githubusercontent.com/44657623/203992843-7e2b316f-40a3-4f0f-974f-850eff60562f.png)
<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createAnimation
<br>![14](https://user-images.githubusercontent.com/44657623/203993009-3222df91-fef8-4d69-bea8-86a8572714c5.png)
<br>4.&nbsp;ファイルパスを指定してcreateAnimation
<br>![15](https://user-images.githubusercontent.com/44657623/203993199-7998066e-c22e-4429-84a6-b251e0681781.png)
<br>5.&nbsp;下記のようにノードをつないでください。
<br>![28](https://user-images.githubusercontent.com/44657623/205442940-603f9d8c-6c27-4bd0-8b3b-b0f4ae28b073.png)
<br>![29](https://user-images.githubusercontent.com/44657623/205442946-cad314d2-6462-4090-8b61-1e71aa06624f.png)


# tklファイル出力
**Level_Parameterパネルにtkl用のパラメータを追加しています。**
<br>![32](https://user-images.githubusercontent.com/44657623/206342443-4c19ecd1-9d6d-47b8-87b9-258b0233b3e6.png)
<br>
<br>
1.&nbsp;コレクションを選択。(コレクションを選択しない場合は、シーンコレクションを選択した扱いになって、すべてのオブジェクトが対象になります。)
<br>![18](https://user-images.githubusercontent.com/44657623/204429635-0fc5d36d-19d7-43f9-9db3-342d4995b955.png)
<br>2.&nbsp;オブジェクトプロパティ→TKExporter→createLevel
<br>![19](https://user-images.githubusercontent.com/44657623/204430215-f301527c-8abc-47c6-bcd3-90f03ddc2bb6.png)
<br>3.&nbsp;Delete name after the dot(オブジェクトの名前の.以下が無視されます)に✓を入れて、createLevel
<br>![20](https://user-images.githubusercontent.com/44657623/204430196-2639f642-1b5f-48b3-9a03-eca593ba41bc.png)





