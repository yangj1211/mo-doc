.PHONY: html html-zh html-en clean

# 输出目录:matrixone 产品的 build 落到仓库根目录的 build/html/matrixone/
# 不在 matrixone/build 下建,避免和根目录 Makefile 的产物分散两处。
BUILD = ../build/html/matrixone

# Sphinx 通过 -c 指定 confdir(本目录),位置参数指定 sourcedir。
# SPHINX_LANG 环境变量被 conf.py 用来切换品牌标题(中文 → 英文 → 中文)。
# -D language= 是 Sphinx 标准语言开关,用于搜索分词、UI 字符串等。
# -a 强制重写所有输出,避免增量构建跳过 CSS/JS 更新。

html-zh:
	SPHINX_LANG=zh_CN uv run sphinx-build -a -c . -D language=zh_CN -b html source/zh $(BUILD)/zh

html-en:
	SPHINX_LANG=en uv run sphinx-build -a -c . -D language=en -b html source/en $(BUILD)/en

html: html-zh html-en

clean:
	rm -rf $(BUILD)
