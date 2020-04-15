"""
1. build conversation tree
The structure is [(parent, index), ["the", "cat", ...], hashtag]
2. build dictionary

Notes:
    1. replace @XX to MEN
    2. replace #XX to HASH
    3. replace numbers to DIG
    3. remove url links
    4. "we're" -> ["we", "'re"]
"""
import logging
import os
import itertools
import gensim
from scipy import sparse
import pickle
import numpy as np
import re
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

data_folder = "."
message_fn = os.path.join(data_folder, "twitter_conv.data")

def extractSentWords(doc, remove_url=True, replace_digit=False, lemm=True):
    doc = gensim.utils.to_unicode(doc, 'latin1').strip()
    # filter non-ascii words

    meta_doc = doc.split("%%%")
    if len(meta_doc) == 1:
        raise Exception("missing meta: %s" % doc)
    tree_info, sent = meta_doc
    sent = re.sub(r'[^\x00-\x7F]+', ' ', sent)

    if remove_url:
        re_url = r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        sent = re.sub(re_url, "", sent)

    sent = re.sub("'", " '", sent)

    sent = sent.lower()
    hashtag = ""
    hashtags = re.findall(r"#[\S]+", sent)
    if hashtags:
        hashtag = hashtags[0]
    sent = re.sub(r"#[\S]+", "HASH", sent)
    sent = re.sub(r"@[\S]+", "MEN", sent)

    if replace_digit:
        sent = re.sub(r"-?\d+(\.\d+)?", "DIG", sent)

    words = re.split(r"[\s+,\.;:`\"()?!{}\-*\/&%=_<>\[\]~\|\$\\]", sent)
    if lemm:
        wnl = WordNetLemmatizer()
        words = list(map(lambda w: wnl.lemmatize(w, 'v'), words))
    words = list(filter(lambda w: w and not w == "'" and True or False, words))
    return tree_info, words, hashtag

# def iter_docs(fn):
#     with open(fn, encoding="utf-8") as fin:
#         lines = fin.readlines()
#     num_posts = 0
#     tree_dict = {}
#     conv_trees = []
#     conv_tree = []
#     for l_id, line in enumerate(lines):
#         if l_id % 10000 == 0:
#             print("processed %d posts" % l_id)
#         try:
#             tree_info, words, hashtag = extractSentWords(line, lemm=False)
#         except Exception as inst:
#             print("%s in line %d" % (inst.args, l_id))  # the exception instance
#             continue
#         tree_infos = tree_info.split("\t")
#
#         if tree_infos[1] == "null":  # root, we could empty the dict to save space
#             tree_dict[tree_infos[0]] = [0, 1]  # (parent, index)
#             parent_index = 0
#             self_index = 1
#             if conv_tree:
#                 conv_trees.append(conv_tree)
#                 num_posts += len(conv_tree)
#             conv_tree = [[(parent_index, self_index), words, hashtag]]  # init a conversation tree
#         else:
#             tree_dict[tree_infos[0]] = [tree_dict[tree_infos[1]][0], self_index + 1]
#
#             parent_index = tree_dict[tree_infos[0]][0]
#             self_index = tree_dict[tree_infos[0]][1]
#             conv_tree.append([(parent_index, self_index), words, hashtag])
#     if conv_tree:
#         conv_trees.append(conv_tree)
#         num_posts += len(conv_tree)
#     print("total %d posts, %d conversations" % (num_posts, len(conv_trees)))
#     return conv_trees


