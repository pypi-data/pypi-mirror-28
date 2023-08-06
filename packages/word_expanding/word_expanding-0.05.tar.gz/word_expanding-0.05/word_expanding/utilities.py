import hashlib
import os
import subprocess


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def connect_words(words, connecter='-'):
    return connecter.join(map(str, words))


def hash_string(string):
    return hashlib.md5(string.encode()).hexdigest()


def get_file_lines(file):
    if os.name == 'nt':  # window operation system cannot call wc -l
        res = 0
        with open(file):
            for _ in file: res +=1
        return res
    else:
        p = subprocess.Popen(['wc', '-l', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])


def logging_info(key_words):
    print('##' * 22 + ' ' + key_words.upper() + ' ' + '##' * 22)


if __name__ == '__main__':
    assert md5('data/dict.txt') == md5('../data3.txt')
    assert md5('data/dict.txt') != md5('../data_2.txt')

    assert hash_string('test1') == hash_string('test1')
    assert hash_string('test1') != hash_string('test2')

    assert get_file_lines('data/dict.txt') == 1, get_file_lines('data/dict.txt')
    logging_info('embedding')
