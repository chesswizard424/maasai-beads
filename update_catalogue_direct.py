#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import re
import shutil
import subprocess
import sys

FILE = Path("js/products.js")


# ============================================================
# PRICE MAP
# ============================================================

prices = {
    # NECKLACES
    "MB-NK-001": 4000, "MB-NK-002": 2000, "MB-NK-003": 4500,
    "MB-NK-004": 4000, "MB-NK-005": 4000, "MB-NK-006": 3500,
    "MB-NK-007": 2500, "MB-NK-008": 4000, "MB-NK-009": 3000,
    "MB-NK-010": 4000, "MB-NK-011": 3000, "MB-NK-012": 2500,
  
    "MB-NK-014": 2000, "MB-NK-015": 2000, "MB-NK-016": 3500,
    "MB-NK-017": 1500, "MB-NK-018": 3500, "MB-NK-019": 5000,
    "MB-NK-020": 4500, "MB-NK-021": 1500, "MB-NK-022": 1500,
    "MB-NK-023": 14000, 
    "MB-NK-026": 1200, "MB-NK-027": 4500,"MB-NK-028": 8000, 
    "MB-NK-029": 3000, "MB-NK-030": 250, "MB-NK-031": 2500,
    "MB-NK-032": 2000, "MB-NK-033": 6000, "MB-NK-034": 3500,
    "MB-NK-035": 2000, "MB-NK-036": 1000, "MB-NK-037": 3000,
    "MB-NK-038": 250, "MB-NK-039": 8000, "MB-NK-040": 5000,
    "MB-NK-041": 4500, "MB-NK-042": 3500, "MB-NK-043": 1500,
    "MB-NK-044": 8000, "MB-NK-045": 2000, "MB-NK-046": 4500,
    "MB-NK-047": 5500, "MB-NK-048": 3500, "MB-NK-049": 3500,
    "MB-NK-050": 3000,

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


# ============================================================
# HELPERS
# ============================================================

def die(message):
    print(f"\nERROR: {message}")
    sys.exit(1)


def get_product_block(text, product_id):
    """
    Get one product block without rebuilding the JS object.
    The block ends immediately before the next product key.
    """
    pattern = re.compile(
        rf'(?ms)^(\s*)"{re.escape(product_id)}"\s*:\s*\{{.*?(?=^\s*"MB-[A-Z0-9]+-\d{{3}}"\s*:\s*\{{|\Z)'
    )

    match = pattern.search(text)

    if not match:
        return None

    return match.group(0)


def update_price(text, product_id, price):
    block = get_product_block(text, product_id)

    if block is None:
        die(f"Could not find product block: {product_id}")

    new_block, count = re.subn(
        r'(^\s*price:\s*)[^,\n]+',
        rf'\g<1>{price}',
        block,
        count=1,
        flags=re.MULTILINE
    )

    if count != 1:
        die(f"Could not update price for {product_id}")

    return text.replace(block, new_block, 1)


def update_category(text, product_id, category):
    block = get_product_block(text, product_id)

    if block is None:
        die(f"Could not find product block: {product_id}")

    new_block, count = re.subn(
        r'(^\s*category:\s*)"[^"]*"',
        rf'\g<1>"{category}"',
        block,
        count=1,
        flags=re.MULTILINE
    )

    if count != 1:
        die(f"Could not update category for {product_id}")

    return text.replace(block, new_block, 1)


def rename_product(text, old_id, new_id):
    block = get_product_block(text, old_id)

    if block is None:
        die(f"Could not find product block: {old_id}")

    if get_product_block(text, new_id) is not None:
        die(f"Target ID already exists: {new_id}")

    new_block = re.sub(
        rf'(^\s*)"{re.escape(old_id)}"(\s*:)',
        rf'\1"{new_id}"\2',
        block,
        count=1,
        flags=re.MULTILINE
    )

    if new_block == block:
        die(f"Could not rename {old_id} to {new_id}")

    return text.replace(block, new_block, 1)


def change_sandal_id_by_image(text, image_name, new_id):
    """
    Find the sandal containing this image and change only its key.
    This safely handles the duplicate MB-SND-010.
    """

    pattern = re.compile(
        rf'(?ms)^(\s*)"MB-SND-\d{{3}}"\s*:\s*\{{.*?'
        rf'(?=^\s*"MB-[A-Z0-9]+-\d{{3}}"\s*:\s*\{{|\Z)'
    )

    matches = list(pattern.finditer(text))

    found = None

    for match in matches:
        block = match.group(0)

        if image_name in block:
            if found is not None:
                die(
                    f"Multiple sandal blocks contain image {image_name}"
                )

            found = match

    if found is None:
        die(f"No sandal found containing image {image_name}")

    old_block = found.group(0)

    if re.search(
        rf'^\s*"{re.escape(new_id)}"\s*:',
        text,
        re.MULTILINE
    ):
        # If the target already exists, it must be the same block.
        current_key = re.search(
            r'^\s*"(MB-SND-\d{3})"\s*:',
            old_block,
            re.MULTILINE
        )

        if not current_key or current_key.group(1) != new_id:
            die(
                f"Target sandal ID {new_id} already exists."
            )

    new_block = re.sub(
        r'(^\s*)"MB-SND-\d{3}"(\s*:)',
        rf'\1"{new_id}"\2',
        old_block,
        count=1,
        flags=re.MULTILINE
    )

    return text[:found.start()] + new_block + text[found.end():]


def move_block_after(text, product_id, after_id):
    """
    Move an existing product block while preserving its exact content.
    """
    block = get_product_block(text, product_id)

    if block is None:
        die(f"Could not find {product_id} to move.")

    after_block = get_product_block(text, after_id)

    if after_block is None:
        die(f"Could not find {after_id}.")

    # Remove the original block.
    remaining = text.replace(block, "", 1)

    # Re-fetch after block because its position may have changed.
    after_block = get_product_block(remaining, after_id)

    if after_block is None:
        die(f"Could not locate {after_id} after removing {product_id}.")

    insert_at = remaining.find(after_block) + len(after_block)

    return (
        remaining[:insert_at]
        + block
        + remaining[insert_at:]
    )


def count_product_keys(text):
    return re.findall(
        r'(?m)^\s*"(MB-[A-Z0-9]+-\d{3})"\s*:\s*\{',
        text
    )


# ============================================================
# LOAD
# ============================================================

if not FILE.exists():
    die(f"{FILE} does not exist.")

original = FILE.read_text()

ids = count_product_keys(original)

print(f"Product blocks detected: {len(ids)}")

if len(ids) != 205:
    die(
        f"Expected 205 product blocks, found {len(ids)}."
    )


# ============================================================
# BACKUP
# ============================================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = FILE.with_name(
    f"{FILE.name}.backup_{timestamp}"
)

