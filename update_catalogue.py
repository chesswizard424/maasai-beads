#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil
import re
import subprocess
import sys

PRODUCTS = Path("js/products.js")

if not PRODUCTS.exists():
    print("ERROR: js/products.js not found.")
    sys.exit(1)

# ------------------------------------------------------------
# PRICE LIST
# ------------------------------------------------------------

prices = {
    # Necklaces
    "MB-NK-001": 4000,
    "MB-NK-002": 2000,
    "MB-NK-003": 4500,
    "MB-NK-004": 4000,
    "MB-NK-005": 4000,
    "MB-NK-006": 3500,
    "MB-NK-007": 2500,
    "MB-NK-008": 4000,
    "MB-NK-009": 3000,
    "MB-NK-010": 4000,
    "MB-NK-011": 3000,
    "MB-NK-012": 2500,
    "MB-NK-013": 1000,
    "MB-NK-014": 2000,
    "MB-NK-015": 2000,
    "MB-NK-016": 3500,
    "MB-NK-017": 1500,
    "MB-NK-018": 3500,
    "MB-NK-019": 5000,
    "MB-NK-020": 4500,
    "MB-NK-021": 1500,
    "MB-NK-022": 1500,
    "MB-NK-023": 14000,
    "MB-NK-024": 250,
    "MB-NK-025": 8000,
    "MB-NK-026": 1200,
    "MB-NK-027": 4500,
    "MB-NK-028": 8000,
    "MB-NK-029": 3000,
    "MB-NK-030": 250,
    "MB-NK-031": 2500,
    "MB-NK-032": 2000,
    "MB-NK-033": 6000,
    "MB-NK-034": 3500,
    "MB-NK-035": 2000,
    "MB-NK-036": 1000,
    "MB-NK-037": 3000,
    "MB-NK-038": 250,
    "MB-NK-039": 8000,
    "MB-NK-040": 5000,
    "MB-NK-041": 4500,
    "MB-NK-042": 3500,
    "MB-NK-043": 1500,
    "MB-NK-044": 8000,
    "MB-NK-045": 2000,
    "MB-NK-046": 4500,
    "MB-NK-047": 5500,
    "MB-NK-048": 3500,
    "MB-NK-049": 3500,
    "MB-NK-050": 3000,

    # Bracelets
    "MB-BR-001": 1500,
    "MB-BR-002": 2000,
    "MB-BR-003": 1500,
    "MB-BR-004": 800,
    "MB-BR-005": 1500,
    "MB-BR-006": 1500,
    "MB-BR-007": 500,
    "MB-BR-008": 800,
    "MB-BR-009": 1000,
    "MB-BR-010": 1000,
    "MB-BR-011": 1000,
    "MB-BR-012": 1500,
    "MB-BR-013": 1000,
    "MB-BR-014": 500,
    "MB-BR-015": 1000,
    "MB-BR-016": 500,
    "MB-BR-017": 1500,
    "MB-BR-018": 1500,
    "MB-BR-019": 1500,
    "MB-BR-020": 1200,
    "MB-BR-021": 1000,
    "MB-BR-022": 1500,
    "MB-BR-023": 550,
    "MB-BR-024": 400,
    "MB-BR-025": 1500,
    "MB-BR-026": 1000,
    "MB-BR-027": 550,
    "MB-BR-028": 1000,
    "MB-BR-029": 1500,
    "MB-BR-030": 1000,
    "MB-BR-031": 1500,
    "MB-BR-032": 1500,
    "MB-BR-033": 1000,
    "MB-BR-034": 1000,
    "MB-BR-035": 1500,
    "MB-BR-036": 500,
    "MB-BR-037": 1500,
    "MB-BR-038": 1250,
    "MB-BR-039": 650,
    "MB-BR-040": 2000,
    "MB-BR-041": 1500,
    "MB-BR-042": 1000,
    "MB-BR-043": 500,
    "MB-BR-044": 1200,
    "MB-BR-045": 1500,
    "MB-BR-046": 1500,
    "MB-BR-047": 1000,
    "MB-BR-048": 500,
    "MB-BR-049": 1500,
    "MB-BR-050": 500,
    "MB-BR-051": 1000,
    "MB-BR-052": 2000,
    "MB-BR-053": 750,
    "MB-BR-054": 1200,
    "MB-BR-055": 2000,
    "MB-BR-056": 1200,
    "MB-BR-057": 1000,
    "MB-BR-058": 1000,
    "MB-BR-059": 2000,
    "MB-BR-060": 1000,
    "MB-BR-061": 2500,

    # Earrings
    "MB-ER-001": 250,
    "MB-ER-002": 250,
    "MB-ER-003": 250,
    "MB-ER-004": 250,
    "MB-ER-005": 350,
    "MB-ER-006": 250,
    "MB-ER-007": 250,
    "MB-ER-008": 350,
    "MB-ER-009": 350,
    "MB-ER-010": 300,
    "MB-ER-011": 400,

    # Other
    "MB-OTH-001": 2000,
    "MB-OTH-002": 5500,
    "MB-OTH-003": 5000,
    "MB-OTH-004": 350,
    "MB-OTH-005": 3500,
    "MB-OTH-006": 6500,
    "MB-OTH-007": 1500,
    "MB-OTH-008": 500,
    "MB-OTH-009": 3000,
    "MB-OTH-010": 3500,
    "MB-OTH-011": 5000,

    # Belts
    "MB-BELT-001": 6000,
    "MB-BELT-002": 6000,
    "MB-BELT-003": 8000,
    "MB-BELT-004": 5000,
    "MB-BELT-005": 5000,
    "MB-BELT-006": 5000,
    "MB-BELT-007": 5000,
    "MB-BELT-008": 5000,
    "MB-BELT-009": 5000,
    "MB-BELT-010": 8000,
    "MB-BELT-011": 5500,
    "MB-BELT-012": 5000,
    "MB-BELT-013": 5000,
    "MB-BELT-014": 5000,
    "MB-BELT-015": 5000,
    "MB-BELT-016": 5000,
    "MB-BELT-017": 6000,
    "MB-BELT-018": 5000,
    "MB-BELT-019": 5500,
    "MB-BELT-020": 5000,
    "MB-BELT-021": 5000,
    "MB-BELT-022": 5000,
    "MB-BELT-023": 8000,
    "MB-BELT-024": 6000,
    "MB-BELT-025": 5500,
    "MB-BELT-026": 5000,
    "MB-BELT-027": 4500,
    "MB-BELT-028": 8000,

    # Hats
    "MB-HAT-001": 2500,
    "MB-HAT-002": 2500,
    "MB-HAT-003": 2500,
    "MB-HAT-004": 2500,

    # Outfits
    "MB-OUT-001": 8500,
    "MB-OUT-002": 8500,
    "MB-OUT-003": 8500,
    "MB-OUT-004": 8500,
    "MB-OUT-005": 8500,

    # Sandals — exact current 12-product mapping
    "MB-SND-001": 2500,
    "MB-SND-002": 3000,
    "MB-SND-003": 2500,
    "MB-SND-004": 3500,
    "MB-SND-005": 3000,
    "MB-SND-006": 4500,
    "MB-SND-007": 3500,
    "MB-SND-008": 5000,
    "MB-SND-009": 3500,
    "MB-SND-010": 3000,
    "MB-SND-011": 2550,
    "MB-SND-012": 2500,

    # Bags
    "MB-BAG-001": 3000,
    "MB-BAG-002": 2500,
    "MB-BAG-003": 3500,
    "MB-BAG-004": 3000,
    "MB-BAG-005": 10000,
    "MB-BAG-006": 10000,

    # Pouches
    "MB-POU-001": 1500,
    "MB-POU-002": 250,

    # Mats
    "MB-MAT-001": 2000,
    "MB-MAT-002": 2000,
    "MB-MAT-003": 2000,
    "MB-MAT-004": 1000,
    "MB-MAT-005": 1500,
    "MB-MAT-006": 1000,
    "MB-MAT-007": 1500,
    "MB-MAT-008": 1500,
    "MB-MAT-009": 2000,
    "MB-MAT-010": 1000,

    # Headwear
    "MB-HDW-001": 2500,
    "MB-HDW-002": 3500,

    # Key holders
    "MB-KH-001": 150,
    "MB-KH-002": 550,

    # Rungus
    "MB-RG-001": 1500,
    "MB-RG-002": 3000,
}

