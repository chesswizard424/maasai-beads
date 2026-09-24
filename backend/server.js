require("dotenv").config();

const express = require("express");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { Pool } = require("pg");
console.log("DATABASE_URL exists:", !!process.env.DATABASE_URL);

const app = express();
const PORT = process.env.PORT || 5000;

// Database connection
const pool = new Pool(
    process.env.DATABASE_URL
        ? {
            connectionString: process.env.DATABASE_URL,
            ssl: process.env.NODE_ENV === "production"
                ? { rejectUnauthorized: false }
                : false
        }
        : {
            user: process.env.DB_USER,
            host: process.env.DB_HOST,
            database: process.env.DB_NAME,
            password: process.env.DB_PASSWORD,
            port: process.env.DB_PORT
        }
);

// Middleware
app.use(express.json());

app.use(cors({
    origin: [
        "http://localhost:8000",
        "http://10.110.232.180:8000"
    ]
}));

const viewLimiter = rateLimit({
    windowMs: 60 * 1000,
    max: 30,
    message: {
        message: "Too many view requests. Please try again later."
    }
});

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: {
        message: "Too many login attempts. Please try again later."
    }
});


// Test API route
app.get("/", (req, res) => {
    res.json({
        message: "Maasai Beadwork API is running."
    });
});

// Test database connection
// Test database connection
app.get("/api/test-db", async (req, res) => {

    try {

        const result = await pool.query(
            "SELECT NOW()"
        );

        res.json({
            message: "Database connected successfully.",
            time: result.rows[0].now
        });

    } catch (error) {

        console.error("Database error:", error);

        res.status(500).json({
            message: "Database connection failed."
        });

    }

});


// Record a product view
app.post(
    "/api/products/:productId/view",
    viewLimiter,
    async (req, res) => {

    const { productId } = req.params;

    if (!/^MB-[A-Z]+-\d{3}$/.test(productId)) {
        return res.status(400).json({
            message: "Invalid product ID."
        });
    }

    const { visitorId } = req.body || {};

    if (!visitorId) {
        return res.status(400).json({
            message: "Visitor ID is required."
        });
    }

    const client = await pool.connect();

    try {

        await client.query("BEGIN");

        /*
         * Record this visitor first.
         * ON CONFLICT prevents the same visitor
         * from being counted twice for the same product.
         */
        const viewerResult = await client.query(
            `
            INSERT INTO product_viewers
                (product_id, visitor_id)
            VALUES
                ($1, $2)

            ON CONFLICT (product_id, visitor_id)
            DO NOTHING

            RETURNING product_id, visitor_id;
            `,
            [productId, visitorId]
        );

        /*
         * Visitor has already viewed this product.
         * Do not increase the view count.
         */
        if (viewerResult.rows.length === 0) {

            await client.query("COMMIT");

            return res.json({
                message: "View already recorded for this visitor."
            });
        }

        /*
         * New visitor.
         * Increase the product's total view count.
         */
        const result = await client.query(
            `
            INSERT INTO product_views
                (product_id, view_count, last_viewed)
            VALUES
                ($1, 1, CURRENT_TIMESTAMP)

            ON CONFLICT (product_id)
            DO UPDATE SET
                view_count = product_views.view_count + 1,
                last_viewed = CURRENT_TIMESTAMP

            RETURNING product_id, view_count, last_viewed;
            `,
            [productId]
        );

        await client.query("COMMIT");

        res.json({
            message: "Product view recorded.",
            product: result.rows[0]
        });

    } catch (error) {

        try {
            await client.query("ROLLBACK");
        } catch (rollbackError) {
            console.error("Rollback error:", rollbackError);
        }

        console.error("View tracking error:", error);

        res.status(500).json({
            message: "Failed to record product view."
        });

    } finally {

        client.release();

    }

});
// Get most viewed products

app.get("/api/products/:productId/inventory", async (req, res) => {

    const { productId } = req.params;

    if (!/^MB-[A-Z]+-\d{3}$/.test(productId)) {
        return res.status(400).json({
            message: "Invalid product ID."
        });
    }

    try {

        const result = await pool.query(
            `
            SELECT product_id, status, updated_at
            FROM product_inventory
            WHERE product_id = $1;
            `,
            [productId]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({
                message: "Inventory record not found."
            });
        }

        res.json({
            inventory: result.rows[0]
        });

    } catch (error) {

        console.error("Inventory lookup error:", error);

        res.status(500).json({
            message: "Failed to retrieve inventory."
        });

    }

});

app.get("/api/products/inventory", async (req, res) => {

    try {

        const result = await pool.query(`
            SELECT product_id, status, updated_at
            FROM product_inventory
            ORDER BY product_id;
        `);

        res.json({
            inventory: result.rows
        });

    } catch (error) {

        console.error("Inventory lookup error:", error);

        res.status(500).json({
            message: "Failed to retrieve inventory."
        });

    }

});

async function authenticateAdmin(req, res, next) {

    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return res.status(401).json({
            message: "Authentication required."
        });
    }

    const token = authHeader.split(" ")[1];

    try {

        const decoded = jwt.verify(
            token,
            process.env.JWT_SECRET
        );

        const result = await pool.query(
            `
            SELECT id, username
            FROM admin_users
            WHERE id = $1;
            `,
            [decoded.adminId]
        );

        if (result.rows.length === 0) {
            return res.status(401).json({
                message: "Admin account not found."
            });
        }

        req.admin = result.rows[0];

        next();

    } catch (error) {

        console.error("Authentication error:", error);

        return res.status(401).json({
            message: "Invalid or expired token."
        });

    }

}


