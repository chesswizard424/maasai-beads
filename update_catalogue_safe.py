#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import re
import shutil
import subprocess
import sys

FILE = Path("js/products.js")

# ------------------------------------------------------------
# PRICE MAP
# ------------------------------------------------------------

prices = {
    # NECKLACES
    "MB-NK-001": 4000, "MB-NK-002": 2000, "MB-NK-003": 4500,
    "MB-NK-004": 4000, "MB-NK-005": 4000, "MB-NK-006": 3500,
    "MB-NK-007": 2500, "MB-NK-008": 4000, "MB-NK-009": 3000,
    "MB-NK-010": 4000, "MB-NK-011": 3000, "MB-NK-012": 2500,
    "MB-NK-014": 2000, "MB-NK-015": 2000, "MB-NK-016": 3500,
    "MB-NK-017": 1500, "MB-NK-018": 3500, "MB-NK-019": 5000,
    "MB-NK-020": 4500, "MB-NK-021": 1500, "MB-NK-022": 1500,
    "MB-NK-023": 14000, "MB-NK-026": 1200, "MB-NK-027": 4500,
    "MB-NK-028": 8000, "MB-NK-029": 3000, "MB-NK-030": 250,
    "MB-NK-031": 2500, "MB-NK-032": 2000, "MB-NK-033": 6000,
    "MB-NK-034": 3500, "MB-NK-035": 2000, "MB-NK-036": 1000,
    "MB-NK-037": 3000, "MB-NK-038": 250, "MB-NK-039": 8000,
    "MB-NK-040": 5000, "MB-NK-041": 4500, "MB-NK-042": 3500,
    "MB-NK-043": 1500, "MB-NK-044": 8000, "MB-NK-045": 2000,
    "MB-NK-046": 4500, "MB-NK-047": 5500, "MB-NK-048": 3500,
    "MB-NK-049": 3500, "MB-NK-050": 3000,

    # BRACELETS
    "MB-BR-001": 1500, "MB-BR-002": 2000, "MB-BR-003": 1500,
    "MB-BR-004": 800, "MB-BR-005": 1500, "MB-BR-006": 1500,
    "MB-BR-007": 500, "MB-BR-008": 800, "MB-BR-009": 1000,
    "MB-BR-010": 1000, "MB-BR-011": 1000, "MB-BR-012": 1500,
    "MB-BR-013": 1000, "MB-BR-014": 500, "MB-BR-015": 1000,
    "MB-BR-016": 500, "MB-BR-017": 1500, "MB-BR-018": 1500,
    "MB-BR-019": 1500, "MB-BR-020": 1200, "MB-BR-021": 1000,
    "MB-BR-022": 1500, "MB-BR-023": 550, "MB-BR-024": 400,
    "MB-BR-025": 1500, "MB-BR-026": 1000, "MB-BR-027": 550,
    "MB-BR-028": 1000, "MB-BR-029": 1500, "MB-BR-030": 1000,
    "MB-BR-031": 1500, "MB-BR-032": 1500, "MB-BR-033": 1000,
    "MB-BR-034": 1000, "MB-BR-035": 1500, "MB-BR-036": 500,
    "MB-BR-037": 1500, "MB-BR-038": 1250, "MB-BR-039": 650,
    "MB-BR-040": 2000, "MB-BR-041": 1500, "MB-BR-042": 1000,
    "MB-BR-043": 500, "MB-BR-044": 1200, "MB-BR-045": 1500,
    "MB-BR-046": 1500, "MB-BR-047": 1000, "MB-BR-048": 500,
    "MB-BR-049": 1500, "MB-BR-050": 500, "MB-BR-051": 1000,
    "MB-BR-052": 2000, "MB-BR-053": 750, "MB-BR-054": 1200,
    "MB-BR-055": 2000, "MB-BR-056": 1200, "MB-BR-057": 1000,
    "MB-BR-058": 1000, "MB-BR-059": 2000, "MB-BR-060": 1000,
    "MB-BR-061": 2500,

    # EARRINGS
    "MB-ER-001": 250, "MB-ER-002": 250, "MB-ER-003": 250,
    "MB-ER-004": 250, "MB-ER-005": 350, "MB-ER-006": 250,
    "MB-ER-007": 250, "MB-ER-008": 350, "MB-ER-009": 350,
    "MB-ER-010": 300, "MB-ER-011": 400,
    "MB-ER-012": 250, "MB-ER-013": 250,

    # OTHER
    "MB-OTH-001": 2000, "MB-OTH-002": 5500, "MB-OTH-003": 5000,
    "MB-OTH-004": 350, "MB-OTH-005": 3500, "MB-OTH-006": 6500,
    "MB-OTH-007": 1500, "MB-OTH-008": 500, "MB-OTH-009": 3000,
    "MB-OTH-010": 3500, "MB-OTH-011": 5000,

    # BELTS
    "MB-BELT-001": 6000, "MB-BELT-002": 6000, "MB-BELT-003": 8000,
    "MB-BELT-004": 5000, "MB-BELT-005": 5000, "MB-BELT-006": 5000,
    "MB-BELT-007": 5000, "MB-BELT-008": 5000, "MB-BELT-009": 5000,
    "MB-BELT-010": 8000, "MB-BELT-011": 5500, "MB-BELT-012": 5000,
    "MB-BELT-013": 5000, "MB-BELT-014": 5000, "MB-BELT-015": 5000,
    "MB-BELT-016": 5000, "MB-BELT-017": 6000, "MB-BELT-018": 5000,
    "MB-BELT-019": 5500, "MB-BELT-020": 5000, "MB-BELT-021": 5000,
    "MB-BELT-022": 5000, "MB-BELT-023": 8000, "MB-BELT-024": 6000,
    "MB-BELT-025": 5500, "MB-BELT-026": 5000, "MB-BELT-027": 4500,
    "MB-BELT-028": 8000,

    # HATS
    "MB-HAT-001": 2500, "MB-HAT-002": 2500,
    "MB-HAT-003": 2500, "MB-HAT-004": 2500,

    # OUTFITS
    "MB-OUT-001": 8500, "MB-OUT-002": 8500, "MB-OUT-003": 8500,
    "MB-OUT-004": 8500, "MB-OUT-005": 8500,

    # BAGS
    "MB-BAG-001": 3000, "MB-BAG-002": 2500, "MB-BAG-003": 3500,
    "MB-BAG-004": 3000, "MB-BAG-005": 10000,

    # POUCHES
    "MB-POU-001": 1500, "MB-POU-002": 250,

    # MATS
    "MB-MAT-001": 2000, "MB-MAT-002": 2000, "MB-MAT-003": 2000,
    "MB-MAT-004": 1000, "MB-MAT-005": 1500, "MB-MAT-006": 1000,
    "MB-MAT-007": 1500, "MB-MAT-008": 1500, "MB-MAT-009": 2000,
    "MB-MAT-010": 1000,

    # HEADWEAR
    "MB-HDW-001": 2500, "MB-HDW-002": 3500,
    "MB-HDW-003": 1000,

    # KEY HOLDERS
    "MB-KH-001": 150, "MB-KH-002": 550,

    # RUNGUS
    "MB-RG-001": 1500, "MB-RG-002": 3000,

    # SANDALS
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
}


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def die(message):
    print(f"\nERROR: {message}")
    sys.exit(1)


