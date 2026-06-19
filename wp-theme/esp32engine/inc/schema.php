<?php
/* ── Production URL helper ───────────────────────────────────────────────
   Replaces the local home_url() base with the ESP32_PROD_URL constant when
   defined, so canonical tags and schema @id values always use the live
   domain even during local development. Once deployed and siteurl/home are
   updated in the DB, home_url() will naturally return the production URL
   and this helper becomes a transparent pass-through.
────────────────────────────────────────────────────────────────────────── */
function esp32_prod_url( string $path = '/' ): string {
    $base = defined( 'ESP32_PROD_URL' ) ? rtrim( ESP32_PROD_URL, '/' ) : rtrim( home_url(), '/' );
    return $base . '/' . ltrim( $path, '/' );
}

function esp32_prod_permalink( int $post_id = 0 ): string {
    $permalink = $post_id ? get_permalink( $post_id ) : get_permalink();
    if ( ! defined( 'ESP32_PROD_URL' ) ) return $permalink;
    return str_replace( rtrim( home_url(), '/' ), rtrim( ESP32_PROD_URL, '/' ), $permalink );
}

function esp32_prod_term_link( $term ): string {
    $link = get_term_link( $term );
    if ( is_wp_error( $link ) || ! defined( 'ESP32_PROD_URL' ) ) return is_wp_error( $link ) ? '' : $link;
    return str_replace( rtrim( home_url(), '/' ), rtrim( ESP32_PROD_URL, '/' ), $link );
}

/* ── Canonical + Meta Description ── */
add_action( 'wp_head', 'esp32_output_seo_meta', 4 );

function esp32_output_seo_meta(): void {
    /* Canonical — always uses production domain */
    if ( is_singular() ) {
        $canonical = esp32_prod_permalink();
    } elseif ( is_post_type_archive( 'esp32_guide' ) ) {
        $canonical = esp32_prod_url( '/guides/' );
    } elseif ( is_post_type_archive( 'esp32_project' ) ) {
        $canonical = esp32_prod_url( '/projects/' );
    } elseif ( is_tax( 'project_category' ) ) {
        $canonical = esp32_prod_term_link( get_queried_object() );
    } elseif ( is_front_page() ) {
        $canonical = esp32_prod_url( '/' );
    } else {
        $canonical = '';
    }
    if ( $canonical && ! is_wp_error( $canonical ) ) {
        echo '<link rel="canonical" href="' . esc_url( $canonical ) . '">' . "\n";
    }

    /* Meta description */
    $desc = '';
    if ( is_singular( 'esp32_guide' ) ) {
        $desc = get_post_meta( get_the_ID(), '_meta_description', true );
        if ( ! $desc ) $desc = wp_trim_words( get_the_excerpt() ?: wp_strip_all_tags( get_the_content() ), 25 );
    } elseif ( is_singular( 'esp32_project' ) ) {
        $desc = get_post_meta( get_the_ID(), 'project_lead', true );
        if ( ! $desc ) $desc = wp_trim_words( get_the_excerpt() ?: '', 25 );
    } elseif ( is_tax( 'project_category' ) ) {
        $term = get_queried_object();
        $desc = $term->description ?: ( $term->name . ' projects for ESP32 — wiring, code, and step-by-step tutorials.' );
    } elseif ( is_post_type_archive( 'esp32_project' ) ) {
        $desc = 'ESP32 projects with full Arduino code, wiring diagrams, and Beginner / Intermediate / Advanced guides.';
    } elseif ( is_post_type_archive( 'esp32_guide' ) ) {
        $desc = 'ESP32 guides and tutorials — from chip fundamentals to GPIO control, ADC, Wi-Fi, and beyond.';
    } elseif ( is_front_page() ) {
        $desc = 'ESP32Engine — the premium ESP32 learning platform. Step-by-step guides, wiring diagrams, Arduino code, and real-hardware projects.';
    }
    if ( $desc ) {
        echo '<meta name="description" content="' . esc_attr( wp_strip_all_tags( $desc ) ) . '">' . "\n";
        echo '<meta property="og:description" content="' . esc_attr( wp_strip_all_tags( $desc ) ) . '">' . "\n";
    }

    /* OG title + url */
    if ( is_singular() ) {
        echo '<meta property="og:title" content="' . esc_attr( get_the_title() . ' — ESP32Engine' ) . '">' . "\n";
        echo '<meta property="og:url" content="' . esc_url( esp32_prod_permalink() ) . '">' . "\n";
        echo '<meta property="og:type" content="article">' . "\n";
    } else {
        echo '<meta property="og:url" content="' . esc_url( $canonical ?: esp32_prod_url( '/' ) ) . '">' . "\n";
        echo '<meta property="og:type" content="website">' . "\n";
    }
    echo '<meta property="og:image" content="' . esc_url( esp32_prod_url( '/og-image.jpg' ) ) . '">' . "\n";
    echo '<meta property="og:image:width" content="1200">' . "\n";
    echo '<meta property="og:image:height" content="630">' . "\n";
    echo '<meta property="og:site_name" content="ESP32Engine">' . "\n";
}

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
        esp32_schema( esp32_schema_guide_faq() );
        esp32_schema( esp32_schema_breadcrumb() );
    } elseif ( is_tax( 'project_category' ) ) {
        // CollectionPage + Breadcrumb emitted directly in taxonomy-project_category.php
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
        'url'      => esp32_prod_url( '/' ),
        'logo'     => esp32_prod_url( '/og-image.jpg' ),
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
        'url'             => esp32_prod_url( '/' ),
        'publisher'       => [ '@type' => 'Organization', 'name' => 'ESP32 Engine' ],
        'potentialAction' => [
            '@type'       => 'SearchAction',
            'target'      => esp32_prod_url( '/?s={search_term_string}' ),
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
        'image'             => esp32_prod_url( '/og-image.jpg' ),
        'author'            => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'url' => esp32_prod_url( '/' ) ],
        'publisher'         => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'logo' => [ '@type' => 'ImageObject', 'url' => esp32_prod_url( '/og-image.jpg' ) ] ],
        'mainEntityOfPage'  => [ '@type' => 'WebPage', '@id' => esp32_prod_permalink() ],
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
    /* Project FAQs — uses 'question'/'answer' keys */
    $faq_raw = get_post_meta( get_the_ID(), 'faq_items', true );
    if ( ! $faq_raw ) return [];
    $entities = [];
    foreach ( (array) $faq_raw as $item ) {
        if ( ! is_array( $item ) ) continue;
        /* Support both key formats: question/answer and q/a */
        $q = $item['question'] ?? ( $item['q'] ?? '' );
        $a = $item['answer']   ?? ( $item['a'] ?? '' );
        if ( ! $q || ! $a ) continue;
        $entities[] = [
            '@type'          => 'Question',
            'name'           => wp_strip_all_tags( $q ),
            'acceptedAnswer' => [ '@type' => 'Answer', 'text' => wp_strip_all_tags( $a ) ],
        ];
    }
    if ( ! $entities ) return [];
    return [
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        'mainEntity' => $entities,
    ];
}

