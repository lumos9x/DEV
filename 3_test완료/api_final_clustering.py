
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


data = pd.read_csv("total.csv", encoding = 'CP949')
data.head()


# In[4]:


data = data.drop(['Unnamed: 0'], 1)
data.head()


# In[5]:


data = data.drop_duplicates(["명칭"])
data.head()


# In[6]:


data = data.reset_index(drop= True)
data.head()


# In[7]:


light_data = pd.DataFrame(columns=['feature_ID', '밝기', '분류', '명칭', '위도', '경도'])

### 시설물에 밝기 점수 주기
for i in range(len(data)) :
    score = 0 
    if data['분류'][i] == '파출소' :
        score += 25.471
    elif data['분류'][i] == '보안등' :    
        score += 21.774
    elif data['분류'][i] == '편의점' :    
        score += 24.357
    else :    
        score += 28.397
        
    tmp = {'feature_ID' : 'Point_%d' % i, 
           '밝기' : score, 
           '분류' :data.loc[i,'분류'], '명칭' : data.loc[i,'명칭'], 
           '위도' : data.loc[i,'위도'], '경도' : data.loc[i,'경도'] 
           } 
    light_data = light_data.append(light_data.from_dict(tmp, orient = 'index').T)

light_data.reset_index(inplace=True,drop=True)
#light_data   # 1722 rows × 6 columns
light_data.head()


# In[10]:


light_data1 = data[['위도','경도']]
light_data1.head()


# In[50]:


#light_data2 = light_data[['밝기']]
#light_data2.head()
light_data_r = pd.DataFrame()
light_data_r['위도'] = light_data1['위도']
light_data_r['경도'] = light_data1['경도']
light_data_r['lux'] = light_data2['밝기']
light_data_r


# In[34]:


#light_data_r_copy = light_data_r.copy(deep = False)
#light_data_r['경도'] = light_data_r['경도'].apply(lambda x : x/4)


# In[51]:


light_data_r.head()


# In[53]:


feature = light_data_r[['위도', '경도', 'lux']]
feature = feature.rename(columns={'위도': 'lat', '경도' :'lon'})


# In[54]:


feature.head()


# In[56]:


lat = pd.qcut(feature.lat, 3)
#lon = pd.qcut(feature.lon, 3) ##그냥 위도만 나누자


# In[57]:


lat


# In[58]:


from sklearn.cluster import KMeans


# In[59]:


import seaborn as sns


# In[88]:


df1 = feature[feature.lat <=37.498]
df1 = df1.reset_index(drop = True)
df1['lon'] = df1['lon'].apply(lambda x: x/4)
df1


# In[89]:


df2 = feature[(37.498 < feature.lat) &  (feature.lat<=37.504)]
df2 = df2.reset_index(drop = True)
df2['lon'] = df2['lon'].apply(lambda x: x/4)
df2


# In[90]:


df3 = feature[(37.504 < feature.lat)]
df3 = df3.reset_index(drop = True)
df3['lon'] = df3['lon'].apply(lambda x: x/4)
df3


# In[92]:


df11 = df1.drop(['lux'],1)
df21 = df2.drop(['lux'],1)
df31 = df3.drop(['lux'],1)


# In[93]:


data_points = df11.values
kmeans = KMeans(n_clusters=3).fit(data_points)
kmeans.labels_
df11['cluster_id'] = kmeans.labels_
df11


# In[95]:


sns.lmplot('lat', 'lon', data = df11, fit_reg=False,
          scatter_kws = {"s": 10},
          hue = "cluster_id")
plt.title('kmeans plot df11')


# In[118]:


#list1 =kmeans.cluster_centers_.tolist()
#list1
df111 = pd.DataFrame({'lat': [37.494092572454164, 37.49139403233431, 37.496639234692886], 'lon': [31.759175225171298, 31.758715076080883, 31.75881450409]})
df111


# In[122]:



import folium
from haversine import haversine


# In[209]:


maxValues = [float(0),float(0),float(0)]
maxCoord = pd.DataFrame(columns = ['lat','lon','lux'])

for i in range(len(df111)) :
    s_point = (df111.loc[i,'lat'], df111.loc[i,'lon']) # 시작점
    for n in range(len(df1)) :
        t_point = (df1.loc[n,'lat'], df1.loc[n,'lon']) # 타겟
        d_m = haversine(s_point, t_point, unit='m') #  시작점과 타겟의 거리  단위 미터
        # 반경 10M 를 범위로 잡음
        if d_m <= 20 :
            if (maxValues[i] < df1.lux.max()) :
                maxValues[i] =  df1.lux.max()
            if(df1.loc[n,'lux'] == 28.397):
                maxCoord.loc[n,'lat'] = df1.loc[n,'lat']
                maxCoord.loc[n,'lon'] = df1.loc[n,'lon']
                maxCoord.loc[n,'lux'] = df1.loc[n,'lux']
                