def find_blocks(text):
    """
    Locate product blocks by their top-level product key.
    This does NOT try to parse the whole JS object.
    """
    pattern = re.compile(
        r'(?m)^(\s*)"((?:MB)-[A-Z0-9]+-\d{3})"\s*:\s*\{'
    )

    matches = list(pattern.finditer(text))
    blocks = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        blocks.append({
            "id": match.group(2),
            "start": start,
            "end": end,
            "text": text[start:end],
        })

    return blocks


def replace_field(block, field, value):
    pattern = re.compile(
        rf'(^\s*{re.escape(field)}:\s*)[^,\n]+',
        re.MULTILINE
    )

    new_block, count = pattern.subn(
        rf'\g<1>{value}',
        block,
        count=1
    )

    if count != 1:
        die(f"Could not update field '{field}' in product block.")

    return new_block


def replace_string_field(block, field, value):
    pattern = re.compile(
        rf'(^\s*{re.escape(field)}:\s*)"[^"]*"',
        re.MULTILINE
    )

    new_block, count = pattern.subn(
        rf'\g<1>"{value}"',
        block,
        count=1
    )

    if count != 1:
        die(f"Could not update string field '{field}'.")

    return new_block


def get_blocks(text):
    return find_blocks(text)


# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

if not FILE.exists():
    die(f"{FILE} does not exist.")

original = FILE.read_text()

blocks = get_blocks(original)

print(f"Product blocks detected: {len(blocks)}")

