const productGrid = document.getElementById("product-grid");
const filterButtons = document.querySelectorAll(".filter-btn");
const searchInput = document.getElementById("search-input");
const sortSelect = document.getElementById("sort-select");
const productCount = document.getElementById("product-count");
const clearFilters = document.getElementById("clear-filters");

let inventory = {};

fetch("https://YOUR-RENDER-URL.onrender.com/api/products/inventory")
    .then(response => response.json())
    .then(data => {

        data.inventory.forEach(item => {
            inventory[item.product_id] = item.status;
        });

        displayProducts();

    })
    .catch(error => {
        console.error("Inventory lookup failed:", error);
        displayProducts();
    });

function displayProducts(category = "All") {

    productGrid.innerHTML = "";

    const searchTerm = searchInput.value.toLowerCase().trim();
    const sortOption = sortSelect.value;

    let filteredProducts = [];

    for (const productId in products) {

        const product = products[productId];

        if (category !== "All" && product.category !== category) {
            continue;
        }

        const searchableText = `
            ${productId}
            ${product.name}
            ${product.category}
            ${product.description || ""}
        `.toLowerCase();

        if (searchTerm && !searchableText.includes(searchTerm)) {
            continue;
        }

        filteredProducts.push({
            id: productId,
            ...product
        });
    }

    if (sortOption === "price-low") {
        filteredProducts.sort((a, b) => a.price - b.price);
    }

    if (sortOption === "price-high") {
        filteredProducts.sort((a, b) => b.price - a.price);
    }

    if (sortOption === "name-az") {
        filteredProducts.sort((a, b) =>
            a.name.localeCompare(b.name)
        );
    }

    if (sortOption === "name-za") {
        filteredProducts.sort((a, b) =>
            b.name.localeCompare(a.name)
        );
    }

if (filteredProducts.length === 0) {

    productCount.textContent = "Showing 0 products";

    productGrid.innerHTML = `
        <div class="no-results">
            <h3>No products found</h3>
            <p>Try another search or clear your filters.</p>
        </div>
    `;

    return;
}
   productCount.textContent =
    `Showing ${filteredProducts.length} product${filteredProducts.length === 1 ? "" : "s"}`;

    filteredProducts.forEach(product => {

        const productId = product.id;

        const productCard = document.createElement("div");
        productCard.className = "product-card";

const isNew =
    product.added &&
    (new Date() - new Date(product.added)) /
        (1000 * 60 * 60 * 24) <= 14;

        productCard.innerHTML = `
${isNew ? '<span class="new-badge">NEW</span>' : ''}

    <div class="product-image" onclick="window.location.href='product.html?id=${productId}'">
        <img src="${product.image}" alt="${product.name}">
    </div>

    <div class="product-info">

        <p class="product-category">
            ${product.category}
        </p>

        <h3 onclick="window.location.href='product.html?id=${productId}'">
            ${product.name}
        </h3>

        <p class="product-id">
            ${productId}
        </p>

        <p class="product-price">
            KSh ${product.price.toLocaleString()}
        </p>

        <p class="product-status ${((inventory[productId] || product.status).toLowerCase())}">
            ${inventory[productId] || product.status}
        </p>

        <a href="product.html?id=${productId}">
            View Design →
        </a>

    </div>
`;

        productGrid.appendChild(productCard);

    });
}


filterButtons.forEach(button => {

    button.addEventListener("click", function() {

        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        this.classList.add("active");

        const category = this.dataset.category;

        displayProducts(category);

    });

});

searchInput.addEventListener("input", function() {

    const activeButton = document.querySelector(".filter-btn.active");

    const category = activeButton
        ? activeButton.dataset.category
        : "All";

    displayProducts(category);

});

sortSelect.addEventListener("change", function() {

    const activeButton = document.querySelector(".filter-btn.active");

    const category = activeButton
        ? activeButton.dataset.category
        : "All";

    displayProducts(category);

});

clearFilters.addEventListener("click", function() {

    searchInput.value = "";
    sortSelect.value = "default";

    filterButtons.forEach(button => {
        button.classList.remove("active");
    });

    const allButton = document.querySelector(
        '.filter-btn[data-category="All"]'
    );

    allButton.classList.add("active");

    displayProducts("All");

});
