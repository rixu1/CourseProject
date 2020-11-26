"""
Loading Gensim and nltk libraries
"""
# pip install gensim
import gensim
import nltk
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import os, codecs, re
from research_interests_mapping import KEYWORDS_RESEARCH_AREA_MAPPING

stemmer = SnowballStemmer("english")


def main(bio_dir, out_path):
    results = []
    print("proprocessing documents")
    count = 0
    for i in range(len(os.listdir(bio_dir)) - 2):
        try:
            with codecs.open(
                os.path.join(bio_dir, str(i) + ".txt"),
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                document = f.read().lower()
                word_tokens = nltk.word_tokenize(document)
                is_noun = lambda pos: pos[:2] == 'NN'
                nouns = [word for (word, pos) in nltk.pos_tag(word_tokens) if is_noun(pos)]
                word_set = set()
                for word in nouns:
                    if word not in STOPWORDS:
                        word_set.add(word)
                areas = set()
                for word in word_set:
                    for key, v in KEYWORDS_RESEARCH_AREA_MAPPING.items():
                        if key in word:
                            areas.add(v)
                areas_list = list(areas)[:10]
                result = ",".join(areas_list)
                results.append(result)
                if count % 1000 == 0:
                    print(count)
                count += 1
        except:
            pass

    with codecs.open(out_path, 'w', encoding='utf-8', errors='ignore') as f:
        for area in results[:-1]:
            f.write(area + '\n')
        if area[-1] == '':
            f.write('\n')
        else:
            f.write(results[-1])
    # print("Building Vocalbulary")
    # dictionary = gensim.corpora.Dictionary(documents)

    # count = 0
    # for k, v in dictionary.iteritems():
    #     print(k, v)
    #     count += 1
    #     if count > 10:
    #         break
    # dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n= 1000)
    #
    # count = 0
    # for k, v in dictionary.iteritems():
    #     print(k, v)

    # bow_corpus = [dictionary.doc2bow(doc) for doc in documents]
    #
    # print("executing LDA...")
    # lda_model = gensim.models.LdaMulticore(bow_corpus,
    #                                        num_topics=10,
    #                                        id2word=dictionary,
    #                                        passes=10,
    #                                        workers=2)
    #
    # for idx, topic in lda_model.print_topics(-1):
    #     print("Topic: {} \nWords: {}".format(idx, topic))
    #     print("\n")


if __name__ == "__main__":
    main("../data/compiled_bios/", "../data/interests")

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()
