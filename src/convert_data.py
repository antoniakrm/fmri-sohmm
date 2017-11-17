#!/usr/bin/python
#  -*- coding: utf-8 -*-

from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

import scipy.io as sio
import os, argparse
import numpy as np
import codecs


def vec2tensor(vector, mapping):
    tensor = np.zeros((51, 61, 23))
    for i in range(len(vector)):
        x, y, z = mapping(i)
        tensor[x][y][z] = vector[i]
    return tensor


def concatenate(matrices):
    """
    Input: n matrices of shape (m, d)
    Output: matrix of shape (m, d*n)
    """
    outmat = []
    m = len(matrices[0])
    for i in range(m):
        outmat.append([])
        for mx in matrices:
            outmat[i].extend(mx[i])
    return np.array(outmat)


def map_words2vecs(words, times, vecs, normalize=True, lookout=4.0, lookback=0.0):
    def vecavg(vs):
        vsum = np.zeros(vs[0].shape[0])
        for v in vs:
            vsum = vsum + v
        return vsum / len(vs)

    def vecs_by_timeframe(t_start, t_end):
        return vecs[int(t_start*2):int(t_end*2)]  # there are 2 vectors for every second, e.g. vector #40 is at 20 sec

    vecs_out = []
    m = len(words)
    for i in range(m):
        start = times[i] - lookback
        end = times[i] + 0.5 + lookout
        vecs_out.append(vecavg(vecs_by_timeframe(start, end)))
    if normalize:
        mms = MinMaxScaler()
        vecs_out = mms.fit_transform(vecs_out)
    words2vecs = [(w, vs) for w, vs in zip(words, vecs_out)]
    return words2vecs


def inflate(vecs):
    inflated = []
    for v in vecs:
        for _ in range(4):
            inflated.append(v)
    return np.array(inflated)


def remove_punct(word):
    """
    :param word:
    :return: the (possibly modified) word, a boolean variable whether end of sentence
    """
    word = ''.join(ch for ch in word if ch not in "‘\"")
    exceptions = ["Mr.", "Mrs.", "Ms.", "Dr."]
    if word in exceptions:
        return word, False
    if word == '--':
        return "<punct>", True
    eos = False
    eospunct = set(".?!…—")
    for p in eospunct:
        if word.endswith(p):
            eos = True
        word = word.strip(p)
    eospunct.update(set("@,:;\""))
    word = ''.join(ch for ch in word if ch not in eospunct)
    # prevent empty word
    if word == "":
        word = "<punct>"
    return word, eos


def convert(data_dir, outfile_name, vec_dim=100, subjects=8, normalize=True, lookout=4.0, lookback=0.0):
    pca = PCA(n_components=vec_dim)
    words = []
    times = []
    reduced_vecs = []
    for i in range(1, subjects+1):
        print(i)
        matfile = os.path.join(data_dir, "subject_{}.mat".format(i))
        data = sio.loadmat(matfile)
        if i == 1:
            for w in data["words"][0]:
                words.append(w[0][0][0][0])
                times.append(w[1][0][0])
        # vec2tensor_map = data["meta"][0][0][6]
        vecs = data["data"]
        reduced_vecs.append(pca.fit_transform(vecs))  # 1351 TRs, to be mapped to 5176 words

    reduced_vecs = concatenate(np.array(reduced_vecs))
    reduced_vecs = inflate(reduced_vecs)
    print("RVecs shape")
    print(reduced_vecs.shape)
    words2vecs = map_words2vecs(words, times, reduced_vecs, normalize, lookout, lookback)
    wc = 0
    sc = 0
    outfile_name = "data/vecs/{}-{}-{}-{}-{}.vecs".format(outfile_name, subjects, lookback, lookout, vec_dim)
    print("Writing vectors to file: "+outfile_name)
    outfile = codecs.open(outfile_name, "w", "utf-8")
    print(outfile)
    # fileidx = 0
    for w, v in words2vecs:
        eos = False
        w, eos = remove_punct(w)
        if w == "+" or w == "<punct>":
            # of.write("\n")
            continue
        outfile.write("{}_{}".format(w, wc))
        wc += 1
        for i in range(v.shape[0]):
            outfile.write("\t{}".format(v[i]))
        outfile.write("\n")
        if eos:
            sc += 1
            outfile.write("\n")
            # if sc in [41, 82]:  # make splits here
                # fileidx += 1


def main():
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    data_dir = '../fmri/data'
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', default=data_dir, help='Features and labels')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true')
    parser.add_argument('--output', '-o', help="Output file", default='potter')
    parser.add_argument('--dim', type=int, help="Dimensionality of features per subject", default=100)
    parser.add_argument('--subjects', '-s', type=int, help="Number of subjects", default=8)
    parser.add_argument('--normalize', dest='normalize', help="Column-wise normalization of features", action='store_true')
    parser.add_argument('--no-normalize', '-N', dest='normalize', help="No column-wise normalization of features", action='store_false')
    parser.add_argument('--lookout', type=float, help="future context", default=4.0)
    parser.add_argument('--lookback', type=float, help="past context", default=0.0)
    parser.set_defaults(normalize=True)
    args = parser.parse_args()
    convert(args.data, args.output, args.dim, args.subjects, args.normalize, args.lookout, args.lookback)

if __name__ == "__main__":
    main()
