# 搜索引擎大作业报告

[TOC]

## 数据抓取

### heritrix配置说明

#### Meta:项目说明

```java
		 metadata.operatorContactUrl=https://github.com/luohy15
		 metadata.jobName=for search engine
		 metadata.description=html and pdf and docx now
```
#### Seed:种子

使用news等网站作为种子

```java
				 http://news.tsinghua.edu.cn
				 http://www.cs.tsinghua.edu.cn/
				 http://graduate.tsinghua.edu.cn
				 ...
```

#### Surtsource:接受和拒绝的URL

使用去掉lib的tsinghua.edu.cn下的子域名

```java
				 +http://(cn,edu,tsinghua,
				 -http://(cn,edu,tsinghua,lib,
```
#### Regexlist:核心规则

通过拒绝非html/doc/pdf类型来抓取html/doc/pdf

```java
			<value>^(?:(?!\.html)(?!\.htm)(?!\.pdf)(?!\.PDF)(?!\.doc)(?!\.docx)(?!\.DOC)(?!\.DOCX)(?!\.htmlx)(?!\.HTML)(?!\.HTM)(?!\.HTMLX).)+</value>
			<value>[\S]*lib.tsinghua.edu.cn[\S]*</value>
			<value>[\S]*166.111.120.[\S]*</value>
```
### 解压

未在Windows上找到合适的提取warc的方法,使用OSX上的`The Unarchiver`提取

由于前期设置压缩包最大为1G,所以`ls -d W*/ | xargs -I {} cp -r {} all`将10G的解压后文件至同一个目录下

### 参考

[用Solr构建垂直搜索引擎](https://fliaping.gitbooks.io/create-your-vertical-search-engine-with-solr/content/crawl-web-page-by-using-heritrix.html)

[THUSearchEngine](https://github.com/ChenGuangbinTHU/THUSearchEngine/blob/master/WebPreprocess/crawler-beans.cxml)

## 数据索引

### html解析

遍历数据目录,建立file->id的dict,采用编码探测方案,首先用UTF8,若失败则尝试cp936,若还是失败则忽略这个file,使用`BeautifulSoup`解析正确解码的html文件,以如下格式输出文档信息到`id.txt`中:

```
id.txt

lineno		content
1 		id
2		url
3		out-edge target ids, space seperated
4		title
5		content, newlines removed
```

### pdf解析

### doc,docx解析

## 链接结构分析

### PageRank

### 生成xml

## 内容检索

