#!/usr/bin/env 
import sys
import random

def get_slot(list_slot):
    dict_slot = {}
    for line in list_slot:
        list_1 = line.split("\t")
        dict_slot[list_1[0]] = list_1[1]
    
    return dict_slot

def get_slot_val(list_slot):
    dict_slot_val = {}
    for line in list_slot:
        list_2 = line.split("\t")
        if (len(list_2) == 4):
            dict_slot_val[list_2[1]] = list_2[3].split(",")
        else:
            dict_slot_val[list_2[1]] = []
    return dict_slot_val

def change_slot(fr_dstc, list_slot):
    dict_slot = get_slot(list_slot)
    dict_slot_val = get_slot_val(list_slot)
    for data in fr_dstc:
        data = data.strip()
        if(len(data) == 0):
            print(data)
        else:
            dict_dstc = eval(data)
            list_slot = []
            if (dict_dstc.__contains__("db_result") == True):
                dict_dstc["db_result"] = {}


            for slot in dict_slot.keys():
                if (dict_dstc.__contains__("goals") == True):
                    for key in dict_dstc["goals"].keys():
                        dict_dstc["goals"][key] = "dontcare"
                if (slot in dict_dstc["text"]):
                    dict_dstc["text"] = dict_dstc["text"].replace(slot, dict_slot[slot])
                if (len(dict_dstc["dialog_acts"]) != 0):
                    if (slot in dict_dstc["dialog_acts"][0]["act"]):
                        dict_dstc["dialog_acts"][0]["act"] = dict_dstc["dialog_acts"][0]["act"].replace(slot, dict_slot[slot].replace(" ", "_"))
                    
                    if (len(dict_dstc["dialog_acts"][0]["slots"]) != 0):
                        if (dict_dstc["dialog_acts"][0]["slots"][0][0] != "this"):
                            for dict_item in dict_dstc["dialog_acts"]:
                                for slot_val in dict_item["slots"]:
                                    list_sub_slot = []

                                    if (slot == slot_val[0]):
                                        new_slot = dict_slot[slot]
                                        old_slot = slot
                                        old_val = slot_val[1]
                                        if (dict_slot_val[dict_slot[slot]] != []):
                                            new_val = random.choice(dict_slot_val[dict_slot[slot]])
                                        else:
                                            new_val = ""
                                        
                                        list_sub_slot.append(new_slot)
                                        list_sub_slot.append(new_val)

                                        list_slot.append(list_sub_slot)
                                        
                                        dict_dstc["text"] = dict_dstc["text"].replace(old_slot, new_slot)
                                        dict_dstc["text"] = dict_dstc["text"].replace(old_val, new_val)
                                        if (dict_dstc.__contains__("goals") == True):
                                            try:
                                                dict_dstc["goals"][slot] = new_val
                                            except:
                                                pass
            

            dict_dstc["text"] = dict_dstc["text"].replace('\"', '\\"')
            dict_dstc["text"] = dict_dstc["text"].replace('\'', '')

            if(len(list_slot) != 0):
                dict_dstc["dialog_acts"][0]["slots"]= list_slot
            try:
                dict_dstc["dialog_acts"] = [dict_dstc["dialog_acts"][0]]
            except:
                pass
            for slot in dict_slot.keys(): 
                if (slot in str(dict_dstc)):
                    dict_dstc = str(dict_dstc).replace(slot, dict_slot[slot])

            str_dict_dstc = str(dict_dstc).replace("'", "\"")
            str_dict_dstc = eval(repr(str_dict_dstc).replace('\\\\', '\\')) 
            print(str_dict_dstc)                          
    return dict_dstc


if __name__ == '__main__':
    fr_dstc = open(sys.argv[1],"r")
    fr_slot = open('slot.txt',"r")
    
    list_slot = []
    for line in fr_slot:
        line = line.strip()
        list_slot.append(line)
    change_slot(fr_dstc, list_slot)
    