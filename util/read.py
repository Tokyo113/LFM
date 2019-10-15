#coding:utf-8
'''
@Time: 2019/10/14 上午10:17
@author: Tokyo
@file: read.py
@desc: util function
'''

import os
def get_item_info(input_file):
    """
    get item info
    :param input_file: item info file
    Return:
    dict: key: itemid, value: [title, genre]
    """

    if not os.path.exists(input_file):
        return {}
    # item_info = {}
    # fp = open(input_file, encoding='gb18030', errors='ignore')
    # for line in fp:
    #     item = line.strip().split("::")
    #     itemid, title, genre = item[0], item[1], item[2]
    #     item_info[itemid] = [title, genre]
    # fp.close()
    # return item_info
    item_info = {}
    linenum = 0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemid] = [title, genre]
    fp.close()
    return item_info


def get_avg_score(input_file):
    """
    get item average rating score
    :param input_file:
    Return:  a dict
    key: itemid,   value:avg score
    """

    if not os.path.exists(input_file):
        return {}


    record_dict = {}
    score_dict = {}
    fp = open(input_file)
    for line in fp:

        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record_dict:
            record_dict[itemid] = [0, 0]
        # 分别记录被多少人打分过，总得分
        record_dict[itemid][0] += 1
        record_dict[itemid][1] += rating
    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0], 3)
    return score_dict

def get_train_data(input_file):
    """
    get train data for  LFM model train
    :param input_file:

    Return:  a list[(userid, itemid, label), (userid1, itemid1, label)]
    label = 1 or 0
    """
    if not os.path.exists(input_file):
        return []
    score_dic = get_avg_score(input_file)
    # 正负样本数据保持一致, 大于４分为正样本
    # dict    {userid1:[(itemid, label), (itemid, label2), ...]
    #          userid2:[(itemid, label), (itemid, label2), ...
    #          }
    pos_dict = {}
    neg_dict = {}
    train_data = []
    fp = open(input_file)

    score_thre = 4.0
    for line in fp:

        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if userid not in pos_dict:
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []
        if rating >= score_thre:
            pos_dict[userid].append((itemid, 1))
        else:
            # 存储的是平均得分，不是０
            score = score_dic.get(itemid, 0)
            neg_dict[userid].append((itemid, score))
    fp.close()
    # 正负样本的均衡以及负采样
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num > 0:
            # 正样本采样
            train_data += [(userid, zuhe[0], zuhe[1]) for zuhe in pos_dict[userid]][:data_num]
        else:
            continue

        # 按平均得分降序排列
        sorted_neg_list = sorted(neg_dict[userid], key=lambda ele: ele[1], reverse=True)[:data_num]
        # 负样本采样,优先选取平均评分高的电影
        # 负样本采样的原则2: 要选取那些热门而用户没有行为的物品
        train_data += [(userid, zuhe[0], 0) for zuhe in sorted_neg_list]
        # if userid == "24":
        #     print(data_num)
        #     print(len(pos_dict[userid]))
        #     print(len(neg_dict[userid]))
        #     print(sorted_neg_list)

    return train_data



if __name__ == '__main__':
    # item_dict = get_item_info("../data/movies2.txt")
    # print(len(item_dict))
    # print(item_dict["1"])
    # print(item_dict["11"])
    #
    # score_dic = get_avg_score("../data/ratings.dat")
    # print(len(score_dic))
    # print(score_dic["31"])
    train_data = get_train_data("../data/ratings.dat")
    print(len(train_data))
    print(train_data[:20])