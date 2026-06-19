<?php
global $wpdb;
$ids = $wpdb->get_col(
    "SELECT ID FROM {$wpdb->posts} WHERE post_type='esp32_guide' AND post_status='future'"
);
foreach ( $ids as $id ) {
    $wpdb->update(
        $wpdb->posts,
        [
            'post_status'   => 'publish',
            'post_date'     => '2026-06-18 12:00:00',
            'post_date_gmt' => '2026-06-18 12:00:00',
        ],
        [ 'ID' => $id ],
        [ '%s', '%s', '%s' ],
        [ '%d' ]
    );
    clean_post_cache( $id );
    WP_CLI::log( "Published post ID $id" );
}
WP_CLI::success( 'Done. Fixed ' . count( $ids ) . ' posts.' );
