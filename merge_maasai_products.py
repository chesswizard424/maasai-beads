from pathlib import Path
import re

PRODUCTS = Path("js/products.js")

# Verified 116-item allocation
allocation = {
    1:  ("MB-NK-016", "Circular Maasai Beaded Necklace"),
    2:  ("MB-BR-038", "Maasai Beaded Hand Bracelet"),
    3:  ("MB-NK-017", "White Fringe Beaded Necklace"),
    4:  ("MB-SND-001", "Beaded Maasai Sandals"),
    5:  ("MB-BAG-001", "Colourful Woven Bead Bags"),
    6:  ("MB-BR-039", "Kenyan Flag Beaded Bracelets"),
    7:  ("MB-BELT-020", "Blue & White Beaded Belts"),
    8:  ("MB-NK-018", "Blue & Red Maasai Beaded Necklace"),
    9:  ("MB-SND-002", "Colourful Maasai Beaded Sandals"),
    10: ("MB-SND-003", "Colourful Maasai Beaded Sandals"),
    11: ("MB-ER-005", "Floral Circular Beaded Earrings"),
    12: ("MB-MAT-001", "Circular Woven Cup Mat"),
    13: ("MB-BR-040", "Kenyan Flag Shield Beaded Bracelet"),
    14: ("MB-NK-019", "Layered Beaded Necklace"),
    15: ("MB-BELT-021", "Triangular Beaded Belts"),
    16: ("MB-SND-004", "Blue & Red Maasai Beaded Sandals"),
    17: ("MB-NK-020", "Brown Woven-Style Necklace"),
    18: ("MB-SND-005", "Colourful Maasai Beaded Sandals"),
    19: ("MB-BR-041", "Geometric Beaded Bracelet"),
    20: ("MB-OTH-001", "Mixed Colour Beadwork Set"),
    21: ("MB-NK-021", "Blue & White Layered Necklace"),
    22: ("MB-BAG-002", "Lilac Woven Pouches"),
    23: ("MB-KH-001", "Multicolour Beaded Key Holders"),
    24: ("MB-ER-006", "Natural-Tone Beaded Earrings"),
    25: ("MB-NK-022", "Cream & Brown Beaded Necklace"),
    26: ("MB-SND-006", "Circular Beaded Sandals"),
    27: ("MB-MAT-002", "Concentric Woven Mat"),
    28: ("MB-NK-023", "Cream Beaded Necklace"),
    29: ("MB-RG-002", "Blue & White Maasai Rungus"),
    30: ("MB-MAT-003", "Stacked Woven Mats"),
    31: ("MB-BAG-003", "Brown Patterned Beaded Purses"),
    32: ("MB-NK-024", "Blue & Green Beaded Necklaces"),
    33: ("MB-NK-025", "Green & Geometric Beaded Necklace"),
    34: ("MB-NK-026", "Multicolour Maasai Beaded Necklace"),
    35: ("MB-SND-007", "Black & White Maasai Beaded Sandals"),
    36: ("MB-BR-042", "Multicolour Beaded Bracelets"),
    37: ("MB-NK-027", "Multicolour Beaded Necklaces"),
    38: ("MB-NK-028", "Brown & Blue Statement Necklace"),
    39: ("MB-BR-043", "Blue Patterned Beaded Bracelets"),
    40: ("MB-BASK-001", "Multicolour Beaded Pouches & Woven Baskets"),
    41: ("MB-NK-029", "Blue & White Circular Beaded Necklace"),
    42: ("MB-ER-007", "Multicolour Beaded Earrings"),
    43: ("MB-SND-008", "White & Black Maasai Beaded Sandals"),
    44: ("MB-NK-030", "White Geometric Beaded Necklace"),
    45: ("MB-NK-031", "Layered Maasai Beaded Necklace"),
    46: ("MB-MAT-004", "Circular Woven Tea & Coffee Mats"),
    47: ("MB-SND-009", "Brown & White Maasai Beaded Sandals"),
    48: ("MB-BELT-022", "Blue Patterned Beaded Belts"),
    49: ("MB-MAT-005", "Brown Spiral Woven Mat"),
    50: ("MB-SND-010", "Pink & Cream Maasai Sandals"),
    51: ("MB-NK-032", "White Beaded Necklaces"),
    52: ("MB-NK-033", "Layered Multicolour Maasai Necklace"),
    53: ("MB-HDW-001", "Beaded Maasai Headband"),
    54: ("MB-BR-044", "Union Jack Beaded Bracelet"),
    55: ("MB-BR-045", "Beaded Wrist Bracelet"),
    56: ("MB-NK-034", "White Circular Beaded Necklace"),
    57: ("MB-BR-046", "Brown Beaded Bracelet"),
    58: ("MB-ER-008", "Mixed Beaded Earrings"),
    59: ("MB-BELT-023", "White & Grey Beaded Belts"),
    60: ("MB-BR-047", "Cream & Orange Beaded Bracelet"),
    61: ("MB-BR-048", "Blue & White Beaded Bracelets"),
    62: ("MB-SND-011", "Decorated Maasai Beaded Sandal"),
    63: ("MB-NK-035", "White Statement Beaded Necklace"),
    64: ("MB-NK-036", "Multicolour Beaded Necklaces"),
    65: ("MB-BR-049", "Blue & Red Beaded Bracelet"),
    66: ("MB-NK-037", "Brown Circular Beaded Necklace"),
    67: ("MB-MAT-006", "Multicolour Beaded Mats"),
    68: ("MB-BELT-024", "Red & Blue Beaded Belts"),
    69: ("MB-OTH-002", "Multicolour Beaded Strands"),
    70: ("MB-MAT-007", "Beaded Dining Mat"),
    71: ("MB-BAG-004", "Natural Woven Bag"),
    72: ("MB-MAT-008", "Round Woven Mats"),
    73: ("MB-BR-050", "Geometric Beaded Bracelet"),
    74: ("MB-BR-051", "Multicolour Beaded Bracelets"),
    75: ("MB-NK-038", "Blue Circular Beaded Necklace"),
    76: ("MB-NK-039", "Pink & Green Circular Beaded Necklace"),
    77: ("MB-NK-040", "Multicolour Layered Beaded Necklace"),
    78: ("MB-BR-052", "Geometric Beaded Bracelet"),
    79: ("MB-BR-053", "Kenyan Flag Beaded Bracelet"),
    80: ("MB-NK-041", "Brown & White Circular Beaded Necklace"),
    81: ("MB-NK-042", "Large Geometric Beaded Necklace"),
    82: ("MB-HAT-004", "Beaded Maasai Hats"),
    83: ("MB-OUT-004", "Multicolour Beaded Outfit"),
    84: ("MB-NK-043", "White & Red Beaded Necklaces"),
    85: ("MB-NK-044", "Blue & Brown Circular Beaded Necklace"),
    86: ("MB-SND-012", "Brown & Cream Maasai Sandals"),
    87: ("MB-NK-045", "White & Brown Beaded Necklace"),
    88: ("MB-NK-046", "Brown & Red Statement Necklace"),
    89: ("MB-BAG-005", "Red Beaded Handbag"),
    90: ("MB-ER-009", "Natural-Tone Beaded Earrings"),
    91: ("MB-BR-054", "Multicolour Beaded Bracelets"),
    92: ("MB-BELT-025", "Multicolour Geometric Beaded Belts"),
    93: ("MB-NK-047", "Yellow Background Statement Necklace"),
    94: ("MB-ER-010", "Multicolour Beaded Earrings"),
    95: ("MB-MAT-009", "Circular Woven Mats"),
    96: ("MB-BR-055", "Blue & White Beaded Bracelet"),
    97: ("MB-BR-056", "Heritage Bead Collection"),
    98: ("MB-OTH-003", "Rainbow Strand Collection"),
    99: ("MB-NK-048", "Blue Spiral Medallion"),
    100: ("MB-BELT-026", "Triple Heritage Tassels"),
    101: ("MB-OTH-004", "Golden Maasai Mosaic"),
    102: ("MB-BR-057", "Colourway Bead Panels"),
    103: ("MB-BR-058", "Blue & Crimson Heritage Cuff"),
    104: ("MB-HDW-002", "Ceremonial Geometry Pendant"),
    105: ("MB-BAG-006", "Statement Beaded Piece"),
    106: ("MB-NK-049", "Silver Circle Charm"),
    107: ("MB-BELT-027", "Earth-Tone Coil Set"),
    108: ("MB-KH-002", "Four Winds Tassels"),
    109: ("MB-OTH-005", "White Pearl Strands"),
    110: ("MB-NK-050", "Seven-Colour Circle Bracelet"),
    111: ("MB-MAT-010", "Six Petal Medallions"),
    112: ("MB-BR-059", "Beaded Hand/Wrist Collection"),
    113: ("MB-BR-060", "Rainbow Heritage Cuff"),
    114: ("MB-BAG-007", "Silver Heritage Collar"),
    115: ("MB-ER-011", "Colour Mosaic Panel"),
    116: ("MB-SND-013", "Ivory Beaded Sandals"),
}

