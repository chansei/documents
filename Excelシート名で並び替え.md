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
1. 表示されたコードブロックの中身を以下に置き換え
    ```vba
    Private Sub CommandButton1_Click()
        Dim i As Long, j As Long, cnt As Long
        Dim buf() As String, swap As String, base_sheet As String

        cnt = Worksheets.Count
        '並び替えボタンを置いたシート名↓
        base_sheet = "@並び替え"

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

        'フォーカスが一番最後のシートになるので先頭まで戻す
        Worksheets(base_sheet).Activate

        'あとはお好みで
        '簡単に更新時間を載せてます
        Worksheets(base_sheet).Range("A1") = "並び替え日時"
        Worksheets(base_sheet).Range("A2") = Now
        Worksheets(base_sheet).Range("A2").NumberFormatLocal = "yy/MM/dd"
        Worksheets(base_sheet).Range("A2").ShrinkToFit = True
        Worksheets(base_sheet).Range("B2") = Now
        Worksheets(base_sheet).Range("B2").NumberFormatLocal = "hh:mm:ss"
        Worksheets(base_sheet).Range("B2").ShrinkToFit = True
    End Sub
    ```
    参考：https://www.moug.net/tech/exvba/0040060.html
    - こんなかんじになる
        ![20220614_182846](https://user-images.githubusercontent.com/29759976/173544654-82c39a1c-631f-412b-a5f3-f499bf3b470c.png)
1. VBAウィンドウを閉じて(閉じなくても良い)、「デザインモード」を解除してから配置したボタンをクリック
    - シートが並び替えられる(はず)


