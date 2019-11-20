#-*- coding:utf-8 -*-

import io
import sys
import urllib
import urllib.request
import time
from bs4 import BeautifulSoup

import importlib
importlib.reload(sys)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

from flask import Flask,request
import json

tmall_url = 'https://tophub.today/' 
app=Flask(__name__)

# 蜘蛛帮助类
class Spider:
	# 加载数据
	def load_data(self,url):
		# user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
		user_agent="Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10"
		headers = {"User-Agent": user_agent}

		req = urllib.request.Request(url, headers = headers)
		response = urllib.request.urlopen(req)
		html = response.read()

		return html

# 通用Model
class WeiBoModel:
	def __init__(self,url,index,title,note):
	    self.url = url
	    self.index = index
	    self.title = title
	    self.note = note


	

# 微博热搜接口
@app.route("/api/v1/WeiBoData",methods=["GET"])
def WeiBoData():
	return ProcessData("node-1")

# 知乎热榜
@app.route("/api/v1/ZhiHuData",methods=["GET"])
def ZhiHuData():
	return ProcessData("node-6")

# 微信24h热文榜
@app.route("/api/v1/WeXinData",methods=["GET"])
def WeXinData():
	return ProcessData("node-5")

# 百度实时热点
@app.route("/api/v1/BaiDuData",methods=["GET"])
def BaiDuData():
	return ProcessData("node-2")

# 数据处理方法
def ProcessData(node_id):
	#url 拼接
	commentUrl = tmall_url

	# 加载数据
	spider = Spider()
	data = spider.load_data(commentUrl)
	# 处理数据
	soup = BeautifulSoup(data,"html.parser")
	# weibo_data = soup.find(id="node-1")
	weibo_data = soup.find(id=node_id)

	weibo_data_list = weibo_data.select('.nano-content a')
	# 组装数据
	data=[]
	for item in weibo_data_list:
		url = item["href"]
		index = item.find("span",class_="s").string
		title = item.find("span",class_="t").string
		note = item.find("span",class_="e").string
		data.append(WeiBoModel(url,index,title,note).__dict__)

	return json.dumps(data,ensure_ascii=False)



if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)

	