def iter_docs(fn):

    with open(fn, "U") as fin:
        lines = fin.readlines()
    num_posts = 0
    tree_dict = {}
    conv_trees = []
    conv_tree = []
    for l_id, line in enumerate(lines):
        if l_id % 10000 == 0:
            print("processed %d posts" % l_id)
        line = line.strip()
        tree_info, words, hashtag = line.split("%%%")
        words = words.split()
        tree_infos = tree_info.split("\t")
        self_id = tree_infos[0]
        parent_id = tree_infos[1]

        if parent_id == "null":  # root, we could empty the dict to save space
            tree_dict[self_id] = [0, 1]  # (parent, index)
            self_index = 1
            if conv_tree:
                conv_trees.append(conv_tree)
                num_posts += len(conv_tree)
            conv_tree = [[(tree_dict[self_id][0], tree_dict[self_id][1]), words, hashtag]]  # init a conversation tree
        else:
            if parent_id in tree_dict:
                tree_dict[self_id] = [tree_dict[parent_id][1], self_index + 1]
                self_index = tree_dict[self_id][1]
                conv_tree.append([(tree_dict[self_id][0], self_index), words, hashtag])
    if conv_tree:
        conv_trees.append(conv_tree)
        num_posts += len(conv_tree)
    print("total %d posts, %d conversations" % (num_posts, len(conv_trees)))
    return conv_trees

def build_dictionary(conv_trees):
    texts = []
    for conv_tree in conv_trees:
        for tree_info, words, hashtag in conv_tree:
            texts.append(words)
    seq_dictionary = gensim.corpora.Dictionary(texts)
    seq_dictionary.filter_tokens(list(map(seq_dictionary.token2id.get, ["HASH", "MEN", "DIG"])))
    seq_dictionary.compactify()
    import copy
    bow_dictionary = copy.deepcopy(seq_dictionary)
    bow_dictionary.filter_tokens(list(map(bow_dictionary.token2id.get, STOPWORDS)))
    len_1_words = list(filter(lambda w: len(w) == 1, bow_dictionary.values()))
    bow_dictionary.filter_tokens(list(map(bow_dictionary.token2id.get, len_1_words)))
    bow_dictionary.filter_extremes(no_below=4, keep_n=None)
    bow_dictionary.compactify()
    return bow_dictionary, seq_dictionary

def collect_hashtag(conv_trees):
    ht_dict_conv = Counter()
    ht_dict_post = Counter()
    for conv_tree in conv_trees:
        ht_c = Counter()
        for tree_info, words, hashtag in conv_tree:
            if hashtag != "null":
                ht_c[hashtag] += 1
                ht_dict_post[hashtag] += 1

        ht_conv = ht_c.most_common(1)
        if ht_conv:
            ht_conv = ht_conv[0][0]
            ht_dict_conv[ht_conv] += 1
    #             ht_dict_post[ht_conv] += len(conv_tree)
    print(ht_dict_conv.most_common(50))
    return ht_dict_conv, ht_dict_post

