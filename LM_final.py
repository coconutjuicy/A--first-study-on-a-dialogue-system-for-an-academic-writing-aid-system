import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import torch.utils.data as Data
from transformers import BertTokenizer, BertForSequenceClassification
import json


def pretrain_LM(tensors, eopch_num, words_number, save_pth, batch_size=64, show_step=50, eval_step=500):
    device=torch.device('cuda')
    tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')
    model=BertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=words_number)
    model.train()
    model=model.to(device)
    loss_f=nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    count=0
    print_loss=0
    tensors_backup=tensors.copy()
    for epoch in range(eopch_num):
        print('-----------','Epoch: ',epoch,'------------------')
        tensors_new=tensors_backup.copy()
        data_iter=mask_LM(tensors_new, batch_size=batch_size)
        for src, tgt in data_iter:
            count+=1
            optimizer.zero_grad()
            output=model(src.to(device))[0]
            loss=loss_f(output, tgt.to(device))
            loss.backward()
            optimizer.step()
            print_loss+=float(loss)
            if count%show_step==0:
                print('LM Training Loss: ', round(print_loss/show_step, 3))
                print_loss=0
            if count%eval_step==0:
                model.eval()
                out=model(src.to(device))[0].argmax(-1)
                print('src: ', tokenizer.decode(src[0].cpu().numpy().tolist()))
                print('tgt: ', tokenizer.decode([tgt[0].cpu().numpy().tolist()]))
                print('out: ', tokenizer.decode([out[0].cpu().numpy().tolist()]))
                model.train()
    model.eval()
    torch.save(model.state_dict(), save_pth)
    return

def eval_model(tensors, save_pth, batch_size=64):
    device=torch.device('cuda')
    tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')
    model=BertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=tokenizer.vocab_size)
    model=model.to(device)
    model.load_state_dict(torch.load(save_pth))
    model.eval()
    tensors=torch.cat(tensors, 0)
    dataset = Data.TensorDataset(tensors, tensors)
    data_iter=torch.utils.data.DataLoader(dataset, batch_size=batch_size, 
                                        shuffle=False, num_workers=4) 
    words=[]
    for src, _ in data_iter:
        output=model(src.to(device))[0].argmax(-1)
        words.append(tokenizer.decode(output.cpu().numpy().tolist(), skip_special_tokens=True))
    return words


def data_processor(pth, max_len):
    tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')
    f=open(pth)
    lines=f.readlines()
    f.close()
    tensors=[]
    for line in lines:
        if line.count("\t")==0:
            continue
        if line.split("\t")[1].count(" ") == 0:
            continue
        tensor=tokenizer.encode(line.strip().split("\t"))[:max_len]
        # tensor=tokenizer.encode(line)[:max_len]
        for _ in range(max_len-len(tensor)):
            tensor.append(0)
        tensors.append(tensor)
    return tensors # list

def mask_LM(tensors, batch_size=64):
    src=[]
    tgt=[]
    for tensor in tensors:
        length=0
        for i in tensor:
            if i !=0:
                length+=1
            else:
                break
        mask_position=random.randint(1, length-2)
        tgt.append(torch.tensor(tensor[mask_position]).unsqueeze(0))
        new_tensor=tensor.copy()
        new_tensor[mask_position]=103     # [mask]
        src.append(torch.tensor(new_tensor.copy()).unsqueeze(0))
    src=torch.cat(src, 0)
    tgt=torch.cat(tgt, 0)
    dataset = Data.TensorDataset(src, tgt)
    data_iter=torch.utils.data.DataLoader(dataset, batch_size=batch_size, 
                                        shuffle=True, num_workers=4) 
    return data_iter
def mask(tensors, masks):
    out=[]
    for i in range(len(tensors)):
        tmp=[]
        tensor=tensors[i]
        mask=masks[i]
        tmp.append(torch.tensor(tensor[:mask]).view(-1))
        tmp.append(torch.tensor([103]))
        tmp.append(torch.tensor(tensor[mask+1:]).view(-1))
        out.append(torch.cat(tmp, -1).view(1,-1).clone())
    return out