shutil.copy2(FILE, backup)

print(f"Backup created: {backup}")


# ============================================================
# WORKING COPY
# ============================================================

text = original


# ============================================================
# RENAME MOVED PRODUCTS
# ============================================================

# Necklace -> Headwear
text = rename_product(
    text,
    "MB-NK-013",
    "MB-HDW-003"
)

text = update_category(
    text,
    "MB-HDW-003",
    "Headwear"
)


# Necklace -> Earrings
text = rename_product(
    text,
    "MB-NK-024",
    "MB-ER-013"
)

text = update_category(
    text,
    "MB-ER-013",
    "Earrings"
)


# Necklace -> Belt
text = rename_product(
    text,
    "MB-NK-025",
    "MB-BELT-028"
)

text = update_category(
    text,
    "MB-BELT-028",
    "Belts"
)


# ============================================================
# FIX SANDALS
# ============================================================

# ============================================================
# FIX SANDALS
# ============================================================

# First temporarily rename ALL existing sandal IDs so that
# none of the final IDs can collide during the renumbering.

sandal_pattern = re.compile(
    r'(?ms)^(\s*)"MB-SND-\d{3}"\s*:\s*\{.*?'
    r'(?=^\s*"MB-[A-Z0-9]+-\d{3}"\s*:\s*\{|\Z)'
)

