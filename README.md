# LeanShell

* https://github.com/gunthercox/ChatterBot
* fock from flask-chatterbot(https://github.com/chamkank/flask-chatterbot)

## Description

This is a Shell for LeanCloud, by Python(master branch) and Nodejs(NodeJS branch).

## How it work

It provide some API, in API, it use <procstreams> library to shell the command, and print output of shell command in console.

## API

* ls:   A test API, shell command such as "ls -l".
* top:  top -b -n 1 -H
* ps:   ps -eLf
* cpuinfo:  cat /etc/issue && cat /proc/cpuinfo
* shell:    shell command use subprocess.Popen method.

## Features


## Requirements

* psutil>=5.4.3(Python)

* procstreams >= 0.3.0(Nodejs)

## Installation

* just deploy and open https://leancloud.cn/dashboard/apionline/index.html

## Credits



## License
* 
* 深度学习对话系统理论篇--数据集和评价指标介绍 https://blog.csdn.net/liuchonge/article/details/79104045
* ChatterBot安装,Mongo安装,简单测试 https://blog.csdn.net/hgy413/article/details/82496845

对话系统常用数据集

这部分主要介绍一下当前使用比较广泛的对话系统数据集的细节构成。也会稍微介绍一下公开的中文数据集。可以参考“A Survey of Available Corpora for Building Data-Driven Dialogue Systems”这篇论文，而且作者把所有的数据集按照不同类别进行分类总结，里面涵盖了很多数据集，这里不会全部涉及，有兴趣的同学可以看这个链接。
英文数据集

    Cornell Movie Dialogs：电影对话数据集，下载地址：http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
    Ubuntu Dialogue Corpus：Ubuntu日志对话数据，下载地址：https://arxiv.org/abs/1506.08909
    OpenSubtitles：电影字幕，下载地址：http://opus.lingfil.uu.se/OpenSubtitles.php
    Twitter：twitter数据集，下载地址：https://github.com/Marsan-Ma/twitter_scraper
    Papaya Conversational Data Set：基于Cornell、Reddit等数据集重新整理之后，好像挺干净的，下载链接：https://github.com/bshao001/ChatLearner

相关数据集的处理代码或者处理好的数据可以参见下面两个github项目：

    DeepQA
    chat_corpus

中文数据集

    dgk_shooter_min.conv：中文电影台词数据集，下载链接：https://github.com/rustch3n/dgk_lost_conv
    白鹭时代中文问答语料：白鹭时代论坛问答数据，一个问题对应一个最好的答案。下载链接：https://github.com/Samurais/egret-wenda-corpus
    微博数据集：华为李航实验室发布，也是论文“Neural Responding Machine for Short-Text Conversation”使用的数据集下载链接：http://61.93.89.94/Noah_NRM_Data/
    新浪微博数据集，评论回复短句，下载地址：http://lwc.daanvanesch.nl/openaccess.php



