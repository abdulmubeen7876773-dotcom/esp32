<?php
defined( 'ABSPATH' ) || exit;

/* ---------------------------------------------------------------
   Theme setup
--------------------------------------------------------------- */
add_action( 'after_setup_theme', function () {
    load_theme_textdomain( 'esp32engine', get_template_directory() . '/languages' );

    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'align-wide' );
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'html5', [
        'search-form', 'comment-form', 'comment-list',
        'gallery', 'caption', 'style', 'script',
    ] );
    add_theme_support( 'custom-logo', [
        'height'      => 60,
        'width'       => 200,
        'flex-width'  => true,
        'flex-height' => true,
    ] );
    add_theme_support( 'editor-color-palette', [
        [ 'name' => 'Primary',   'slug' => 'primary',   'color' => '#6D28D9' ],
        [ 'name' => 'Secondary', 'slug' => 'secondary', 'color' => '#7C3AED' ],
        [ 'name' => 'Accent',    'slug' => 'accent',    'color' => '#A855F7' ],
    ] );

    // Image sizes used by project cards and guide cards
    add_image_size( 'esp32-card',   480, 320, true );
    add_image_size( 'esp32-banner', 960, 400, true );
    add_image_size( 'esp32-og',    1200, 630, true );

    register_nav_menus( [
        'primary'          => __( 'Primary Navigation', 'esp32engine' ),
        'footer-explore'   => __( 'Footer: Explore', 'esp32engine' ),
        'footer-cats'      => __( 'Footer: Categories', 'esp32engine' ),
        'footer-company'   => __( 'Footer: Company', 'esp32engine' ),
    ] );
} );

/* ---------------------------------------------------------------
   Enqueue assets
--------------------------------------------------------------- */
add_action( 'wp_enqueue_scripts', function () {
    $ver = '20260619';

    wp_enqueue_style(
        'google-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap',
        [],
        null
    );

    wp_enqueue_style(
        'esp32engine-style',
        get_template_directory_uri() . '/assets/css/style.css',
        [ 'google-fonts' ],
        $ver
    );

    wp_enqueue_script(
        'esp32engine-ui',
        get_template_directory_uri() . '/assets/js/ui.js',
        [],
        $ver,
        true
    );

    // GA4 ID from Customizer — injected before ui.js executes
    $ga4_id = get_theme_mod( 'esp32_ga4_id', 'G-WLHZKSEFP3' );
    wp_add_inline_script(
        'esp32engine-ui',
        'window.SITE_GA4=' . wp_json_encode( $ga4_id ) . ';',
        'before'
    );

    if ( is_singular( 'esp32_project' ) ) {
        wp_enqueue_script(
            'esp32engine-project',
            get_template_directory_uri() . '/assets/js/project.js',
            [],
            $ver,
            true
        );
    }

    if (
        is_post_type_archive( 'esp32_project' ) ||
        is_tax( 'project_category' ) ||
        is_search()
    ) {
        wp_enqueue_script(
            'esp32engine-projects',
            get_template_directory_uri() . '/assets/js/projects.js',
            [],
            $ver,
            true
        );
    }

    wp_enqueue_script(
        'esp32engine-icons',
        get_template_directory_uri() . '/assets/js/project-icons.js',
        [],
        $ver,
        true
    );

    /* Theme: dark mode + TOC + reading progress + phase filter */
    wp_enqueue_script(
        'esp32engine-theme',
        get_template_directory_uri() . '/assets/js/theme.js',
        [],
        $ver,
        false  // load in <head> so dark-mode applies before first paint
    );
} );

/* ---------------------------------------------------------------
   Remove wp-emoji and other unused head bloat
--------------------------------------------------------------- */
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'rsd_link' );

/* ---------------------------------------------------------------
   Custom excerpt length
--------------------------------------------------------------- */
add_filter( 'excerpt_length', fn() => 28 );
add_filter( 'excerpt_more', fn() => '…' );

/* ---------------------------------------------------------------
   Add SVG to allowed upload mime types
--------------------------------------------------------------- */
add_filter( 'upload_mimes', function ( $mimes ) {
    $mimes['svg']  = 'image/svg+xml';
    $mimes['svgz'] = 'image/svg+xml';
    return $mimes;
} );

/* ---------------------------------------------------------------
   REST API: expose custom meta fields for projects
--------------------------------------------------------------- */
add_action( 'rest_api_init', function () {
    $meta_fields = [
        'project_icon_class', 'project_icon_svg', 'project_lead',
        'project_read_time', 'project_dependencies',
        'beginner_overview', 'intermediate_overview', 'advanced_overview',
    ];
    foreach ( $meta_fields as $field ) {
        register_post_meta( 'esp32_project', $field, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => fn() => current_user_can( 'edit_posts' ),
        ] );
    }
} );

