<?php
/**
 * ESP32 Engine — Content Import Script
 *
 * Run once via WP-CLI after installing WordPress and activating the theme:
 *   wp eval-file wp-content/themes/esp32engine/tools/import-content.php
 *
 * This script reads the YAML content files from the old static site
 * and creates WordPress posts with all meta fields populated.
 *
 * Prerequisites:
 *   - WordPress installed and configured
 *   - esp32engine theme active
 *   - Symfony YAML parser: composer require symfony/yaml (in theme dir)
 *     OR use the simple YAML parser included below.
 *   - Set YAML_SOURCE_DIR to the absolute path of your esp32-main/content/ directory.
 */

defined( 'ABSPATH' ) || define( 'ABSPATH', dirname( __DIR__, 4 ) . '/' );
defined( 'WPINC' )  || require ABSPATH . 'wp-load.php';

// ---- CONFIG ----
define( 'YAML_SOURCE_DIR', 'D:/xampp/htdocs/esp32engine/esp32-main/content/' );
define( 'DRY_RUN', false ); // set true to test without inserting

// ---- HELPERS ----
function esp32_import_log( string $msg ): void {
    echo date( '[H:i:s] ' ) . $msg . PHP_EOL;
}

/**
 * Minimal YAML parser sufficient for the project YAML files.
 * For complex YAML use symfony/yaml instead.
 */
function esp32_parse_yaml( string $file ): array {
    if ( ! file_exists( $file ) ) return [];
    // Try symfony/yaml if available
    $autoload = dirname( __DIR__ ) . '/vendor/autoload.php';
    if ( file_exists( $autoload ) ) {
        require_once $autoload;
        if ( class_exists( '\Symfony\Component\Yaml\Yaml' ) ) {
            return \Symfony\Component\Yaml\Yaml::parseFile( $file ) ?: [];
        }
    }
    // Fallback: use PHP yaml extension if available
    if ( function_exists( 'yaml_parse_file' ) ) {
        return yaml_parse_file( $file ) ?: [];
    }
    esp32_import_log( "WARNING: No YAML parser found. Install symfony/yaml or php-yaml extension." );
    return [];
}

// ---- CATEGORY IMPORT ----
function esp32_import_categories(): void {
    esp32_import_log( "Importing categories..." );
    $categories = [
        'agriculture'           => [ 'Agriculture',           'ESP32 Agriculture & Smart Irrigation projects' ],
        'ai-projects'           => [ 'AI Projects',           'ESP32 AI, TinyML and machine learning projects' ],
        'education'             => [ 'Education',             'ESP32 educational and learning projects' ],
        'energy-monitoring'     => [ 'Energy Monitoring',     'ESP32 energy monitoring and smart meter projects' ],
        'environmental'         => [ 'Environmental',         'ESP32 environmental monitoring projects' ],
        'esp32-cam'             => [ 'ESP32-CAM',             'ESP32 camera and computer vision projects' ],
        'healthcare'            => [ 'Healthcare',            'ESP32 health monitoring and medical projects' ],
        'home-automation'       => [ 'Home Automation',       'ESP32 smart home and automation projects' ],
        'industrial-automation' => [ 'Industrial Automation', 'ESP32 industrial monitoring and automation projects' ],
        'iot-projects'          => [ 'IoT Projects',          'ESP32 Internet of Things connectivity projects' ],
        'led-projects'          => [ 'LED Projects',          'ESP32 LED and lighting control projects' ],
        'robotics'              => [ 'Robotics',              'ESP32 robotics and motor control projects' ],
        'security-projects'     => [ 'Security Projects',     'ESP32 security, surveillance and alert projects' ],
        'sensor-projects'       => [ 'Sensor Projects',       'ESP32 sensor interfacing and data projects' ],
        'smart-city'            => [ 'Smart City',            'ESP32 smart city infrastructure projects' ],
    ];
    foreach ( $categories as $slug => [ $name, $desc ] ) {
        if ( DRY_RUN ) {
            esp32_import_log( "  [DRY] Would create category: {$name} ({$slug})" );
            continue;
        }
        $existing = get_term_by( 'slug', $slug, 'project_category' );
        if ( $existing ) {
            esp32_import_log( "  SKIP category (exists): {$name}" );
            continue;
        }
        $result = wp_insert_term( $name, 'project_category', [ 'slug' => $slug, 'description' => $desc ] );
        if ( is_wp_error( $result ) ) {
            esp32_import_log( "  ERROR creating category {$name}: " . $result->get_error_message() );
        } else {
            esp32_import_log( "  OK category: {$name}" );
        }
    }
}

