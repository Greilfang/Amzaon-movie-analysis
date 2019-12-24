import pandas as pd
import json
import time
import os
from collections import Counter

cid = 0
sum=0
symbol = 0
image_path ="cnt"

#电影节点
prid=[]
tit=[]
intr=[]
imb=[]
scco=[]
ye=[]
emoti=[]


#评论节点 以及评论和电影的关系
commenid=[]
commenid_r=[]
usname=[]
ti=[]
summar=[]
te=[]
scor=[]
helpf=[]
emo=[]
prodid=[]

#类型节点 以及类型和电影关系
ty=[]
tmid=[]
#导演节点 以及导演和电影关系
direc=[]
direcmid=[]

#演员节点 以及演员和电影关系
acto=[]
actomid=[]
isS=[]

#演员和演员的合作关系
acooperations=[]
#导演和演员的合作关系
dcooperations=[]

#版本
version_dict = dict()

for root, dirs, files in os.walk(image_path):
    for file in files:
        actor_list = []
        director_list = []
        symbol = symbol + 1
        print(str(symbol) + "  " + file)
        with open('cnt/'+ file, 'r')as file_open:
            data = json.load(file_open)

            #建立电影节点
            try:
                x = data["Emotion"]
            except:
                x = 0.5
            prid.append(data["ID"])
            tit.append(data["Title"])
            intr.append(data["Intro"])
            imb.append(data["IMDB"])
            scco.append(data["Score"])
            ye.append(data["Year"])
            emoti.append(x)

            #建立评论节点/与电影关系
            for re in data["Reviews"]:
                prodid.append(data["ID"])
                commenid.append(cid)
                commenid_r.append(cid)

                if re["Moment"]["Year"] == -1:
                    timestr = str(2019) + "-" + str(1) + "-" + str(1)
                else:
                    timestr = str(re["Moment"]["Year"]) + "-" + str(re["Moment"]["Month"]) + "-" + str(
                        re["Moment"]["Day"])
                strptime = time.strptime(timestr, "%Y-%m-%d")
                ctime = int(time.mktime(strptime))
                try:
                    x = re["Emotion"]
                except:
                    x = 0.5
                usname.append(re["Profile"])
                ti.append(ctime)
                summar.append(re["Summary"])
                te.append(re["Text"])
                scor.append(re["Score"])
                helpf.append(re["Helpful"])
                emo.append(x)
                cid=cid+1

            # 建立类型节点/与类型关系
            for gt in data["Genre"]:
                ty.append(gt)
                tmid.append(data["ID"])

            # 建立导演节点/导演电影关系
            for dt in data["Director"]:
                direc.append(dt)
                direcmid.append(data["ID"])

            # 建立演员节点/演员电影关系
            for ac in data["Starring"]:
                acto.append(ac)
                actomid.append(data["ID"])
                isS.append(True)

            if data["Supporting"]:
                for sac in data["Supporting"]:
                    acto.append(sac)
                    actomid.append(data["ID"])
                    isS.append(False)

            #演员之间合作关系/导演演员合作关系
            if 'Starring' in data and data['Starring']:
                for star in data['Starring']:
                    actor_list.append(star)
            if 'Supporting' in data and data['Supporting']:
                for support in data['Supporting']:
                    actor_list.append(support)

            if 'Director' in data and data['Director']:
                for di in data['Director']:
                    director_list.append(di)

            director_list = sorted(director_list)
            actor_list = sorted(actor_list)
            length = len(actor_list)
            for i in range(0, length):
                for j in range(i + 1, length):
                    acooperations.append((actor_list[i], actor_list[j]))
                for d in director_list:
                    dcooperations.append((d,actor_list[i]))

            #版本初步建立
            title = data['Title']
            if title not in version_dict:
                version_dict[title] = list()
            version_dict[title].append(data['ID'])

        file_open.close()
        if symbol==100000:


            xmovie_has_comment = {'ProductId': prodid, 'CommentId': commenid_r}

            movie_has_comment = pd.DataFrame(xmovie_has_comment, columns=['ProductId', 'CommentId'])

            movie_has_comment.to_csv(path_or_buf='csvfile/movie_has_comment1.csv', header=True, index=False)

            commenid_r = []
            prodid = []

