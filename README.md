# jdbook
## scrapy_redis去重方法
- 使用sha1加密request得到指纹
- 把指纹存在redis的集合中
- 下一次新来一个request，同样的方式生成指纹，判断指纹是否存在reids的集合中

## redis数据库出现的内容
1 jd:dupefilter 抓到过的request对象指纹 (指纹集合，存放的是已经进入scheduler队列的request对象的指纹，指纹默认由请求方法，url和请求体组成)
2 jd:items  爬取的内容
3 jd:requests 待爬取项  (dumpfilter的数量减去request的数量是已经抓爬取过的数量)

## 数据存储
redispipeline中仅仅实现了item数据存储到redis的过程,我们新建一个pipeline（jdbook.pipelines.BookPipeline）,让数据存储到本地mysql。

## 实现持久化爬虫
在setting文件中添加去重类和scheduler队列,同时修改redis数据库链接,并保证数据库是可用的。
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
REDIS_URL = "redis://127.0.0.1:6379"


## 在mysql存储的样本
'''
小说	历史	https://img11.360buyimg.com/n7/jfs/t12805/60/2282123829/387388/26ab5008/5a38b251N1c205cef.jpg	大秦帝国全套全6部11卷全新修订版孙皓晖版中国通史现当代原版历史长篇经典名著小说读物近十热播剧	孙皓晖	上海人民出版社	2016-10	598
传记	自传	https://img12.360buyimg.com/n7/jfs/t4576/272/1802830831/291229/5fc1765/58e7096dN544555de.jpg	海伦·凯勒自传 我生活的故事（经典无删节版图文美绘双语典藏）/海量阅读海外名著系列	海伦·凯勒	江西人民出版社	2017-02	42
艺术	篆刻	https://img12.360buyimg.com/n7/jfs/t25948/64/1882095286/317638/154e28fd/5bbe4c00Nc404c838.jpg	正版 启功体硬笔书法技法训练楷书 名家书法技法 文阿禅编著 启功硬笔楷书字帖 启功钢笔	文阿禅	岭南美术出版社	2009-09	26.8
'''
