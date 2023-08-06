from jieba import posseg
import jieba
from collections import Counter
import pandas as pd
from word_expanding.utilities import get_file_lines
from tqdm import tqdm


class TextManager:

    def __init__(self, dict=None):
        self.__cutter = jieba
        self.__posseg = posseg
        if dict is not None: self.__cutter.load_userdict(dict)
        self.all_words = Counter()

    def get_stopwords(self, stop_words_size=20):
        return self.all_words.most_common(n=stop_words_size)

    def cut(self, string):
        words = [w.upper() for w in list(self.__cutter.cut(string))]
        self.all_words.update(words)
        return words

    def get_split_line(self, string): return ' '.join(self.cut(str(string).strip()))

    @staticmethod
    def write_to_file(line, f):
        f.write('{}\n'.format(line))

    def append_text_file(self, new_file, old_file):
        try:
            file_lines = get_file_lines(new_file)
        except Exception as e:
            file_lines = None

        with open(new_file, 'r', encoding='utf-8') as f:
            if file_lines is not None:
                file_writer = tqdm(enumerate(f), total=file_lines)
            else:
                file_writer = tqdm(enumerate(f))

            for ii, line in file_writer:
                self.write_to_file(self.get_split_line(line), old_file)
                file_writer.set_description(desc=str(new_file))
                file_writer.set_postfix(line=ii)

    def append_csv_file(self, csv_file, old_file):
        content = pd.read_csv(csv_file, encoding='utf-8')
        rows = len(content)
        columns_n = len(content.columns)

        tqdm_iterator = tqdm(enumerate(content.iterrows()), total=int(rows))
        for ii, row in tqdm_iterator:
            for column in self.get_valid_columns(row[1]):
                self.write_to_file(self.get_split_line(column), old_file)
            tqdm_iterator.update(columns_n)
            tqdm_iterator.set_description(desc=str(csv_file))
            tqdm_iterator.set_postfix(line=ii)

    @staticmethod
    def get_valid_columns(row):
        return filter(TextManager.is_valid_content, row.tolist())

    @staticmethod
    def is_valid_content(s):
        conds = [
            TextManager.is_pure_person_name,
            TextManager.is_pure_number
        ]
        return not any([cond(str(s)) for cond in conds])

    @staticmethod
    def is_pure_number(s): return str(s).isnumeric()

    @staticmethod
    def is_person_name(t): return t.startswith('nr')

    @staticmethod
    def is_pure_person_name(string):
        return all([TextManager.is_person_name(t) for w, t in posseg.cut(string) if t != 'x'])


if __name__ == '__main__':
    assert TextManager.is_pure_person_name('李英杰')
    assert not TextManager.is_pure_person_name('李英杰是个好人')
    assert TextManager.is_pure_person_name('"李英杰","段涵洲"')
    assert TextManager.is_pure_number('1321421312890')
    assert TextManager.is_valid_content('2088202933720187') is False
    assert TextManager.is_valid_content('万代高达模型工具通用展示台支架底座mg rg hg敢达配件1/144 100') is True
    assert TextManager.is_valid_content('李英杰') is False

    W = TextManager(dict='data/dict.txt')

    s = '万代高达模型工具通用展示台支架底座mg'
    assert W.cut(s) == ['万代', '高达', '模型', '工具', '通用', '展示台', '支架', '底座', 'MG'], W.cut(s)
