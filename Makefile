.PHONY: html serve clean

BUILD = build/html

# URL 结构：/<产品>/<语言>/...
#   /matrixone/zh/        中文
#   /matrixone/en/        英文
#   /intelligence/zh/     中文（暂无英文）
#   /matrixone/index.html       浏览器语言自动选 zh/en
#   /intelligence/index.html    永远跳 zh/
#   /index.html                 产品选择页（两张卡片）

html:
	@# -a：写出所有输出文件（即使源未变动），避免 Sphinx 增量构建跳过 CSS/JS 更新
	uv run sphinx-build -a -b html matrixone       $(BUILD)/matrixone/zh
	uv run sphinx-build -a -b html matrixone_en    $(BUILD)/matrixone/en
	uv run sphinx-build -a -b html intelligence    $(BUILD)/intelligence/zh
	uv run sphinx-build -a -b html intelligence_en $(BUILD)/intelligence/en
	@# matrixone：浏览器语言自动选 zh/en
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixOne</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/matrixone/index.html
	@# intelligence：浏览器语言自动选 zh/en（en 站只含 4 篇核心文档 + 主页）
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixOne Intelligence</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/intelligence/index.html
	@# 根目录：产品选择页（脚本生成，模板见 scripts/build_picker.py）
	uv run python scripts/build_picker.py $(BUILD)/index.html
	@echo ""
	@echo "→ Picker:                 $(BUILD)/index.html"
	@echo "→ MatrixOne (auto):       $(BUILD)/matrixone/"
	@echo "→ MatrixOne Chinese:      $(BUILD)/matrixone/zh/"
	@echo "→ MatrixOne English:      $(BUILD)/matrixone/en/"
	@echo "→ Intelligence (auto):    $(BUILD)/intelligence/"
	@echo "→ Intelligence Chinese:   $(BUILD)/intelligence/zh/"
	@echo "→ Intelligence English:   $(BUILD)/intelligence/en/  (4 core docs only)"

serve: html
	@echo ""
	@echo "→ http://localhost:8000"
	@echo ""
	cd $(BUILD) && uv run python -m http.server 8000

clean:
	rm -rf build
