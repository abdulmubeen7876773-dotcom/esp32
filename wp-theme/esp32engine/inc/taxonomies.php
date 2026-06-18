<?php
add_action( 'init', function () {

    register_taxonomy( 'project_category', 'esp32_project', [
        'labels' => [
            'name'              => 'Project Categories',
            'singular_name'     => 'Project Category',
            'add_new_item'      => 'Add New Category',
            'edit_item'         => 'Edit Category',
            'new_item'          => 'New Category',
            'view_item'         => 'View Category',
            'search_items'      => 'Search Categories',
            'not_found'         => 'No categories found',
            'all_items'         => 'All Categories',
            'menu_name'         => 'Categories',
        ],
        'public'            => true,
        'hierarchical'      => true,
        'show_ui'           => true,
        'show_in_rest'      => true,
        'show_admin_column' => true,
        'rewrite'           => [ 'slug' => 'category', 'with_front' => false ],
        'query_var'         => true,
    ] );

    register_taxonomy( 'difficulty_level', 'esp32_project', [
        'labels' => [
            'name'          => 'Difficulty Levels',
            'singular_name' => 'Difficulty Level',
            'all_items'     => 'All Levels',
            'edit_item'     => 'Edit Level',
            'add_new_item'  => 'Add New Level',
        ],
        'public'            => false,
        'hierarchical'      => false,
        'show_ui'           => true,
        'show_in_rest'      => true,
        'show_admin_column' => true,
        'rewrite'           => false,
        'query_var'         => true,
    ] );
} );

/**
 * Map category slug to CSS thumb class (mirrors the static site's t-* classes).
 */
function esp32_category_thumb_class( string $slug ): string {
    $map = [
        'iot-projects'          => 't-iot',
        'home-automation'       => 't-home',
        'esp32-cam'             => 't-cam',
        'robotics'              => 't-robot',
        'sensor-projects'       => 't-sensor',
        'ai-projects'           => 't-ai',
        'security-projects'     => 't-security',
        'led-projects'          => 't-led',
        'agriculture'           => 't-agriculture',
        'environmental'         => 't-agriculture',
        'healthcare'            => 't-sensor',
        'energy-monitoring'     => 't-default',
        'smart-city'            => 't-iot',
        'industrial-automation' => 't-default',
        'education'             => 't-default',
    ];
    return $map[ $slug ] ?? 't-default';
}
