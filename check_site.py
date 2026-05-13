from pathlib import Path


ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

html = INDEX.read_text(encoding="utf-8")
normalized_html = " ".join(html.split())

required_text = [
    "Сдаётся 2-комн. квартира, 52,1 м²",
    "в ЖК «Холланд Парк»",
    "Сдаётся · Москва",
    "Сдаётся уютная двухкомнатная квартира в современном ЖК «Holland Park»",
    "квартира остаётся в новом состоянии",
    "Можно с детьми от 6 лет, без домашних животных.",
    "Волоколамское ш., 71/13к1",
    "м. Тушинская",
    "МЦД Стрешнево",
    "10 мин.",
    "Комиссия",
    "Предоплата",
    "Срок аренды",
    "ЖКХ и счётчики включены",
    "Залог 100 000 ₽",
    "Интернет",
    "Телевизор",
    "В Квартире есть",
    "52,1",
]

required_images = [
    "images/kitchen-entry.jpg",
    "images/neighborhood-park.jpg",
    "images/view-window.jpg",
]

for text in required_text:
    assert text in normalized_html, f"Missing text: {text}"

for image in required_images:
    assert image in html, f"Image not referenced: {image}"
    assert (ROOT / image).exists(), f"Image file missing: {image}"

assert "svg-icon" in html, "Expected inline SVG icon styling"
assert html.count('class="photo photo-') >= 11, "Expected expanded gallery"

for image in [
    "images/listing-specs.jpg",
    "images/rental-terms.jpg",
    "images/amenities-list.jpg",
]:
    assert image not in html, f"Screenshot should not be embedded in page: {image}"

assert 'class="terms-grid"' in html, "Expected concise rental terms cards"
assert "Главное без лишних деталей" not in html, "Terms section heading should be removed"
assert "images/living-2.jpg" not in html, "Requested living room photo should be removed"
assert "Всё включено" not in html, "Amenities heading should be renamed"
assert 'class="apartment-tags"' not in html, "Apartment tag block should be removed"
assert "hero-stat-icon" not in html, "Header stats should be restored without icons"
assert "hero-chip-icon" not in html, "Header transport chips should be restored without icons"
assert 'class="hero-address"' in html, "Address should be moved into a readable hero address row"
assert "marker=55.815418%2C37.426132" in html, "Map marker should match Volokolamskoe sh., 71/13k1"

gallery_order = [
    "images/kitchen-entry.jpg",
    "images/kitchen-2.jpg",
    "images/kitchen-1.jpg",
    "images/living-1.jpg",
    "images/living-3.jpg",
    "images/bedroom-1.jpg",
    "images/bedroom-2.jpg",
    "images/view-window.jpg",
    "images/building.jpg",
    "images/neighborhood-park.jpg",
    "images/church.jpg",
]
gallery_start = html.index('<section class="gallery">')
gallery_end = html.index("</section>", gallery_start)
gallery_html = html[gallery_start:gallery_end]
positions = [gallery_html.index(image) for image in gallery_order]
assert positions == sorted(positions), "Gallery should show apartment photos before view and neighborhood"

print("Site content checks passed.")
