# 手动构建与验证

普通使用者直接让 Codex 使用 Skill 即可。以下供维护工具或排查排版时使用。

## 依赖

Python 3.10+；Python包见根目录`requirements.txt`。生成Word需要python-docx和lxml，PDF页数检查需要pypdf。字体需要本机合法安装的Abadi MT Condensed Light和等线Light，本仓库不分发字体。

Codex桌面环境优先使用其workspace dependency loader给出的Python和Documents渲染工具；其他环境可自行准备Python依赖与Word/LibreOffice渲染器。构建器本身不会调用AI或网络接口，也不会从PPT自动推断内容。

## 构建

在仓库根目录执行，`PYTHON_BIN`替换为选定的Python解释器路径：

```bash
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/build_cheatsheet.py \
  examples/style-demo.json work/demo.docx
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/audit_cheatsheet.py \
  work/demo.docx --expected-chapters 3
```

`{{...}}`是可替换语法，输出为灰底；固定部分黑底。需要少数淡蓝核心token时使用显式code_core/identifier_core runs。JSON字段和角色见[排版规范](../skills/artifact-template-cheatsheet/references/formatting.md)。

仓库中的可编辑示例还插入了原生小符号，插入步骤由`examples/build_demo.py`提供；直接运行此脚本可重建含全部17类符号的示例。它将输出写到`work/`，不会修改保留模板。

## 渲染

已具备Documents工具时，把DOCUMENTS_SKILL_DIR设为其实际目录：

```bash
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/render_with_fonts.py \
  work/demo.docx --documents-skill-dir "$DOCUMENTS_SKILL_DIR" --outdir work/render
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/audit_cheatsheet.py \
  work/demo.docx --expected-chapters 3 \
  --rendered-pdf work/render/demo.pdf --page-limit 1
```

没有Documents工具时，可用Word导出PDF，再将每页转为图片检查。render_with_fonts.py是Documents的包装器，不是独立渲染器；它在支持的Mac环境把本机Word字体加入临时fontconfig，未复制或安装字体。若缺少字体，不能把替代字体结果声称为精确复现。

## 验证边界

- Audit检查页面参数、字号、圈号域、代码颜色和图片布局，不判断课程内容是否完整或正确。
- 页数必须来自实际渲染的PDF，不能从DOCX XML推断。
- 逐页打开图片，检查字体、圈号、代码黑灰边界、裁图、箭头和双线间隙；Word与LibreOffice可能分页不同。
- 学生的材料、答案、生成文件、字体和渲染缓存不进入本仓库。更新公开包采用文件白名单，不复制私人skill整个assets目录。
