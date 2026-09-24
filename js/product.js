// Get product ID from URL

const params = new URLSearchParams(window.location.search);

const productId = params.get("id");


// Find product

const product = products[productId];


// Display product

if (product) {

    document.getElementById("product-id").textContent = productId;
    
    document.getElementById("product-category").textContent = product.category;
    
    document.getElementById("product-name").textContent = product.name;
     
    document.getElementById("product-description").textContent = product.description;

   fetch(`https://YOUR-RENDER-URL.onrender.com/api/products/${encodeURIComponent(productId)}/inventory`)
    .then(response => response.json())
    .then(data => {

        if (!data.inventory) return;

        const statusElement =
            document.getElementById("product-status");

        const status =
            data.inventory.status;

        statusElement.textContent = status;
        statusElement.className =
            `product-status ${status.toLowerCase()}`;

    })
    .catch(error => {

        console.error("Inventory lookup failed:", error);

        const statusElement =
            document.getElementById("product-status");

        const status = product.status;

        statusElement.textContent = status;
        statusElement.className =
            `product-status ${status.toLowerCase()}`;

    }); 
   
    document.getElementById("product-price").textContent =
    `KSh ${product.price.toLocaleString()}`;

    document.getElementById("product-image").src = product.image;
} else {

    document.getElementById("product-name").textContent = "Product Not Found";

    document.getElementById("product-description").textContent =
        "Sorry, we couldn't find this product.";

}
const customLink = document.getElementById("custom-link");

if (customLink && product) {
    customLink.href = `custom.html?reference=${productId}`;
}

const whatsappLink = document.getElementById("whatsapp-link");

if (whatsappLink && product) {

    const phoneNumber = "254711936249";

    const message = `Hello! I'd like to ask about this beadwork piece.

Product ID: ${productId}
Product: ${product.name}

Is this piece still available?`;

    whatsappLink.href =
        `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
}


// =========================
// SHARE PRODUCT
// =========================

const shareButton = document.getElementById("share-product");

if (shareButton) {

    shareButton.addEventListener("click", async () => {

        const productUrl = window.location.href;

        try {

            if (navigator.share) {

                await navigator.share({
                    title: product.name,
                    text: `Check out this Maasai beadwork design: ${product.name}`,
                    url: productUrl
                });

            } else {

                await navigator.clipboard.writeText(productUrl);

                alert("Product link copied!");

            }

        } catch (error) {

            console.log("Share cancelled or failed:", error);

        }

    });

}


// =========================
// YOU MAY ALSO LIKE
// =========================

const relatedProductsContainer =
    document.getElementById("related-products");

if (relatedProductsContainer && product) {

    // Products from the same category
    let relatedProducts = Object.entries(products)
        .filter(([id, item]) =>
            id !== productId &&
            item.category === product.category
        );

    // Shuffle recommendations
    for (let i = relatedProducts.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [relatedProducts[i], relatedProducts[j]] =
            [relatedProducts[j], relatedProducts[i]];
    }

    // Take up to 4
    relatedProducts = relatedProducts.slice(0, 4);

    // If the category has fewer than 4 products,
    // fill the remaining spaces with products
    // from other categories.
    if (relatedProducts.length < 4) {

        const existingIds =
            new Set(relatedProducts.map(([id]) => id));

        let fallbackProducts = Object.entries(products)
            .filter(([id, item]) =>
                id !== productId &&
                !existingIds.has(id) &&
                item.category !== product.category
            );

        // Shuffle fallback products
        for (let i = fallbackProducts.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [fallbackProducts[i], fallbackProducts[j]] =
                [fallbackProducts[j], fallbackProducts[i]];
        }

        relatedProducts.push(
            ...fallbackProducts.slice(
                0,
                4 - relatedProducts.length
            )
        );
    }

    relatedProducts.forEach(([id, item]) => {

        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <div class="product-image">
                <a href="product.html?id=${encodeURIComponent(id)}">
                    <img
                        src="${item.image}"
                        alt="${item.name}"
                        loading="lazy"
                    >
                </a>
            </div>

            <div class="product-info">

                <p class="product-category">
                    ${item.category}
                </p>

                <h3>
                    <a href="product.html?id=${encodeURIComponent(id)}">
                        ${item.name}
                    </a>
                </h3>

                <p class="product-id">
                    ${id}
                </p>

                <p class="product-price">
                    KSh ${Number(item.price).toLocaleString()}
                </p>

                <p class="product-status ${item.status.toLowerCase()}">
                    ${item.status}
                </p>

                <a href="product.html?id=${encodeURIComponent(id)}">
                    View Design →
                </a>

            </div>
        `;

        relatedProductsContainer.appendChild(card);

        // Replace the catalogue status with live database status
        fetch(
            `https://YOUR-RENDER-URL.onrender.com/api/products/${encodeURIComponent(id)}/inventory`
        )
            .then(response => response.json())
            .then(data => {

                if (!data.inventory) return;

                const statusElement =
                    card.querySelector(".product-status");

                if (!statusElement) return;

                const status =
                    data.inventory.status;

                statusElement.textContent = status;
                statusElement.className =
                    `product-status ${status.toLowerCase()}`;

            })
            .catch(error => {

                console.error(
                    `Inventory lookup failed for ${id}:`,
                    error
                );

            });

    });
}



// =========================
// FAVORITES
// =========================

const favoriteButton =
    document.getElementById("favorite-product");

if (favoriteButton && product) {

    let favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];

    function updateFavoriteButton() {

        if (favorites.includes(productId)) {

            favoriteButton.textContent =
                "♥ Remove from Favorites";

        } else {

            favoriteButton.textContent =
                "♡ Add to Favorites";

        }

    }

    updateFavoriteButton();

    favoriteButton.addEventListener("click", () => {

        if (favorites.includes(productId)) {

            favorites = favorites.filter(
                id => id !== productId
            );

        } else {

            favorites.push(productId);

        }

        localStorage.setItem(
            "favorites",
            JSON.stringify(favorites)
        );

        updateFavoriteButton();

    });

}


if (product) {

    let visitorId = localStorage.getItem("visitorId");

    if (!visitorId) {
        visitorId = crypto.randomUUID();
        localStorage.setItem("visitorId", visitorId);
    }

    fetch(
        `https://YOUR-RENDER-URL.onrender.com/api/products/${encodeURIComponent(productId)}/view`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                visitorId: visitorId
            })
        }
    )
    .then(response => response.json())
    .then(data => {
        console.log("View tracking response:", data);
    })
    .catch(error => {
        console.error("View tracking failed:", error);
    });

}
