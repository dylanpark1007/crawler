size = input()
size = int(size)

def process_input(size):
    input_list = []
    cnt = 0
    input_list.append(0)
    while cnt<size:
        buffer = int(input())
        input_list.append(buffer)
        cnt+=1
    return input_list



def cut_rod(input_list, size):
  original_list = [0 for _ in range(size+1)]
  mod_list = [0 for _ in range(size+1)]
  for idx in range(1,size+1):
    hyper = -100
    for idx_idx in range(1,idx+1):
      if input_list[idx_idx]+original_list[idx - idx_idx] >= hyper:
        hyper = max(hyper, input_list[idx_idx] + original_list[idx - idx_idx])
        mod_list[idx] = idx_idx
    if hyper > 0:
      original_list[idx] = hyper
  return original_list, mod_list


Original_List, Mod_List = cut_rod(process_input(size), size)

num = size
output_list = []

while num > 0:
  output_list.append(Mod_List[num])
  num = num - Mod_List[num]

print('%d' % Original_List[size])

for idx in reversed(range(int(len(output_list)))):
  print('%d' % output_list[idx])








import pickle
with open('C:/Users/dilab/PycharmProjects/crawler-cqa/ag_test_result_2.bin','rb') as f:
    t = pickle.load(f)




with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/ag_news_train.txt','w') as f1:
    for idx, i in enumerate(t):
        c_list = []
        text = i[0]
        text = text.strip()
        f1.write(text)
        f1.write('\n')

with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/c1_ag_news_train.txt','w') as f2:
    for idx, i in enumerate(t):
        c_list = []
        for cnt, k in enumerate(i[1]):
            c_list.append(str(k[1]))
            if cnt == 0:
                f2.write((' ').join(c_list))
                f2.write('\n')


with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/c3_ag_news_train.txt','w') as f3:
    for idx, i in enumerate(t):
        c_list = []
        for cnt, k in enumerate(i[1]):
            c_list.append(str(k[1]))
            if cnt == 2:
                f3.write((' ').join(c_list))
                f3.write('\n')

with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/c5_ag_news_train.txt','w') as f4:
    for idx, i in enumerate(t):
        c_list = []
        for cnt, k in enumerate(i[1]):
            c_list.append(str(k[1]))
            if cnt == 4:
                f4.write((' ').join(c_list))
                f4.write('\n')

with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/c7_ag_news_train.txt','w') as f5:
    for idx, i in enumerate(t):
        c_list = []
        for cnt, k in enumerate(i[1]):
            c_list.append(str(k[1]))
            if cnt == 6:
                f5.write((' ').join(c_list))
                f5.write('\n')


with open('C:/Users/dilab/PycharmProjects/crawler-cqa/data/c9_ag_news_train.txt','w') as f6:
    for idx, i in enumerate(t):
        c_list = []
        for cnt, k in enumerate(i[1]):
            c_list.append(str(k[1]))
            if cnt == 8:
                f6.write((' ').join(c_list))
                f6.write('\n')



ctgr_list = []
for idx,i in enumerate(t):
    c_list = []
    text = i[0]
    text = text.strip()
    f1.write(text)
    f1.write('\n')
    print(text)
    print(idx)
    for cnt, k in enumerate(i[1]):
        c_list.append(str(k[1]))
        ctgr_list.append(k[1])
        if cnt == 0:
            f2.write((' ').join(c_list))
            f2.write('\n')
        if cnt == 2:
            f3.write((' ').join(c_list))
            f3.write('\n')
        if cnt == 4:
            f4.write((' ').join(c_list))
            f4.write('\n')
        if cnt == 6:
            f5.write((' ').join(c_list))
            f5.write('\n')
        if cnt == 8:
            f6.write((' ').join(c_list))
            f6.write('\n')
