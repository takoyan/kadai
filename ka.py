#!/usr/bin/env python
# -*- coding: utf-8 -*-

#外部ファイルから質問リストを読み込み辞書に保存するプログラム
import math
import sys
from janome.tokenizer import Tokenizer
import rospy
from std_msgs.msg import String

#text = String()
t = Tokenizer()
qa_dict = {}

def get_Cos_up(v1, v2):
    sum=0
    for word in v1:
        if word in v2:
            sum += 1
    return sum


def get_Cos_under(list):
    return math.sqrt(len(list))


def get_Cos_sim(v1, v2):
    return float(get_Cos_up(v1, v2)/get_Cos_under(v1)*get_Cos_under(v2))


def get_Surface(words):
    surface=[]
    for word in words:
        surface.append(word.surface)
    return surface


def callback(data):
    text = data.data
    print(text)
    text = text.decode('utf-8')
    print(text)
    word_surface = get_Surface(t.tokenize(text)) #自分で打ち込んだ形態素解析された質問文
    max=0
    answer=0
    for q, a in qa_dict.items():
        q_surfaces = get_Surface(t.tokenize(q))
        score = get_Cos_sim(word_surface, q_surfaces)
        if (score > max):
            max = score
            answer = a

    if answer is not 0:
        print answer
    else:
        print '答えは見つかりません'


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()



if __name__ == '__main__':
    with open('./dic.txt', 'r') as f: #pythonでのファイルオープン
        qa_list = f.readlines()
        for qa in qa_list:
            qa = qa.rstrip().decode('utf-8').split(',') #改行コードを削除し，デコードした後カンマで質問と解答に区切る
            qa_dict[qa[0]] = qa[1] #辞書に質問をキー，解答を値として保存
    listener()
