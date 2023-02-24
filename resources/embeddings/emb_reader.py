import pickle
import os


def get_embeddings():
    emb_path = os.path.dirname(os.path.realpath(__file__)) + '/polyglot-th.pkl'
    with open(emb_path, 'rb') as emb_file:
        (word_list, emb_matrix) = pickle.load(emb_file, encoding='latin1')
        embeddings = dict()
        for i in range(len(word_list)):
            word = word_list[i]
            embeddings[word] = emb_matrix[i, :]

        return embeddings


if __name__ == '__main__':
    get_embeddings()