# ------------------------------------------------------------
# SPECIAL CATEGORY MOVES
# ------------------------------------------------------------

category_changes = {
    "MB-NK-013": "Headwear",
    "MB-NK-024": "Earrings",
    "MB-NK-025": "Belts",
}

# ------------------------------------------------------------
# BACKUP
# ------------------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = PRODUCTS.with_name(f"products.js.backup_{timestamp}")

shutil.copy2(PRODUCTS, backup)
print(f"Backup created: {backup}")

text = PRODUCTS.read_text(encoding="utf-8")

# ------------------------------------------------------------
# EXTRACT TOP-LEVEL PRODUCT BLOCKS
# ------------------------------------------------------------

pattern = re.compile(
    r'(?ms)^    ("MB-[A-Z0-9-]+": \{\n.*?^    \},)(?=\n|$)'
)

matches = list(pattern.finditer(text))

if not matches:
    print("ERROR: No product blocks found.")
    sys.exit(1)

blocks = [m.group(1) for m in matches]

print(f"Product blocks found: {len(blocks)}")

# ------------------------------------------------------------
# FIX SANDAL IDs USING THEIR ACTUAL IMAGE NUMBERS
# ------------------------------------------------------------

sandal_image_to_id = {
    "050.png": "MB-SND-009",
    "062.png": "MB-SND-010",
    "086.png": "MB-SND-011",
    "116.png": "MB-SND-012",
}

fixed_blocks = []

for block in blocks:

    # Identify image filename.
    image_match = re.search(r'image:\s*"[^"]*/([^"/]+\.png)"', block)
    image_name = image_match.group(1) if image_match else None

    # Rename the four sandal entries that were out of sequence.
    if image_name in sandal_image_to_id:
        new_id = sandal_image_to_id[image_name]

        block = re.sub(
            r'^    "MB-SND-\d{3}": \{',
            f'    "{new_id}": {{',
            block,
            count=1,
            flags=re.MULTILINE
        )

    fixed_blocks.append(block)

blocks = fixed_blocks

# ------------------------------------------------------------
# UPDATE CATEGORIES
# ------------------------------------------------------------

for i, block in enumerate(blocks):

    id_match = re.search(r'^    "(MB-[A-Z0-9-]+)": \{', block, re.MULTILINE)

    if not id_match:
        continue

    product_id = id_match.group(1)

    if product_id in category_changes:
        block = re.sub(
            r'category:\s*"[^"]+"',
            f'category: "{category_changes[product_id]}"',
            block,
            count=1
        )

    blocks[i] = block

# ------------------------------------------------------------
# UPDATE PRICES
# ------------------------------------------------------------

present_ids = []
updated_ids = []

for i, block in enumerate(blocks):

    id_match = re.search(r'^    "(MB-[A-Z0-9-]+)": \{', block, re.MULTILINE)

    if not id_match:
        continue

    product_id = id_match.group(1)
    present_ids.append(product_id)

    if product_id in prices:
        block = re.sub(
            r'price:\s*\d+',
            f'price: {prices[product_id]}',
            block,
            count=1
        )
        updated_ids.append(product_id)

    blocks[i] = block

# ------------------------------------------------------------
# MOVE MB-BR-061 AFTER MB-BR-060
# ------------------------------------------------------------

bracelet_061 = None
remaining = []

for block in blocks:

    if re.match(r'^    "MB-BR-061": \{', block):
        bracelet_061 = block
    else:
        remaining.append(block)

if bracelet_061 is None:
    print("ERROR: MB-BR-061 not found.")
    sys.exit(1)

blocks = remaining

inserted = False
new_blocks = []

for block in blocks:
    new_blocks.append(block)

    if re.match(r'^    "MB-BR-060": \{', block):
        new_blocks.append(bracelet_061)
        inserted = True

if not inserted:
    print("ERROR: MB-BR-060 not found.")
    sys.exit(1)

blocks = new_blocks

# ------------------------------------------------------------
# REBUILD FILE
# ------------------------------------------------------------

new_text = "{\n" + "\n".join(blocks) + "\n};\n"

# Preserve an existing export line if the file uses one.
if "export default products" in text:
    new_text += "\nexport default products;\n"

PRODUCTS.write_text(new_text, encoding="utf-8")

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

final_text = PRODUCTS.read_text(encoding="utf-8")

ids = re.findall(r'^    "(MB-[A-Z0-9-]+)": \{', final_text, re.MULTILINE)

unique_ids = set(ids)

print()
print("========== VALIDATION ==========")
print(f"Product blocks: {len(ids)}")
print(f"Unique IDs:     {len(unique_ids)}")

if len(ids) != 205 or len(unique_ids) != 205:
    print("ERROR: Expected exactly 205 unique products.")
    print("Duplicate IDs:")

    seen = set()
    for pid in ids:
        if pid in seen:
            print(f"  DUPLICATE: {pid}")
        seen.add(pid)

    sys.exit(1)

print("✓ 205 unique products")

# Check zero prices
zero_price_ids = []

for block in re.finditer(
    r'(?ms)^    "(MB-[A-Z0-9-]+)": \{\n.*?^    \},',
    final_text
):
    block_text = block.group(0)

    id_match = re.search(r'^    "(MB-[A-Z0-9-]+)":', block_text, re.MULTILINE)
    price_match = re.search(r'price:\s*(\d+)', block_text)

    if id_match and price_match and int(price_match.group(1)) == 0:
        zero_price_ids.append(id_match.group(1))

if zero_price_ids:
    print("ERROR: Products still have price 0:")
    for pid in zero_price_ids:
        print(f"  {pid}")
    sys.exit(1)

print("✓ No products with price 0")

# Category counts
category_counts = {}

for block in re.finditer(
    r'(?ms)^    "(MB-[A-Z0-9-]+)": \{\n.*?^    \},',
    final_text
):
    block_text = block.group(0)

    cat_match = re.search(r'category:\s*"([^"]+)"', block_text)

    if cat_match:
        category = cat_match.group(1)
        category_counts[category] = category_counts.get(category, 0) + 1

print()
print("Category counts:")

for category in sorted(category_counts):
    print(f"  {category}: {category_counts[category]}")

expected_categories = {
    "Bags": 5,
    "Beaded Hats": 4,
    "Beaded Outfits": 5,
    "Belts": 28,
    "Bracelets": 61,
    "Earrings": 13,
    "Headwear": 3,
    "Key Holders": 2,
    "Maasai Beaded Sandals": 12,
    "Maasai Rungus": 2,
    "Mats": 10,
    "Necklaces": 47,
    "Other": 11,
    "Pouches": 2,
}

if category_counts != expected_categories:
    print()
    print("ERROR: Category counts do not match expected final counts.")
    print("Expected:")
    for k, v in sorted(expected_categories.items()):
        print(f"  {k}: {v}")
    sys.exit(1)

print("✓ Category counts match expected 205-product catalogue")

# Check sandal IDs
sandal_ids = sorted(
    [pid for pid in unique_ids if pid.startswith("MB-SND-")]
)

expected_sandals = [f"MB-SND-{i:03d}" for i in range(1, 13)]

if sandal_ids != expected_sandals:
    print("ERROR: Sandal IDs are not exactly 001–012.")
    print("Found:", sandal_ids)
    sys.exit(1)

print("✓ Sandals numbered MB-SND-001 through MB-SND-012")

# Check bracelet order
br_ids = [
    pid for pid in ids
    if pid.startswith("MB-BR-")
]

if br_ids[-1] != "MB-BR-061":
    print("ERROR: MB-BR-061 is not the last bracelet.")
    sys.exit(1)

print("✓ MB-BR-061 is after MB-BR-060")

# Node syntax check
result = subprocess.run(
    ["node", "--check", str(PRODUCTS)],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("ERROR: node --check failed.")
    print(result.stderr)
    sys.exit(1)

print("✓ node --check passed")

# Check expected price IDs that actually exist.
unused_prices = sorted(set(prices) - set(unique_ids))

if unused_prices:
    print()
    print("Price-list IDs not present in current catalogue:")
    for pid in unused_prices:
        print(f"  {pid}")

print()
print("================================")
print("CATALOGUE UPDATE SUCCESSFUL")
print("================================")
print(f"Backup: {backup}")
print(f"Products: {len(unique_ids)}")
