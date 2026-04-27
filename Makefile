.PHONY: html serve clean matrixone matrixone-intelligence picker redirects

BUILD = build/html

# 顶级入口:把每个产品的构建委派给产品自身的 Makefile,
# 再补两个产品级 redirect 和一个根目录产品选择页。
#
# 单独构建一个产品:cd matrixone && make html
# 单独构建一种语言:cd matrixone && make html-zh / make html-en

html: matrixone matrixone-intelligence redirects picker
	@echo ""
	@echo "→ Picker:                          $(BUILD)/index.html"
	@echo "→ MatrixOne (auto):                $(BUILD)/matrixone/"
	@echo "→ MatrixOne Chinese:               $(BUILD)/matrixone/zh/"
	@echo "→ MatrixOne English:               $(BUILD)/matrixone/en/"
	@echo "→ MatrixOne Intelligence (auto):   $(BUILD)/matrixone-intelligence/"
	@echo "→ MatrixOne Intelligence Chinese:  $(BUILD)/matrixone-intelligence/zh/"
	@echo "→ MatrixOne Intelligence English:  $(BUILD)/matrixone-intelligence/en/  (5 core docs only)"

matrixone:
	$(MAKE) -C matrixone html

matrixone-intelligence:
	$(MAKE) -C matrixone-intelligence html

redirects:
	@mkdir -p $(BUILD)/matrixone $(BUILD)/matrixone-intelligence
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixOne</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/matrixone/index.html
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixOne Intelligence</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/matrixone-intelligence/index.html

picker:
	uv run python scripts/build_picker.py $(BUILD)/index.html

serve: html
	@echo ""
	@echo "→ http://localhost:8000"
	@echo ""
	cd $(BUILD) && uv run python -m http.server 8000

clean:
	rm -rf build
