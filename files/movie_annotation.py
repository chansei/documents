# 指定ディレクトリに存在する動画ファイルをラベルづけするスクリプト

import argparse
import glob

import cv2
import pandas as pd

# ラベルづけに使用するキーとラベルの辞書
label_keys = {
    '1': 'Hesitation',
    '2': 'Take some goods',
    # 他のラベルとキーをここに追加
}


def movie(path):
    # ラベルづけの状態を保持する辞書
    label_states = {label: None for label in label_keys.values()}

    # フレームごとのラベルデータを保持するリスト
    frame_labels = []

    # 動画を開く
    cap = cv2.VideoCapture(path)

    # 動画が開けなかった場合の処理
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    current_frame = 0
    paused = False

    output_csv = True

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Reached end of video, exiting.")
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # 現在のフレーム数を描画
        cv2.putText(frame, f"{current_frame}/{int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)

        # ラベルづけの状態を描画
        for i, (label, state) in enumerate(label_states.items()):
            if state is None:
                cv2.putText(frame, f"{i+1}: {label}", (10, 60 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            else:
                cv2.putText(frame, f"{i+1}: {label} (started at {state})", (10, 60 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)

        cv2.imshow(path, frame)

        key = cv2.waitKey(10) & 0xFF  # 30fpsの動画でフレームごとに33ms待つ

        if key == ord(' '):  # スペースキーで一時停止・再開
            paused = not paused

        elif key == ord('d'):  # 'd'でフレームを進める
            # 次のフレームを読み込む
            ret, frame = cap.read()
            if not ret:
                print("Reached end of video, exiting.")
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            paused = True

        elif key == ord('a'):  # 'a'でフレームを戻す
            current_frame -= 2  # 1フレーム戻す
            # 前のフレームを読み込む
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                print("Reached beginning of video, exiting.")
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            paused = True

        elif chr(key) in label_keys:  # ラベルキーが押されたときの処理
            label = label_keys[chr(key)]
            if label_states[label] is None:  # ラベル開始
                print("Label {} started at frame {}".format(label, current_frame))
                label_states[label] = current_frame
            else:
                print("Label {} ended at frame {}".format(label, current_frame))
                start_frame = label_states[label]
                end_frame = current_frame
                frame_labels.append({'label': label, 'start': start_frame, 'end': end_frame})
                label_states[label] = None

        elif key == ord('q'):  # 'q'で終了
            break

        elif key == ord('e'):  # 'e'でスキップ
            print("Skipped")
            output_csv = False
            break

    # ラベルづけの状態を確認
    for label, state in label_states.items():
        if state is not None:
            print("Warning: Label {} started at frame {} but did not end.".format(label, state))
            # 最終フレームまでのラベルを追加
            start_frame = state
            end_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_labels.append({'label': label, 'start': start_frame, 'end': end_frame})

    # 動画を解放
    cap.release()
    cv2.destroyAllWindows()

    # CSVファイルへの書き出し
    if output_csv:
        df = pd.DataFrame(frame_labels)
        filename = path.split('\\')[-1]
        filename = filename.split('.')[0]
        _dirpath = path.split('\\')
        _dirpath.pop(-1)
        dirpath = _dirpath[0]
        df.to_csv(f'{dirpath}/{filename}_label.csv', index=False)
        print(f"Successfully wrote labels to {dirpath}/{filename}_label.csv.")


def main():
    DIR = "MOVIE_DIR"
    files = glob.glob(f"{DIR}/*.mp4")

    print(files)

    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", "-s", type=int)
    args = parser.parse_args()

    for file in files:
        if args.skip:
            args.skip -= 1
            continue

        print(file)
        movie(file)


if __name__ == '__main__':
    main()
