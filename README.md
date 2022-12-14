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
  <br>&nbsp;&nbsp;スキンウェイト・スキンインデックスも出力できるように(動作要検証)
<br>
 **11/23&nbsp;&nbsp;ver.1.2.0**
  <br>&nbsp;&nbsp;tksファイル出力実装(動作要検証)
<br>
 **11/25&nbsp;&nbsp;ver.1.3.0**
  <br>&nbsp;&nbsp;tkaファイル出力実装(動作要検証、アニメーショイベント対応)
<br>
 **11/27&nbsp;&nbsp;ver.1.3.1**
  <br>&nbsp;&nbsp;複数のマテリアルを割り当てられている単一メッシュのtkmファイル出力対応(動作要検証)。
 <br>
 **11/28&nbsp;&nbsp;ver.1.3.2**
  <br>&nbsp;&nbsp;tkm出力の際に、重複する頂点データは使いまわすように(動作要検証)。
   <br>
 **11/29&nbsp;&nbsp;ver.1.4.0**
  <br>&nbsp;&nbsp;tklファイル出力実装(動作要検証)。
     <br>
 **11/30&nbsp;&nbsp;ver.1.5.0**
　<br>&nbsp;&nbsp;Collection内にある全てのMeshを1つのtkmファイルとして出力できるように。
  <br>&nbsp;&nbsp;tkmファイル出力時に、各頂点座標にワールド行列を乗算するようにした(これでいいのかは分からない)。
  <br>
 **12/1&nbsp;&nbsp;ver.1.5.1**
　<br>&nbsp;&nbsp;tkmファイル出力時の、頂点データのスキンインデックスの値を修正。
  <br>
 **12/2&nbsp;&nbsp;ver.1.5.2**
　<br>&nbsp;&nbsp;tkmファイル出力時、アルベド以外のテクスチャも設定可能に。
  <br>
 **12/3&nbsp;&nbsp;ver.1.6.0**
　<br>&nbsp;&nbsp;OSL(Open Shading Language)版k2EngineShader.fxを追加(**要検証**)。
 <br>
  **12/8&nbsp;&nbsp;ver.1.6.1**
　<br>&nbsp;&nbsp;tklファイル用のパラメータを追加(isShadowCaster、isShadowReceiver)。
  <br>&nbsp;&nbsp;各オペレーターに説明分を追加。
  <br>&nbsp;&nbsp;シェーダーを修正。
  <br>
 **12/13&nbsp;&nbsp;ver.1.6.2**
　<br>&nbsp;&nbsp;tkm出力時に、フラットシェーディングか否かを選択できるオプションを追加。
 <br>
 **12/14&nbsp;&nbsp;ver.1.6.3**
　<br>&nbsp;&nbsp;tkl用に、int・float・char・vector型のパラメータを設定、出力できるように(TklFileクラスを修正する必要あり)。
 <br>
 **12/19&nbsp;&nbsp;ver.1.6.4**
　<br>&nbsp;&nbsp;tkm出力において、複数のオブジェクト選択に対応。
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
<br>![28](https://user-images.githubusercontent.com/44657623/209309617-65fbec35-51f0-42c2-ac74-08e0c09b4ee0.png)
<br>![29](https://user-images.githubusercontent.com/44657623/209309637-522b6a51-4030-4730-ad54-5804ecae8bff.png)


<br>6.&nbsp;シェーディングを「**レンダー**」に
<br>![30](https://user-images.githubusercontent.com/44657623/205444034-77432cab-8bbe-456b-a789-efe6fe818709.png)
<br>![33](https://user-images.githubusercontent.com/44657623/206437076-b995e07b-d44a-41fb-a6a8-111cc55a6dcb.png)
<br>各パラメータを弄れば、以下のようにモデルがライティングされます。
<br>![31](https://user-images.githubusercontent.com/44657623/208937625-a6d9dc8e-83b6-4665-9a0e-07aa6f7cea94.png)
<br>![35](https://user-images.githubusercontent.com/44657623/209309347-35936f41-a617-45a4-a1a3-11f172190fa4.png)
<br>![34](https://user-images.githubusercontent.com/44657623/208937688-5321ed94-6c6a-4f22-842b-5c91ffb52c2b.png)









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
1.&nbsp;tkmファイルに出力したい**メッシュオブジェクト**(複数可)を選択or**Collection**を選択
<br>* **ボーンを紐付ける場合は、アーマチュアオブジェクトも一緒に選択してください。**
<br>![6](https://user-images.githubusercontent.com/44657623/208357027-5674e439-3d44-4261-818c-bd99960efed2.png)
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