acooperations = Counter(acooperations).items()
dcooperations = Counter(dcooperations).items()


xmovie={'ProductId':prid,
        'Title': tit,
        'Intro': intr,
        'IMDB': imb,
        'Score': scco,
        'Year': ye,
        'Emotion': emoti}
xmovie_has_comment={'ProductId':prodid,'CommentId':commenid_r}
xcomment={'CommentId':commenid,
         'Username':usname,
         'Time':ti,
         'Summary':summar,
         'Text':te,
         'Score':scor,
         'Helpful':helpf,
         'Emotion':emo}
xtype={'Genre':ty}
xtype_has_movie={'Genre':ty,'ProductId':tmid}
xdirector={'Name':direc}
xactor={'Name':acto}
xdirect_movie={'Name':direc,'ProductId':direcmid}
xact_movie={'Name':acto,'ProductId':actomid,'IsStar':isS}

version_frame = []
count = 0
for name in version_dict.keys():
    if count % 1000 == 0:
        print("{} names finished".format(count))
    count = count + 1
    if len(version_dict[name]) == 1:continue
    for i in range(len(version_dict[name])-1):
        version_frame.append([version_dict[name][i],version_dict[name][i+1]])
    version_frame.append([version_dict[name][-1],version_dict[name][0]])


movie = pd.DataFrame(xmovie,columns=['ProductId', 'Title', 'Intro', 'IMDB', 'Score', 'Year', 'Emotion'])
movie_has_comment = pd.DataFrame(xmovie_has_comment,columns=['ProductId', 'CommentId'])
comment = pd.DataFrame(xcomment,columns=['CommentId', 'Username', 'Time', 'Summary', 'Text', 'Score', 'Helpful','Emotion'])
type = pd.DataFrame(xtype,columns=['Genre'])
type_has_movie = pd.DataFrame(xtype_has_movie,columns=['Genre', 'ProductId'])
director = pd.DataFrame(xdirector,columns=['Name'])
actor = pd.DataFrame(xactor,columns=['Name'])
direct_movie = pd.DataFrame(xdirect_movie,columns=['Name', 'ProductId'])
act_movie = pd.DataFrame(xact_movie,columns=['Name', 'ProductId', 'IsStar'])
actor_coop_actor = pd.DataFrame(columns=['ANameA', 'ANameB', 'Times'])
direct_coop_actor = pd.DataFrame(columns=['DName', 'AName', 'Times'])
version_df = pd.DataFrame(version_frame,columns=["Name_1","Name_2"])

count = 0
for coop in acooperations:
    actor_coop_actor.loc[count]=[coop[0][0],coop[0][1],coop[1]]
    count = count+1
    print(count)
count = 0
for coop in dcooperations:
    direct_coop_actor.loc[count]=[coop[0][0],coop[0][1],coop[1]]
    count = count+1
    print(count)

type=type.drop_duplicates(['Genre'])
director=director.drop_duplicates(['Name'])
actor=actor.drop_duplicates(['Name'])

movie.to_csv(path_or_buf='csvfile/movie.csv', header=True, index=False)
movie_has_comment.to_csv(path_or_buf='csvfile/movie_has_comment2.csv', header=True, index=False)
comment.to_csv(path_or_buf='csvfile/comment.csv', header=True,index=False)
type.to_csv(path_or_buf='csvfile/type.csv', header=True, index=False)
type_has_movie.to_csv(path_or_buf='csvfile/type_has_movie.csv', header=True, index=False)
director.to_csv(path_or_buf='csvfile/director.csv', header=True,index=False)
actor.to_csv(path_or_buf='csvfile/actor.csv', header=True, index=False)
direct_movie.to_csv(path_or_buf='csvfile/direct_movie.csv', header=True, index=False)
act_movie.to_csv(path_or_buf='csvfile/act_movie.csv', header=True, index=False)
actor_coop_actor.to_csv('csvfile/actor_to_actor.csv')
direct_coop_actor.to_csv('csvfile/direct_coop_actor.csv')
version_df.to_csv('csvfile/version.csv')