/* ---------------------------------------------------------------
   Redirect /projects.html, /guides.html, etc. to clean URLs
--------------------------------------------------------------- */
add_action( 'template_redirect', function () {
    $redirects = [
        '/projects.html'  => '/projects/',
        '/guides.html'    => '/guides/',
        '/about.html'     => '/about/',
        '/contact.html'   => '/contact/',
        '/privacy.html'   => '/privacy/',
        '/terms.html'     => '/terms/',
        '/disclaimer.html'=> '/disclaimer/',
        '/sitemap.html'   => '/sitemap_index.xml',
    ];
    $path = parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ) ?? '';
    if ( isset( $redirects[ $path ] ) ) {
        wp_redirect( home_url( $redirects[ $path ] ), 301 );
        exit;
    }
    // /category/iot-projects.html → /category/iot-projects/
    if ( preg_match( '#^/category/([^/]+)\.html$#', $path, $m ) ) {
        wp_redirect( home_url( '/category/' . $m[1] . '/' ), 301 );
        exit;
    }
    // /projects/esp32-air-quality-monitor.html → /projects/esp32-air-quality-monitor/
    if ( preg_match( '#^/projects/([^/]+)\.html$#', $path, $m ) ) {
        wp_redirect( home_url( '/projects/' . $m[1] . '/' ), 301 );
        exit;
    }
    // /guides/what-is-esp32.html → /guides/what-is-esp32/
    if ( preg_match( '#^/guides/([^/]+)\.html$#', $path, $m ) ) {
        wp_redirect( home_url( '/guides/' . $m[1] . '/' ), 301 );
        exit;
    }
} );

/* ---------------------------------------------------------------
   Helper: site logo markup (reusable in header.php)
--------------------------------------------------------------- */
function esp32_logo_html(): string {
    return '<a class="site-logo" href="' . esc_url( home_url( '/' ) ) . '">'
        . '<span class="logo-mark" aria-hidden="true"></span>'
        . '<span class="logo-text">ESP32<span class="logo-accent">Engine</span></span>'
        . '<span class="logo-tagline">Learn | Build | Innovate</span>'
        . '</a>';
}

/* ---------------------------------------------------------------
   Helper: active nav class
--------------------------------------------------------------- */
function esp32_nav_class( string $url ): string {
    $current = home_url( add_query_arg( [], $GLOBALS['wp']->request ?? '' ) );
    return ( rtrim( $current, '/' ) === rtrim( $url, '/' ) ) ? ' class="active"' : '';
}

/* ---------------------------------------------------------------
   Helper: render breadcrumb (used in templates)
--------------------------------------------------------------- */
function esp32_breadcrumb( array $crumbs ): void {
    echo '<nav class="breadcrumb" aria-label="Breadcrumb"><ol>';
    foreach ( $crumbs as $i => $crumb ) {
        $last = ( $i === array_key_last( $crumbs ) );
        if ( $last ) {
            echo '<li aria-current="page">' . esc_html( $crumb['label'] ) . '</li>';
        } else {
            echo '<li><a href="' . esc_url( $crumb['url'] ) . '">' . esc_html( $crumb['label'] ) . '</a></li>';
        }
    }
    echo '</ol></nav>';
}

