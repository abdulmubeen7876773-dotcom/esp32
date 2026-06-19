<?php
/**
 * ESP32 Engine — Phase 3 Guide Importer
 * Run via WP-CLI: php wp.phar eval-file tools/import-phase3-guides.php --path=D:\xampp\htdocs\esp32
 */

$guides = array_merge(
    require __DIR__ . '/phase3-data-1.php',
    require __DIR__ . '/phase3-data-2.php'
);

$imported = 0;
$updated  = 0;
$failed   = [];

foreach ( $guides as $g ) {
    $slug      = $g['slug'];
    $title     = $g['title'];
    $meta_desc = $g['meta_desc'] ?? '';
    $read_time = $g['read_time'] ?? '12 min';
    $phase     = $g['phase']     ?? 'Phase 3: GPIO & Hardware';
    $faqs      = $g['faqs']      ?? [];
    $related   = $g['related']   ?? [];
    $body_html = $g['body_html'] ?? '';

    /* ── Upsert ── */
    $existing = get_posts( [
        'name'           => $slug,
        'post_type'      => 'esp32_guide',
        'post_status'    => 'any',
        'posts_per_page' => 1,
    ] );

    $post_data = [
        'post_type'    => 'esp32_guide',
        'post_status'  => 'publish',
        'post_title'   => $title,
        'post_name'    => $slug,
        'post_content' => $body_html,
        'post_excerpt' => $meta_desc,
        'post_date'    => '2026-06-19 12:00:00',
        'post_date_gmt'=> '2026-06-19 12:00:00',
    ];

    if ( ! empty( $existing ) ) {
        $post_data['ID'] = $existing[0]->ID;
        $result = wp_update_post( $post_data, true );
        if ( is_wp_error( $result ) ) {
            $failed[] = "$slug: " . $result->get_error_message();
            continue;
        }
        $post_id = $result;
        $updated++;
    } else {
        $result = wp_insert_post( $post_data, true );
        if ( is_wp_error( $result ) ) {
            $failed[] = "$slug: " . $result->get_error_message();
            continue;
        }
        $post_id = $result;
        $imported++;
    }

    /* ── Meta ── */
    update_post_meta( $post_id, 'guide_phase',      $phase );
    update_post_meta( $post_id, 'guide_read_time',  $read_time );
    update_post_meta( $post_id, '_meta_description', $meta_desc );
    update_post_meta( $post_id, 'faq_items',        $faqs );
    update_post_meta( $post_id, '_related_guides',  $related );

    WP_CLI::log( "  ✓ $slug (ID $post_id)" );
}

WP_CLI::success( "Phase 3 import done. Imported: $imported  Updated: $updated  Failed: " . count( $failed ) );
if ( $failed ) {
    foreach ( $failed as $f ) WP_CLI::warning( "  ✗ $f" );
}
