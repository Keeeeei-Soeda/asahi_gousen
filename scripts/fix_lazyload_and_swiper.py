#!/usr/bin/env python3
"""
全HTMLファイルに対して以下を実施:
1. lazyload img (data-src) → 直接 src に書き換え
2. data-srcset → srcset に書き換え
3. Swiper.js / CSS を CDN から追加し、ページ内の Swiper を初期化
"""
import os
import re
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent / "asahigousen"
html_files = sorted(SITE_DIR.rglob("*.html"))

# ---- Swiper 初期化スクリプト（</body> 直前に挿入） ----
SWIPER_RESOURCES = """\
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.elementor-image-carousel-wrapper.swiper').forEach(function(el) {
    var settingsAttr = el.querySelector('[data-settings]');
    var settings = {};
    if (settingsAttr) {
      try { settings = JSON.parse(settingsAttr.getAttribute('data-settings')); } catch(e) {}
    }
    new Swiper(el, {
      slidesPerView: parseInt(settings.slides_to_show) || 3,
      loop: settings.infinite === 'yes',
      autoplay: settings.autoplay === 'yes'
        ? { delay: parseInt(settings.autoplay_speed) || 5000, pauseOnMouseEnter: settings.pause_on_hover === 'yes' }
        : false,
      speed: parseInt(settings.speed) || 500,
      navigation: settings.navigation !== 'none'
        ? { nextEl: el.querySelector('.elementor-swiper-button-next'),
            prevEl: el.querySelector('.elementor-swiper-button-prev') }
        : false,
      pagination: { el: el.querySelector('.swiper-pagination'), clickable: true },
    });
  });
});
</script>"""

total_lazy_fixed = 0
total_swiper_added = 0

for html_path in html_files:
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    original = content
    counter = [0]

    # 1. data-src → src (lazyload img)
    #    <img ... class="lazyload ..." src="data:image/..." data-src="REAL_URL" ...>
    #    → src="REAL_URL" class（lazyload除去）
    def fix_lazyload_img(m):
        tag = m.group(0)
        # data-src を src に昇格
        data_src_m = re.search(r'\bdata-src="([^"]+)"', tag)
        if not data_src_m:
            return tag
        real_src = data_src_m.group(1)
        # src="data:..." を real_src に置換
        tag = re.sub(r'\bsrc="data:[^"]*"', f'src="{real_src}"', tag)
        # data-src 属性を削除
        tag = re.sub(r'\s*data-src="[^"]*"', '', tag)
        # lazyload クラスを除去
        tag = re.sub(r'\blazyload\s*', '', tag)
        counter[0] += 1
        return tag

    content = re.sub(r'<img\b[^>]*\bdata-src="[^"]*"[^>]*>', fix_lazyload_img, content)

    # 2. data-srcset → srcset
    content = re.sub(r'\bdata-srcset="', 'srcset="', content)

    # 3. data-sizes → sizes
    content = re.sub(r'\bdata-sizes="', 'sizes="', content)

    # 4. Swiper がある場合のみリソースを追加（重複防止）
    has_swiper = 'elementor-image-carousel-wrapper swiper' in content
    swiper_already = 'swiper-bundle.min.js' in content

    if has_swiper and not swiper_already:
        content = content.replace('</body>', SWIPER_RESOURCES + '\n</body>', 1)
        total_swiper_added += 1

    lazy_count = counter[0]
    if content != original:
        html_path.write_text(content, encoding="utf-8")
        rel = html_path.relative_to(SITE_DIR)
        print(f"  [{rel}] lazyload修正:{lazy_count}件"
              + (" + Swiper追加" if has_swiper and not swiper_already else ""))
        total_lazy_fixed += lazy_count

print(f"\n完了: lazyload修正 {total_lazy_fixed}件 / Swiper初期化追加 {total_swiper_added}ページ")