print(maxCoord)


# In[210]:


maxCoord = maxCoord.reset_index(drop = True)
maxCoord


# In[201]:


data_points = df21.values
kmeans = KMeans(n_clusters=3).fit(data_points)
kmeans.labels_
df21['cluster_id'] = kmeans.labels_
df21


# In[202]:


sns.lmplot('lat', 'lon', data = df21, fit_reg=False,
          scatter_kws = {"s": 10},
          hue = "cluster_id")
plt.title('kmeans plot df21')


# In[203]:


kmeans.cluster_centers_


# In[204]:


df222 = pd.DataFrame({'lat': [37.50250453, 37.49957123, 37.50276726], 'lon': [31.75757852, 31.75857058, 31.75998485]})
df222


# In[205]:


maxValues2 = [float(0),float(0),float(0)]
maxCoord2 = pd.DataFrame(columns = ['lat','lon','lux'])

for i in range(len(df222)) :
    s_point = (df222.loc[i,'lat'], df222.loc[i,'lon']) # 시작점
    for n in range(len(df2)) :
        t_point = (df2.loc[n,'lat'], df2.loc[n,'lon']) # 타겟
        d_m = haversine(s_point, t_point, unit='m') #  시작점과 타겟의 거리  단위 미터
        # 반경 50M 를 범위로 잡음
        if d_m <= 50 :
            if (maxValues2[i] < df2.lux.max()) :
                maxValues2[i] =  df2.lux.max()
            if(df2.loc[n,'lux'] == 28.397):
                maxCoord2.loc[n,'lat'] = df2.loc[n,'lat']
                maxCoord2.loc[n,'lon'] = df2.loc[n,'lon']
                maxCoord2.loc[n,'lux'] = df2.loc[n,'lux']

print(maxCoord2)


# In[206]:


maxCoord2 = maxCoord2.reset_index(drop = True)
maxCoord2


# In[183]:


data_points = df31.values
kmeans = KMeans(n_clusters=3).fit(data_points)
kmeans.labels_
df31['cluster_id'] = kmeans.labels_
df31


# In[184]:


sns.lmplot('lat', 'lon', data = df31, fit_reg=False,
          scatter_kws = {"s": 10},
          hue = "cluster_id")
plt.title('kmeans plot df31')


# In[185]:


kmeans.cluster_centers_


# In[186]:


df333 = pd.DataFrame({'lat': [37.5051841, 37.50540407, 37.50795173], 'lon': [31.75819295, 31.76068225, 31.76031079]})
df333


# In[213]:


maxValues3 = [float(0),float(0),float(0)]
maxCoord3 = pd.DataFrame(columns = ['lat','lon','lux'])

for i in range(len(df333)) :
    s_point = (df333.loc[i,'lat'], df333.loc[i,'lon']) # 시작점
    for n in range(len(df3)) :
        t_point = (df3.loc[n,'lat'], df3.loc[n,'lon']) # 타겟
        d_m = haversine(s_point, t_point, unit='m') #  시작점과 타겟의 거리  단위 미터
        # 반경 20M 를 범위로 잡음
        if d_m <= 40 :
            if (maxValues3[i] < df3.lux.max()) :
                maxValues3[i] =  df3.lux.max()
            if(df3.loc[n,'lux'] == 28.397):
                maxCoord3.loc[n,'lat'] = df3.loc[n,'lat']
                maxCoord3.loc[n,'lon'] = df3.loc[n,'lon']
                maxCoord3.loc[n,'lux'] = df3.loc[n,'lux']

print(maxCoord3)


# In[214]:


maxCoord3 = maxCoord3.reset_index(drop = True)
maxCoord3


# In[215]:


#maxCoord['lon'] = maxCoord['lon'].apply(lambda x: x*4)
#maxCoord2['lon'] = maxCoord2['lon'].apply(lambda x: x*4)
maxCoord3['lon'] = maxCoord3['lon'].apply(lambda x: x*4)


# In[217]:


#print(maxCoord)
print(maxCoord2)
print(maxCoord3)


# In[36]:


from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns


# In[76]:


model = DBSCAN(min_samples=6)
predict = pd.DataFrame(model.fit_predict(feature))
predict.columns = ['predict']


# In[47]:


r = pd.concat([feature,predict], axis = 1)


# In[41]:


from mpl_toolkits.mplot3d import Axes3D


# In[49]:


fig = plt.figure(figsize=(6,6))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev = 48, azim = 134)
ax.scatter(r['lat'], r['lon'], r['lux'], c=r['predict'], alpha = 0.5)
ax.set_xlabel('lat')
ax.set_ylabel('lon')
ax.set_zlabel('lux')
plt.show()


# In[ ]:


df1 = 