if len(blocks) != 205:
    print(
        "\nWARNING: The file currently contains "
        f"{len(blocks)} detected product blocks, not 205."
    )
    print("The script will NOT modify the file.")
    sys.exit(1)


# ------------------------------------------------------------
# BACKUP
# ------------------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = FILE.with_name(f"{FILE.name}.backup_{timestamp}")

shutil.copy2(FILE, backup)

print(f"Backup created: {backup}")


# ------------------------------------------------------------
# CONVERT BLOCK LIST TO WORKING MAP
# ------------------------------------------------------------

# Build working blocks while allowing the known duplicate
# MB-SND-010. The duplicate sandal will be resolved later
# using its image filename.

working = {}
duplicate_blocks = []

for b in blocks:
    product_id = b["id"]

    if product_id in working:
        duplicate_blocks.append(b)
    else:
        working[product_id] = b["text"]


if duplicate_blocks:
    unexpected_duplicates = []

    for b in duplicate_blocks:
        if b["id"] != "MB-SND-010":
            unexpected_duplicates.append(b["id"])

    if unexpected_duplicates:
        die(
            "Unexpected duplicate product IDs detected: "
            + ", ".join(unexpected_duplicates)
        )


if len(working) != 204:
    die(
        f"Expected 204 unique IDs before fixing the known "
        f"duplicate sandal, found {len(working)}."
    )


# The duplicate MB-SND-010 is preserved separately so that
# the sandal-image logic below can process BOTH blocks.
if duplicate_blocks:
    for b in duplicate_blocks:
        working[f"__DUPLICATE__{b['id']}"] = b["text"]


# ------------------------------------------------------------
# CATEGORY / ID MOVES
# ------------------------------------------------------------

moves = {
    "MB-NK-013": "MB-HDW-003",
    "MB-NK-024": "MB-ER-013",
    "MB-NK-025": "MB-BELT-028",
}

for old_id, new_id in moves.items():

    if old_id not in working:
        die(f"{old_id} was not found.")

    if new_id in working:
        die(
            f"Cannot rename {old_id} -> {new_id}: "
            f"{new_id} already exists."
        )

    block = working.pop(old_id)

    block = re.sub(
        rf'(^\s*)"{re.escape(old_id)}"(\s*:)',
        rf'\1"{new_id}"\2',
        block,
        count=1,
        flags=re.MULTILINE
    )

    working[new_id] = block


# ------------------------------------------------------------
# UPDATE MOVED PRODUCT CATEGORIES
# ------------------------------------------------------------

working["MB-HDW-003"] = replace_string_field(
    working["MB-HDW-003"],
    "category",
    "Headwear"
)

working["MB-ER-013"] = replace_string_field(
    working["MB-ER-013"],
    "category",
    "Earrings"
)

working["MB-BELT-028"] = replace_string_field(
    working["MB-BELT-028"],
    "category",
    "Belts"
)


# ------------------------------------------------------------
# FIX SANDAL IDS USING IMAGE FILENAMES
# ------------------------------------------------------------

sandal_image_to_id = {
    "/004.png": "MB-SND-001",
    "/010.png": "MB-SND-002",
    "/016.png": "MB-SND-003",
    "/018.png": "MB-SND-004",
    "/026.png": "MB-SND-005",
    "/035.png": "MB-SND-006",
    "/043.png": "MB-SND-007",
    "/047.png": "MB-SND-008",
    "/050.png": "MB-SND-009",
    "/062.png": "MB-SND-010",
    "/086.png": "MB-SND-011",
    "/116.png": "MB-SND-012",
}

sandal_blocks = {}

for old_id, block in list(working.items()):

    if '"Maasai Beaded Sandals"' not in block:
        continue

    found = None

    for image_suffix, final_id in sandal_image_to_id.items():
        if image_suffix in block:
            found = final_id
            break

    if found is None:
        die(
            f"Could not determine final sandal ID from image "
            f"for {old_id}."
        )

    if found in sandal_blocks:
        die(f"Duplicate sandal target ID detected: {found}")

    sandal_blocks[found] = block


if len(sandal_blocks) != 12:
    die(
        f"Expected 12 sandal blocks, found {len(sandal_blocks)}."
    )


# Remove all existing sandal keys first
for old_id in list(working.keys()):
    if '"Maasai Beaded Sandals"' in working[old_id]:
        del working[old_id]


# Reinsert under final IDs
for final_id, block in sandal_blocks.items():

    block = re.sub(
        r'(^\s*)"(MB-SND-\d{3})"(\s*:)',
        rf'\1"{final_id}"\3',
        block,
        count=1,
        flags=re.MULTILINE
    )

    working[final_id] = block


