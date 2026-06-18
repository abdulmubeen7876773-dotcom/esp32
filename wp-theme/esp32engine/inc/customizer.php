<?php
defined( 'ABSPATH' ) || exit;

add_action( 'customize_register', function ( WP_Customize_Manager $wp_customize ): void {

    /* --------------------------------------------------------
       Section: ESP32 Engine Settings
    -------------------------------------------------------- */
    $wp_customize->add_section( 'esp32_settings', [
        'title'    => 'ESP32 Engine Settings',
        'priority' => 30,
    ] );

    // GA4 Measurement ID
    $wp_customize->add_setting( 'esp32_ga4_id', [
        'default'           => 'G-WLHZKSEFP3',
        'sanitize_callback' => 'sanitize_text_field',
        'transport'         => 'refresh',
    ] );
    $wp_customize->add_control( 'esp32_ga4_id', [
        'label'       => 'Google Analytics 4 ID',
        'description' => 'e.g. G-XXXXXXXXXX',
        'section'     => 'esp32_settings',
        'type'        => 'text',
    ] );

    // GitHub URL
    $wp_customize->add_setting( 'esp32_github_url', [
        'default'           => 'https://github.com/abdulmubeen7876773-dotcom/esp32',
        'sanitize_callback' => 'esc_url_raw',
    ] );
    $wp_customize->add_control( 'esp32_github_url', [
        'label'   => 'GitHub Repository URL',
        'section' => 'esp32_settings',
        'type'    => 'url',
    ] );

    // YouTube URL
    $wp_customize->add_setting( 'esp32_youtube_url', [
        'default'           => 'https://www.youtube.com/@ESP32Engine',
        'sanitize_callback' => 'esc_url_raw',
    ] );
    $wp_customize->add_control( 'esp32_youtube_url', [
        'label'   => 'YouTube Channel URL',
        'section' => 'esp32_settings',
        'type'    => 'url',
    ] );

    // Footer copyright name
    $wp_customize->add_setting( 'esp32_footer_name', [
        'default'           => 'ESP32 Engine',
        'sanitize_callback' => 'sanitize_text_field',
    ] );
    $wp_customize->add_control( 'esp32_footer_name', [
        'label'   => 'Footer Copyright Name',
        'section' => 'esp32_settings',
        'type'    => 'text',
    ] );

    /* --------------------------------------------------------
       Section: Accent Colors
    -------------------------------------------------------- */
    $wp_customize->add_section( 'esp32_colors', [
        'title'    => 'Theme Accent Colors',
        'priority' => 35,
    ] );

    $color_settings = [
        'esp32_color_primary'    => [ 'Primary Color',   '#6D28D9' ],
        'esp32_color_secondary'  => [ 'Secondary Color', '#7C3AED' ],
        'esp32_color_accent'     => [ 'Accent Color',    '#A855F7' ],
    ];
    foreach ( $color_settings as $setting_id => [ $label, $default ] ) {
        $wp_customize->add_setting( $setting_id, [
            'default'           => $default,
            'sanitize_callback' => 'sanitize_hex_color',
            'transport'         => 'postMessage',
        ] );
        $wp_customize->add_control(
            new WP_Customize_Color_Control( $wp_customize, $setting_id, [
                'label'   => $label,
                'section' => 'esp32_colors',
            ] )
        );
    }
} );

/* ============================================================
   Output customizer CSS variables inline
   ============================================================ */
add_action( 'wp_head', function (): void {
    $primary   = get_theme_mod( 'esp32_color_primary',   '#6D28D9' );
    $secondary = get_theme_mod( 'esp32_color_secondary', '#7C3AED' );
    $accent    = get_theme_mod( 'esp32_color_accent',    '#A855F7' );

    if (
        $primary   === '#6D28D9' &&
        $secondary === '#7C3AED' &&
        $accent    === '#A855F7'
    ) return; // defaults — no inline style needed, CSS file handles it

    echo '<style id="esp32-custom-colors">:root{'
        . '--primary:'   . sanitize_hex_color( $primary )   . ';'
        . '--secondary:' . sanitize_hex_color( $secondary ) . ';'
        . '--accent:'    . sanitize_hex_color( $accent )    . ';'
        . '}</style>' . "\n";
}, 20 );

/* ============================================================
   Helper: get customizer values for use in templates
   ============================================================ */
function esp32_get( string $key, string $default = '' ): string {
    return (string) get_theme_mod( 'esp32_' . $key, $default );
}
