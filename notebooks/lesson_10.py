from itertools import islice
from pathlib import Path
import pickle, gzip, math, os, time, shutil, matplotlib as mpl, matplotlib.pyplot as plt


MNIST_URL='https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/data/mnist.pkl.gz?raw=true'
path_data = Path('data')
path_data.mkdir(exist_ok=True)
path_gz = path_data/'mnist.pkl.gz'

#%%

from urllib.request import urlretrieve
if not path_gz.exists(): urlretrieve(MNIST_URL, path_gz)

with gzip.open(path_gz, 'rb') as f: ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding='latin-1')
#%%
lst1 = list(x_train[0])
vals = lst1[200:210]
vals

# will soon be itertools.batched
def chunks(x, sz):
    for i in range(0, len(x), sz): yield x[i:i+sz]


mpl.rcParams['image.cmap'] = 'gray'
plt.imshow(list(chunks(lst1, 28)))
plt.show()
#%%
it = iter(lst1)
img = list(iter(lambda: list(islice(it, 28)), []))
class Matrix:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        res = self._data
        if isinstance(key, int):
            return self._data[key]
        elif isinstance(key, tuple):
            cpy = self._data
            for i in key:
                cpy = cpy[i]
            return cpy
        return key

mm = Matrix(img)
mm[20,15]

