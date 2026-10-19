# 语法模板与练习

## 按类别还是按Syntax组织

有并列类别时，逐类写完“名称：解释＋该类语法”再进入下一类；编号按实际层级。例如：

```text
6. Set operations
(1) UNION: in A or B; eliminates duplicates.
SELECT x FROM A UNION SELECT y FROM B;
(2) INTERSECT: in A and B.
SELECT x FROM A INTERSECT SELECT y FROM B;
(3) EXCEPT: in A but not B.
SELECT x FROM A EXCEPT SELECT y FROM B;
```

JOIN的各类别、Modify table的Add/Remove/Add constraints也如此，不能先合列所有代码再集中解释。这些是组织方式的例子，不是所有课程的固定知识清单。

已有`(1) 概念`且内部说明较多时，用`① Syntax:`引出一个完整代码块，随后②③解释。Syntax为普通正文，不涂代码底色；多行代码不重复编号。若直接在罗马主题下展开，则可用普通1/2/3点，不能规定Syntax永远用圈号。

短定义加一条简单模板（如Renaming）可以直接接代码，不机械新增Syntax或空层级。只有一个主题时直接展开，示例：

```text
VII. Assertion
1. Definition / purpose.
2. Syntax: ...
3. Checking time / cost.
```

这里1/2/3为正文要点，不加深蓝“1. Assertion”重复父标题。

## 模板如何选内容

用一个综合模板涵盖本课出现的同类语法；下方按“关键词：解释”逐项说明。数据类型可各自一行，不抄完整业务系统的多张表来代替语法模板。保留能直接改用的最小上下文，不能只是同一查询换一组名称。

以PPT框架和老师逐字稿为界，技术上成立不等于本课讲过。只讲SOME就不加ANY，不自行加同义关系、推论或额外模式。核验模板有效性时发现问题须回看来源，不把核验所得课外知识扩为正文。

复杂查询若课件/用户要求，同时列理解顺序和书写顺序并区别其用途：

```text
理解顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
书写顺序：SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY
```

条件、分组字段和排序表达式要有效；不要把一个具体课程的SQL顺序推广为其他语言结构。

## 逐token分色

- 固定关键字、具体函数、运算符、括号/逗号/句点：黑底白字加粗。
- 具体名称、别名、参数、值、可替换函数占位符：灰底黑字，英文普通字重。
- 多解核心如MAX、>= ALL、NOT EXISTS：只将该token字体改为95DCF7，底色和字重保留。
- 解释、Syntax标签和编号不涂代码底色。

`{{T}}.{{attribute}} AS {{output_name}}`中的名称灰色，句点、空格和AS黑色。`VARCHAR({{15}})`中15灰色，VARCHAR与括号黑色。不能只按大小写推断角色。

## 纳入练习时

先按材料/共享schema分组，用`Table(column1,column2,...)`列出全部表及列名，再按原题号列题意和返回列。每题逐个写`Method n — 核心方法`、一句Idea、完整代码；老师多解全部保留，只有一解不自创。每种方法的核心区别须清楚，不能只有一堆没有思路说明的代码。

输出题保留原查询和紧凑答案；课堂明确错误解标WRONG并说明关键差别；有据的口头勘误简短标记。不重复共享数据行或长推导。Exercise自然接在理论后，除非用户指定，不强制换栏/分页。

Tutorial独立新点先报告差异，选择后嵌入最近理论条目；综合题仍在Exercise。用户指定重复展示CASE一类速查内容时可以照办，不能因别处已出现而省略指定入口。
