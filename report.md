# 搜索引擎大作业报告

[TOC]

## 基础配置

### 依赖
* 数据抓取
    * `heritrix3`
    * `The Unarchiver`
* 数据索引
    * `antiword`
    * python3库 `BeautifulSoup``pdfminer3k``python-docx``docx2txt`

### 运行
```bash
# 抓取,若数据量较大可考虑在外置硬盘建立项目
参考数据抓取部分配置heritrix抓取文件

# 索引,生成索引结果至DataParse/build
修改rawdata/totxt.py,rawdata/totxt2.py中data_path为对应路径
cd DataParser
mkdir build
cd ../rawdata
python3 totxt.py
python3 totxt2.py

# 链接结构分析,生成结果至input/html.xml和input/file.xml
cd ../DataParser/build
python3 ../txts2graph.py
cmake .. && make
./pr
python3 ../genxml.py
python3 ../genfilexml.py

# myeclipse,tomcat配置
参考[图片搜索作业](https://github.com/luohy15/ImageSearch/blob/master/README.md)的配置过程,新增的操作见内容检索部分
```

------------------------------------------------------------------------------
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

------------------------------------------------------------------------------
## 数据索引

抓取下来的文件是未经处理的 html, pdf 等, 不便于索引.
因此我们首先进行数据预处理, 将数据处理为适合索引的模式.

### html 预处理
#### 基本思路和数据格式
首先, 对于每一个 html, 我们保存如下信息
* 标题
* 内容
* url
* 从这个 html 所在的网页出发, 又指向哪些网页 (即 `<a href="..."> ... </a>` 中的 `href`)

我们对每个 html 进行编号, 称为该 html 的 id.
预处理这个 html 得到 `id.txt`, 其中有且仅有 5 行内容, 分别是
1. 该 html 的 id
2. 该 html 的 url
3. 从这个 html 出发, 指向的网页的 id 号
4. 该 html 的标题
5. 该 html 的文本内容, 压缩成一行 (因为换行信息对索引无用)

#### 处理实现
代码参见 `rawdata/totxt.py`. 流程基本如下

1. 遍历所有 html 文件, 建立 url 到 id 的映射.
  这一步中我们要剔除掉无法用 utf 或 cp936 打开的 html, 还要剔除打开但是无法解析的 html.
  这样得到一系列我们能够处理的 html 文件.

2. 对于第 1 步中得到的 html 文件, 显然我们已知其 id, url.
  标题和内容使用 `BeautifulSoup` 解析 html 得到, 指向网页需要解析锚节点,
  并且只保留在第一步中得到的链接.

### 文件解析
本次作业考虑了如下三种文件的解析
1. pdf 文件
2. doc 文件
3. docx 文件

#### 基本思路

考虑到文件没有出连接, 而且只有一个入链接, 所以我们对于文件无需进行链接分析.
所以对于每个文件, 我们保存如下信息
* url
* 文件内容
* 文件名 (实际上这个是通过 url 得到的)

我们仿照上面, 对每个文件处理生成一个 `typeXX.txt`;
其中 `type` 是 pdf, doc 或者 docx, `XX` 是文件的编号.
内容两行, 分别为
1. url
2. 文件内容, 压缩成一行

#### 处理实现
对于每一种文件格式, 都有一个程序用来抽取其中内容.
对于 `pdf`, 是 `rawdata/pdf2txt`
对于 `doc`, 是 `antiword`
对于 `docx`, 是 `rawdata/docx2txt`.

这个程序 `xxx2txt` 这个程序的接口要求很简单,
即运行 `xxx2txt abc.xxx`,
就会在标准输出中打印 `abc.xxx` 的文本内容.
这也是通常工具的标准接口.

我们通过 `subprocess` 来调用这个外部程序, 使用 `check_output` 获取其输出.
若处理某文件时发生错误, 我们直接跳过该文件.

------------------------------------------------------------------------------
## 链接结构分析
这里只考虑 html 链接结构分析, 因为 pdf 等文件没有链接结构.

### PageRank
考虑到 PageRank 部分不需要考虑汉字处理,
因此 PageRank 沿用[戴臻旸第二次作业](https://bitbucket.org/hoblovski/pagerank)的程序.
它使用 C 写成, 代码不到 300 行, 但是高效安全,
在 i5-4200U 机器上处理第二次作业超过 200 MB 的数据仅需 30 秒.
它接受一个输入 `xxx.graph` 文件, 输出各个节点的 pagerank 值.

为了适应本次作业, 我们还有如下修改
1. 增加 `DataParser/txts2graph.py`, 从之前生成的 `.txt` 文件生成 `.graph` 文件
2. 输出 PageRank 值到各个 `.txt` 文件的第六行.

### 生成xml
为了尽量重用图片搜索的代码, 我们把诸 `.txt` 文件生成一个 `html.xml` 文件, 让 `ImageIndexer` 处理.
`html.xml` 文件中每个 `.txt` 文件包含如下字段
1. 标题, 直接参与索引
2. id, `ImageIndexer` 需要读取 id.txt 文件的内容, 参与索引
3. PageRank 值, 作为 Lucene 中的 document boost.
4. url, 不索引但是需要保存

生成代码参见 `DataParser/genxml.py`.

另外我们对于文件也生成一个 `file.xml`, 每个文件包含标题, url 和 id, 同上处理.
参见 `DataParser/genfilexml.py`.

------------------------------------------------------------------------------
## 内容检索
主要的工作在图片检索中已经完成,
代码沿用图片搜索的代码 (BM25, 分词多 Field 查询),
并做了尽量少的修改.

下面主要叙述本次作业新增内容.

* **标题和内容不同的权重**: 对每个 `Field` 设置 boost.
  本次作业中, 标题的 boost 是 1e4, 内容的 boost 是 1.

* **集成 PageRank**: 对于每个 `Document` 设置 boost 为 PageRank.
  我试验过对 PageRank 加上非线性, 如 log,
  但是效果不好, 直接使用 PageRank 作为 boost 反而效果很好.

* **文字搜索高亮**: 使用 `HighLighter` 类封装, 其接受被检索的关键词和检索到的结果,
  以 html 形式返回高亮 (即结果中关键词加红) 的结果.

* **文件检索**:
  1. 复制 `ImageIndexer`, `ImageSearcher`, `ImageServer` 得到对应的 `FileIndexer` 等, 稍作修改 (如索引字段不同, 不考虑 PageRank 值).
  2. 复制 `imagesearch.jsp`, `imageshow.jsp` 得到对应的 `filesearch.jsp` 等, 稍作修改 (修改标题, 配色).
  3. 修改 `WebRoot/WEB-INF/web.xml`, 加入新的 Servlet `FileServer`.

------------------------------------------------------------------------------
## 参考资料
* heritrix环境配置参考了[用Solr构建垂直搜索引擎](https://fliaping.gitbooks.io/create-your-vertical-search-engine-with-solr/content/crawl-web-page-by-using-heritrix.html)和[THUSearchEngine](https://github.com/ChenGuangbinTHU/THUSearchEngine/blob/master/WebPreprocess/crawler-beans.cxml)
* html 到中间 txt 再重用 xml 的架构参考了 [THUSearch](https://github.com/Terranlee/THUSearch).
* 前端参考了 Bootstrap 的 [Cover](https://getbootstrap.com/docs/4.1/examples/cover/)
* 图片背景的设计参考了 [Bing](cn.bing.com)

