import crawler
from threading import Thread
import utils
import pandas as pd

#Using multithreading to improve the efficiency
class AThread(Thread):
    def __init__(self, gametype,gamepage):
        Thread.__init__(self)
        self.cr = crawler.GameCrawler(gametype,gamepage)

    def run(self):
        self.result = self.cr.getGameInfo()

    def get_result(self):
        return self.result


thd1 = AThread('休闲',1950)
thd2 = AThread('体育',280)
thd3 = AThread('冒险',1950)
thd4 = AThread('动作',2000)
thd5 = AThread('大型多人在线',160)
thd6 = AThread('模拟',1300)
thd7 = AThread('独立',3000)
thd8 = AThread('竞速',230)
thd9 = AThread('策略',1200)
thd10 = AThread('角色扮演',1100)

thd1.start()
thd2.start()
thd3.start()
thd4.start()
thd5.start()
thd6.start()
thd7.start()
thd8.start()
thd9.start()
thd10.start()
thd1.join()
thd2.join()
thd3.join()
thd4.join()
thd5.join()
thd6.join()
thd7.join()
thd8.join()
thd9.join()
thd10.join()

res = []
tp1 = thd1.get_result()
tp2 = thd2.get_result()
tp3 = thd3.get_result()
tp4 = thd4.get_result()
tp5 = thd5.get_result()
tp6 = thd6.get_result()
tp7 = thd7.get_result()
tp8 = thd8.get_result()
tp9 = thd9.get_result()
tp10 = thd10.get_result()

res.extend(tp1)
res.extend(tp2)
res.extend(tp3)
res.extend(tp4)
res.extend(tp5)
res.extend(tp6)
res.extend(tp7)
res.extend(tp8)
res.extend(tp9)
res.extend(tp10)

print(res)
name = ['title','review','recommendation','helpful','funny','hour_played']
steamReview = pd.DataFrame(columns=name,data=res)
steamReview.to_csv('./testcsv.csv',encoding='utf-8')



