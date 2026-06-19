<?php
global $wpdb;
$rows = $wpdb->get_results(
    "SELECT ID, post_name, post_status FROM {$wpdb->posts} WHERE post_type='esp32_guide' ORDER BY ID DESC LIMIT 15"
);
foreach ( $rows as $r ) {
    WP_CLI::log( $r->ID . ' | ' . $r->post_name . ' | ' . $r->post_status );
}
WP_CLI::log( 'Total esp32_guide rows: ' . $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='esp32_guide'") );
