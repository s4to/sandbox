# coding: utf-8

from bs4 import BeautifulSoup
import re

FORMAT_TAG = "instrText"
CONVERT_STRING = re.compile(r"\ *-\ *")
IGNORE_STRING = " "
ARABIC_OPTION = " ArabicDash "


def contains_prev_inlinetext(elm):
    """
    手前の兄弟要素の inline text を処理
    """

    # フィールドの区切りタグを無視する
    prev_elm = elm.previous_sibling
    prev_convert_no = 0

    while True:
        # 前のタグをどんどん見ていく
        prev_elm = prev_elm.previous_sibling
        res, prev_convert_no = contains_arabic_element(prev_elm, prev_convert_no)

        if not res:
            break

    return prev_elm, prev_convert_no


def contains_next_inlinetext(elm):
    """
    次の兄弟要素の inline text を処理
    """
    # フィールドの区切りタグを無視する
    next_elm = elm.next_sibling.next_sibling.next_sibling
    next_convert_no = 0

    while True:
        next_elm = next_elm.next_sibling
        res, next_convert_no = contains_arabic_element(next_elm, next_convert_no)

        if not res:
            break

    return next_elm, next_convert_no


def contains_arabic_element(elm, convert_no):
    """
    arabic 要素を含んでいる位置を特定する
    Args:
        elm: XMLの要素
        convert_no: 位置
    Returns:
        bool: 次のelementを処理するかどうか
        int: 整形する可能性のある番号
    """

    # 直前のタグが存在しない、もしくは、rタグでない場合そく終了する
    if not elm or elm.name != "r":
        return False, 0

    inline_text = elm.find("t", recursive=False)
    if not inline_text:
        return False, 0

    # インナーテキストが空の場合、半角スペースとして認識するよう
    if inline_text.string == IGNORE_STRING:
        convert_no += 1
        return True, convert_no

    # ダッシュが含まれるかどうか
    if CONVERT_STRING.match(inline_text.string):
        convert_no += 1
        return False, convert_no
    else:
        return False, 0


def formatting_page_no(file_path):
    f = open(file_path, 'r')
    _xml = f.read()

    soup = BeautifulSoup(_xml, "xml")

    # すべてのw:instrTextを取得
    instrTexts = soup.find_all(FORMAT_TAG)

    # TODO: 複数に対応する予定 とりあえず
    instrTexts = instrTexts[0]

    # TODO: PAGE かどうか。  (\* ArabicDash を含まない)
    if not instrTexts.string.find(r"\ PAGE\ "):
        return

    page_no_elm = instrTexts.parent

    # TODO: ここでinstrTextsのフォーマットを検証
    # 開始位置と終了位置を取得する

    prev_elm, prev_no = contains_prev_inlinetext(page_no_elm)
    next_elm, next_no = contains_next_inlinetext(page_no_elm)

    if prev_no == 0 or next_no == 0:
        return

    for _ in range(prev_no):
        e = prev_elm
        prev_elm = prev_elm.next_sibling
        e.decompose()

    for _ in range(next_no):
        e = next_elm
        next_elm = next_elm.previous_sibling
        e.decompose()

    field = instrTexts.string.split("\*")
    field.insert(1, ARABIC_OPTION)

    instrTexts.string = "\*".join(field)

    print("exec 0")
    return soup


if __name__ == '__main__':
    # TODO: zipを解凍する処理
    # 解凍後にフッターを検索する
    # 整形する処理(一部みかん)
    # 解凍したファイルを再度zipにまとめる。

    footer = formatting_page_no("footer1.xml")
    f = open("res.xml", 'w')
    f.write(str(footer))

    footer = formatting_page_no("footer2.xml")
    f = open("res2.xml", 'w')
    f.write(str(footer))
