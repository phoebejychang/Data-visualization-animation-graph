import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
from pandas_datareader import wb

data = wb.download(country = ['USA','CN'], indicator = 'NY.GDP.MKTP.CD', start = 1960, end = 2017)
data = data.reset_index()
data.iloc[:,2] = data.iloc[:,2] / 1000000000000
china = data[data.country == 'China']
usa = data[data.country != 'China']
fig, ax = plt.subplots()
x = np.linspace(1960, 2017, 229)
y_china = np.array([np.nan]*229)
y_usa = np.array([np.nan]*229)
for i in range(58):
    y_china[i*4] = china.iloc[i,2]
    try:
        beta = (china.iloc[i+1,2] - china.iloc[i,2]) / 4
        y_china[i*4+1] = y_china[i*4] + beta
        y_china[i*4+2] = y_china[i*4+1] + beta
        y_china[i*4+3] = y_china[i*4+2] + beta 
    except:
        'hahaha'
    y_usa[i*4] = usa.iloc[i,2]
    try:
        beta = (usa.iloc[i+1,2] - usa.iloc[i,2]) / 4
        y_usa[i*4+1] = y_usa[i*4] + beta
        y_usa[i*4+2] = y_usa[i*4+1] + beta
        y_usa[i*4+3] = y_usa[i*4+2] + beta  
    except:
        'h'
y_china = y_china[::-1]
y_usa = y_usa[::-1]
def make_frame(t):
    ax.clear()
    y_c = np.array([np.nan]*229)
    y_u = np.array([np.nan]*229)
    t = int(np.floor(t/0.05))
    y_c[:t] = y_china[:t]
    y_u[:t] = y_usa[:t]
    ax.plot(x, y_c, lw=3)
    ax.set_xlabel('year')
    ax.set_ylabel('$')
    ax.set_title('GDP')
    ax.text(1970,23,'USA: ' + str(np.round(y_u[t-1:t],2)) + 'trillion')
    ax.text(1970,20,'China: ' + str(np.round(y_c[t-1:t],2)) + 'trillion')
    ax.plot(x, y_u, lw=3)
    ax.legend(['China','USA'])
    ax.set_xlim(1959, 2018)
    ax.set_ylim(0,np.ceil(max(y_usa + y_china) + 1))
    ax.set_xticks(list(range(1960,2018,10)))
    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration=11)
animation.write_gif('matplotlib.gif', fps=20)