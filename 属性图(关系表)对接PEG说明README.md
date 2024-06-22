# 属性图对接PEG说明文档

本文档提供了一个数据转换工具pg2rdf，可基于csv文件生成PEG导入数据，实现PEG图数据库在属性数据上的建库。

以下是流程框架图，整体流程分为下面4个步骤，我们将依次详细介绍各个步骤，并给出在PEG图数据库上查询数据的详细样例。

- 1. 导入数据
- 2. 数据转换

- 3. 数据导出

- 4. 数据导入PEG

![image-20240622163850861](.\image-20240622163850861.png)

## 1.导入数据

导入数据需全部存放在名为**input**的文件夹中，所有数据以**csv文件**形式存储，每一个文件包含一张关系表的记录。在此我们提供了输入样例，共有五个csv文件student.csv，course.csv ,  score.csv和know.csv，分别表示学生数据、课程数据、学生成绩、学生人际认知数据，输入数据的文件结构如下：

```markdown
- input
  - student.csv
  - course.csv
  - score.csv
  - know.csv
```

下面将分别介绍各个csv文件内的详细内容。

### 学生表（student.csv）

以下学生表中记录了每个学生的个人信息，下面第一行为列名，共有四列，分别为`sid` ，`sname` ，`sage` ，`ssex`，代表学生的ID，姓名，年龄和性别。从第二行开始，每一行为一个学生的个人信息，如第二行数据中学生ID为1，姓名为Alice，年龄20，性别女。

<font color=red>**注：**</font> 表的列名后续会用于描述查询语句，是查询语句的部分语义，因此请清晰定义并记住各表中的列名。（下表同）

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

以下课程表记录了各个课程信息，第一行为列名，共有三列，分别为`cid` ，`cname` ，`tname` ，代表课程的ID，名称和授课老师姓名。从第二行开始，每一行为一个课程的信息，如第二行数据中课程ID为1，名称为Mathematics，授课老师姓名为Ethan。

```
cid,cname,tname
1,Mathematics,Ethan
2,Physics,Olivia
3,Chemistry,Mason
4,Biology,Sophia
5,Computer Science,Jackson
6,English Literature,Isabella
7,History,Liam
8,Geography,Ava
9,Economics,Lucas
10,Art,Emma
```

### 学生成绩表(score.csv)

以下学生成绩表记录了学生的选课信息，第一行为列名，共有三列，分别为`sid` ，`cid` ，`grade` ，代表学生ID，课程ID和课程成绩。从第二行开始，每一行为一个学生的成绩信息，如第二行数据中表示学生ID为`sid`的学生选了课程ID为`cid`的课程成绩，该学生的成绩为`grade`。

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

### 学生人际认知表(know.csv)

以下学生人际认知表记录了学生的人际认知信息，第一行为列名，共有两列，分别为`sid1` ，`sid2` ，代表编号为`sid1`的学生认识编号为`sid2`的学生，注意此处为单向认识

```
sid1,sid2
1,2
2,3
2,4
4,1
3,1
4,5
5,6
6,4
7,8
8,7
```



## 2.数据转化

我们提供了一个数据转化工具pg2rdf，用于转化上述导入数据，生成对应的中间文件，实现PEG图数据库在属性数据上的建库。具体代码见给定文件夹中的pg2rdf.py文件，使用前请确保已安装Python 3.x版本。

### 使用方法

数据转化工具用法如下，表示利用 `pg2rdf.py` 转换文件夹`input_folder` 中的导入数据，并将转换结果存放在文件夹`output_folder`中。

```python
python3 pg2rdf.py input_folder output_folder
```

实际使用中，您应将上述`input_folder`替换为包含导入数据的文件夹地址，将上述`output_folder`替换为想要存放导出数据的文件夹地址，为方便使用，我们建议您将文件夹目录设置为：将包含导入数据的文件夹，存放导出数据的文件夹和`pg2rdf.py`放在同一目录下，举例如下：

