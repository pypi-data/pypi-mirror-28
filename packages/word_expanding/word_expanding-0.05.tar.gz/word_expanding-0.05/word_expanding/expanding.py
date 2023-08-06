from gensim.models import KeyedVectors
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm
import csv
from word_expanding.text_manager import TextManager


def expanding_words(initial_words_file, expanding_time, word2vec_model, mark="", stopwords=None):
    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%s')[:-8]
    model = KeyedVectors.load_word2vec_format(word2vec_model)

    initial_words = [line.strip() for line in open(initial_words_file, encoding='utf-8')]
    already_know = [w.upper() for w in initial_words]
    unprocessed = [w for w in already_know if w in model.vocab]
    occurence = defaultdict(int)

    calculated = set()

    tqdm_iterator = tqdm(range(expanding_time), total=expanding_time)

    while len(unprocessed) > 0 and expanding_time >= 0:
        w = unprocessed.pop()
        tqdm_iterator.set_description('Iter: {}'.format(expanding_time))
        if w in calculated: continue
        most_similar = [w for w, v in model.wv.most_similar(w)]
        for _w in most_similar:
            tqdm_iterator.set_postfix(new_word=_w)
            occurence[_w] += 1
        unprocessed += most_similar
        expanding_time -= 1
        tqdm_iterator.update(1)
        calculated.add(w)

    occurence = sorted(occurence.items(), key=lambda x: x[1], reverse=True)

    def contain_in_initial(w):
        for iw in already_know:
            if iw.find(w) >= 0 or w.find(iw) >= 0: return True
        return False

    suspected = [(w, c) for w, c in occurence[:100] if not contain_in_initial(w) and w not in stopwords]
    suspected = [(w, c) for w, c in suspected if TextManager.is_valid_content(w)]

    with open('{}-{}-expanding.csv'.format(now, mark), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'value'])
        for w, c in suspected:
            writer.writerow([w, c])

    print('expanding end!')



