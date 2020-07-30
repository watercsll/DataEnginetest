# 使用KMeans进行聚类
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

# 数据加载
data = pd.read_csv('./CarPrice_Assignment.csv', encoding='gbk')
#print(data)
'''#去除多余的car_ID以及CarName
data = data.drop(columns = ['car_ID','CarName'])'''
#print(data)
#赋值给train_X
train_x = data[["symboling","fueltype", "aspiration","doornumber","carbody","drivewheel","enginelocation","wheelbase","carlength","carwidth","carheight","curbweight","enginetype","cylindernumber","enginesize","fuelsystem","boreratio","stroke","compressionratio","horsepower","peakrpm","citympg","highwaympg","price"]]
#print(train_x)
# 使用LabelEncoder将字符数据转化为数值
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
#设置循环
column_name = 'symboling','fueltype','aspiration','doornumber','carbody','drivewheel','enginelocation','enginetype','cylindernumber','fuelsystem'
#print(column_name)
for i in range(len(column_name)):
    train_x[column_name[i]] = le.fit_transform(train_x[column_name[i]])
    i = i+1
#print(train_x)

# 规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
pd.DataFrame(train_x).to_csv('temp.csv', index=False)
#print(train_x)


#使用KMeans聚类,通过如下手肘法测定，同时参考层次聚类的图像结果，K值最终设定为：K = 4
kmeans = KMeans(n_clusters=4)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
print(result)
# 将结果导出到CSV文件中
result.to_csv("car_cluster_result.csv",index=False)


# K-Means 手肘法大致判断 K=5左右时为拐点，故4-6均比较合适，然后使用如下层次聚类绘图看趋势
import matplotlib.pyplot as plt
sse = []
for k in range(1, 50):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 50)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()


# 使用层次聚类，发现层次聚类中分成了4个明显的大类，故取用K = 4更合适
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
model = AgglomerativeClustering(linkage='ward', n_clusters=4)
y = model.fit_predict(train_x)
print(y)

linkage_matrix = ward(train_x)
dendrogram(linkage_matrix)
plt.show()