```shell
input
  - student.csv
  - course.csv
  - score.csv
  - know.csv
output
pg2rdf.py
```

参照以上例子，**<font color=red>您需要在存放`pg2rdf.py`的根目录下执行以下指令</font>**，完成数据转换。

```python
 python3 pg2rdf.py ./input/ ./output/
```

### 注意事项

csv文件第一行为列名，各个元素以逗号分隔，第二行开始为数据值，数据值统一按字符串处理，**请避免数据值包含非法字符**，尤其避免出现前导空格和后导空格！

#### **非法字符：**

1. **保留字符**：这些字符在PEG数据格式中有特殊的意义，包括：
   - `:`、`/`、`?`、`#`、`[`、`]`、`@`、`!`、`$`、`&`、`'`、`(`、`)`、`*`、`+`、`,`、`;`、`=`
2. **非ASCII字符**：非ASCII字符（即字符编码大于127）
3. **空格**：空格不是合法的
4. **控制字符**：控制字符（如换行符`\n`、制表符`\t`等）也是不允许的
5. **未保留但不允许的字符**：某些字符虽然在PEG数据格式中没有特殊含义，但出于兼容性和安全性的考虑不接受，例如`{}`、`|`、`\`、`^`、`~`、`"`（双引号）等
6. **特殊字符**：某些特殊字符，例如`%`、`<`、`>`等

## 3.数据导出

执行转换指令后，原本为空的`output`文件夹中，新增了五个导出文件，分别为`student.nt` ,`course.nt` ,`score.nt`, `know.nt` 和`all.nt`，前四个文件代表四个数据表的数据转换结果，**<font color=red>`all.nt` 表示所有数据转换结果的汇总，即前四个文件的集合，也是查询需要使用的唯一文件。</font>**

下面是数据转换执行及代码输出内容：

```shell
# 转换指令
[root@localhost pg2rdf]$  python3 pg2rdf.py ./input/ ./output/
# 代码执行的输出，最后一行为转化结果汇总all.nt的输出路径，其中.为当前目录
Processed ./input/student.csv -> ./output/student.nt
Processed ./input/course.csv -> ./output/course.nt
Processed ./input/score.csv -> ./output/score.nt
Processed ./input/know.csv -> ./output/know.nt
Processed all data -> ./output/all.nt
# 查看当前目录位置
[root@localhost pg2rdf]$ pwd
/pg2rdf
# 当前目录位置替换all.nt输出路径中的.，就可以得到转化结果汇总all.nt的绝对路径
# /pg2rdf/output/all.nt为转化结果汇总all.nt的绝对路径
```

## 4.数据导入PEG

上一步中生成的`all.nt`包含转化后的所有数据，接下来我们依据该数据建立数据库，并导入PEG，方便后续的查询执行。

### 开启http服务

```shell
[root@localhost pg2rdf]$ cd bussiness-static-aarch64
[root@localhost bussiness-static-aarch64]$ nohup bin/http -c 1 &
```

http接口采用的是`http`协议，支持多种方式访问接口，如果http启动的端口为`9000`,则接口对接内容如下：

接口地址：

>  http://ip:9000/

接口支持 `get`请求和`post`请求，其中`get`请求参数是放在url中，`post`请求是将参数放在`body`请求

**注意：`GET`请求中各参数如果含有特殊字符，如？，@,&等字符时，需要采用urlencode进行编码，尤其是`sparql`参数必须进行编码**

### 数据导入PEG

#### 使用简述

使用curl发送post请求调用 **`PEG创建图数据库`** 接口导入数据，请注意替换"db_name"的值为您创建的数据库名，替换"db_path"的值为您第三步生成的<font color=red>`all.nt`</font>的文件路径（推荐使用绝对路径）

```bash
curl -i -H 'content-type: application/json' -X POST -d '{"operation":"build","username":"root","password":"123456","db_name":"db_name_value","db_path":"all_nt_path_value"}' http://127.0.0.1:9000
```

#### 举例

将`all.nt`导入PEG，并创建为school数据库。

