# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com

import numpy as np

# Convert from world coordinate system to screen coordinates,
# pay attention to the incoming row vector
def worldCoord2ScreenCoord(worldCoord,screenSize, res):
    wc = np.append(worldCoord,1.0)
    # To flip the y-axis
    mirrorMat = np.matrix([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])
    scaleMat = np.matrix([
        [res,0.0,0.0],
        [0.0,res,0.0],
        [0.0,0.0,1.0]
    ])
    transMat = np.matrix([
        [1.0,0.0,0.0],
        [0.0,1.0,0.0],
        [0.0,screenSize[1],1.0]
    ])
    result = wc*scaleMat*mirrorMat*transMat
    return np.array(np.round(result.tolist()[0][:2]),dtype= np.int64)


def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):
    return np.max(x, 0)   # Keep compatiable with numpy in 1.14.0 version


#Calculate the distance from the point to the line segment, and calculate the unit vector from the point to the intersection with the line segment

def distanceP2W(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    ymp0 = point-p0
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        cross = p0 + t*d
    elif t >= 1.0:
        ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        cross = p0 + t*d
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    return dist,npw

def distanceP2O(point, obs):
    p0 = np.array([obs[0],obs[1]])
    dist = np.linalg.norm (p0-point)
    npo = normalize(p0-point)
    return dist,npo

if __name__ == '__main__':
    # v1 = np.array([3.33,3.33])
    # print(worldCoord2ScreenCoord(v1, [1000,800],30))
    # v2 = np.array([23.31,3.33])
    # print(worldCoord2ScreenCoord(v2,[1000,800] ,30))
    # v3 = np.array([29.97,23.31])
    # print(worldCoord2ScreenCoord(v3, [1000,800],30))
    wall = [3.33, 3.33, 29.97, 3.33]
    print (distanceP2W(np.array([10.0,10.0]),wall))
    # print distanceP2W(np.array([0.5,2.0]),wall)
    # print distanceP2W(np.array([2.0,2.0]),wall)
