"""
Training Word Embedding
"""

import jieba
import os
from word_expanding import utilities
from word_expanding.text_manager import TextManager
import fasttext
from word_expanding.utilities import connect_words
from word_expanding.utilities import hash_string
from word_expanding.utilities import logging_info
from word_expanding.expanding import expanding_words


class Embedding:
    def __init__(self, input_files=None, initial_words_file=None, dim=50, expanding_time=50, method='skip-gram', self_define_dictionary=None, update_corpus=False):
        """
        :param dim: the dimonsion of word2vec, default is 50.
        :param expanding_time: the expanding times, default is 50, the more expanding time, the further model search.
        :param method: skip-gram or cbow, default is skip-gram
        :param self_define_dictionary: self-defined dictionay file name, e.g 'your-self-dict.txt'
        :param update_corpus: Boolean, if is true, will update all the train corpus.

        e.g
            files = [
                root + 'gamble_paid.csv',
                root + 'group_names.txt',
            ]

            embedding = Embedding(input_files=files,
                                initial_words_file='../initial_words.txt',
                                dim=50, expanding_time=100, update_corpus=False)
            embedding.expanding_new_words()
        """
        if self_define_dictionary is not None: jieba.load_userdict(self_define_dictionary)

        initial_words_file = initial_words_file or './initial_words.txt'
        src_dir = './source_files'
        input_files = input_files or ["{}/{}".format(src_dir, f) for f in os.listdir(src_dir)]

        target_dir = './targets'
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        self.target_dir = target_dir
        self.dict = self_define_dictionary
        self.initial_words_file = initial_words_file
        self.method = method
        self.input_files = input_files
        self.dim = dim
        self.text_manager = TextManager(self_define_dictionary)
        self.update_corpus = update_corpus
        self.expanding_time = expanding_time

    def expanding_new_words(self):
        if self.embedding_exist():
            self.expanding()
        else:
            self.get_embedding()
            self.expanding_new_words()

    def expanding(self):
        expanding_words(
            self.initial_words_file,
            self.expanding_time,
            self.get_w2v_model_name()+'.vec',
            mark=str(self.dim) + '-' + str(self.expanding_time),
            stopwords=self.text_manager.get_stopwords(),
        )

    def get_embedding(self):
        if self.update_corpus is True or not self.line_corpus_exist():
            self.get_line_corpus()

        assert os.path.exists(self.get_line_corpus_name())

        if self.method.lower() == 'skip-gram':
            embedding = fasttext.skipgram
        elif self.method.lower() == 'cbow':
            embedding = fasttext.cbow
        else:
            raise TypeError('Unsupported embedding method, <skip-gram(default), cbow> are supported!')

        logging_info('training embedding')
        embedding(self.get_line_corpus_name(), self.get_w2v_model_name(), dim=self.dim)
        logging_info('end embedding')

    def get_line_corpus_name(self):
        line_corpus_file = hash_string(connect_words([self.input_files, self.dict])) + '.txt'
        return self.target_dir + '/' + line_corpus_file

    def get_w2v_model_name(self):
        if self.dict is not None and os.path.exists(self.dict):
            dict_md5 = utilities.md5(self.dict)
        else:
            dict_md5 = ""

        w2v_model_name = hash_string(connect_words([self.input_files, self.dim, self.method, dict_md5]))

        return self.target_dir + '/' + w2v_model_name

    def line_corpus_exist(self):
        return os.path.exists(self.get_line_corpus_name())

    def embedding_exist(self):
        return os.path.exists(self.get_w2v_model_name() + '.vec')

    def get_line_corpus(self):
        logging_info('get training corpus')
        with open(self.get_line_corpus_name(), 'w', encoding='utf-8') as fline:
            self.input_files = [f.strip() for f in self.input_files]
            for file in self.input_files:
                if file.endswith('.csv'):
                    self.text_manager.append_csv_file(file, fline)
                else: self.text_manager.append_text_file(file, fline)


if __name__ == '__main__':
    embedding = Embedding(dim=80, expanding_time=60)
    embedding.expanding_new_words()