以下指令中，您需要将`"db_path"`的值改为您的<font color=red>`all.nt`</font>文件存放地址，上述生成的<font color=red>`all.nt`</font>文件的位置为`/pg2rdf/output/all.nt`，`"db_name"`的值改为您想要创建数据库的名字，这里为`school`。

```shell
[root@localhost bussiness-static-aarch64]$ curl -i -H 'content-type: application/json' -X POST -d '{"operation":"build","username":"root","password":"123456","db_name":"school","db_path":"/pg2rdf/output/all.nt"}' http://127.0.0.1:9000
```

### 将school数据库加载到内存

```
[root@localhost bussiness-static-aarch64]$ curl -i -H 'content-type: application/json' -X POST -d '{"operation":"load","username":"root","password":"123456","db_name":"school","csr":"1"}' http://127.0.0.1:9000
```



## 5.数据查询

>  以下示例均在本文第2步导入PEG执行完成后才可正常执行

### 查询使用简述

使用curl发送post请求调用 **`PEG创建数据库查询`** 接口执行SPARQL查询，请注意替换"db_name"的值为您创建的数据库名，"sparql"的值为指您准备执行的sparql语句内容

```bash
curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"db_name_value","format":"json","sparql":"sparql_value"}' http://127.0.0.1:9000
```

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
# 查询姓名为Alice的学生的性别
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT * WHERE { ?student	<sname>	<Alice>	. ?student	<ssex>	?sex	. }"}' http://127.0.0.1:9000

# 返回结果：可知学生Alice的性别为Female
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 265
Cache-Control: no-cache
Pragma: no-cache
Expires: 0

{"head":{"link":[],"vars":["student","sex"]},"results":{"bindings":[{"student":{"type":"uri","value":"student_1"},"sex":{"type":"uri","value":"Female"}}]},"StatusCode":0,"StatusMsg":"success","AnsNum":1,"OutputLimit":-1,"ThreadId":"139666590172928","QueryTime":"1"}
```

### 查询姓名为Alice的学生已选的所有课程名称

SPARQL

```SPARQL
SELECT ?cname WHERE {
	?student	<sname>	<Alice>	.
    ?student	<sid>	?sid	.
    ?score	<sid>	?sid	.
    ?score	<cid>	?cid	.
    ?course	<cid>	?cid	.
    ?course	<cname>	?cname	.
}
```

运行示例

```shell
# 查询姓名为Alice的学生已选的所有课程名称
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT ?cname WHERE { ?student	<sname>	<Alice>	. ?student	<sid>	?sid	. ?score	<sid>	?sid	. ?score	<cid>	?cid	. ?course	<cid>	?cid	. ?course	<cname>	?cname	. }"}' http://127.0.0.1:9000


# 返回结果：可知学生Alice的已选的课程有Mathematics和Chemistry
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 264
Cache-Control: no-cache
Pragma: no-cache
Expires: 0

{"head":{"link":[],"vars":["cname"]},"results":{"bindings":[{"cname":{"type":"uri","value":"Mathematics"}},{"cname":{"type":"uri","value":"Chemistry"}}]},"StatusCode":0,"StatusMsg":"success","AnsNum":2,"OutputLimit":-1,"ThreadId":"139665013188352","QueryTime":"1"}

