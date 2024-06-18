---
title: "互联网爬虫协议 robots.txt文件全解"
date: "2017-11-16"
categories: 
  - "网络基础"
---

该文章转自：http://www.cnblogs.com/wangkundentisy/articles/4562703.html

##### **一、robots.txt有什么用？**

如果您不希望互联网爬虫（又叫蜘蛛、Crawler、Spider等）抓取您网站的每一个公开的链接，而只抓取您指定的某一部分链接，或根本不抓取任何链接，你可以使用robots.txt向搜索引擎汇报爬虫信息。

robots.txt（统一小写）是一种存放于网站根目录下的ASCII编码的文本文件。 比如 **`http://www.sitemap-xml.org/robots.txt`** 大多数主流搜索引擎支持robots协议，它通常告诉搜索引擎，此网站中的哪些内容是不能抓取的，哪些是可以被抓取的。

##### **二、怎么使用robots.txt？**

建议您在站点的根目录下存放一个robots.txt文件。我们的爬虫在第一次抓取您站点时会首先确认根目录下是否有robots.txt文件。例如，您的网站地址是www.7softs.com，我们会首先抓取http://www.softs.com/robots.txt再进行后续操作。如无法访问robots.txt文件，系统则默认为您站点的每个链接都可以被抓取。这就是七彩软件站（http://softs.7softs.com）不设置robots.txt文件的原因。

##### **三、怎么写robots.txt文件？**

**robots.txt** 是个很简单的文本文件，您只要标明“谁不能访问哪些链接”即可。

在文件的第一行写：

**User-Agent: Baiduspider**

这就告诉了爬虫下面的描述是针对名叫Baiduspider的爬虫。您还可以写：

**`User-Agent: *`**

这就意味着向所有的爬虫开放。需要注意的是一个robots.txt文件里只能有一个"User-Agent: \*"。

接下来是不希望被访问的链接前缀。例如：

**Disallow: /private**

这就告诉爬虫不要抓取以"/private"开头的所有链接。包括/private.html，/private/some.html，/private/some/haha.html。如果您写成：

**Disallow: /**

则表明整个站点都不希望被访问。您也可以分多行来指定不希望被抓取的链接前缀，例如：

**Disallow: /tmp**

**Disallow: /disallow**

那么所有以"/tmp"和"/disallow"开头的链接都不会被访问了。

最后形成的robots.txt文件如下：

**User-Agent: Baiduspider**

**Disallow: /tmp**

**Disallow: /private**

请注意，如果您的robots.txt文件里有中文等非英语字符，请确定该文件是由UTF-8编码编写。

##### **四、怎样分别指定不同的网络爬虫？**

这个操作很简单，只要分别指定“谁能或不能访问怎样的链接”即可。例如：

**User-Agent: YodaoBo**

**Disallow:**

**`User-Agent: *`**

**Disallow: /private**

上面的**robots.txt**表明，名为Baiduspider的爬虫可以抓所有的内容，其它名称的爬虫不能抓以"/private"开头的链接