sandal_matches = list(sandal_pattern.finditer(text))

if len(sandal_matches) != 12:
    die(
        f"Expected 12 sandal blocks, found {len(sandal_matches)}."
    )


# Give every existing sandal a temporary unique ID.
# Do this from the bottom backwards so positions remain valid.

for index in range(len(sandal_matches) - 1, -1, -1):

    match = sandal_matches[index]

    block = match.group(0)

    temp_id = f"MB-SND-TEMP-{index + 1:03d}"

    new_block = re.sub(
        r'(^\s*)"MB-SND-\d{3}"(\s*:)',
        rf'\1"{temp_id}"\2',
        block,
        count=1,
        flags=re.MULTILINE
    )

    text = (
        text[:match.start()]
        + new_block
        + text[match.end():]
    )


# Now locate each temporary sandal by its image and give it
# its final ID.

sandal_fixes = [
    ("004.png", "MB-SND-001"),
    ("010.png", "MB-SND-002"),
    ("016.png", "MB-SND-003"),
    ("018.png", "MB-SND-004"),
    ("026.png", "MB-SND-005"),
    ("035.png", "MB-SND-006"),
    ("043.png", "MB-SND-007"),
    ("047.png", "MB-SND-008"),
    ("050.png", "MB-SND-009"),
    ("062.png", "MB-SND-010"),
    ("086.png", "MB-SND-011"),
    ("116.png", "MB-SND-012"),
]


temp_pattern = re.compile(
    r'(?ms)^(\s*)"MB-SND-TEMP-\d{3}"\s*:\s*\{.*?'
    r'(?=^\s*"MB-[A-Z0-9]+-\d{3}"\s*:\s*\{|\Z)'
)


for image_name, final_id in sandal_fixes:

    matches = list(temp_pattern.finditer(text))

    found = None

    for match in matches:

        block = match.group(0)

        if image_name in block:

            if found is not None:
                die(
                    f"Multiple sandal blocks contain {image_name}"
                )

            found = match

    if found is None:
        die(
            f"Could not find sandal containing image {image_name}"
        )

    old_block = found.group(0)

    new_block = re.sub(
        r'(^\s*)"MB-SND-TEMP-\d{3}"(\s*:)',
        rf'\1"{final_id}"\2',
        old_block,
        count=1,
        flags=re.MULTILINE
    )

    text = (
        text[:found.start()]
        + new_block
        + text[found.end():]
    )


# ============================================================
# APPLY PRICES
# ============================================================

# These IDs are deliberately checked after all renames.
for product_id, price in prices.items():

    if get_product_block(text, product_id) is None:
        die(
            f"Price map contains {product_id}, "
            f"but that product does not exist after ID changes."
        )

    text = update_price(
        text,
        product_id,
        price
    )


# ============================================================
# MOVE BR-061
# ============================================================

text = move_block_after(
    text,
    "MB-BR-061",
    "MB-BR-060"
)


# ============================================================
# VALIDATE PRODUCT COUNT
# ============================================================

final_ids = count_product_keys(text)

if len(final_ids) != 205:
    die(
        f"Final product count would be {len(final_ids)}, "
        f"expected 205."
    )


# ============================================================
# VALIDATE UNIQUE IDS
# ============================================================

unique_ids = set(final_ids)

if len(unique_ids) != 205:
    duplicates = sorted(
        product_id
        for product_id in unique_ids
        if final_ids.count(product_id) > 1
    )

    print("\nDuplicate IDs:")
    for product_id in duplicates:
        print(f"  {product_id}")

    die(
        f"Final catalogue would contain {len(unique_ids)} "
        f"unique IDs instead of 205."
    )


