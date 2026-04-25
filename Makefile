.PHONY: html serve clean

BUILD = build/html

html:
	@# -a：写出所有输出文件（即使源未变动），避免 Sphinx 增量构建跳过 CSS/JS 更新
	uv run sphinx-build -a -b html source    $(BUILD)/zh
	uv run sphinx-build -a -b html source_en $(BUILD)/en
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixOne Docs</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/index.html
	@echo ""
	@echo "→ Chinese: $(BUILD)/zh/index.html"
	@echo "→ English: $(BUILD)/en/index.html"

serve: html
	@echo ""
	@echo "→ http://localhost:8000"
	@echo ""
	cd $(BUILD) && uv run python -m http.server 8000

clean:
	rm -rf build
