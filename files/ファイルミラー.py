import glob
import logging
import os
import shutil
import traceback
from datetime import datetime
from tkinter import filedialog

############################
BUILD_VER = '1.0.6'
############################

logger = logging.getLogger()


def search():
    # dstが基準となるフォルダー(空のフォルダー)
    # srcが検索対象とするフォルダー

    dst = filedialog.askdirectory(title='基準となるフォルダーを選択してください')
    src = filedialog.askdirectory(title='検索対象のフォルダーを選択してください')

    if len(dst) == 0 or len(src) == 0:
        print(f'基準フォルダーまたは検索対象フォルダーが空です')
        logger.error('フォルダー未設定')
        return

    out_dir = dst+'\\'+'@出力'
    if os.path.exists(out_dir):
        print(f'出力先のフィルダーは既に存在しています')
        ans = input(f'削除しますか？(y/n)')
        if ans == 'y':
            try:
                shutil.rmtree(out_dir)
                print(f'削除しました')
            except Exception:
                print(f'失敗しました')
                logger.error('出力先フォルダー削除失敗', exc_info=True)

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
        logger.error('出力先フォルダー作成失敗', exc_info=True)

    not_exist_dirs = []

    for i, dst_dir in enumerate(dst_dirs):
        find_flag = False
        print(yellow(f'{str(len(dst_dirs))}個中{str(i+1)}個目のフォルダーを検索中...'))
        for cand in glob.glob(src+'/**/', recursive=True):
            cand_dir_name_list = cand.split('\\')
            cand_dir_name = cand_dir_name_list[len(cand_dir_name_list)-2]
            if os.path.isdir(cand) and dst_dir == cand_dir_name:
                find_flag = True
                print(f"コピー元：{cand}")
                print(f'コピーしています...')
                logger.info(f"コピー元：{cand}, コピー先：{out_dir}\{dst_dir}")
                try:
                    if os.path.exists(out_dir+'\\'+dst_dir):
                        logger.warning(f'上書きを行います：{out_dir}\{dst_dir}')
                        print(f'既にフォルダーが存在するため上書きを行います')
                    shutil.copytree(cand, out_dir+'\\' +
                                    dst_dir, dirs_exist_ok=True)
                    print(f'完了しました')
                except Exception:
                    print(f'エラーが発生し、その内容はログに出力されました')
                    logger.error('コピー失敗', exc_info=True)
        if not find_flag:
            not_exist_dirs.append(dst_dir)
            print(f'"{dst_dir}"は存在しません')

    print(yellow(f'検索が完了しました'))

    if not_exist_dirs:
        for dir in not_exist_dirs:
            logger.warning(f"存在しません：{dir}")
        print(red(f'存在しないフォルダーが{len(not_exist_dirs)}個ありました'))
        print(f'詳細はログファイルを確認してください')


def check():
    dst = filedialog.askdirectory(title='対象となるフォルダーを選択してください')

    if len(dst) == 0:
        print(f'対象フォルダーが空です')
        logger.error('フォルダー未設定')
        return

    out_dir = dst+'\\'+'@空のフォルダー'
    if os.path.exists(out_dir):
        print(f'出力先のフィルダーは既に存在しています')
        ans = input(f'削除しますか？(y/n)')
        if ans == 'y':
            try:
                shutil.rmtree(out_dir)
                print(f'削除しました')
            except Exception:
                print(f'失敗しました')
                logger.error('出力先フォルダー削除失敗', exc_info=True)

    files = os.listdir(dst)
    dst_dirs = [f for f in files if os.path.isdir(os.path.join(dst, f))]

    print(yellow(f'{len(dst_dirs)}個のフォルダーが見つかりました'))
    logger.info(f'対象フォルダー：{dst}, {len(dst_dirs)}個のフォルダー')

    for i, dst_dir in enumerate(dst_dirs):
        path = os.path.join(dst, dst_dir)
        print(f'{str(len(dst_dirs))}個中{str(i+1)}個目のフォルダーを検索中...')
        if is_folder_empty(path):
            print(f'"{dst_dir}"は空です')
            logger.info(f'空のフォルダー：{dst_dir}')
            shutil.move(path, os.path.join(dst, out_dir))

    print(yellow(f'検索が完了しました'))


def is_folder_empty(path):
    files = os.listdir(path)

    # ファイル数が0でなければFalse
    if len([f for f in files if os.path.isfile(os.path.join(path, f))]) > 0:
        return False

    # フォルダーが存在するなら再帰的に関数を呼び出し
    for dir in [f for f in files if os.path.isdir(os.path.join(path, f))]:
        rtn = is_folder_empty(os.path.join(path, dir))
        if rtn == False:
            return False

    # ファイルもフォルダーも0ならTrue
    return True


def yellow(txt):  # 文字の色づけ
    return '\033[33m'+txt+'\033[0m'


def red(txt):
    return '\033[31m'+txt+'\033[0m'


if __name__ == '__main__':
    log_file_name = '{:%Y-%m-%d-%H%M%S}'.format(datetime.now())+'.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file_name, format="%(asctime)s %(levelname)-7s %(message)s")
    print(f'***CopyRight 2022 Chansei MIT License***')
    print(f'***Build Version {BUILD_VER}***')
    print(f'***https://github.com/chansei/documents***')
    print(yellow(f'ログファイル：{log_file_name}'))

    num = input(
        '=================\n操作を選択してください\n1:フォルダー検索\n2:空フォルダーの確認\n=================\n')
    logger.info(f'操作：{num}')
    if num == '1':
        search()
    elif num == '2':
        check()

    _ = input('何かキーを押すと終了します...')
