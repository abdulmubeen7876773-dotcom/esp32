#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ESP32Engine — Production Deployment Script                             ║
# ║  Run on the production server (Linux/Apache shared hosting or VPS)      ║
# ║  Prerequisites: PHP 8.1+, MySQL, WP-CLI (wp), SSH access               ║
# ╚══════════════════════════════════════════════════════════════════════════╝
set -euo pipefail

# ── Variables — edit before running ──────────────────────────────────────────
WP_DIR="/var/www/html"                          # web root on production server
DB_NAME="esp32engine"
DB_USER="your_db_user"
DB_PASS="your_db_password"
DB_HOST="localhost"
BACKUP_SQL="esp32engine-db-export-2026-06-19.sql"

echo "═══════════════════════════════════════════════"
echo " ESP32Engine Production Deploy — $(date)"
echo "═══════════════════════════════════════════════"

# ── Step 1: Upload WordPress files ───────────────────────────────────────────
echo ""
echo "Step 1: Upload WordPress files (run from local machine via rsync)"
echo "  rsync -avz --delete D:/xampp/htdocs/esp32/ user@yourhost.com:$WP_DIR/"
echo "  (skip wp-config.php — will be set separately)"

# ── Step 2: Upload and import database ───────────────────────────────────────
echo ""
echo "Step 2: Import database"
echo "  # Create DB first:"
echo "  mysql -u root -p -e \"CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\""
echo ""
echo "  # Import dump:"
echo "  mysql -u $DB_USER -p $DB_NAME < $BACKUP_SQL"

# ── Step 3: Write production wp-config.php ───────────────────────────────────
echo ""
echo "Step 3: Create production wp-config.php"
cat > /tmp/wp-config-prod.php << 'WPCONFIG'
<?php
define('DB_NAME',     'esp32engine');
define('DB_USER',     'your_db_user');
define('DB_PASSWORD', 'your_db_password');
define('DB_HOST',     'localhost');
define('DB_CHARSET',  'utf8mb4');
define('DB_COLLATE',  '');

// Generate fresh keys at: https://api.wordpress.org/secret-key/1.1/salt/
define('AUTH_KEY',         'PUT_YOUR_KEY_HERE');
define('SECURE_AUTH_KEY',  'PUT_YOUR_KEY_HERE');
define('LOGGED_IN_KEY',    'PUT_YOUR_KEY_HERE');
define('NONCE_KEY',        'PUT_YOUR_KEY_HERE');
define('AUTH_SALT',        'PUT_YOUR_KEY_HERE');
define('SECURE_AUTH_SALT', 'PUT_YOUR_KEY_HERE');
define('LOGGED_IN_SALT',   'PUT_YOUR_KEY_HERE');
define('NONCE_SALT',       'PUT_YOUR_KEY_HERE');

$table_prefix = 'wp_';

define('WP_DEBUG',          false);
define('WP_DEBUG_LOG',      false);
define('DISALLOW_FILE_EDIT', true);

// HTTPS enforcement
define('FORCE_SSL_ADMIN', true);
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

// NOTE: ESP32_PROD_URL constant is NOT needed on production because
// siteurl/home in DB will be set to https://esp32engine.com directly.
// Remove it from any local dev wp-config.php before copying.

if (!defined('ABSPATH')) define('ABSPATH', __DIR__ . '/');
require_once ABSPATH . 'wp-settings.php';
WPCONFIG
echo "  # Written to /tmp/wp-config-prod.php — copy to $WP_DIR/wp-config.php"

# ── Step 4: Update siteurl and home in database ───────────────────────────────
echo ""
echo "Step 4: Update WordPress URLs in database (run via WP-CLI)"
echo "  wp option update siteurl 'https://esp32engine.com' --path=$WP_DIR"
echo "  wp option update home    'https://esp32engine.com' --path=$WP_DIR"
echo ""
echo "  # Verify:"
echo "  wp option get siteurl --path=$WP_DIR"
echo "  wp option get home    --path=$WP_DIR"

# ── Step 5: Search-replace localhost URLs in post content ────────────────────
echo ""
echo "Step 5: Search-replace any localhost/esp32 URLs in post content"
echo "  wp search-replace 'http://localhost/esp32' 'https://esp32engine.com' \\"
echo "    --path=$WP_DIR --all-tables --dry-run"
echo ""
echo "  # If dry-run output looks correct, run without --dry-run:"
echo "  wp search-replace 'http://localhost/esp32' 'https://esp32engine.com' \\"
echo "    --path=$WP_DIR --all-tables"

# ── Step 6: Flush rewrite rules and caches ────────────────────────────────────
echo ""
echo "Step 6: Flush rewrite rules and transients"
echo "  wp rewrite flush --path=$WP_DIR"
echo "  wp cache flush  --path=$WP_DIR"
echo "  wp transient delete --all --path=$WP_DIR"

# ── Step 7: Remove the ESP32_PROD_URL constant from wp-config.php ────────────
echo ""
echo "Step 7: Remove ESP32_PROD_URL from wp-config.php"
echo "  # Delete this line from wp-config.php on the production server:"
echo "  # define( 'ESP32_PROD_URL', 'https://esp32engine.com' );"
echo "  # (not needed once siteurl/home are set correctly in DB)"

# ── Step 8: Configure .htaccess for root install ──────────────────────────────
echo ""
echo "Step 8: Replace .htaccess with production version"
echo "  # Use wp-theme/esp32engine/tools/production-htaccess.txt"
echo "  cp production-htaccess.txt $WP_DIR/.htaccess"
echo "  # Key difference from local: RewriteBase / (not /esp32/)"

# ── Step 9: Upload og-image.jpg if not already there ─────────────────────────
echo ""
echo "Step 9: Verify og-image.jpg exists at web root"
echo "  ls -la $WP_DIR/og-image.jpg"
echo "  # If missing: upload from D:/xampp/htdocs/esp32/og-image.jpg"
echo "  # Must be at https://esp32engine.com/og-image.jpg"

# ── Step 10: Verify production analytics ─────────────────────────────────────
echo ""
echo "Step 10: Post-deploy analytics verification"
echo "  curl -s https://esp32engine.com/ | grep -o 'G-WLHZKSEFP3'"
echo "  curl -s https://esp32engine.com/guides/ | grep -o 'G-WLHZKSEFP3'"
echo "  curl -s https://esp32engine.com/wp-sitemap.xml | grep -c '<loc>'"

# ── Step 11: Google Search Console ───────────────────────────────────────────
echo ""
echo "Step 11: Google Search Console (manual)"
echo "  1. Open https://search.google.com/search-console"
echo "  2. Add property: https://esp32engine.com"
echo "  3. Submit sitemap: https://esp32engine.com/wp-sitemap.xml"
echo "  4. Request indexing for: https://esp32engine.com/"
echo "  5. Install Tag Assistant extension, visit https://esp32engine.com"
echo "     Verify G-WLHZKSEFP3 fires page_view events"

echo ""
echo "═══════════════════════════════════════════════"
echo " Deploy checklist complete."
echo "═══════════════════════════════════════════════"
