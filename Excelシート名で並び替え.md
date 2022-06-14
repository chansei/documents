## Excelシート名で並び替え
### 下準備
1. Excelの開発タブを有効化
「オプション」>「リボンのユーザー設定」>「開発」にチェック
2. マクロ有効形式で保存

### 手順
1. 並び替え操作用のシートを準備
    - 「@～」の形式だと常に先頭に来るはず
1. 「開発」>「挿入」>「ActiveXコントロール」>「コマンドボタン」を適当なエリアに配置
1. 配置したボタンを右クリック>「コードの表示」
    - 右クリックが効かないときは「デザインモード」を有効にする
1. 「Private Sub CommandButton1_Click()」～のイベントコードが表示されるので，イベントハンドラ内に次を記述
    ```vba
    Dim i As Long, j As Long, cnt As Long
    Dim buf() As String, swap As String
    
    cnt = Worksheets.Count
    ReDim buf(cnt)
    
    'ワークシート名を配列に入れる
    For i = 1 To cnt
        buf(i) = Worksheets(i).Name
    Next i
    
    '配列の要素をソートする
    For i = 1 To cnt
        For j = cnt To i Step -1
            If buf(i) > buf(j) Then
                swap = buf(i)
                buf(i) = buf(j)
                buf(j) = swap
            End If
        Next j
    Next i
    
    'ワークシートの位置を並べ替える
    Worksheets(buf(1)).Move Before:=Worksheets(1)
    For i = 2 To cnt
        Worksheets(buf(i)).Move After:=Worksheets(i - 1)
    Next i
    ```
    参考：https://www.moug.net/tech/exvba/0040060.html
1. VBAウィンドウを閉じて(閉じなくても良い)、「デザインモード」を解除してから配置したボタンをクリック
    - シートが並び替えられる(はず)
