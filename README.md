vrep_dynamic_texture
===
Python上で作成した画像（動画）を，v-repのシリンダオブジェクトの曲面上にテクスチャマッピングするためのサンプルです．

## 必要なソフトなど
- v-rep 3.4.0
- python, numpy, matplotlib, six

## 実行方法
1. `launch_vrep.bat` を実行すると，v-repが起動し `simple.ttt` が読み込まれます．
2. `python main.py` を実行する，あるいはspyder上で `main.py` を実行すると，v-rep内のシリンダーにpythonから送られた画像が表示されます．

## 仕組み
次の2つを組合せることで，Python側で用意した画像をv-repのシェイプに表示することができます．

1. primitive-shapeのテクスチャとして，Vision sensor から取得された映像を指定することができる．
2. Pythonなどの外部スクリプトから，Vision sensorに画像をセットすることができる．

### シェイプのテクスチャにビジョンセンサを指定する
- まず，シーンにシリンダとビジョンセンサを追加します．
    - Add -> Primitive shape -> Cylinder
    - Add -> Vision sensor -> Perspective type
- シリンダのScene Object Propertiesダイアログを開きます．
    - Scene hierarchyのCylinderのアイコンをダブルクリック
- `Adjust texture` ボタンを押します
- `Select texture from existing textures` ボタンを押し， `Vision_sensor` を選択します．
- `Mapping mode` を `cylinder` にします．
- これでシリンダの曲面にビジョンセンサからの映像がテクスチャマッピングされました．

### ビジョンセンサにPythonから画像をセットする
- [simxSetVisionSensorImage関数](http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxSetVisionSensorImage)を使うことで，任意の画像をビジョンセンサが見たことにできます．
- 注意点として，v-rep内のビジョンセンサの解像度の設定値と，Pythonから送信する画像データの画素数が一致している必要があります．
    - ビジョンセンサの解像度は，ビジョンセンサのScene Object Propertiesから設定できます．

### 参考資料
- http://www.forum.coppeliarobotics.com/viewtopic.php?f=9&t=799
- http://www.coppeliarobotics.com/helpFiles/en/textureDialog.htm
- http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxSetVisionSensorImage
