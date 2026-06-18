# ESP32 Engine — WordPress Setup Guide

## 1. Install WordPress on XAMPP

1. Download WordPress from https://wordpress.org/download/
2. Extract to `D:\xampp\htdocs\esp32\` (or any folder you prefer)
3. Start XAMPP: Apache + MySQL

## 2. Create Database

Open phpMyAdmin at http://localhost/phpmyadmin  
Create a new database named `esp32engine` (charset: `utf8mb4`, collation: `utf8mb4_unicode_ci`)

## 3. WordPress config

Copy `wp-config-sample.php` → `wp-config.php` and set:
```php
define( 'DB_NAME',     'esp32engine' );
define( 'DB_USER',     'root' );        // XAMPP default
define( 'DB_PASSWORD', '' );            // XAMPP default (empty)
define( 'DB_HOST',     'localhost' );
define( 'DB_CHARSET',  'utf8mb4' );
```

Generate fresh keys at https://api.wordpress.org/secret-key/1.1/salt/

## 4. Install WordPress

Visit http://localhost/esp32/ and complete the 5-minute install.  
Set Site URL to `http://localhost/esp32/`

## 5. Activate the Theme

1. Copy `wp-theme/esp32engine/` to `wp-content/themes/esp32engine/`
2. Go to **Appearance → Themes** and activate **ESP32 Engine**

## 6. Set Permalinks

Go to **Settings → Permalinks** → select **Post name** → Save Changes  
This flushes rewrite rules and makes `/projects/my-project/` work.

Copy `wp-theme/esp32engine/htaccess.txt` → rename to `.htaccess` in your WordPress root.

## 7. Set Up Menus

Go to **Appearance → Menus** and create:
- **Primary Navigation** — add Home, Projects, Guides, About, Contact
- **Footer: Explore** — optional footer links
- **Footer: Categories** — optional category links

Assign each menu to its location.

## 8. Configure Theme Options

Go to **Appearance → Customize → ESP32 Engine Settings**:
- Set your **GA4 ID** (e.g. `G-WLHZKSEFP3`)
- Set **GitHub URL** and **YouTube URL**
- Optionally tweak accent colors

## 9. Import Content (Optional)

If you have the static site content:
```bash
# From WordPress root, using WP-CLI:
wp eval-file wp-content/themes/esp32engine/tools/import-content.php
```

Or create posts manually via **Projects → Add New**.

## 10. Creating a New Project

1. Go to **Projects → Add New**
2. Fill in the **Title** (becomes the URL slug)
3. Fill in the **Project Details** sidebar: icon, lead sentence, read time, components
4. Use the **Difficulty Level Content** tab panel to add content for Beginner / Intermediate / Advanced
5. Assign a **Project Category** and **Featured Image**
6. Publish

## Local URL Structure

| URL | Page |
|---|---|
| `http://localhost/esp32/` | Homepage |
| `http://localhost/esp32/projects/` | All Projects |
| `http://localhost/esp32/projects/esp32-air-quality-monitor/` | Project detail |
| `http://localhost/esp32/guides/` | All Guides |
| `http://localhost/esp32/category/iot-projects/` | Category archive |
| `http://localhost/esp32/wp-admin/` | Admin panel |

## Deploying to Live Hosting

1. Export your local database: phpMyAdmin → Export → SQL
2. Upload all WordPress files to `public_html/` via FTP
3. Import SQL on live host's phpMyAdmin
4. Update `wp-config.php` with live DB credentials
5. Update Site URL: **Settings → General** → change to `https://esp32engine.com/`
6. Point your domain DNS to the hosting server
