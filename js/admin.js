const API_URL = "https://maasai-beads-api.onrender.com";

const loginSection = document.getElementById("login-section");
const dashboardSection = document.getElementById("dashboard-section");

const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

const logoutButton = document.getElementById("logout-button");

const inventoryGrid = document.getElementById("inventory-grid");
const inventorySearch = document.getElementById("inventory-search");
const totalViews =
    document.getElementById("total-views");

const uniqueVisitors =
    document.getElementById("unique-visitors");

const productsViewed =
    document.getElementById("products-viewed");

const mostViewedList =
    document.getElementById("most-viewed-list");

const recentActivityList =
    document.getElementById("recent-activity-list");

const viewsChart =
    document.getElementById("views-chart");
const viewsChartTotal = document.getElementById("views-chart-total");

const filterButtons =
    document.querySelectorAll(".filter-button");


let inventory = [];
let currentFilter = "All";


/* =========================
   SCREEN CONTROL
========================= */

function showLogin() {

    loginSection.style.display = "flex";
    dashboardSection.style.display = "none";

}


function showDashboard() {

    loginSection.style.display = "none";
    dashboardSection.style.display = "block";

}

function updateInventorySummary() {

    const total =
        inventory.length;

    const available =
        inventory.filter(
            item => item.status === "Available"
        ).length;

    const sold =
        inventory.filter(
            item => item.status === "Sold"
        ).length;


    document.getElementById(
        "total-products"
    ).textContent = total;


    document.getElementById(
        "available-products"
    ).textContent = available;


    document.getElementById(
        "sold-products"
    ).textContent = sold;

}

async function loadAnalyticsSummary() {

    try {

        const response = await fetch(
            `${API_URL}/api/analytics/summary`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                "Failed to load analytics."
            );
        }

        totalViews.textContent =
            Number(data.analytics.totalViews);

        uniqueVisitors.textContent =
            Number(data.analytics.uniqueVisitors);

        productsViewed.textContent =
            Number(data.analytics.productsViewed);

    } catch (error) {

        console.error(
            "Analytics lookup failed:",
            error
        );

    }

}

async function loadMostViewedProducts() {

    try {

        const response = await fetch(
            `${API_URL}/api/products/most-viewed`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                "Failed to load most viewed products."
            );
        }

        mostViewedList.innerHTML = "";

        if (!data.products || data.products.length === 0) {

            mostViewedList.innerHTML = `
                <p>
                    No product views yet.
                </p>
            `;

            return;
        }

        data.products.forEach((item, index) => {

            const product =
                products[item.product_id];

            if (!product) return;

            const viewItem =
                document.createElement("div");

            viewItem.className =
                "most-viewed-item";

            viewItem.innerHTML = `

                <div class="most-viewed-image">

                    <img
                        src="${product.image}"
                        alt="${product.name}"
                    >

                </div>


                <div class="most-viewed-info">

                    <strong>
                        ${product.name}
                    </strong>

                    <span>
                        ${item.product_id}
                    </span>

                </div>


                <div class="most-viewed-count">

                    <strong>
                        ${item.view_count}
                    </strong>

                    <span>
                        ${item.view_count === 1
                            ? "view"
                            : "views"}
                    </span>

                </div>

            `;

            mostViewedList.appendChild(viewItem);

        });

    } catch (error) {

        console.error(
            "Most viewed lookup failed:",
            error
        );

        mostViewedList.innerHTML = `
            <p>
                Unable to load most viewed products.
            </p>
        `;

    }

}

async function loadRecentActivity() {

    try {

        const response = await fetch(
            `${API_URL}/api/analytics/recent`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                "Failed to load recent activity."
            );
        }

        recentActivityList.innerHTML = "";

        if (
            !data.activity ||
            data.activity.length === 0
        ) {

            recentActivityList.innerHTML = `
                <p>
                    No recent activity yet.
                </p>
            `;

            return;
        }

        data.activity.forEach(item => {

            const product =
                products[item.product_id];

            if (!product) return;

            const activityItem =
                document.createElement("div");

            activityItem.className =
                "recent-activity-item";

            const viewedAt =
                new Date(item.viewed_at);

            let timeText;

const now = new Date();
const diffSeconds =
    Math.floor((now - viewedAt) / 1000);

if (diffSeconds < 60) {

    timeText = "Just now";

} else if (diffSeconds < 3600) {

    const minutes =
        Math.floor(diffSeconds / 60);

    timeText =
        `${minutes} ${minutes === 1 ? "minute" : "minutes"} ago`;

} else if (diffSeconds < 86400) {

    const hours =
        Math.floor(diffSeconds / 3600);

    timeText =
        `${hours} ${hours === 1 ? "hour" : "hours"} ago`;

} else if (diffSeconds < 172800) {

    timeText = "Yesterday";

} else {

    timeText =
        viewedAt.toLocaleDateString(
            undefined,
            {
                month: "short",
                day: "numeric",
                year: "numeric"
            }
        );

}

            activityItem.innerHTML = `

                <div class="recent-activity-icon">
                    👁️
                </div>

                <div class="recent-activity-info">

                    <strong>
                        ${product.name}
                    </strong>

                    <span>
                        ${item.product_id}
                    </span>

                </div>

                <div class="recent-activity-time">
    ${timeText}
</div>

            `;

            recentActivityList.appendChild(
                activityItem
            );

        });

    } catch (error) {

        console.error(
            "Recent activity lookup failed:",
            error
        );

        recentActivityList.innerHTML = `
            <p>
                Unable to load recent activity.
            </p>
        `;

    }

}

