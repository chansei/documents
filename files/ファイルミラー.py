import glob
import logging
import os
import shutil
import traceback
from datetime import datetime
from tkinter import filedialog

############################
BUILD_VER = '1.0.2'
############################

logger = logging.getLogger()

def main():
    # dstが基準となるフォルダー(空のフォルダー)
    # srcが検索対象とするフォルダー
    
    dst = filedialog.askdirectory(title='基準となるフォルダーを選択してください') 
    src = filedialog.askdirectory(title='検索対象のフォルダーを選択してください')

    if len(dst)==0 or len(src)==0:
        print(f'基準フォルダーまたは検索対象フォルダーが空です')
        logger.error('フォルダー未設定')
        _ = input('何かキーを押すと終了します...')
        return

    files = os.listdir(dst)
    dst_dirs = [f for f in files if os.path.isdir(os.path.join(dst, f))]

    print(f'基準フォルダー：{dst}')
    print(f'検索対象フォルダー：{src}')

    print(color(f'{len(dst_dirs)}個のフォルダーが見つかりました'))
    logger.info(f'基準フォルダー：{dst}, 検索対象フォルダー：{src}, {len(dst_dirs)}個のフォルダー')

    print(f'出力先のフォルダーを作成中...')
    try:
        out_dir = dst+'\\'+'@出力'
        os.mkdir(out_dir)
        print(f'完了しました')
    except Exception:
        print(f'既に存在しているか、アクセス権限がありません')
        logger.error('出力先フォルダー作成失敗',exc_info=True)

    for i, dst_dir in enumerate(dst_dirs):
        print(color(f'{str(len(dst_dirs))}個中{str(i+1)}個目のフォルダーを検索中...'))
        for cand in glob.glob(src+'/**/', recursive=True):
            cand_dir_name_list = cand.split('\\')
            cand_dir_name = cand_dir_name_list[len(cand_dir_name_list)-2]
            if os.path.isdir(cand) and dst_dir==cand_dir_name:
                print(f'コピーしています...')
                logger.info(f"コピー元：{cand}, コピー先：{out_dir}\{dst_dir}")
                try:
                    print(cand)
                    shutil.copytree(cand, out_dir+'\\'+dst_dir)
                    print(f'完了しました')
                except Exception:
                    print(f'エラーが発生し、その内容はログに出力されました')
                    logger.error('コピー失敗',exc_info=True)
            else:
                logger.info(f"存在しません：{dst_dir}")
                print(f'フィルダーが見つかりませんでした')

    _ = input('何かキーを押すと終了します...')

def color(txt): # 文字の色づけ
    return '\033[33m'+txt+'\033[0m'

if __name__ == '__main__':
    log_file_name = '{:%Y-%m-%d-%H%M%S}'.format(datetime.now())+'.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file_name, format="%(asctime)s %(levelname)-7s %(message)s")
    print(f'***CopyRight 2022 Chansei***')
    print(f'***Build Version {BUILD_VER}***')
    print(f'このソフトウェアはMITライセンスのもと公開されています')
    print(color(f'ログファイル：{log_file_name}'))
    main()