// ---- PROJECT IMPORT ----
function esp32_import_projects(): void {
    esp32_import_log( "Importing projects..." );
    $projects_dir = YAML_SOURCE_DIR . 'projects/';
    if ( ! is_dir( $projects_dir ) ) {
        esp32_import_log( "ERROR: projects dir not found: {$projects_dir}" );
        return;
    }
    $files = glob( $projects_dir . '*.yaml' );
    if ( ! $files ) {
        esp32_import_log( "No project YAML files found in {$projects_dir}" );
        return;
    }
    foreach ( $files as $file ) {
        $data = esp32_parse_yaml( $file );
        if ( ! $data ) {
            esp32_import_log( "  SKIP (empty/parse error): " . basename( $file ) );
            continue;
        }
        esp32_import_project( $data, basename( $file, '.yaml' ) );
    }
}

function esp32_import_project( array $data, string $slug ): void {
    $title = $data['title'] ?? $slug;
    esp32_import_log( "  Project: {$title}" );

    if ( DRY_RUN ) {
        esp32_import_log( "  [DRY] Would create project: {$title}" );
        return;
    }

    // Check for existing post
    $existing = get_posts( [ 'post_type' => 'esp32_project', 'name' => $slug, 'posts_per_page' => 1 ] );
    if ( $existing ) {
        esp32_import_log( "    SKIP (already imported): {$title}" );
        return;
    }

    // Build post content from description
    $content = $data['description'] ?? ( $data['intro'] ?? '' );

    $post_id = wp_insert_post( [
        'post_type'    => 'esp32_project',
        'post_title'   => $title,
        'post_name'    => $slug,
        'post_content' => $content,
        'post_excerpt' => $data['description'] ?? '',
        'post_status'  => 'publish',
        'post_date'    => $data['date_published'] ?? current_time( 'mysql' ),
    ] );

    if ( is_wp_error( $post_id ) ) {
        esp32_import_log( "    ERROR: " . $post_id->get_error_message() );
        return;
    }

    // Taxonomy: project_category
    $cat_slug = $data['category'] ?? '';
    if ( $cat_slug ) {
        $term = get_term_by( 'slug', $cat_slug, 'project_category' );
        if ( $term ) wp_set_post_terms( $post_id, [ $term->term_id ], 'project_category' );
    }

    // Meta: icon
    update_post_meta( $post_id, 'project_icon_class', esp32_category_to_thumb_class( $cat_slug ) );
    update_post_meta( $post_id, 'project_lead', $data['description'] ?? '' );
    update_post_meta( $post_id, 'project_dependencies', $data['components_summary'] ?? '' );

    // Meta: difficulty levels
    $levels = [ 'beginner', 'intermediate', 'advanced' ];
    foreach ( $levels as $level ) {
        $ld = $data[ $level ] ?? $data[ 'level_' . $level ] ?? [];
        if ( ! $ld ) continue;

        update_post_meta( $post_id, $level . '_overview',   $ld['overview']   ?? '' );
        update_post_meta( $post_id, $level . '_code',       $ld['code']       ?? '' );
        update_post_meta( $post_id, $level . '_code_filename', $ld['code_filename'] ?? ( $slug . '_' . $level . '.ino' ) );

        // Serialised arrays
        if ( ! empty( $ld['components'] ) )      update_post_meta( $post_id, $level . '_components',      $ld['components'] );
        if ( ! empty( $ld['wiring'] ) )           update_post_meta( $post_id, $level . '_wiring',          $ld['wiring'] );
        if ( ! empty( $ld['how_it_works'] ) )     update_post_meta( $post_id, $level . '_how_it_works',    $ld['how_it_works'] );
        if ( ! empty( $ld['applications'] ) )     update_post_meta( $post_id, $level . '_applications',    $ld['applications'] );
        if ( ! empty( $ld['troubleshooting'] ) )  update_post_meta( $post_id, $level . '_troubleshooting', $ld['troubleshooting'] );
        if ( ! empty( $ld['upgrades'] ) )         update_post_meta( $post_id, $level . '_upgrades',        $ld['upgrades'] );
        if ( ! empty( $ld['faq'] ) )              update_post_meta( $post_id, $level . '_faq',             $ld['faq'] );
    }

    // HowTo steps (from beginner level how_it_works)
    $how = $data['beginner']['how_it_works'] ?? [];
    if ( $how ) {
        update_post_meta( $post_id, 'howto_steps', array_map( fn($s) => is_array($s) ? ($s['text']??'') : $s, $how ) );
    }

    // FAQ items (from beginner faq)
    $faq = $data['beginner']['faq'] ?? [];
    if ( $faq ) {
        update_post_meta( $post_id, 'faq_items', $faq );
    }

    esp32_import_log( "    CREATED post_id={$post_id}" );
}