def get_indexinput(conv_trees, bow_dict, seq_dict, ht_dict):
    labels = list(list(zip(*(ht_dict.most_common(50))))[0])
    label_dict = {k: v for v, k in enumerate(labels)}

    seq_doc = []
    origin_hashtag = []
    conv_group = []
    all_posts = []
    conv_posts = []
    # all_hashtag = []
    row, row_p = [], []
    col, col_p = [], []
    value, value_p = [], []
    avergl = []
    maxl = 0
    avergc = []
    maxc = 0
    row_id = 0
    btm = []
    firstblood = False
    for c_i, conv_tree in enumerate(conv_trees):
        ht_c = Counter()
        for tree_info, words, hashtag in conv_tree:
            if hashtag:
                ht_c[hashtag] += 1
        ht_conv = ht_c.most_common(1)
        if not ht_conv:
            continue
        ht_conv = ht_conv[0][0]
        if ht_conv in labels:
            # print("index: %d with label: %s" % (c_i, ht_conv))
            # build index input
            text = []
            first_post = True

            for tree_info, words, hashtag in conv_tree:
                if not first_post:
                    continue
                first_post = False
                # btm
                btm_lst = []
                if len(bow_dict.doc2bow(words)) == 0:
                    continue
                for i, j in bow_dict.doc2bow(words):
                    # for btm
                    btm_lst += [i + 1] * j
                    row_p.append(row_id)
                    col_p.append(i)
                    value_p.append(j)
                row_id += 1
                btm.append(btm_lst)
                wids = list(map(seq_dict.token2id.get, words))
                wids = np.array(list(filter(lambda x: x is not None, wids))) + 1


                # all_posts.append(wids)
            #     text.append(wids)
                seq_doc.append(wids)
                origin_hashtag.append(label_dict[ht_conv])
            # if len(text) > 0:   # avoiding the first post is filtered
            #     text = list(itertools.chain.from_iterable(text))
            #     conv_posts.append(np.array(text) + 1)
            #
            # avergc.append(len(text))
            # maxc = max(maxc, len(text))
            # for w_id in text:
            #     row.append(len(conv_posts) - 1)
            #     col.append(w_id)
            #     value.append(1)
    print("rid", row_id)
    lens = list(map(len, seq_doc))
    # bowConv = sparse.coo_matrix((value, (row, col)), shape=(len(conv_posts), len(vocab_dict)))
    bowPost = sparse.coo_matrix((value_p, (row_p, col_p)), shape=(row_id, len(bow_dict)))
    print("get %d docs, avg len: %d, max len: %d" %
          (len(seq_doc), np.mean(lens), np.max(lens)))

    # split data
    indices = np.arange(len(seq_doc))
    np.random.shuffle(indices)
    nb_test_samples = int(0.2 * len(seq_doc))
    seq_title = np.array(seq_doc)[indices]
    seq_title_train = seq_title[:-nb_test_samples]
    seq_title_test = seq_title[-nb_test_samples:]
    bow_title = bowPost.tocsr()
    bow_title = bow_title[indices]
    bow_title_train = bow_title[:-nb_test_samples]
    bow_title_test = bow_title[-nb_test_samples:]
    label_title = np.array(origin_hashtag)[indices]
    label_title_train = label_title[:-nb_test_samples]
    label_title_test = label_title[-nb_test_samples:]
    btm = np.array(btm)[indices]
    btm_title_train = btm[:-nb_test_samples]
    btm_title_test = btm[-nb_test_samples:]

    pickle.dump(seq_title, open("dataPost", 'wb'))
    pickle.dump(seq_title_train, open("dataPostTrain", "wb"))
    pickle.dump(seq_title_test, open("dataPostTest", "wb"))
    pickle.dump(bow_title, open("dataPostBow", "wb"))
    pickle.dump(bow_title_train, open("dataPostBowTrain", "wb"))
    pickle.dump(bow_title_test, open("dataPostBowTest", "wb"))
    pickle.dump(label_title, open("dataPostLabel", 'wb'))
    pickle.dump(label_title_train, open("dataPostLabelTrain", "wb"))
    pickle.dump(label_title_test, open("dataPostLabelTest", "wb"))
    pickle.dump(btm_title_train, open("dataPostBtmTrain", "wb"))
    pickle.dump(btm_title_test, open("dataPostBtmTest", "wb"))
    pickle.dump(label_dict, open("hashtagMap", "wb"))
    bow_dict.save("dataDictBow")
    seq_dict.save("dataDictSeq")

    return seq_title, seq_title_train, seq_title_test, bow_title, bow_title_train, bow_title_test, label_title, label_title_train, label_title_test, btm_title_train, btm_title_test, label_dict, bow_dict, seq_dict

conv_trees = iter_docs(message_fn)
ht_dict_conv, ht_dict_post = collect_hashtag(conv_trees)
bow_dict, seq_dict = build_dictionary(conv_trees)
seq_title, seq_title_train, seq_title_test, bow_title, bow_title_train, bow_title_test, label_title, label_title_train, label_title_test, btm_title_train, btm_title_test, label_dict, bow_dict, seq_dict = get_indexinput(conv_trees, bow_dict, bow_dict, ht_dict_conv)


convert = []
for seq in seq_title:
    sent = []
    for idx in seq:
        word = seq_dict.id2token[idx]
        sent.append(word)
    convert.append(sent)