folder_map = {
    "Bracelets": "01-Bracelets",
    "Necklaces": "02-Necklaces",
    "Earrings": "03-Earrings",
    "Beaded Hats": "04-Beaded-Hats",
    "Belts": "05-Belts",
    "Maasai Rungus": "06-Maasai-Rungus",
    "Beaded Outfits": "07-Beaded-Outfits",
    "Other": "08-Other",
    "Maasai Beaded Sandals": "09-Maasai-Beaded-Sandals",
    "Bags": "10-Bags",
    "Baskets": "11-Baskets",
    "Mats": "12-Mats",
    "Headwear": "13-Headwear",
    "Key Holders": "14-Key-Holders",
}

category_map = {
    "MB-BR": "Bracelets",
    "MB-NK": "Necklaces",
    "MB-ER": "Earrings",
    "MB-HAT": "Beaded Hats",
    "MB-BELT": "Belts",
    "MB-RG": "Maasai Rungus",
    "MB-OUT": "Beaded Outfits",
    "MB-OTH": "Other",
    "MB-SND": "Maasai Beaded Sandals",
    "MB-BAG": "Bags",
    "MB-BASK": "Baskets",
    "MB-MAT": "Mats",
    "MB-HDW": "Headwear",
    "MB-KH": "Key Holders",
}

