# -*- coding: utf-8 -*-
import re
import os
import csv
from Support import *
from imp import reload

import sys
reload(sys)
#sys.setdefaultencoding('utf-8')

def writeReview(products, i):
    csvfile = open('csv/reviews_' + str(i) + '.csv', 'w',encoding='utf-8',newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['ProductId', 'UserId', 'ProfileName', 'Helpfulness', 'Score', 'Time', 'Summary', 'Text'])
    #写入影评数据到csv文件当中
    try:
        writer.writerows(products)
    except:
        print('errors happen!')
        print(products)


def wrilteId(productsId, j):
    productsId = list(productsId)
    csvfile = open('productId_' + str(j) + '.csv', 'w',encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(['ProductId'])
    for i in range(len(productsId)):
        writer.writerow([productsId[i]])
    print(str(len(productsId)) + " product Id get!")
    csvfile.close()

# 清除一些出错的影评数据
def errorData():
    fe = open('error/dislocation_error.txt','w', encoding='utf-8')
    fn = open('new_movies.txt','w',encoding='utf-8')
    count = 0
    tmp = ""
    with open('movies.txt', 'r',encoding='utf-8',errors='ignore') as fo:
        for index,line in enumerate(fo):
            print('line:',index)
            count += 1
            if line == '\n':
                fn.write(line)
                continue
            if len(re.findall(pattern=dislocationPattern, string=line)) == 0:
                error = "error_" + str(count)
                print(error)
                fe.write(error + " | " + tmp + " | " + line + "\n")
                print(tmp + " | " + line)

            else:
                tmp = line
                fn.write(line)
        print('total index:',index)

    fn.close()
    fo.close()
    fe.close()


def run():
    fe = open('error/error.txt', 'w')
    ind = 1
    product = []
    products = []
    #用于记录出现了几部不同的电影数
    productsId = set()
    review_count = 0
    line_count = 0
    with open('new_movies.txt', 'r',encoding='utf-8') as f:
        for line in f:
            line_count += 1
            if line != '\n' and line[-1]=='\n':
                product.append(line.strip('\n'))
                
            # 以空行为分割
            if (line=='\n'):
                if len(product)<8:
                    continue
                review_count=review_count+1
                try:
                    #在每一条影评记录中寻找信息
                    productId = re.findall(pattern=productIdPattern, string=product[0])[0].strip(' ')
                    userId = re.findall(pattern=userIdPattern, string=product[1])[0].strip(' ')
                    profileName = re.findall(pattern=profileNameParttern, string=product[2])[0]
                    # delete useless information
                    index = profileName.find("\"")
                    profileName = profileName[:index-1]
                    helpfulness = re.findall(pattern=helpfulnessParttern, string=product[3])[0].strip(' ')
                    helpfulness = helpfulness.replace('/',',')
                    score = re.findall(pattern=scoreParttern, string=product[4])[0].strip(' ')
                    time = re.findall(pattern=timeParttern, string=product[5])[0].strip(' ')
                    summary = re.findall(pattern=summaryParttern, string=product[6])[0]
                    text = re.findall(pattern=textParttern, string=product[7])[0]
                    product_tuple = (productId, userId, profileName, helpfulness, score, time, summary, text)
                    products.append(product_tuple)
                    product = []
                    productsId.add(productId)
                except:
                    print('error_' + str(line_count))
                    fe.write('error_' + str(review_count)+'\n')
                    fe.write(productId+'\n')
                    fe.write(userId+'\n')
                    fe.write(profileName+'\n')
                    fe.write(helpfulness+'\n')
                    fe.write(score+'\n')
                    fe.write(time+'\n')
                    fe.write(summary+'\n')
                    fe.write(text + '\n')
            
            if (review_count / 100000 == ind):
                writeReview(products, ind)
                products = []
                ind += 1
                print(str(review_count) + " reviews have been handled!")

    writeReview(products, ind)
    print(product)
    print(str(review_count) + " reviews have been handled!")
    f.close()
    fe.close()
    wrilteId(productsId, 0)


if __name__ == '__main__':
    #errorData()
    run()