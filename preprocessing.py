import os
from os import listdir
from os.path import isfile, join
import natsort, csv

import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize th  e histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    r=[]
    g=[]
    b=[]
    p=[]
    s=[]
    v=[]

    # loop over the percentage of each cluster and the color of each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

        p.append(percent) #Percent
        r.append(color[0]) #R
        g.append(color[1]) #G
        b.append(color[2]) #B
        s.append(colorsys.rgb_to_hsv(color[0], color[1], color[2])[1]) #채도
        v.append(colorsys.rgb_to_hsv(color[0], color[1], color[2])[2]) #명도

    # 평균 R 구하기 (가중치 부여) -----------------------------------
    r_sum = 0
    for i in range(0, k) :
        r_sum += r[i] * p[i]
    r_avg = r_sum / k

    # 평균 G 구하기 (가중치 부여) -----------------------------------
    g_sum = 0
    for i in range(0, k):
        g_sum += g[i] * p[i]
    g_avg = g_sum / k

    # 평균 B 구하기 (가중치 부여) -----------------------------------
    b_sum = 0
    for i in range(0, k):
        b_sum += b[i] * p[i]
    b_avg = b_sum / k

    # 색분산 구하기 -----------------------------------
    dt = []
    for i in range(0, k) :
        deviation = ((r[i] - r_avg)**2 + (g[i] - g_avg)**2 + (b[i] - b_avg)**2)**(1/2)
        dt.append(deviation)
    dt_n = np.array(dt)
    final_dt = np.var(dt_n) #색분산

    # 채도 배색 조화도 구하기 -----------------------------------
    s_sum = 0
    for i in range(0, k):
        s_sum += s[i] * p[i]
    s_avg = s_sum / k # 채도 평균 구하기 (가중치 부여)

    ss = 0
    for i in range(0,k):
        ss += (s[i] - s_avg)**2
    final_s = ss / k # 채도 분산 구하기

    # 명도 배색 조화도 구하기 -----------------------------------
    v_sum = 0
    for i in range(0, k):
        v_sum += v[i] * p[i]
    v_avg = v_sum / k  # 명도 평균 구하기 (가중치 부여)

    vv = 0
    for i in range(0, k):
        vv += (v[i] - v_avg) ** 2
    final_v = vv / k  # 명도 분산 구하기


    print("평균 R:", r_avg)
    print("평균 G:", g_avg)
    print("평균 B:", b_avg)
    print("색 분산: ", final_dt)
    print("명도 분산:", final_v)
    print("채도 분산: ", final_s)

    with open('../output.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[img_name, r_avg, g_avg, b_avg, final_dt, final_v, final_s]])


    # return the bar chart
    return bar

img_folder = './images'
img_files = [f for f in listdir(img_folder) if isfile(join(img_folder, f))]
img_files = natsort.natsorted(img_files, reverse=False)

print(img_files)

for img_name in img_files :
    os.chdir(img_folder)
    print(img_name)
    image = cv2.imread(img_name, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    print(image.shape)

    k = 5
    clt = KMeans(n_clusters=k)
    clt.fit(image)

    hist = centroid_histogram(clt)

    bar = plot_colors(hist, clt.cluster_centers_)

    fname, ext = os.path.splitext(img_name)

    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    os.chdir('../colorSpectrum')
    plt.savefig(fname+".png")
    os.chdir('../')

#plt.show()