text = PRODUCTS.read_text()

# Safety: never modify a file unless all 116 IDs are absent.
existing_ids = set(re.findall(r'"(MB-[A-Z0-9-]+)"\s*:', text))
new_ids = {pid for pid, _ in allocation.values()}

overlap = existing_ids & new_ids
if overlap:
    raise SystemExit(f"ABORT: these new IDs already exist: {sorted(overlap)}")

if len(allocation) != 116:
    raise SystemExit(f"ABORT: allocation contains {len(allocation)} records, expected 116")

entries = []

for number in range(1, 117):
    pid, name = allocation[number]
    prefix = pid.rsplit("-", 1)[0]
    category = category_map[prefix]
    folder = folder_map[category]

    image = f"images/processed/new-catalogue-116/{folder}/{number:03d}.png"

    if not Path(image).is_file():
        raise SystemExit(f"ABORT: missing image: {image}")

    entries.append(
f'''    "{pid}": {{
        name: "{name}",
        category: "{category}",
        image: "{image}",
        price: 0,
        status: "Available",
        added: "2026-09-21"
    }}'''
    )

block = ",\n\n".join(entries)

# Insert immediately before the final closing brace.
pos = text.rfind("};")
if pos == -1:
    raise SystemExit("ABORT: could not find final }; in products.js")

new_text = text[:pos].rstrip()
if not new_text.endswith(","):
    new_text += ","

new_text += "\n\n" + block + "\n" + text[pos:]

PRODUCTS.write_text(new_text)

print("SUCCESS")
print("Original products:", len(existing_ids))
print("New products:", len(new_ids))
print("Total products:", len(existing_ids) + len(new_ids))
