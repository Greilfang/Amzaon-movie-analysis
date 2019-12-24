import pymongo
import os
import json
import keras
import re
import numpy as np
from keras.preprocessing import text
from keras.preprocessing import sequence
from keras.utils import plot_model

Reg = re.compile(r'[A-Za-z]*')
stop_words = ['is','the','a']

max_features = 5000
word_embedding_size = 50
maxlen = 400
filters = 250
kernel_size = 3
hidden_dims = 250

def gen_predict_data(token,content):
    sent = prepross(content)
    #print('sent:',sent)
    x = token.texts_to_sequences([sent])
    x = sequence.pad_sequences(x,maxlen=maxlen)
    return x

def imdb_load(path):
    root_path = "./"
    # 遍历所有文件
    file_lists = []
    pos_path = root_path + path + "/pos/"
    for f in os.listdir(pos_path):
        file_lists.append(pos_path + f)
    neg_path = root_path + path + "/neg/"
    for f in os.listdir(neg_path):
        file_lists.append(neg_path + f)
    # file_lists中前12500个为pos，后面为neg，labels与其保持一致
    labels = [1 for i in range(12500)]
    labels.extend([0 for i in range(12500)])
    # 将文件随机打乱，注意file与label打乱后依旧要通过下标一一对应。
    # 否则会导致 file与label不一致
    index = np.arange(len(labels))
    np.random.shuffle(index)
    # 转化为numpy格式
    labels = np.array(labels)
    file_lists = np.array(file_lists)
    labels[index]
    file_lists[index]
    # 逐个处理文件
    sentenses = []
    for file in file_lists:
        sentenses.append(fprepross(file))
    return sentenses,labels

def fprepross(file):
    with open(file,encoding='utf-8') as f:
        data = f.readlines()
        data = Reg.findall(data[0])
        # 将句子中的每个单词转化为小写
        data = [x.lower() for x in data]
        # 将句子中的部分词从停用词表中剔除
        data = [x for x in data if x!='' and x not in stop_words]
        # 返回值必须是个句子，不能是单词列表
        return ' '.join(data)

def prepross(content):
    #content = Reg.findall(content[0])
    # 将句子中的每个单词转化为小写
    content = content.lower()
    # 将句子中的部分词从停用词表中剔除
    content = [x for x in content.split() if x!='' and x not in stop_words]
    # 返回值必须是个句子，不能是单词列表
    return ' '.join(content)


class ReviewHandler():
    def __init__(self,addr='localhost',port=27017,base_name='Amazon-Movie'):
        self.client = pymongo.MongoClient(addr,port)
        self.database = self.client[base_name]
    
    def insertOneReview(self,collection_name,review):
        collection=self.database[collection_name]
        collection.insert_one(review)

    def insertManyReviews(self,collection_name,reviews):
        collection=self.database[collection_name]
        collection.insert_many(reviews)
    
    def loadDatas(self,collection_name):
        collection=self.database[collection_name]
        names=os.listdir('cnt_1')
        #print(names)
        #载入模型
        model=keras.models.load_model('demo_imdb_rnn.h5')
        #获得词向量
        x_train,t_train = imdb_load("train")
        #print('x_train:',x_train)
        token = text.Tokenizer(num_words=max_features)
        token.fit_on_texts(x_train)
        
        count=0
        for name in names:
            sum_emotion=0
            count=count+1
            if count%1000==0:
                print(count,' changed')
            print(name)
            with open('./cnt_1/'+name,'r') as f:
                data=json.load(f)
                #reviews=data['Reviews']
                for review in data['Reviews']:
                    content=' '
                    if review['Summary']:
                        content=review['Summary']+content
                    if review['Text']:
                        content=content+review['Text']
                    x_predict=gen_predict_data(token=token,content=content)
                    review['Emotion']=model.predict(x_predict)[0][0].astype('float')
                    review['Emotion']=round(review['Emotion'],2)
                    sum_emotion=sum_emotion+review['Emotion']
                if len(data['Reviews']):
                    data['Emotion']=sum_emotion/len(data['Reviews'])
                    data['Emotion']=round(data['Emotion'],2)
                with open('./new_cnt_1/'+name,'w') as f2:
                    json.dump(data,f2)

                    #review['ProductId']=data['ID']
                    #review['Title']=data['Title']
                    #collection.insert_one(review)

if __name__ == "__main__":
    st = ReviewHandler(addr='localhost',port=27017,base_name='Amazon-Movie')
    st.loadDatas('Review')