```

### 查询姓名为Alice的学生已选的所有课程名称及成绩

SPARQL

```SELECT ?course WHERE {
SELECT ?cname?grade WHERE {
	?student	<sname>	<Alice>	.
    ?student	<sid>	?sid	.
    ?score	<sid>	?sid	.
    ?score	<cid>	?cid	.
    ?score	<grade>	?grade	.
    ?course	<cid>	?cid	.
    ?course	<cname>	?cname	.
}
```

运行示例

```shell
# 查询姓名为Alice的学生已选的所有课程名称及成绩
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT ?cname ?grade WHERE { ?student	<sname>	<Alice>	. ?student	<sid>	?sid	. ?score	<sid>	?sid	. ?score	<cid>	?cid	.  ?score	<grade>	?grade	.	?course	<cid>	?cid	. ?course	<cname>	?cname	. }"}' http://127.0.0.1:9000



# 返回结果：可知学生Alice的Mathematics课程85分，Chemistry课程79分
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 344
Cache-Control: no-cache
Pragma: no-cache
Expires: 0

{"head":{"link":[],"vars":["cname","grade"]},"results":{"bindings":[{"cname":{"type":"uri","value":"Mathematics"},"grade":{"type":"uri","value":"85"}},{"cname":{"type":"uri","value":"Chemistry"},"grade":{"type":"uri","value":"79"}}]},"StatusCode":0,"StatusMsg":"success","AnsNum":2,"OutputLimit":-1,"ThreadId":"139666590172928","QueryTime":"1"}

```

### 查询参与同一节课程中存在三角传递认识关系的学生姓名

SPARQL

```SPARQL
SELECT ?sname1 ?sname2 ?sname3 WHERE {
	?student1	<sname>	?sname1	.
    ?student2	<sname>	?sname2	.
    ?student3	<sname>	?sname3	.
    ?student1	<sid>	?sid1	.
    ?student2	<sid>	?sid2	.
    ?student3	<sid>	?sid3	.
    ?f1	<sid1>	?sid1	.
    ?f1	<sid2>	?sid2	.
    ?f2	<sid1>	?sid2	.
    ?f2	<sid2>	?sid3	.
    ?f3	<sid1>	?sid3	.
    ?f3	<sid2>	?sid1	.
    ?course1	<sid>	?sid1	.
    ?course2	<sid>	?sid2	.
    ?course3	<sid>	?sid3	.
    ?course1	<cid>	?cid	.
    ?course2	<cid>	?cid	.
    ?course3	<cid>	?cid	.
}
```

运行示例

```shell
# 查询参与同一节课程中存在三角传递认识关系的学生姓名
[root@localhost bussiness-static-aarch64]$ curl -i -H 'Content-Type: application/json' -X POST -d '{"operation":"query","username":"root","password":"123456","db_name":"school","format":"json","sparql":"SELECT ?sname1 ?sname2 ?sname3 WHERE { ?student1	<sname>	?sname1	. ?student2	<sname>	?sname2	. ?student3	<sname>	?sname3	. ?student1	<sid>	?sid1	. ?student2	<sid>	?sid2	. ?student3	<sid>	?sid3	. ?f1	<sid1>	?sid1	. ?f1	<sid2>	?sid2	. ?f2	<sid1>	?sid2	. ?f2	<sid2>	?sid3	. ?f3	<sid1>	?sid3	. ?f3	<sid2>	?sid1	. ?course1	<sid>	?sid1	. ?course2	<sid>	?sid2	. ?course3	<sid>	?sid3	. ?course1	<cid>	?cid	. ?course2	<cid>	?cid	. ?course3	<cid>	?cid	.}"}' http://127.0.0.1:9000

# 返回结果有三条，分别是从Alice、Diana、Bob开始的传递认识链，说明Alice、Diana、Bob选了同一门课且他们存在三角传递认识关系
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 551
Cache-Control: no-cache
Pragma: no-cache
Expires: 0

{"head":{"link":[],"vars":["sname1","sname2","sname3"]},"results":{"bindings":[{"sname1":{"type":"uri","value":"Alice"},"sname2":{"type":"uri","value":"Bob"},"sname3":{"type":"uri","value":"Diana"}},{"sname1":{"type":"uri","value":"Bob"},"sname2":{"type":"uri","value":"Diana"},"sname3":{"type":"uri","value":"Alice"}},{"sname1":{"type":"uri","value":"Diana"},"sname2":{"type":"uri","value":"Alice"},"sname3":{"type":"uri","value":"Bob"}}]},"StatusCode":0,"StatusMsg":"success","AnsNum":3,"OutputLimit":-1,"ThreadId":"139666590172928","QueryTime":"1"}
```