// ---- GUIDE IMPORT ----
function esp32_import_guides(): void {
    esp32_import_log( "Importing guides..." );
    $guides_dir = YAML_SOURCE_DIR . 'guides/';
    if ( ! is_dir( $guides_dir ) ) {
        esp32_import_log( "  WARNING: guides dir not found" );
        return;
    }
    $files = glob( $guides_dir . '*.yaml' );
    foreach ( $files as $file ) {
        $data = esp32_parse_yaml( $file );
        if ( ! $data ) continue;
        $slug  = basename( $file, '.yaml' );
        $title = $data['title'] ?? $slug;
        esp32_import_log( "  Guide: {$title}" );
        if ( DRY_RUN ) { esp32_import_log( "  [DRY] Would import guide" ); continue; }

        $existing = get_posts( [ 'post_type' => 'esp32_guide', 'name' => $slug, 'posts_per_page' => 1 ] );
        if ( $existing ) { esp32_import_log( "    SKIP (exists)" ); continue; }

        $post_id = wp_insert_post( [
            'post_type'    => 'esp32_guide',
            'post_title'   => $title,
            'post_name'    => $slug,
            'post_content' => $data['content'] ?? '',
            'post_excerpt' => $data['description'] ?? '',
            'post_status'  => 'publish',
        ] );
        if ( ! is_wp_error( $post_id ) ) {
            update_post_meta( $post_id, 'guide_phase', $data['phase'] ?? 'Guide' );
            update_post_meta( $post_id, 'guide_read_time', $data['read_time'] ?? '10 min' );
            esp32_import_log( "    CREATED post_id={$post_id}" );
        }
    }
}

function esp32_category_to_thumb_class( string $slug ): string {
    $map = [
        'iot-projects' => 't-iot', 'home-automation' => 't-home',
        'esp32-cam' => 't-cam', 'robotics' => 't-robot',
        'sensor-projects' => 't-sensor', 'ai-projects' => 't-ai',
        'security-projects' => 't-security', 'led-projects' => 't-led',
        'agriculture' => 't-agriculture', 'environmental' => 't-agriculture',
    ];
    return $map[$slug] ?? 't-default';
}

// ---- RUN ----
esp32_import_log( "=== ESP32 Engine Content Import ===" );
esp32_import_log( "DRY_RUN=" . ( DRY_RUN ? 'true' : 'false' ) );
esp32_import_categories();
esp32_import_projects();
esp32_import_guides();
esp32_import_log( "=== Done ===" );