# ------------------------------------------------------------
# APPLY PRICES
# ------------------------------------------------------------

missing_prices = []

for product_id in working:

    if product_id not in prices:
        missing_prices.append(product_id)

if missing_prices:
    print("\nProducts without supplied prices:")

    for product_id in sorted(missing_prices):
        print(f"  {product_id}")

    print(
        "\nThe file has NOT been modified."
    )

    # Restore backup because nothing should be touched.
    FILE.write_text(original)

    sys.exit(1)


for product_id, price in prices.items():

    if product_id not in working:
        continue

    working[product_id] = replace_field(
        working[product_id],
        "price",
        price
    )


# ------------------------------------------------------------
# VALIDATE ALL PRICES
# ------------------------------------------------------------

zero_prices = []

for product_id, block in working.items():

    match = re.search(
        r'^\s*price:\s*(\d+)',
        block,
        re.MULTILINE
    )

    if not match:
        zero_prices.append(f"{product_id} (missing price)")
        continue

    if int(match.group(1)) <= 0:
        zero_prices.append(product_id)

if zero_prices:
    print("\nProducts with zero/missing prices:")

    for product_id in zero_prices:
        print(f"  {product_id}")

    FILE.write_text(original)
    die("Price validation failed. Original file restored.")


# ------------------------------------------------------------
# MOVE BR-061 AFTER BR-060
# ------------------------------------------------------------

br061 = working.pop("MB-BR-061")

ordered_ids = [b["id"] for b in blocks]

# Replace old IDs with renamed IDs where applicable.
for old_id, new_id in moves.items():
    ordered_ids = [
        new_id if x == old_id else x
        for x in ordered_ids
    ]

# Replace all sandal IDs according to image.
new_order = []

for product_id in ordered_ids:

    if product_id in sandal_image_to_id.values():
        # old sandal IDs will be handled below
        continue

    if product_id in working:
        new_order.append(product_id)

# Add all sandal IDs in proper order.
sandals = [
    "MB-SND-001", "MB-SND-002", "MB-SND-003",
    "MB-SND-004", "MB-SND-005", "MB-SND-006",
    "MB-SND-007", "MB-SND-008", "MB-SND-009",
    "MB-SND-010", "MB-SND-011", "MB-SND-012"
]

# If sandals were present in the original order, preserve the
# first sandal position by inserting them there.
first_sandal_position = None

for i, product_id in enumerate(ordered_ids):
    if product_id.startswith("MB-SND-"):
        first_sandal_position = i
        break

if first_sandal_position is not None:
    base_order = []

    for product_id in ordered_ids:
        if product_id.startswith("MB-SND-"):
            continue
        if product_id in working:
            base_order.append(product_id)

    # Find approximate location based on original ordering.
    # Put sandals after the product immediately preceding the
    # first sandal in the original catalogue.
    preceding = None

    for product_id in ordered_ids[:first_sandal_position]:
        if product_id in working and not product_id.startswith("MB-SND-"):
            preceding = product_id

    if preceding and preceding in base_order:
        idx = base_order.index(preceding) + 1
        new_order = (
            base_order[:idx]
            + sandals
            + base_order[idx:]
        )
    else:
        new_order = sandals + base_order
else:
    new_order.extend(sandals)


# Remove duplicates while preserving order
seen = set()
final_order = []

for product_id in new_order:

    if product_id in seen:
        continue

    if product_id not in working:
        continue

    seen.add(product_id)
    final_order.append(product_id)


# Move BR-061 immediately after BR-060
if "MB-BR-061" in final_order:
    final_order.remove("MB-BR-061")

if "MB-BR-060" not in final_order:
    die("MB-BR-060 missing while moving MB-BR-061.")

idx = final_order.index("MB-BR-060") + 1
final_order.insert(idx, "MB-BR-061")

working["MB-BR-061"] = br061


# ------------------------------------------------------------
# FINAL COUNT VALIDATION
# ------------------------------------------------------------

if len(final_order) != 205:
    die(
        f"Final catalogue order contains {len(final_order)} products, "
        "expected 205."
    )

if len(set(final_order)) != 205:
    die("Duplicate product IDs detected in final order.")


# ------------------------------------------------------------
# CATEGORY COUNT VALIDATION
# ------------------------------------------------------------

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

category_counts = {}

