# Data-cleaning-for-JD-reviews

Data exploration and data cleaning/pre-processing. 

For any model training, data exploration on the given data is the first thing.
And possibly a data pre-processing step is necessary, depending on the findings on your data exploration.

JD-binary is a sentiment analysis database contributed by Xiang Zhang and LeCun, 
Xiang Zhang, Yann LeCun, Which Encoding is the Best for Text Classification in Chinese, English, Japanese and Korean?, arXiv 1708.02657

The comments/reviews are from Chinese e-commerce website JD.com.
You can download the train set from:
https://drive.google.com/file/d/0Bz8a_Dbh9QhbN3dVbXRyaUJGU3c/view ,
and the test set from:
https://drive.google.com/file/d/1ktdX1jlF6sd1muju_Emx9gIRTz4xKDYU/view . 

In this test project, assuming the NLP task is Sentiment Classification
Data Exploration

经过对京东评论的观察，可以发现无效数据有以下几个规律：

1.往往为了凑足10个字符而重复打字，这样的情况往往是单一重复的字符（或者中文或者符号或者英文。例如 “111111111111”，”哈哈哈哈哈啊哈哈哈哈哈哈”

2.胡乱打字，此时往往是符号或英文字符，因为英文字符和符号比较容易打出，不像中文需要经过空格确认。例如“asdiqjwdoijciqjw“, “qmwicjiqjwi黑暗时代”

这些数据往往不含有任何有效的情感信息，应该从数据集里面剔除

 

其次是有些有效数据中含有无效信息，对于训练可能造成影响：

\1.     数据中残留一些html格式的字符串。例如&gt，\n\t\r之类

\2.     数据中有大量的重复数字信息。例如大量电话号码和邮箱，或者无意义数字

\3.     数据前后有大量无意义符号。例如中文省略号。。。。。

\4.     数据中大部分评论没有标题，有的标题也没有内容

Data Cleaning

针对筛出无效数据，我设定两个条件，第一是计算信息有效度，也即实际有意义的字符占总字符的比例；第二计算中英文字的比例。

有效信息度=评论中的唯一字符长度/总评论字符长度

中英文比例=英文字符长度/中文字符长度

如果有效信息度小于三分之一，则被认为是脏数据。之所以设定三分之一是因为为了满足评论大于10个字的规则，例如，“十个字十个字十个字十个字”或“10个字10个字10个字”

需要至少打三遍，所以如此的脏数据可以被有效信息度规则过滤掉。

如果中英文比率超过1，则被认为是脏数据，因为京东是中国的电商，通常评论用中文表达，如果英文字符较多很有可能是为了凑10个字评论的脏数据。

 

针对筛出有效数据中的无效信息，我主要用了正则表达式以及strip来去除那些无效数据。


