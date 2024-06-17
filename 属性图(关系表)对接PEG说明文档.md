# 属性图对接PEG说明文档

在此文档中，提供了一个用于将CSV格式的数据转换为NT图格式的工具。输入数据以CSV文件形式存储，每个文件包含了关系表的记录，我们的目标是将每条记录转换为三元组形式，以便使用PEG完成知识图谱应用的构建。

## 1.csv数据样例

输入数据以CSV文件形式存储，每个文件包含了一张关系表的记录。

此文档中我们提供了三个关系表，分别是学生表、课程表、学生选课表，具体数据如下：

### 学生表（student.csv）

```shell
sid,sname,sage,ssex
1,Alice,20,Female
2,Bob,22,Male
3,Charlie,21,Male
4,Diana,19,Female
5,Eve,NULL,Other
6,Frank,23,Male
7,Grace,20,Female
8,Henry,22,Male
```

### 课程表（course.csv）

```
cid,cname,tno
1,Mathematics,101
2,Physics,102
3,Chemistry,103
4,Biology,104
5,Computer Science,105
6,English Literature,106
7,History,107
8,Geography,108
9,Economics,109
10,Art,110
```

### 学生选课表(sc.csv)

```
sid,cid,grade
1,1,85
1,3,79
2,1,88
2,2,78
3,2,81
3,3,92
4,1,90
5,3,85
```

## 2.数据转化和导入PEG

### csv转nt工具
pg2rdf.py为我们使用的数据转化工具，使用前请确保已安装Python 3.x版本
```shell
# 查看转化脚本pg2rdf使用说明
[root@localhost /pg2rdf]$ python3 pg2rdf.py -h
usage: python3 pg2rdf.py input_folder output_folder

Convert CSV files in a folder to NT files.

positional arguments:
  input_folder   Path to the input folder containing CSV files.
  output_folder  Path to the output folder to save NT files.

optional arguments:
  -h, --help     show this help message and exit
 
# 使用pg2rdf将./input/目录底下所有csv文件转化为nt文件并保存到./output/文件夹中，其中./input/目录底下包含步骤1中的三个csv文件，执行后输出目录将生成每个csv转化的nt文件以及包含所有转化数据的all.nt，即/pg2rdf/output/all.nt为转化后的数据
[root@localhost /pg2rdf]$  python3 pg2rdf.py ./input/ ./output/
Processed ./input/sc.csv -> ./output/sc.nt
Processed ./input/student.csv -> ./output/student.nt
Processed ./input/course.csv -> ./output/course.nt
Processed all data -> ./output/all.nt

```

### 数据导入PEG

上一步生成的all.nt包含转化后的所有数据，我们的目标是将其导入PEG创建为school数据库，school数据库为后续第3和第4使用的前提。

```shell
# 在PEG项目目录开启http服务
[root@localhost /pg2rdf]$ cd bussiness-static-aarch64
[root@localhost /pg2rdf]$ nohup bin/http -c 1 &

# 将/pg2rdf/output/all.n导入到PEG为school数据库
[root@localhost bussiness-static-aarch64]$ curl -i -H 'content-type: application/json' -X POST -d '{"operation":"build","username":"root","password":"123456","db_name":"school","db_path":"/pg2rdf/output/all.nt"}' http://127.0.0.1:9000

# 将school数据库加载到内存
[root@localhost bussiness-static-aarch64]$ curl -i -H 'content-type: application/json' -X POST -d '{"operation":"load","username":"root","password":"123456","db_name":"school","csr":"1"}' http://127.0.0.1:9000
```



## 3.数据查询

>  以下示例均在本文第2步导入PEG执行完成后才可正常执行

### 查询姓名为Alice的学生的性别

SPARQL

```SPARQL
SELECT * WHERE {
	?student	<sname>	<Alice>	.
    ?student	<ssex>	?sex	.
}
```

运行示例

```shell
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT * WHERE { ?student	<sname>	<Alice>	. ?student	<ssex>	?sex	. }"}' http://127.0.0.1:9000

```

### 查询姓名为Alice的学生已选的所有课程名称

SPARQL

```SPARQL
SELECT ?course WHERE {
	?student	<sname>	<Alice>	.
    ?student	<sid>	?sid	.
    ?sc	<sid>	?sid	.
    ?sc	<cid>	?cid	.
    ?course	<cid>	?cid	.
    ?course	<cname>	?cname	.
}
```

运行示例

```shell
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT ?course WHERE { ?student	<sname>	<Alice>	. ?student	<sid>	?sid	. ?sc	<sid>	?sid	. ?sc	<cid>	?cid	. ?course	<cid>	?cid	. ?course	<cname>	?cname	. }"}' http://127.0.0.1:9000

```

