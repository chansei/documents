import glob
import logging
import os
import shutil
import traceback
from datetime import datetime
from tkinter import filedialog

############################
BUILD_VER = '1.0.4'
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
    
    out_dir = dst+'\\'+'@出力'
    if os.path.exists(out_dir):
        print(f'出力先のフィルダーは既に存在しています')
        ans = input(f'削除しますか？(y/n)')
        if ans=='y':
            try:
                shutil.rmtree(out_dir)
                print(f'削除しました')
            except Exception:
                print(f'失敗しました')
                logger.error('出力先フォルダー削除失敗',exc_info=True)

    files = os.listdir(dst)
    dst_dirs = [f for f in files if os.path.isdir(os.path.join(dst, f))]

    print(f'基準フォルダー：{dst}')
    print(f'検索対象フォルダー：{src}')

    print(yellow(f'{len(dst_dirs)}個のフォルダーが見つかりました'))
    logger.info(f'基準フォルダー：{dst}, 検索対象フォルダー：{src}, {len(dst_dirs)}個のフォルダー')

    print(f'出力先のフォルダーを作成中...')
    try:
        os.mkdir(out_dir)
        print(f'完了しました')
    except Exception:
        print(f'失敗しました')
        logger.error('出力先フォルダー作成失敗',exc_info=True)

    not_exist_dirs = []

    for i, dst_dir in enumerate(dst_dirs):
        find_flag = False
        print(yellow(f'{str(len(dst_dirs))}個中{str(i+1)}個目のフォルダーを検索中...'))
        for cand in glob.glob(src+'/**/', recursive=True):
            cand_dir_name_list = cand.split('\\')
            cand_dir_name = cand_dir_name_list[len(cand_dir_name_list)-2]
            if os.path.isdir(cand) and dst_dir==cand_dir_name:
                find_flag = True
                print(f'"{dst_dir}"が存在します')
                print(f'コピーしています...')
                logger.info(f"コピー元：{cand}, コピー先：{out_dir}\{dst_dir}")
                try:
                    print(cand)
                    shutil.copytree(cand, out_dir+'\\'+dst_dir)
                    print(f'完了しました')
                except Exception:
                    print(f'エラーが発生し、その内容はログに出力されました')
                    logger.error('コピー失敗',exc_info=True)
        if not find_flag:
            not_exist_dirs.append(dst_dir)
            print(f'"{dst_dir}"は存在しません')

    print(yellow(f'検索が完了しました'))

    if not_exist_dirs:
        for dir in not_exist_dirs:
            logger.warning(f"存在しません：{dir}")
        print(red(f'存在しないフォルダーが{len(not_exist_dirs)}個ありました'))
        print(f'詳細はログファイルを確認してください')

    _ = input('何かキーを押すと終了します...')

def yellow(txt): # 文字の色づけ
    return '\033[33m'+txt+'\033[0m'

def red(txt):
    return '\033[31m'+txt+'\033[0m'

if __name__ == '__main__':
    log_file_name = '{:%Y-%m-%d-%H%M%S}'.format(datetime.now())+'.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file_name, format="%(asctime)s %(levelname)-7s %(message)s")
    print(f'***CopyRight 2022 Chansei***')
    print(f'***Build Version {BUILD_VER}***')
    print(f'このソフトウェアはMITライセンスのもと公開されています')
    print(yellow(f'ログファイル：{log_file_name}'))
    main()