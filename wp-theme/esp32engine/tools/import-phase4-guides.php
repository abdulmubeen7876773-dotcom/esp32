<?php
/**
 * WP-CLI script — import Phase 4 connectivity guides
 * Run: D:\xampp\php\php.exe D:\xampp\htdocs\wp.phar eval-file import-phase4-guides.php --path=D:\xampp\htdocs\esp32
 */
if ( ! defined( 'ABSPATH' ) ) {
    die( 'Must be run via WP-CLI' );
}

$guides = array_merge(
    require __DIR__ . '/phase4-data-1.php',
    require __DIR__ . '/phase4-data-2.php'
);

$imported = 0;
$updated  = 0;

foreach ( $guides as $guide ) {
    $slug  = sanitize_title( $guide['slug'] );
    $title = wp_slash( $guide['title'] );

    /* Upsert */
    $existing = get_posts( [
        'post_type'   => 'esp32_guide',
        'post_status' => 'any',
        'name'        => $slug,
        'numberposts' => 1,
    ] );

    $post_data = [
        'post_type'    => 'esp32_guide',
        'post_status'  => 'publish',
        'post_title'   => $title,
        'post_name'    => $slug,
        'post_content' => wp_slash( $guide['body_html'] ),
        'post_excerpt' => wp_slash( $guide['meta_desc'] ),
        'post_date'    => '2026-06-18 12:00:00',
        'post_date_gmt'=> '2026-06-18 12:00:00',
    ];

    if ( $existing ) {
        $post_data['ID'] = $existing[0]->ID;
        $post_id = wp_update_post( $post_data, true );
        $updated++;
    } else {
        $post_id = wp_insert_post( $post_data, true );
        $imported++;
    }

    if ( is_wp_error( $post_id ) ) {
        WP_CLI::warning( "Error on {$slug}: " . $post_id->get_error_message() );
        continue;
    }

    update_post_meta( $post_id, 'guide_phase',       $guide['phase'] );
    update_post_meta( $post_id, 'guide_read_time',   $guide['read_time'] );
    update_post_meta( $post_id, '_meta_description', $guide['meta_desc'] );
    update_post_meta( $post_id, 'faq_items',         $guide['faqs'] );
    update_post_meta( $post_id, '_related_guides',   $guide['related'] );

    WP_CLI::log( "  [{$post_id}] {$slug}" );
}

WP_CLI::success( "Phase 4 done — {$imported} imported, {$updated} updated." );
