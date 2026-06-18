<?php
/**
 * ESP32 Engine — Phase 1 Guide Importer
 * Usage: php import-phase1-guides.php [--dry-run] [--verbose]
 */
define( 'ABSPATH', 'D:/xampp/htdocs/esp32/' );
require_once 'D:/xampp/htdocs/esp32/wp-load.php';

$dry_run = in_array( '--dry-run', $argv, true );
$verbose = in_array( '--verbose', $argv, true );

$guides = array_merge(
    require __DIR__ . '/guides-data-1.php',
    require __DIR__ . '/guides-data-2.php'
);

$stats = [ 'imported' => 0, 'updated' => 0, 'failed' => 0 ];

foreach ( $guides as $g ) {
    $slug      = $g['slug'];
    $title     = $g['title'];
    $meta_desc = $g['meta_desc'];
    $read_time = $g['read_time'];
    $phase     = $g['phase'];
    $faqs      = $g['faqs'];
    $related   = $g['related'];
    $body_html = $g['body_html'];

    // Build post content — body only (no lead prefix)
    $content = $body_html;

    // Check existing
    $existing = get_posts([
        'name'           => $slug,
        'post_type'      => 'esp32_guide',
        'post_status'    => 'any',
        'posts_per_page' => 1,
        'fields'         => 'ids',
    ]);
    $is_update = ! empty( $existing );

    $post_args = [
        'post_type'    => 'esp32_guide',
        'post_status'  => 'publish',
        'post_title'   => $title,
        'post_name'    => $slug,
        'post_excerpt' => $meta_desc,
        'post_content' => $content,
        'post_date'     => '2026-06-18 12:00:00',
        'post_date_gmt' => '2026-06-18 12:00:00',
    ];
    if ( $is_update ) $post_args['ID'] = $existing[0];

    if ( $dry_run ) {
        echo ( $is_update ? '  – SKIP(exists)' : '  + CREATE' ) . " $slug\n";
        if ( $is_update ) $stats['updated']++; else $stats['imported']++;
        continue;
    }

    $id = $is_update ? wp_update_post( $post_args, true ) : wp_insert_post( $post_args, true );

    if ( is_wp_error( $id ) ) {
        echo "  ✗ FAILED $slug: " . $id->get_error_message() . "\n";
        $stats['failed']++;
        continue;
    }

    // Meta
    update_post_meta( $id, 'guide_read_time',   $read_time );
    update_post_meta( $id, 'guide_phase',        $phase );
    update_post_meta( $id, '_meta_description',  $meta_desc );
    update_post_meta( $id, 'faq_items',          $faqs );
    update_post_meta( $id, '_related_guides',    $related );

    $action = $is_update ? 'Updated' : 'Imported';
    $stats[ $is_update ? 'updated' : 'imported' ]++;
    echo "  ✓ $action [$id] $slug (" . count($faqs) . " FAQs, " . str_word_count(strip_tags($body_html)) . " words)\n";
}

// URL tests
echo "\n=== URL Tests ===\n";
$test_slugs = array_column( $guides, 'slug' );
$pass = 0; $fail = 0;
foreach ( $test_slugs as $slug ) {
    $url  = "http://localhost/esp32/guides/$slug/";
    $ctx  = stream_context_create(['http' => ['timeout' => 6, 'ignore_errors' => true]]);
    @file_get_contents($url, false, $ctx);
    preg_match('/HTTP\/\d\.\d (\d{3})/', $http_response_header[0] ?? '', $m);
    $code = (int)($m[1] ?? 0);
    if ($code === 200) { $pass++; echo "  [200] ✓ $url\n"; }
    else               { $fail++; echo "  [$code] ✗ $url\n"; }
}

// Guides archive
$arch = "http://localhost/esp32/guides/";
$ctx  = stream_context_create(['http' => ['timeout' => 6, 'ignore_errors' => true]]);
@file_get_contents($arch, false, $ctx);
preg_match('/HTTP\/\d\.\d (\d{3})/', $http_response_header[0] ?? '', $m);
$acode = (int)($m[1] ?? 0);
echo "  [$acode] " . ($acode===200?'✓':'✗') . " $arch\n";

echo "\n=== Import Report ===\n";
echo "  Imported: {$stats['imported']}\n";
echo "  Updated:  {$stats['updated']}\n";
echo "  Failed:   {$stats['failed']}\n";
echo "  URL PASS: $pass / " . count($test_slugs) . "\n";
echo "\nDone.\n";
