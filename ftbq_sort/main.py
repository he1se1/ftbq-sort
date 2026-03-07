import argparse
import sys
from .snbt_parser import SnbtParser
from .graph_sorter import GraphSorter
from .lang_sorter import LangSorter

def main():
    parser = argparse.ArgumentParser(description="Sort FTB Quests lang files topologically.")
    parser.add_argument("quests_dir", help="Path to the ftbquests/quests directory (contains 'chapters' dir and 'chapter_groups.snbt')")
    parser.add_argument("lang_in", help="Path to the input lang JSON file")
    parser.add_argument("lang_out", help="Path to the output sorted lang JSON file")
    
    args = parser.parse_args()
    
    # 1. SNBTのパース
    try:
        snbt_parser = SnbtParser(args.quests_dir)
        parsed_chapters = snbt_parser.parse_all()
    except Exception as e:
        print(f"Error parsing SNBT files: {e}")
        sys.exit(1)
        
    # 2. グラフ構築とトポロジカルソート
    sorted_chapters = []
    for chapter in parsed_chapters:
        sorted_ids = GraphSorter.topological_sort(chapter.quests)
        sorted_chapters.append((chapter.chapter_name, sorted_ids))
        
    # 3. langファイルのソートと書き出し
    try:
        lang_sorter = LangSorter(args.lang_in, args.lang_out)
        lang_sorter.sort_and_save(sorted_chapters)
        print(f"Successfully sorted lang keys into {args.lang_out}")
    except Exception as e:
        print(f"Error sorting lang file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()