async function loadViewsChart(range = "7") {

    try {

        const response = await fetch(
            `${API_URL}/api/analytics/views?range=${range}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                "Failed to load view analytics."
            );
        }

        const canvas =
            document.getElementById("views-chart");

        if (!canvas) return;

        const ctx =
            canvas.getContext("2d");

        const views =
            data.views || [];

const totalViewsForRange =
    views.reduce(
        (total, item) =>
            total + Number(item.views),
        0
    );

viewsChartTotal.textContent =
    totalViewsForRange;

        if (views.length === 0) {

            ctx.font = "16px Arial";
            ctx.fillText(
                "No view data yet.",
                20,
                40
            );

            return;
        }

        const width =
            canvas.clientWidth;

        const height = 300;

        canvas.width = width;
        canvas.height = height;

        ctx.clearRect(
            0,
            0,
            width,
            height
        );

        const padding = 45;

        const chartWidth =
            width - padding * 2;

        const chartHeight =
            height - padding * 2;

        const maxViews =
            Math.max(
                ...views.map(
                    item => Number(item.views)
                )
            );

        const points =
            views.map((item, index) => {

                const x =
                    padding +
                    (views.length === 1
                        ? chartWidth / 2
                        : index *
                          (chartWidth /
                          (views.length - 1)));

                const y =
                    padding +
                    chartHeight -
                    (
                        Number(item.views) /
                        maxViews
                    ) *
                    chartHeight;

                return {
                    x,
                    y,
                    value: Number(item.views),
                    date: item.date
                };

            });

        /* Grid */

        ctx.strokeStyle = "#eeeeee";
        ctx.lineWidth = 1;

        for (
            let i = 0;
            i <= 4;
            i++
        ) {

            const y =
                padding +
                (chartHeight / 4) * i;

            ctx.beginPath();

            ctx.moveTo(
                padding,
                y
            );

            ctx.lineTo(
                width - padding,
                y
            );

            ctx.stroke();

        }

        /* Line */

        ctx.strokeStyle = "#222";
        ctx.lineWidth = 3;

        ctx.beginPath();

        points.forEach(
            (point, index) => {

                if (index === 0) {

                    ctx.moveTo(
                        point.x,
                        point.y
                    );

                } else {

                    ctx.lineTo(
                        point.x,
                        point.y
                    );

                }

            }
        );

        ctx.stroke();

        /* Points */

        ctx.fillStyle = "#222";

        points.forEach(point => {

            ctx.beginPath();

            ctx.arc(
                point.x,
                point.y,
                5,
                0,
                Math.PI * 2
            );

            ctx.fill();

        });

        /* Labels */

        ctx.fillStyle = "#777";
        ctx.font = "12px Arial";
        ctx.textAlign = "center";

        points.forEach(point => {

            const date =
                new Date(point.date);

            const label =
                date.toLocaleDateString(
                    undefined,
                    {
                        month: "short",
                        day: "numeric"
                    }
                );

            ctx.fillText(
                label,
                point.x,
                height - 15
            );

        });

    } catch (error) {

        console.error(
            "Views chart lookup failed:",
            error
        );

    }

}


const chartRangeButtons =
    document.querySelectorAll(
        ".chart-range-button"
    );

chartRangeButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            chartRangeButtons.forEach(
                item => {
                    item.classList.remove(
                        "active"
                    );
                }
            );

            button.classList.add("active");

            const range =
                button.dataset.range;

            loadViewsChart(range);

        }
    );

});


/* =========================
   LOGOUT
========================= */

function logout() {

    localStorage.removeItem("adminToken");

    showLogin();

    inventory = [];

    inventoryGrid.innerHTML = "";

}


/* =========================
   LOGIN
========================= */

loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value;

    loginMessage.textContent = "";

    try {

        const response = await fetch(
            `${API_URL}/api/admin/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            loginMessage.textContent =
                data.message || "Login failed.";

            return;
        }

        localStorage.setItem(
            "adminToken",
            data.token
        );

        loginForm.reset();

        showDashboard();

        await loadInventory();

await loadAnalyticsSummary();

await loadMostViewedProducts();

await loadRecentActivity();

await loadViewsChart();

    } catch (error) {

        console.error("Login error:", error);

        loginMessage.textContent =
            "Unable to connect to the server.";

    }

});