# ============================================================
# VALIDATE NO ZERO PRICES
# ============================================================

zero_prices = []

for product_id in final_ids:

    block = get_product_block(text, product_id)

    if block is None:
        zero_prices.append(product_id)
        continue

    match = re.search(
        r'^\s*price:\s*(\d+)',
        block,
        re.MULTILINE
    )

    if not match or int(match.group(1)) <= 0:
        zero_prices.append(product_id)


if zero_prices:
    print("\nProducts with missing/zero prices:")

    for product_id in zero_prices:
        print(f"  {product_id}")

    die("Price validation failed.")


# ============================================================
# VALIDATE CATEGORY COUNTS
# ============================================================

expected = {
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

actual = {}

for product_id in final_ids:

    block = get_product_block(text, product_id)

    match = re.search(
        r'^\s*category:\s*"([^"]+)"',
        block,
        re.MULTILINE
    )

    if not match:
        die(f"Missing category for {product_id}")

    category = match.group(1)

    actual[category] = actual.get(category, 0) + 1


if actual != expected:

    print("\nCATEGORY COUNT MISMATCH")

    print("\nExpected:")
    for category, count in sorted(expected.items()):
        print(f"  {category}: {count}")

    print("\nActual:")
    for category, count in sorted(actual.items()):
        print(f"  {category}: {count}")

    die("Category validation failed.")


# ============================================================
# WRITE TEMPORARY FILE
# ============================================================

temp_file = FILE.with_suffix(".products_test.js")

temp_file.write_text(text)


# ============================================================
# NODE SYNTAX CHECK
# ============================================================

result = subprocess.run(
    ["node", "--check", str(temp_file)],
    capture_output=True,
    text=True
)

if result.returncode != 0:

    print("\nNode syntax check FAILED.")
    print(result.stderr)

    temp_file.unlink(missing_ok=True)

    print("Original file was NOT modified.")
    sys.exit(1)


# ============================================================
# COMMIT
# ============================================================

FILE.write_text(text)

temp_file.unlink(missing_ok=True)


# ============================================================
# FINAL VERIFICATION
# ============================================================

final_content = FILE.read_text()

final_ids = count_product_keys(final_content)

if len(final_ids) != 205:
    FILE.write_text(original)
    die("Final verification failed. Original restored.")


if len(set(final_ids)) != 205:
    FILE.write_text(original)
    die("Final unique-ID verification failed. Original restored.")


# Check BR-061 price
br061 = get_product_block(
    final_content,
    "MB-BR-061"
)

if not br061 or not re.search(
    r'^\s*price:\s*2500',
    br061,
    re.MULTILINE
):
    FILE.write_text(original)
    die("MB-BR-061 price verification failed.")


# Check all sandal IDs
for sandal_id in [
    "MB-SND-001", "MB-SND-002", "MB-SND-003",
    "MB-SND-004", "MB-SND-005", "MB-SND-006",
    "MB-SND-007", "MB-SND-008", "MB-SND-009",
    "MB-SND-010", "MB-SND-011", "MB-SND-012"
]:
    if get_product_block(final_content, sandal_id) is None:
        FILE.write_text(original)
        die(
            f"Missing sandal after final verification: {sandal_id}"
        )


print()
print("============================================")
print("       CATALOGUE UPDATE COMPLETE")
print("============================================")
print()
print("Products:             205")
print("Unique IDs:           205")
print("Zero prices:          0")
print("Node syntax:          OK")
print()
print("ID changes:")
print("  MB-NK-013  -> MB-HDW-003")
print("  MB-NK-024  -> MB-ER-013")
print("  MB-NK-025  -> MB-BELT-028")
print()
print("Bracelet:")
print("  MB-BR-061  -> KSh 2,500")
print("  moved after MB-BR-060")
print()
print("Sandals:")
print("  MB-SND-001 through MB-SND-012")
print()
print(f"Backup: {backup}")
print()
print("============================================")
