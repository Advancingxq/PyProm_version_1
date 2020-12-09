# PyProm_version_1

## 一、简介
一个交互式的工作流网分析工具，包含：基于xml的可移植工作流网存储格式、基于已有过程模型生成日志轨迹，基于日志轨迹发现新过程模型，度量变化前后模型的相似度。 </br>
## 二、环境
1.项目名称：PyProm </br>
2.项目来源：为本科毕业设计搭建的工具，获校优 </br>
3.开发平台：windows10+pycharm
4.编程语言：Python3.6
5.使用框架和包：Pyqt5（图形界面设计）、graphviz（图形化展示）、random（随机数生成）、xml.dom.minidom（xml文件解析）、uuid（随机字符串生成）、numpy（矩阵运算）</br>
## 三、算法实现
1.模型比较：Cao B, Wang J, Fan J, et al. Querying similar process models based on the Hungarian algorithm[J]. IEEE Transactions on Services Computing, 2016, 10(1): 121-135.</br>
2.模型发现：Van der Aalst W, Weijters T, Maruster L. Workflow mining: Discovering process models from event logs[J]. IEEE Transactions on Knowledge and Data Engineering, 2004, 16(9): 1128-1142.</br>
3.日志生成：个人实现，基于随机dfs遍历，具体见代码</br>
4.存储格式：个人实现，基于xml语法，分为库所、变迁、边三部分，具体见代码</br>
 ## 四、效果
 ![Image text](https://github.com/Advancingxq/PyProm_version_1/blob/main/result.png)</br>
 ## 五、意义
 项目涵盖了Petri网模型的常用操作，并提供了一个设计好的界面，可以支持进一步开发。</br>
