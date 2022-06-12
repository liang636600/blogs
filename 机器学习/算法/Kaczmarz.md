求解欠定方程组

![image-20220610091207452](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220610091207452.png)

通过kaczmarz算法解决求逆矩阵问题

![image-20220610092209920](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220610092209920.png)

上图中aj表示A的行向量对应的列向量

代码

A0是归一化后的A，归一化是A每一行归一化，A0=mapslices(r->r.*(1/(r'*r)),A,dims=[2])，其中r表示A的每一行的列向量，结果还是对应A的每一行

![image-20220610092244494](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220610092244494.png)

![image-20220610092807228](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220610092807228.png)

![image-20220610092932312](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220610092932312.png)

