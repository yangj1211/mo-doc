.PHONY: html html-zh html-en clean

BUILD = ../build/html/matrixone-intelligence

# 见 matrixone/Makefile 的注释,结构完全对称。

html-zh:
	SPHINX_LANG=zh_CN uv run sphinx-build -a -c . -D language=zh_CN -b html source/zh $(BUILD)/zh

html-en:
	SPHINX_LANG=en uv run sphinx-build -a -c . -D language=en -b html source/en $(BUILD)/en

html: html-zh html-en

clean:
	rm -rf $(BUILD)