//Get most viewed products
app.get("/api/products/most-viewed", async (req, res) => {

    try {

        const result = await pool.query(`
            SELECT product_id, view_count, last_viewed
            FROM product_views
            ORDER BY view_count DESC
            LIMIT 6;
        `);

        res.json({
            products: result.rows
        });

    } catch (error) {

        console.error("Most viewed error:", error);

        res.status(500).json({
            message: "Failed to retrieve most viewed products."
        });

    }

});

// Get analytics summary
app.get("/api/analytics/summary", async (req, res) => {

    try {

        const result = await pool.query(`
            SELECT
                (SELECT COALESCE(SUM(view_count), 0)
                 FROM product_views) AS "totalViews",

                (SELECT COUNT(DISTINCT visitor_id)
                 FROM product_viewers) AS "uniqueVisitors",

                (SELECT COUNT(DISTINCT product_id)
                 FROM product_viewers) AS "productsViewed";
        `);

        res.json({
            analytics: result.rows[0]
        });

    } catch (error) {

        console.error(
            "Analytics summary error:",
            error
        );

        res.status(500).json({
            message: "Failed to retrieve analytics summary."
        });

    }

});


// Get recent product activity
app.get("/api/analytics/recent", async (req, res) => {

    try {

        const result = await pool.query(`
            SELECT
                product_id,
                viewed_at
            FROM product_viewers
            ORDER BY viewed_at DESC
            LIMIT 10;
        `);

        res.json({
            activity: result.rows
        });

    } catch (error) {

        console.error(
            "Recent analytics error:",
            error
        );

        res.status(500).json({
            message: "Failed to retrieve recent activity."
        });

    }

});


// Get daily product views
// Get product views over time
app.get("/api/analytics/views", async (req, res) => {

    const range =
        req.query.range || "7";

    const allowedRanges = [
        "7",
        "30",
        "all"
    ];

    if (!allowedRanges.includes(range)) {

        return res.status(400).json({
            message: "Invalid analytics range."
        });

    }

    try {

        let query;
        let params = [];

        if (range === "all") {

            query = `
                SELECT
                    dates.date,
                    COALESCE(
                        COUNT(product_viewers.viewed_at),
                        0
                    ) AS views

                FROM generate_series(
                    (
                        SELECT
                            MIN(DATE(viewed_at))
                        FROM product_viewers
                    ),
                    CURRENT_DATE,
                    INTERVAL '1 day'
                ) AS dates(date)

                LEFT JOIN product_viewers
                    ON DATE(product_viewers.viewed_at)
                        = dates.date

                GROUP BY dates.date

                ORDER BY dates.date ASC;
            `;

        } else {

            query = `
                SELECT
                    dates.date,
                    COALESCE(
                        COUNT(product_viewers.viewed_at),
                        0
                    ) AS views

                FROM generate_series(
                    CURRENT_DATE
                        - ($1::integer - 1),
                    CURRENT_DATE,
                    INTERVAL '1 day'
                ) AS dates(date)

                LEFT JOIN product_viewers
                    ON DATE(product_viewers.viewed_at)
                        = dates.date

                GROUP BY dates.date

                ORDER BY dates.date ASC;
            `;

            params = [
                Number(range)
            ];

        }

        const result =
            await pool.query(
                query,
                params
            );

        res.json({
            range,
            views: result.rows
        });

    } catch (error) {

        console.error(
            "Views analytics error:",
            error
        );

        res.status(500).json({
            message:
                "Failed to retrieve view analytics."
        });

    }

});
//login limiter

app.post("/api/admin/login", loginLimiter, async (req, res) => {

    const { username, password } = req.body || {};

    if (!username || !password) {
        return res.status(400).json({
            message: "Username and password are required."
        });
    }

    try {

        const result = await pool.query(
            `
            SELECT id, username, password_hash
            FROM admin_users
            WHERE username = $1;
            `,
            [username]
        );

        if (result.rows.length === 0) {
            return res.status(401).json({
                message: "Invalid credentials."
            });
        }

        const admin = result.rows[0];

        const passwordValid = await bcrypt.compare(
            password,
            admin.password_hash
        );

        if (!passwordValid) {
            return res.status(401).json({
                message: "Invalid credentials."
            });
        }

        const token = jwt.sign(
            {
                adminId: admin.id,
                username: admin.username
            },
            process.env.JWT_SECRET,
            {
                expiresIn: "2h"
            }
        );

        res.json({
            message: "Login successful.",
            token: token
        });

    } catch (error) {

        console.error("Admin login error:", error);

        res.status(500).json({
            message: "Login failed."
        });

    }

});
// Start server
app.put(
    "/api/products/:productId/inventory",
    authenticateAdmin,
    async (req, res) => {

    const { productId } = req.params;
    const { status } = req.body || {};

    if (!/^MB-[A-Z]+-\d{3}$/.test(productId)) {
        return res.status(400).json({
            message: "Invalid product ID."
        });
    }

    if (!["Available", "Sold"].includes(status)) {
        return res.status(400).json({
            message: "Invalid inventory status."
        });
    }

    try {

        const result = await pool.query(
            `
            UPDATE product_inventory
            SET
                status = $1,
                updated_at = CURRENT_TIMESTAMP
            WHERE product_id = $2
            RETURNING product_id, status, updated_at;
            `,
            [status, productId]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({
                message: "Inventory record not found."
            });
        }

        res.json({
            message: "Inventory updated successfully.",
            inventory: result.rows[0]
        });

    } catch (error) {

        console.error(
            "Inventory update error:",
            error
        );

        res.status(500).json({
            message: "Failed to update inventory."
        });

    }

});
app.listen(PORT, "0.0.0.0", () => {
    console.log(
        `Backend server running on port ${PORT}`
    );
});
