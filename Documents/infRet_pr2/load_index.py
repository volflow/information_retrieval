import pickle
from parser import *


if __name__ == '__main__':
    print('Loading index in memory ...')
    fp = 'small_index_dump'
    with open(fp,'rb') as handle:
        index = pickle.load(handle)
    print('done.')
