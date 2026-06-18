<?php
add_action( 'wp_head', 'esp32_output_schema', 5 );

function esp32_output_schema(): void {
    if ( is_front_page() ) {
        esp32_schema( esp32_schema_organization() );
        esp32_schema( esp32_schema_website() );
    } elseif ( is_singular( 'esp32_project' ) ) {
        esp32_schema( esp32_schema_tech_article() );
        esp32_schema( esp32_schema_howto() );
        esp32_schema( esp32_schema_faq() );
        esp32_schema( esp32_schema_breadcrumb() );
    } elseif ( is_singular( 'esp32_guide' ) ) {
        esp32_schema( esp32_schema_article() );
        esp32_schema( esp32_schema_breadcrumb() );
    } elseif ( is_tax( 'project_category' ) ) {
        esp32_schema( esp32_schema_breadcrumb() );
    }
}

function esp32_schema( array $data ): void {
    if ( empty( $data ) ) return;
    echo '<script type="application/ld+json">'
        . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
        . '</script>' . "\n";
}

function esp32_schema_organization(): array {
    return [
        '@context' => 'https://schema.org',
        '@type'    => 'Organization',
        'name'     => 'ESP32 Engine',
        'url'      => home_url( '/' ),
        'logo'     => home_url( '/og-image.jpg' ),
        'sameAs'   => [
            'https://github.com/abdulmubeen7876773-dotcom/esp32',
            'https://www.youtube.com/@ESP32Engine',
        ],
        'contactPoint' => [
            '@type'       => 'ContactPoint',
            'contactType' => 'customer support',
            'url'         => 'https://github.com/abdulmubeen7876773-dotcom/esp32/issues',
        ],
    ];
}

function esp32_schema_website(): array {
    return [
        '@context'        => 'https://schema.org',
        '@type'           => 'WebSite',
        'name'            => 'ESP32 Engine',
        'url'             => home_url( '/' ),
        'publisher'       => [ '@type' => 'Organization', 'name' => 'ESP32 Engine' ],
        'potentialAction' => [
            '@type'       => 'SearchAction',
            'target'      => home_url( '/?s={search_term_string}' ),
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

function esp32_schema_tech_article(): array {
    $cats = get_the_terms( get_the_ID(), 'project_category' );
    $deps = get_post_meta( get_the_ID(), 'project_dependencies', true );
    return [
        '@context'          => 'https://schema.org',
        '@type'             => 'TechArticle',
        'headline'          => get_the_title(),
        'description'       => get_the_excerpt(),
        'datePublished'     => get_the_date( 'c' ),
        'dateModified'      => get_the_modified_date( 'c' ),
        'image'             => home_url( '/og-image.jpg' ),
        'author'            => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'url' => home_url( '/' ) ],
        'publisher'         => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'logo' => [ '@type' => 'ImageObject', 'url' => home_url( '/og-image.jpg' ) ] ],
        'mainEntityOfPage'  => [ '@type' => 'WebPage', '@id' => get_permalink() ],
        'proficiencyLevel'  => 'Beginner',
        'dependencies'      => $deps ?: '',
    ];
}

function esp32_schema_howto(): array {
    $steps_raw = get_post_meta( get_the_ID(), 'howto_steps', true );
    if ( ! $steps_raw ) return [];
    $steps = [];
    foreach ( (array) $steps_raw as $i => $step ) {
        $steps[] = [
            '@type'    => 'HowToStep',
            'position' => $i + 1,
            'name'     => wp_strip_all_tags( $step ),
            'text'     => wp_strip_all_tags( $step ),
        ];
    }
    return [
        '@context'    => 'https://schema.org',
        '@type'       => 'HowTo',
        'name'        => 'How to build ' . get_the_title() . ' (Beginner)',
        'description' => get_the_excerpt(),
        'step'        => $steps,
    ];
}

function esp32_schema_faq(): array {
    $faq_raw = get_post_meta( get_the_ID(), 'faq_items', true );
    if ( ! $faq_raw ) return [];
    $entities = [];
    foreach ( (array) $faq_raw as $item ) {
        if ( empty( $item['question'] ) ) continue;
        $entities[] = [
            '@type'          => 'Question',
            'name'           => $item['question'],
            'acceptedAnswer' => [ '@type' => 'Answer', 'text' => $item['answer'] ?? '' ],
        ];
    }
    if ( ! $entities ) return [];
    return [
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        'mainEntity' => $entities,
    ];
}

function esp32_schema_article(): array {
    return [
        '@context'         => 'https://schema.org',
        '@type'            => 'Article',
        'headline'         => get_the_title(),
        'description'      => get_the_excerpt(),
        'datePublished'    => get_the_date( 'c' ),
        'dateModified'     => get_the_modified_date( 'c' ),
        'image'            => home_url( '/og-image.jpg' ),
        'author'           => [ '@type' => 'Organization', 'name' => 'ESP32 Engine' ],
        'publisher'        => [ '@type' => 'Organization', 'name' => 'ESP32 Engine' ],
        'mainEntityOfPage' => [ '@type' => 'WebPage', '@id' => get_permalink() ],
    ];
}

function esp32_schema_breadcrumb(): array {
    $items   = [];
    $items[] = [ '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url( '/' ) ];
    $pos     = 2;

    if ( is_singular( 'esp32_project' ) ) {
        $cats = get_the_terms( get_the_ID(), 'project_category' );
        if ( $cats && ! is_wp_error( $cats ) ) {
            $items[] = [
                '@type'    => 'ListItem',
                'position' => $pos++,
                'name'     => $cats[0]->name,
                'item'     => get_term_link( $cats[0] ),
            ];
        }
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => get_the_title(), 'item' => get_permalink() ];
    } elseif ( is_singular( 'esp32_guide' ) ) {
        $items[] = [ '@type' => 'ListItem', 'position' => $pos++, 'name' => 'Guides', 'item' => home_url( '/guides/' ) ];
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => get_the_title(), 'item' => get_permalink() ];
    } elseif ( is_tax( 'project_category' ) ) {
        $term    = get_queried_object();
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => $term->name, 'item' => get_term_link( $term ) ];
    }

    return [
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $items,
    ];
}