function esp32_schema_guide_faq(): array {
    /* Guide FAQs — stored with 'q'/'a' keys via faq_items meta */
    $faq_raw = get_post_meta( get_the_ID(), 'faq_items', true );
    if ( ! $faq_raw ) return [];
    $entities = [];
    foreach ( (array) $faq_raw as $item ) {
        if ( ! is_array( $item ) ) continue;
        $q = $item['q'] ?? ( $item['question'] ?? '' );
        $a = $item['a'] ?? ( $item['answer']   ?? '' );
        if ( ! $q || ! $a ) continue;
        $entities[] = [
            '@type'          => 'Question',
            'name'           => wp_strip_all_tags( $q ),
            'acceptedAnswer' => [ '@type' => 'Answer', 'text' => wp_strip_all_tags( $a ) ],
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
    $meta_desc = get_post_meta( get_the_ID(), '_meta_description', true )
                 ?: get_the_excerpt()
                 ?: '';
    $phase     = get_post_meta( get_the_ID(), 'guide_phase', true ) ?: 'ESP32 Guide';
    return [
        '@context'         => 'https://schema.org',
        '@type'            => 'TechArticle',
        'headline'         => get_the_title(),
        'description'      => wp_strip_all_tags( $meta_desc ),
        'datePublished'    => get_the_date( 'c' ),
        'dateModified'     => get_the_modified_date( 'c' ),
        'image'            => esp32_prod_url( '/og-image.jpg' ),
        'author'           => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'url' => esp32_prod_url( '/' ) ],
        'publisher'        => [ '@type' => 'Organization', 'name' => 'ESP32 Engine', 'logo' => [ '@type' => 'ImageObject', 'url' => esp32_prod_url( '/og-image.jpg' ) ] ],
        'mainEntityOfPage' => [ '@type' => 'WebPage', '@id' => esp32_prod_permalink() ],
        'articleSection'   => $phase,
        'keywords'         => 'ESP32, ' . $phase . ', Arduino, microcontroller, GPIO',
    ];
}

function esp32_schema_breadcrumb(): array {
    $items   = [];
    $items[] = [ '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => esp32_prod_url( '/' ) ];
    $pos     = 2;

    if ( is_singular( 'esp32_project' ) ) {
        $cats = get_the_terms( get_the_ID(), 'project_category' );
        if ( $cats && ! is_wp_error( $cats ) ) {
            $items[] = [
                '@type'    => 'ListItem',
                'position' => $pos++,
                'name'     => $cats[0]->name,
                'item'     => esp32_prod_term_link( $cats[0] ),
            ];
        }
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => get_the_title(), 'item' => esp32_prod_permalink() ];
    } elseif ( is_singular( 'esp32_guide' ) ) {
        $items[] = [ '@type' => 'ListItem', 'position' => $pos++, 'name' => 'Guides', 'item' => esp32_prod_url( '/guides/' ) ];
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => get_the_title(), 'item' => esp32_prod_permalink() ];
    } elseif ( is_tax( 'project_category' ) ) {
        $term    = get_queried_object();
        $items[] = [ '@type' => 'ListItem', 'position' => $pos, 'name' => $term->name, 'item' => esp32_prod_term_link( $term ) ];
    }

    return [
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $items,
    ];
}