def print_masks(pth, masks):
    f=open(pth)
    lines=f.readlines()
    f.close()
    tensors=[]
    flag = 0
    for line in lines:
        if line.count(" ") == 0:
            continue
        tensors.append(line.strip().split(" ")[masks[flag]])
        flag += 1
    return tensors

def main():
    pth='word_freq'
    stop_pth='stop_words.txt'
    data_pth = "word_freq"
    BATCH_SIZE=64
    MAX_LENGTH=20
    SAVE_LM_PTH='./LM.pth'
    LM_EPOCH=10
    
    '''
    tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')
    print('Data creating.')
    tensors=data_processor(pth=pth, max_len=MAX_LENGTH)
    
    print('Training.')
    pretrain_LM(tensors, eopch_num=LM_EPOCH, batch_size=BATCH_SIZE, words_number=tokenizer.vocab_size, save_pth=SAVE_LM_PTH, show_step=20)
    ############## masks: list
    '''
    fr_stop = open(stop_pth,"r")
    list_stop = []
    for line in fr_stop:
        list_stop.append(line.strip())
    test_tensors=data_processor(pth=data_pth, max_len=MAX_LENGTH)
    masks=[]
    fr_test = open(data_pth,"r")
    list_mask = []
    label = 1
    for line in fr_test:
        if line.count("\t")==0:
            continue
        line = line.split("\t")[1].strip()
        if line.count(" ") == 0:
            continue
        try:
            list_mask.append((int(line.split("\t")[2].split(",")[-1])))
            #print(line.split("\t")[2].split(",")[0])
            #print(line)
        except:
            #continue
            list_mask.append(int("1"))
        label += 1
    fr_test.close()
    
  
    n=0
    for _ in range(len(test_tensors)):
        masks.append(list_mask[n])
        n=n+1
        
    #print((masks))

'''
    # origin_masks = print_masks(pth, list_mask)
    mask_tensors=mask(test_tensors, list_mask)
    #mask_tensors=mask(test_tensors, masks)
    predict_words=eval_model(mask_tensors, save_pth=SAVE_LM_PTH, batch_size=BATCH_SIZE)
    list_res = []
    for line in predict_words:
        list_line = line.split(" ")
        for item in list_line:
            #if(item!='"'):
                if(item.count(".")!=0):
                    num1 = item.count(".")
                    list_res.append(item.replace(".",""))
                    for i in range(num1):
                        list_res.append(".")
                else:    
                    list_res.append(item)
    dict_sub = {}
    n=0
    for line in origin_masks:
        try:
            if (list_res[n] != '"'):
                dict_sub[line] = list_res[n]
                n = n + 1
        except:
            continue
    fr_test = open(data_pth,"r")
    list_res = []
    for line in fr_test:
        if line.count("\t")==0:
            list_res.append(line.strip())
            print(line.strip())
            continue
        #print(line)
        line = line.strip()
        dict_data = eval(line.split("\t")[0])
        for key, val in dict_sub.items():  
            if(key in dict_data["text"] and key not in list_stop):
                dict_data["text"] = dict_data["text"].replace(key,val).replace("\'","").replace('\"','')
                #str_dict_dstc = str(dict_data)
        if (dict_data.__contains__("db_result") == True):
                dict_data["db_result"] = {}
        dict_data["text"] = dict_data["text"].replace("\'","").replace('\"','')
        str_dict_dstc = str(dict_data).replace("'", "\"")
        str_dict_dstc = eval(repr(str_dict_dstc).replace('\\\\', '\\')) 
        print(str_dict_dstc)
                

        # if (dict_data not in list_res):
        #    list_res.append(dict_data)
        #if (str_dict_dstc not in list_res):
        #    list_res.append(str_dict_dstc)
'''
'''

    n=0
    list111 = []
    for i in list_res:
        n = n + 1
        if (len(i)== 0):
            list111.append(i)
            continue
        dict_res = i
        if( dict_res["speaker"] == 2):
            print(i)
            if (str(list_res[n-1]).count("api_call") == 1 or ((list_res[n-1])["speaker"] == 1)):
                list111.append(i)
            else:
                continue
        else:
            list111.append(i)
    
    for item in list111:
        item = str(item).replace("'", "\"")
        item = eval(repr(item).replace('\\\\', '\\')) 
        print(item)
    return
'''
    
if __name__ == '__main__':
    main()
