# Word 精确排版规范

## 页面与段落

A4竖向、单section，`pgSz w=11906 h=16838` twips。四边57twips，gutter=0；header=851、footer=992，但不新增可见页眉页脚。三等宽栏，`num=3 space=67`，无栏间线；`docGrid type=lines linePitch=312`。每栏约194.3pt。

文字段落与标题均固定6pt：`spacing line=120 lineRule=exact before=0 after=0`，通常左对齐、无大缩进，黄色Chapter居中。用真实文字编号，不用Word自动列表。不新增封面、目录、装饰边框或大空白。

正文docDefaults/Normal显式6.5pt；段落标记、软换行、空格和分栏符也设置对应字体字号，不保留11pt。代码缩进按实际可读性设置，不能给所有编号套大悬挂缩进。不要靠减字号、缩行距或改栏数塞页。

## 字体、字号与字重

- 英文、数字及代码：Abadi MT Condensed Light，ascii/hAnsi显式设定，正文6.5pt。代码不换等宽字体。
- 中文及中文标点：等线 Light / DengXian-Light，5.5pt、加粗；theme major font的Hans应指向等线Light，run可用eastAsiaTheme=majorHAnsi。
- 顶层黄色标题：英文7.5pt、中文6.5pt，均加粗；章内青色主题和深蓝英文小标题仍6.5pt。
- 普通英文解释不加粗；对象名可局部黑色加粗，关键条件红色加粗。不要让整段英文继承标题/代码字重。
- 圈号①–⑳：5.5pt、**不加粗**，用 `= n \* GB3` Word复杂域；起始/分隔/结束run均5.5pt，缓存结果run有`rFonts hint=eastAsia`、继承等线Light。克隆模板真实组件，不强制改英文字形或使用普通加粗Unicode；其后英文恢复6.5pt。

## 颜色按职责选择

使用字符级 `w:highlight`，不用整段底纹；编号本身不自动着标题色。

- `yellow / FFFF00`：Chapter，黑字加粗、居中。
- `cyan / 00FFFF`：I./II.等章内主题，黑字加粗。
- `blue / 0000FF`：真实小标题，白字加粗。普通1/2/3要点不因此涂蓝。
- `black / 000000`：固定代码关键字、函数、运算符和标点，白字加粗。
- `lightGray / C0C0C0`：可替换表名、字段名、别名、参数和值，黑字，英文不加粗；也可用于课内注释/输出。
- 字色`95DCF7`：不同解法的少数核心token，保留原有黑/灰底及字重，不把整个代码块改蓝。
- 字色`EE0000`且加粗：决定性质、条件、方向、比较或易错区别的关键词/短句。不是按“所有专业名词”染红。

## 图片与原生形状

截图独立wp:inline段落、保持比例、默认宽184pt且不超过栏宽；段落自动行高、段前后0、left/right/firstLine=0，图片run和段落标记1pt，四侧distance=0。不能把截图放进固定6pt段落造成裁切。

原生小符号留在固定6pt正文行，整体高5.2pt、run1pt、默认线宽0.40pt；双线仍要有可见间隙。符号库、图形ID和原图优先规则见[截图与行内符号](inline-notation.md)。

## 构建器接口

`paragraphs`按阅读顺序。每项可写`role+text`或`runs`；每个run含`text/role`。可用角色：body、major、topic、term、concept、rule、code、code_core、identifier、identifier_core、comment、output、gloss、circle。

- `major`可带chapter_id防止重复章；topic用于真实主题；concept用于深蓝小标题，不能只凭数字前缀选择。
- `rule`是红色加粗；`term`是黑色加粗；普通英文使用body。
- `code_template`中`{{...}}`为灰底可替换内容，其余为黑底固定语法；各行保持在同一块。
- `code_core`继承code黑底/加粗，仅改字色95DCF7；identifier_core继承identifier灰底/普通字重。
- `keep_next/keep_lines`用于局部整体；`column_break_before:true`只用于用户要求或完整知识块确需换栏，不默认每主题换栏。
- `image:{path,width_pt,alt}`插入已看过的源截图并自动保持比例/行高。
- `clone_paragraph`仅限有意复用所选reference本身的组件/关系；不能将其他DOCX索引混入当前reference。模板内容、示范圈号和特定课程强制分页不复制进新正文。

```json
{"title":"Example Cheatsheet","paragraphs":[
  {"role":"major","chapter_id":"one","text":"Chapter 1 Example"},
  {"role":"topic","text":"I. Topic"},
  {"role":"concept","text":"1. A real subtopic"},
  {"runs":[{"role":"body","text":"(1) "},{"role":"term","text":"Term:"},{"role":"body","text":" short definition; "},{"role":"rule","text":"deciding condition"}]},
  {"runs":[{"role":"circle","text":"①"},{"role":"body","text":" Syntax:"}],"keep_next":true},
  {"code_template":"SELECT {{column}} FROM {{table_name}} WHERE {{condition}};"},
  {"runs":[{"role":"circle","text":"②"},{"role":"body","text":" Short explanation. 简短提示。"}]}
]}
```

接口示例只说明排版，不构成新课程必写清单。脚本不替代内容判断。

## 渲染与局限

使用同一渲染引擎比较前后版本。缺Abadi/等线不能静默替换；render helper可把本机合法Office字体加入临时fontconfig，不全局安装或分发字体。Word与LibreOffice仍可能分页不同；硬性页数时优先做Word原生复核。检查XML数值不能代替每页PNG视觉检查。
