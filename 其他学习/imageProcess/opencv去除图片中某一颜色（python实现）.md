# opencv去除图片中某一颜色（python实现）

### 一 打开图片
打开图片的时候最好使用windows自带的“画图”软件查看（在画图软件下通过句柄精灵获得点的RGB值与opencv中获得的是一样的），在“画图”的左下角可以看到图像中某个点的坐标值如（344,123），如果要在opencv中处理该点的话，需要把坐标值反一下即 img[123, 344]才能取得该点
![image-20211030103141646](https://img-blog.csdnimg.cn/img_convert/67ebf65fab8d39a10ad18055650b7772.png)



### 二 使用句柄精灵等软件获得想要改变的颜色的RGB值

![image-20211030103726100](https://raw.githubusercontent.com/liang636600/cloudImg/master/img/image-20211030103726100.png)

需要注意的是opencv中的R与B通道是反着的（后面代码中有相应说明）



### 三 编写python代码，运行程序

```python
from PIL import Image
import numpy as np
import cv2 as cv

def picWihtCV(img):
    # 获得行数和列数即图片大小
    rowNum, colNum = img.shape[:2]

    for x in range(rowNum):
        for y in range(colNum):
            # 在opencv里b和r通道刚好是反着的， 比如通过句柄精灵获得图片中某个颜色的rgb值为（204,255,255），在使用opencv时需要将img[x, y].tolist() == [xxx, xxx, xxx]中 == 右边的值改为[255, 255, 204]，下面是把所有想改变的颜色变为了白色
            if img[x, y].tolist() == [255, 255, 204]:
                img[x, y] = np.array([255, 255, 255])
            if img[x, y].tolist() == [204, 255, 255]:
                img[x, y] = np.array([255, 255, 255])
            if img[x, y].tolist() == [204, 255, 230]:
                img[x, y] = np.array([255, 255, 255])
            if img[x, y].tolist() == [204, 230, 255]:
                img[x, y] = np.array([255, 255, 255])

    # 保存修改后图片
    cv.imwrite('b.png', img)

if __name__ == '__main__':
    im = Image.open('a.png')
    # 使用OpenCv来处理图片
    im = cv.cvtColor(np.asarray(im), cv.COLOR_RGB2BGR)
    picWihtCV(im)
```