/* ---------------------------------------------------------------
   Helper: category icon SVGs (mirrors project-icons.js)
--------------------------------------------------------------- */
function esp32_category_icon( string $slug ): string {
    $icons = [
        'iot-projects' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M10 28C22 18 42 18 54 28" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M18 36C26 29 38 29 46 36" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M26 44C29 41 35 41 38 44" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="50" r="3" fill="currentColor"/><rect x="26" y="12" width="12" height="8" rx="2" stroke="currentColor" stroke-width="1.6"/></svg>',
        'home-automation' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M10 30L32 14L54 30V50H10V30Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><rect x="24" y="36" width="16" height="14" rx="1" fill="currentColor" opacity=".18" stroke="currentColor" stroke-width="1.8"/><path d="M44 22C44 22 48 18 52 20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="50" cy="18" r="2" fill="currentColor"/></svg>',
        'esp32-cam' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="10" y="22" width="44" height="30" rx="4" stroke="currentColor" stroke-width="2"/><circle cx="32" cy="37" r="9" stroke="currentColor" stroke-width="2"/><circle cx="32" cy="37" r="4" fill="currentColor" opacity=".35"/><path d="M22 22L26 16H38L42 22" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
        'robotics' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="16" y="20" width="32" height="28" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="26" cy="32" r="3" fill="currentColor"/><circle cx="38" cy="32" r="3" fill="currentColor"/><path d="M24 42H40" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M32 12V20M20 16H14M44 16H50" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        'sensor-projects' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><circle cx="32" cy="32" r="10" stroke="currentColor" stroke-width="2"/><path d="M32 10V18M32 46V54M10 32H18M46 32H54M16 16L22 22M42 42L48 48M48 16L42 22M22 42L16 48" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
        'ai-projects' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="18" y="18" width="28" height="28" rx="4" stroke="currentColor" stroke-width="2"/><rect x="24" y="24" width="16" height="16" rx="2" fill="currentColor" opacity=".2"/><path d="M18 26H12M18 32H12M18 38H12M46 26H52M46 32H52M46 38H52M26 18V12M32 18V12M38 18V12M26 46V52M32 46V52M38 46V52" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
        'security-projects' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 10L52 18V32C52 42 43 50 32 54C21 50 12 42 12 32V18L32 10Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M24 32L30 38L42 26" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'led-projects' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 10C22 10 16 18 16 28C16 36 22 40 24 44H40C42 40 48 36 48 28C48 18 42 10 32 10Z" stroke="currentColor" stroke-width="2"/><path d="M24 48H40V52H24V48Z" fill="currentColor" opacity=".25" stroke="currentColor" stroke-width="1.6"/></svg>',
        'agriculture' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 54V34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M32 34C32 34 18 30 16 18C24 20 32 28 32 34Z" fill="currentColor" opacity=".22" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M32 34C32 34 46 30 48 18C40 20 32 28 32 34Z" fill="currentColor" opacity=".22" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M20 54H44" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        'environmental' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 54V34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M32 34C32 34 18 30 16 18C24 20 32 28 32 34Z" fill="currentColor" opacity=".22" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M32 34C32 34 46 30 48 18C40 20 32 28 32 34Z" fill="currentColor" opacity=".22" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M20 54H44" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        'healthcare' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="14" y="14" width="36" height="36" rx="8" stroke="currentColor" stroke-width="2"/><path d="M32 22V42M22 32H42" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
        'energy-monitoring' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M34 10L18 36H30L28 54L46 28H34L34 10Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="currentColor" opacity=".18"/></svg>',
        'smart-city' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="10" y="28" width="14" height="22" stroke="currentColor" stroke-width="2"/><rect x="28" y="18" width="12" height="32" stroke="currentColor" stroke-width="2"/><rect x="44" y="34" width="10" height="16" stroke="currentColor" stroke-width="2"/><path d="M8 50H56" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        'industrial-automation' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M10 50H54V30L42 36V22L30 28V18L10 30V50Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M18 50V40M26 50V36M34 50V42M42 50V34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        'education' => '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M14 14H34C40 14 44 18 44 24V50C40 46 36 44 30 44H14V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M50 14H30C24 14 20 18 20 24V50C24 46 28 44 34 44H50V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    ];
    return $icons[ $slug ] ?? '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><circle cx="32" cy="32" r="20" stroke="currentColor" stroke-width="2"/></svg>';
}

/* ---------------------------------------------------------------
   Prioritize project_category rewrite rules over built-in category.
   Both use /category/ slug — add_rewrite_rule('top') prepends ours
   so they match before WordPress's built-in category rules.
--------------------------------------------------------------- */
add_action( 'init', function (): void {
    add_rewrite_rule(
        'category/([^/]+)/feed/(feed|rdf|rss|rss2|atom)/?$',
        'index.php?project_category=$matches[1]&feed=$matches[2]',
        'top'
    );
    add_rewrite_rule(
        'category/([^/]+)/page/?([0-9]{1,})/?$',
        'index.php?project_category=$matches[1]&paged=$matches[2]',
        'top'
    );
    add_rewrite_rule(
        'category/([^/]+)/embed/?$',
        'index.php?project_category=$matches[1]&embed=true',
        'top'
    );
    add_rewrite_rule(
        'category/([^/]+)/?$',
        'index.php?project_category=$matches[1]',
        'top'
    );
}, 1 );

/* ---------------------------------------------------------------
   Include inc files
--------------------------------------------------------------- */
require_once get_template_directory() . '/inc/post-types.php';
require_once get_template_directory() . '/inc/taxonomies.php';
require_once get_template_directory() . '/inc/schema.php';
require_once get_template_directory() . '/inc/admin.php';
require_once get_template_directory() . '/inc/customizer.php';
