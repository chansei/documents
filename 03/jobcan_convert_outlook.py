import csv
import json
from datetime import datetime, timedelta
from tkinter import filedialog as fd

from bs4 import BeautifulSoup

BUILD_VER = "1.1.0"

# ------- 権利表記ここから ------- #
print(f'***CopyRight 2023 Chansei MIT License***')
print(f'***Build Version {BUILD_VER}***')
print(f'***https://github.com/chansei/documents***')
# ------- 権利表記ここまで ------- #

# ------- メッセージ ------- #
print('>>> 使い方は付属のドキュメントを参照してください')
# ------- メッセージここまで ------- #

# ------- メイン処理ここから ------- #
def main():
    # ファイルの選択
    HTML_PATH = fd.askopenfilename(title="シフト予定表のhtmlファイルを指定してください" ,filetypes=[("htmlファイル", "*.html")])
    WORKS_LIST_PATH = fd.askopenfilename(title="スタッフリストを指定してください", filetypes=[("jsonファイル", "*.json")])

    # ファイルが選択されていなければ終了
    if HTML_PATH == "" or WORKS_LIST_PATH == "":
        print("ファイルが選択されていません")
        return 1

    print(f"シフト予定表のhtmlファイル: {HTML_PATH}")
    print(f"スタッフリスト: {WORKS_LIST_PATH}")

    # 店舗名*変更不可
    STORE_NAME = "スマートライフ碑文谷 BASE"

    print(f"店舗名(変更不可): {STORE_NAME}")

    # シフト設定月
    YEAR = int(input("シフト設定(年): "))
    MONTH = int(input("シフト設定(月): "))
    BEGIN_DATE = datetime(YEAR, MONTH, 1)

    # 不正な値が入力されたら終了
    if YEAR < 2000 or YEAR > 2100 or MONTH < 1 or MONTH > 12:
        print("不正な値が入力されました")
        return 1

    print(f"シフト入力開始日:{YEAR}年{MONTH}月1日")

    # csvのヘッダー*変更不可
    HEADER = [
        "件名", "開始日", "開始時刻", "終了日", "終了時刻", "終日イベント",
        "アラーム オン/オフ", "アラーム日付", "アラーム時刻", "会議の開催者",
        "必須出席者", "任意出席者", "リソース", "プライベート", "経費情報",
        "公開する時間帯の種類", "支払い条件", "場所", "内容", "秘密度",
        "分類", "優先度"
    ]

    # 関数呼び出し
    status, shift_lists, day_count = shift_schedule_extract(HTML_PATH, STORE_NAME)
    if status == 1:
        return 1
    status = output_csv(shift_lists, day_count, WORKS_LIST_PATH, YEAR, MONTH, BEGIN_DATE, HEADER)
    if status == 1:
        return 1
    
    # 終了処理
    return 0

def shift_schedule_extract(html_path, store_name):
    # htmlファイルの読み込み
    try:
        with open(html_path, encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        elem =  soup.find('table', class_='note')
    except Exception as e:
        print(e)
        return 1
    shift_lists = dict()
    day_count = 0

    # シフトリストから出勤日を取得
    for tr in elem.find_all('tr'):
        try:
            # thタグ+divタグの取得
            th = tr.find('th')
            div = th.find('div')
            # スタッフ名の取得
            if div is not None:
                staff_name = th.text
                _days = [_day.text for _day in tr.find_all('td')]
                days = [_day.replace('\n', '').replace(' ', '') for _day in _days]
                bool_days = ['F' if _day in ['-', '休', '有'] else 'T' for _day in days]
                day_count = len(bool_days) # 月の日数
                shift_lists[staff_name.replace(store_name, '')] = bool_days
        except Exception:
            pass

    return 0, shift_lists, day_count

def output_csv(shift_lists, day_count, works_list_path, year, month, begin_date, header):
    # Worksリストと照らし合わせる
    # jsonはWorks名：[ジョブカン上での表示名, Outlookでの表示名]
    # shift_jisに対応しない文字は?に置き換わります(絵文字など)
    try:
        with open(works_list_path, encoding='shift_jis') as f:
            _works_list = f.read()
        works_list = json.loads(_works_list)
    except Exception as e:
        print(e)
        return 1

    for works_name, members in works_list.items():
        member_shift_lists = {member_name[1]: shift_lists[member_name[0]] for member_name in members}
        shift_count_list = []
        for day in range(day_count):
            attendance = []
            for staff, attendance_status in member_shift_lists.items():
                if attendance_status[day] == 'T':
                    attendance.append(staff)
            shift_count_list.append(f"出勤{len(attendance)}:{','.join(attendance)}")
        data = []
        row_data = begin_date
        for title in shift_count_list:
            data.append([
                title, row_data.strftime("%Y/%m/%d"), "10:00:00",
                row_data.strftime("%Y/%m/%d"), "10:30:00", "FALSE",
                "FALSE", "", "", "", "", "", "自動", "", "", "FALSE",
                "", "", "", "", "", "標準", "", "標準"
            ])
            row_data += timedelta(days=1)
        try:
            with open(f"{year}{str(month).zfill(2)}{works_name}.csv", mode="w", newline="", encoding="shift_jis") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            print(f"{year}{str(month).zfill(2)}{works_name}.csvを出力しました")
        except Exception as e:
            print(e)
            return 1
    
    return 0
# ------- メイン処理ここまで ------- #

if __name__ == '__main__':
    status = main()
    if status == 1:
        print(">>> csvファイルの出力に失敗しました")
    else:
        print(">>> csvファイルの出力に成功しました")
    input(">>> 終了するにはEnterキーを押してください")

