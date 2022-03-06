def extract_act(fr_dstc):
    list_dialog_acts_middle = []
    for data in fr_dstc:
        data = data.strip()
        if(len(data)==0):
            pass
        else:
            dict_dstc = eval(data) # 把字符串转化成dict
            try:
                list_dialog_acts_middle.append(dict_dstc["dialog_acts"][0]["act"])
            except:
                pass
    set_dialog_acts = set(list_dialog_acts_middle)
    list_dialog_acts_output = list(set_dialog_acts)
    return list_dialog_acts_output





if __name__ == '__main__':
    fr_dstc_trn = open('1',"r")
    fr_dstc_val = open('2',"r")
    fr_dstc_tst = open('3',"r")
    
    list_dialog_acts_trn = extract_act(fr_dstc_trn)
    list_dialog_acts_val = extract_act(fr_dstc_val)
    list_dialog_acts_tst = extract_act(fr_dstc_tst)
    list_dialog_acts = list_dialog_acts_trn + list_dialog_acts_val + list_dialog_acts_tst
    # list_dialog_acts = list_dialog_acts_tst
    set_dstc = set(list_dialog_acts)
    set_dstc = sorted(set_dstc)
    for act in set_dstc:
        output = act + "\t" + act + "\t"
        print(output)
