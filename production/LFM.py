#coding:utf-8
'''
@Time: 2019/10/14 下午2:26
@author: Tokyo
@file: LFM.py
@desc:LFM model train main function
'''

import numpy as np
import sys
sys.path.append("../util")
import util.read as read
def lfm_train(train_data, F, alpha, beta, step):
    """

    :param train_data:training data for lfm
    :param F:  length of user vector, item vector
    :param alpha:  regularization factor
    :param beta:   learning rate
    :param step:   iteration number
    Return:
    dict: key: itemid  value: list
    dict  key: userid  value: list
    """
    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        for data_instance in train_data:
            userid, itemid, label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F)

        delta = label - model_predict(user_vec[userid], item_vec[itemid])
        for index in range(F):
            user_vec[userid][index] += beta*(delta*item_vec[itemid][index] - alpha*user_vec[userid][index])
            item_vec[itemid][index] += beta*(delta*user_vec[itemid][index] - alpha*item_vec[itemid][index])
        # 学习率衰减
        beta = beta * 0.9
    return user_vec, item_vec


def init_model(vector_len):
    """

    :param vector_len: the length of vector
    Return:
    a ndarray
    """
    return np.random.randn(vector_len)

def model_predict(user_vector, item_vector):
    """
    user_vector and item_vector distance
    :param user_vector:  model produce user vector
    :param item_vector:  model produce item vector
    Return:
    a num
    """
    res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)* np.linalg.norm(item_vector))
    return res


def model_train_process():
    """
    test lfm model train
    """
    train_data = read.get_train_data("../data/ratings.dat")
    user_vec, item_vec = lfm_train(train_data, F=50, alpha=0.01, beta=0.1, step=50)
    print(user_vec["1"])
    print(item_vec["2455"])


if __name__ == '__main__':
    model_train_process()