for product_id in final_order:

    block = working[product_id]

    match = re.search(
        r'^\s*category:\s*"([^"]+)"',
        block,
        re.MULTILINE
    )

    if not match:
        die(f"Category missing for {product_id}")

    category = match.group(1)

    category_counts[category] = category_counts.get(category, 0) + 1


if category_counts != expected_categories:
    print("\nCATEGORY COUNT MISMATCH")
    print("Expected:")
    for k, v in sorted(expected_categories.items()):
        print(f"  {k}: {v}")

    print("\nActual:")
    for k, v in sorted(category_counts.items()):
        print(f"  {k}: {v}")

    FILE.write_text(original)
    die("Original file restored because category validation failed.")


# ------------------------------------------------------------
# REBUILD ONLY THE TOP-LEVEL PRODUCT SECTION
# ------------------------------------------------------------
#
# IMPORTANT:
# We preserve each individual product block exactly.
# We only change their order.
#

block_lookup = working

# Locate first product and the closing region of the catalogue object.
matches = list(re.finditer(
    r'(?m)^\s*"(MB)-[A-Z0-9]+-\d{3}"\s*:\s*\{',
    original
))

if not matches:
    die("Could not locate product section.")

first_start = matches[0].start()

# Everything before the first product is preserved.
prefix = original[:first_start]

# Find the final closing brace of the products object.
# We use the final occurrence of "};" because this is products.js.
last_close = original.rfind("};")

if last_close == -1 or last_close < first_start:
    die("Could not locate end of products object.")

suffix = original[last_close:]

# Determine indentation from original product keys.
first_line = original[matches[0].start():matches[0].end()]
indent_match = re.match(r'(\s*)"', first_line)

indent = indent_match.group(1) if indent_match else "    "

# Product blocks already contain their own indentation and trailing
# comma/newline, so join them directly.
product_text = "\n".join(
    block_lookup[product_id].rstrip()
    for product_id in final_order
)

new_text = prefix + product_text + "\n" + suffix


# ------------------------------------------------------------
# WRITE
# ------------------------------------------------------------

FILE.write_text(new_text)

print("\nCatalogue updated successfully.")


# ------------------------------------------------------------
# FINAL STATIC CHECKS
# ------------------------------------------------------------

updated = FILE.read_text()

final_blocks = find_blocks(updated)

if len(final_blocks) != 205:
    FILE.write_text(original)
    die(
        f"Post-write validation failed: detected "
        f"{len(final_blocks)} blocks. Original restored."
    )

final_ids = [b["id"] for b in final_blocks]

if len(set(final_ids)) != 205:
    FILE.write_text(original)
    die("Post-write duplicate-ID validation failed. Original restored.")


# Check all final prices
for block in final_blocks:

    product_id = block["id"]

    match = re.search(
        r'^\s*price:\s*(\d+)',
        block["text"],
        re.MULTILINE
    )

    if not match or int(match.group(1)) <= 0:
        FILE.write_text(original)
        die(
            f"Post-write price validation failed for "
            f"{product_id}. Original restored."
        )


# Check BR-061 price
br061_match = re.search(
    r'^\s*price:\s*(\d+)',
    working["MB-BR-061"],
    re.MULTILINE
)

if not br061_match or int(br061_match.group(1)) != 2500:
    FILE.write_text(original)
    die("MB-BR-061 price validation failed. Original restored.")


# ------------------------------------------------------------
# NODE SYNTAX CHECK
# ------------------------------------------------------------

result = subprocess.run(
    ["node", "--check", str(FILE)],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    FILE.write_text(original)

    print("\nNode syntax check FAILED.")
    print(result.stderr)

    print("Original file restored.")
    sys.exit(1)


# ------------------------------------------------------------
# SUCCESS SUMMARY
# ------------------------------------------------------------

print("\n========================================")
print(" CATALOGUE UPDATE COMPLETE")
print("========================================")
print("Products:        205")
print("Unique IDs:      205")
print("Zero prices:     0")
print("Node syntax:     OK")
print()
print("Renamed:")
print("  MB-NK-013 -> MB-HDW-003")
print("  MB-NK-024 -> MB-ER-013")
print("  MB-NK-025 -> MB-BELT-028")
print()
print("Bracelets:")
print("  MB-BR-061 -> KSh 2,500")
print("  positioned after MB-BR-060")
print()
print("Sandals:")
print("  MB-SND-001 through MB-SND-012")
print()
print(f"Backup: {backup}")
print("========================================")
