// =========================
// FAVORITES PAGE
// =========================

const favoritesContainer =
    document.getElementById("favorites-products");

const noFavorites =
    document.getElementById("no-favorites");

const favorites =
    JSON.parse(localStorage.getItem("favorites")) || [];

const API_URL =
    "http://10.110.232.180:5000";

let inventory = {};


// =========================
// LOAD INVENTORY
// =========================

fetch(`${API_URL}/api/products/inventory`)
    .then(response => response.json())
    .then(data => {

        data.inventory.forEach(item => {
            inventory[item.product_id] = item.status;
        });

        displayFavorites();

    })
    .catch(error => {

        console.error(
            "Inventory lookup failed:",
            error
        );

        displayFavorites();

    });


// =========================
// DISPLAY FAVORITES
// =========================

function displayFavorites() {
 
    favoritesContainer.innerHTML = "";

    if (favorites.length === 0) {

        noFavorites.style.display = "block";
        return;

    }


    favorites.forEach(productId => {

        const product = products[productId];

        if (!product) return;


        const status =
            inventory[productId] || product.status;


        const card =
            document.createElement("div");

        card.className = "product-card";


        card.innerHTML = `
            <div class="product-image">

                <a href="product.html?id=${productId}">
                    <img
                        src="${product.image}"
                        alt="${product.name}"
                    >
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


                <p class="product-status ${status.toLowerCase()}">
                    ${status}
                </p>


                <a href="product.html?id=${productId}">
                    View Design →
                </a>


                <button
                    class="remove-favorite"
                    data-id="${productId}"
                >
                    Remove from Favorites
                </button>

            </div>
        `;


        favoritesContainer.appendChild(card);

    });


    // =========================
    // REMOVE FAVORITES
    // =========================

    document
        .querySelectorAll(".remove-favorite")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const productId =
                        button.dataset.id;


                    let savedFavorites =
                        JSON.parse(
                            localStorage.getItem(
                                "favorites"
                            )
                        ) || [];


                    savedFavorites =
                        savedFavorites.filter(
                            id => id !== productId
                        );


                    localStorage.setItem(
                        "favorites",
                        JSON.stringify(
                            savedFavorites
                        )
                    );


                    location.reload();

                }
            );

        });

}
