console.log("Maasai Beadwork website loaded!");

let inventory = {};

const inventoryPromise = fetch("https://YOUR-RENDER-URL.onrender.com/api/products/inventory")
    .then(response => response.json())
    .then(data => {
        data.inventory.forEach(item => {
            inventory[item.product_id] = item.status;
        });
    })
    .catch(error => {
        console.error("Inventory lookup failed:", error);
    });

function updateInventoryStatus(card, productId) {

    inventoryPromise.then(() => {

        const statusElement = card.querySelector(".product-status");

        if (!statusElement) return;

        const status = inventory[productId];

        if (!status) return;

        statusElement.textContent = status;
        statusElement.className = `product-status ${status.toLowerCase()}`;

    });

}

// =========================
// FEATURED PRODUCTS
// =========================

const featuredContainer =
    document.getElementById("featured-products");

if (featuredContainer) {

    // Change these IDs anytime to update the homepage showcase.
    const featuredProducts = [
        "MB-NK-016",
        "MB-NK-033",
        "MB-BR-001",
        "MB-BR-024",
        "MB-BELT-008",
        "MB-ER-004",
        "MB-SND-002",
        "MB-OUT-003",
        "MB-MAT-004"
    ];

    featuredProducts.forEach(productId => {

        const product = products[productId];

        if (!product) {
            console.warn(`Featured product not found: ${productId}`);
            return;
        }

        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <div class="product-image">
                <a href="product.html?id=${encodeURIComponent(productId)}">
                    <img
                        src="${product.image}"
                        alt="${product.name}"
                        loading="lazy"
                    >
                </a>
            </div>

            <div class="product-info">

                <p class="product-category">
                    ${product.category}
                </p>

                <h3>
                    <a href="product.html?id=${encodeURIComponent(productId)}">
                        ${product.name}
                    </a>
                </h3>

                <p class="product-id">
                    ${productId}
                </p>

                <p class="product-price">
                    KSh ${Number(product.price).toLocaleString()}
                </p>

                <p class="product-status ${product.status.toLowerCase()}">
                    ${product.status}
                </p>

                <a href="product.html?id=${encodeURIComponent(productId)}">
                    View Design →
                </a>

            </div>
        `;

        featuredContainer.appendChild(card);

        updateInventoryStatus(card, productId);

    });
}


// =========================
// RECENTLY ADDED PRODUCTS
// =========================

const recentProductsContainer =
    document.getElementById("recent-products");

if (recentProductsContainer) {

    const recentProducts = Object.entries(products)
        .filter(([id, product]) => product.added)
        .sort((a, b) =>
            new Date(b[1].added) - new Date(a[1].added)
        )
        .slice(0, 6);

    recentProducts.forEach(([productId, product]) => {

        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <div class="product-image">
                <a href="product.html?id=${productId}">
                    <img src="${product.image}" alt="${product.name}">
                </a>
            </div>

            <div class="product-info">

                <p class="product-category">
                    ${product.category}
                </p>

                <h3>
                    <a href="product.html?id=${productId}">
                        ${product.name}
                    </a>
                </h3>

                <p class="product-id">
                    ${productId}
                </p>

                <p class="product-price">
                    KSh ${product.price.toLocaleString()}
                </p>

                <p class="product-status ${product.status.toLowerCase()}">
                    ${product.status}
                </p>

                <a href="product.html?id=${productId}">
                    View Design →
                </a>

            </div>
        `;

        recentProductsContainer.appendChild(card);

        updateInventoryStatus(card, productId);
    });
}


// =========================
// SERVICE WORKER
// =========================

if ("serviceWorker" in navigator) {

    window.addEventListener("load", () => {

        navigator.serviceWorker.register("sw.js")
            .then(() => {
                console.log("Service worker registered.");
            })
            .catch(error => {
                console.error(
                    "Service worker registration failed:",
                    error
                );
            });

    });

}

const mostViewedContainer =
    document.getElementById("most-viewed-products");

if (mostViewedContainer) {

    fetch("https://YOUR-RENDER-URL.onrender.com/api/products/most-viewed")
        .then(response => response.json())
        .then(data => {

    if (data.products.length === 0) {

        mostViewedContainer.innerHTML = `
            <p class="no-most-viewed">
                Popular designs will appear here as visitors explore the collection.
            </p>
        `;

        return;
    }

    data.products.forEach(view => {

        const product = products[view.product_id];

        if (!product) return;

        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <div class="product-image">
                <a href="product.html?id=${view.product_id}">
                    <img src="${product.image}" alt="${product.name}">
                </a>
            </div>

            <div class="product-info">

                <p class="product-category">
                    ${product.category}
                </p>

                <h3>
                    <a href="product.html?id=${view.product_id}">
                        ${product.name}
                    </a>
                </h3>

                <p class="product-id">
                    ${view.product_id}
                </p>

                <p class="product-price">
                    KSh ${product.price.toLocaleString()}
                </p>

                <p class="product-status ${product.status.toLowerCase()}">
                    ${product.status}
                </p>

                <p class="product-views">
                    ${view.view_count} view${view.view_count === 1 ? "" : "s"}
                </p>

                <a href="product.html?id=${view.product_id}">
                    View Design →
                </a>

            </div>
        `;

        mostViewedContainer.appendChild(card);

        updateInventoryStatus(card, view.product_id);

    });

})
        .catch(error => {
            console.error(
                "Failed to load most viewed products:",
                error
            );
        });
}


      
