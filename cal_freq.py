#!/usr/bin/env 
import sys
import math

def get_data(fr_data):
    list_data = []
    for data in fr_data:
        list_data.append(data.strip())
    return list_data

def get_words_dstc(list_dstc):
    list_words = []
    for data in list_dstc:
        if len(data) != 0:
            dict_data = eval(data)
            str_text = dict_data["text"]
            list_text = str_text.replace(".","").replace("?","").replace(",","").split(" ")
            list_words.extend(list_text)
    return list_words

def get_words_writing(list_writing_aid):
    list_words = []
    for data in list_writing_aid:
        if len(data) != 0:
            list_text = data.replace(".","").replace("?","").replace(",","").split(" ")
            list_words.extend(list_text)
    return list_words


def get_mask_list(fr_dstc, fr_writing_aid, fr_stop_words):
    list_dstc = get_data(fr_dstc)
    num_dstc = len(list_dstc)

    list_writing_aid = get_data(fr_writing_aid)
    list_stop_words = get_data(fr_stop_words)
    num_writing_aid = len(list_writing_aid)

    list_words_dstc = list(set(get_words_dstc(list_dstc)).difference(set(list_stop_words)))
    list_words_writing_aid = list(set(get_words_writing(list_writing_aid)).difference(set(list_stop_words)))
    list_words_dstc_uniq = list(set(list_words_dstc))    
    dict_word_freq = {}
    for dstc_words in list_words_dstc_uniq:
        #print(dstc_words)
        dstc_freq = list_words_dstc.count(dstc_words)/num_dstc
        writing_freq = list_words_writing_aid.count(dstc_words)/num_writing_aid
        log_freq = math.log(abs(dstc_freq - writing_freq))
        abs_freq = abs(log_freq)
        if(abs_freq < 9.72):
            dict_word_freq[dstc_words] = abs_freq
            print(dstc_words + "  " + str(abs_freq))
    
    list_res = sorted(dict_word_freq.items(), key=lambda e:e[1], reverse=True)
    n = 0
    for data in list_dstc:
        if len(data) == 0:
            print(data)
        else:
            dict_data = eval(data)
            text = dict_data["text"]
            list_index = []
            for words in text.split(" "):
                if (dict_word_freq.__contains__(words) == True):
                    list_index.append(str(n))

                n = n + 1
            n = 0
            str_res = str(data) + "\t"  + str(",".join(list_index))
            # + str(text) + "\t"
            #print(str_res)


    

if __name__ == '__main__':
    fr_dstc = open("./dstc2_v3/dstc2-trn.jsonlist","r")
    fr_writing_aid = open("dataset.txt","r")
    fr_stop_words = open("stop_words.txt","r")

    get_mask_list(fr_dstc, fr_writing_aid, fr_stop_words) 