/* =========================
   LOAD INVENTORY
========================= */

async function loadInventory() {

    inventoryGrid.innerHTML =
        "<p>Loading inventory...</p>";

    const token =
        localStorage.getItem("adminToken");

    if (!token) {

        showLogin();

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/api/products/inventory`
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.message || "Failed to load inventory."
            );

        }

        inventory = data.inventory || [];
        updateInventorySummary();

        renderInventory();

    } catch (error) {

        console.error(
            "Inventory loading error:",
            error
        );

        inventoryGrid.innerHTML =
            "<p>Unable to load inventory.</p>";

    }

}


/* =========================
   RENDER INVENTORY
========================= */

function renderInventory() {

    const searchTerm =
        inventorySearch.value
            .trim()
            .toLowerCase();


    const filteredInventory =
        inventory.filter((item) => {

            const product =
                products[item.product_id];


            const name =
                product?.name?.toLowerCase() || "";

            const category =
                product?.category?.toLowerCase() || "";

            const id =
                item.product_id.toLowerCase();


            const matchesSearch =
                id.includes(searchTerm) ||
                name.includes(searchTerm) ||
                category.includes(searchTerm);


            const matchesFilter =
                currentFilter === "All" ||
                item.status === currentFilter;


            return matchesSearch && matchesFilter;

        });


    inventoryGrid.innerHTML = "";


    if (filteredInventory.length === 0) {

        inventoryGrid.innerHTML =
            "<p>No matching products found.</p>";

        return;
    }


    filteredInventory.forEach((item) => {

        const product =
            products[item.product_id] || {};


        const card =
            document.createElement("div");

        card.className = "inventory-card";


            card.innerHTML = `

    <div class="inventory-image-wrapper">

        <img
            src="${product.image || "images/placeholder.jpg"}"
            alt="${product.name || item.product_id}"
            class="inventory-image"
        >

    </div>

    <p class="inventory-id">
        ${item.product_id}
    </p>

    <h3>
        ${product.name || "Unknown Product"}
    </h3>

            <p class="inventory-category">
                ${product.category || "Unknown Category"}
            </p>

            <div class="inventory-controls">

                <select>
                    <option value="Available"
                        ${item.status === "Available" ? "selected" : ""}>
                        Available
                    </option>

                    <option value="Sold"
                        ${item.status === "Sold" ? "selected" : ""}>
                        Sold
                    </option>
                </select>

                <button class="save-button">
                    Save
                </button>

            </div>

        `;


        const select =
            card.querySelector("select");

        const saveButton =
            card.querySelector(".save-button");


        saveButton.addEventListener(
            "click",
            () => updateInventory(
                item.product_id,
                select.value,
                saveButton
            )
        );


        inventoryGrid.appendChild(card);

    });

}


/* =========================
   UPDATE INVENTORY
========================= */

async function updateInventory(
    productId,
    status,
    button
) {

    const token =
        localStorage.getItem("adminToken");

    if (!token) {

        logout();

        return;
    }


    const originalText =
        button.textContent;


    button.textContent = "Saving...";

    button.disabled = true;


    try {

        const response = await fetch(
            `${API_URL}/api/products/${productId}/inventory`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    status
                })
            }
        );


        const data =
            await response.json();


        if (response.status === 401) {

            alert(
                "Your admin session has expired. Please sign in again."
            );

            logout();

            return;
        }


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Failed to update inventory."
            );

        }


        const item =
            inventory.find(
                product =>
                    product.product_id === productId
            );


        if (item) {

            item.status = data.inventory.status;
            updateInventorySummary();

            item.updated_at =
                data.inventory.updated_at;

        }


        button.textContent = "Saved";

        setTimeout(() => {

            button.textContent = originalText;

        }, 1200);


    } catch (error) {

        console.error(
            "Inventory update error:",
            error
        );

        alert(
            error.message ||
            "Failed to update inventory."
        );

        button.textContent =
            originalText;

    } finally {

        button.disabled = false;

    }

}


/* =========================
   SEARCH
========================= */

inventorySearch.addEventListener(
    "input",
    renderInventory
);


/* =========================
   FILTERS
========================= */

filterButtons.forEach((button) => {

    button.addEventListener(
        "click",
        () => {

            filterButtons.forEach(
                btn =>
                    btn.classList.remove("active")
            );


            button.classList.add("active");


            currentFilter =
                button.dataset.filter;


            renderInventory();

        }
    );

});


/* =========================
   LOGOUT BUTTON
========================= */

logoutButton.addEventListener(
    "click",
    logout
);


/* =========================
   INITIAL CHECK
========================= */

const existingToken =
    localStorage.getItem("adminToken");


if (existingToken) {

    showDashboard();

    loadInventory();

    loadAnalyticsSummary();

    loadMostViewedProducts();

    loadRecentActivity();

    loadViewsChart();


} else {

    showLogin();

}
