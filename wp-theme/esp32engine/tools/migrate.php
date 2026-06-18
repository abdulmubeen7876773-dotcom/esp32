<?php
/**
 * ESP32 Engine — Static Site → WordPress Content Migrator
 *
 * Usage:
 *   php migrate.php              # full import
 *   php migrate.php --dry-run    # preview without writing
 *   php migrate.php --verbose    # extra detail
 *   php migrate.php --only=projects|guides|pages
 */
define( 'ABSPATH', 'D:/xampp/htdocs/esp32/' );
require_once 'D:/xampp/htdocs/esp32/wp-load.php';

/* ============================================================
   CLI args
   ============================================================ */
$dry_run = in_array( '--dry-run', $argv, true );
$verbose = in_array( '--verbose', $argv, true );
$only    = '';
foreach ( $argv as $a ) {
    if ( str_starts_with( $a, '--only=' ) ) $only = substr( $a, 7 );
}

$SRC = 'D:/xampp/htdocs/esp32engine/esp32-main';

/* ============================================================
   Report counters
   ============================================================ */
$report = [
    'projects'  => [ 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'failed' => 0 ],
    'guides'    => [ 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'failed' => 0 ],
    'pages'     => [ 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'failed' => 0 ],
    'errors'    => [],
    'missing'   => [],
    'urls'      => [],
];

/* ============================================================
   Category name → taxonomy slug mapping
   ============================================================ */
$cat_map = [
    'iot'                    => 'iot-projects',
    'iot projects'           => 'iot-projects',
    'home automation'        => 'home-automation',
    'smart home'             => 'home-automation',
    'esp32-cam'              => 'esp32-cam',
    'esp32-cam projects'     => 'esp32-cam',
    'robotics'               => 'robotics',
    'sensor'                 => 'sensor-projects',
    'sensor projects'        => 'sensor-projects',
    'ai'                     => 'ai-projects',
    'ai projects'            => 'ai-projects',
    'security'               => 'security-projects',
    'security projects'      => 'security-projects',
    'led'                    => 'led-projects',
    'led projects'           => 'led-projects',
    'agriculture'            => 'agriculture',
    'agriculture & environment' => 'agriculture',
    'environmental'          => 'environmental',
    'environmental monitoring' => 'environmental',
    'healthcare'             => 'healthcare',
    'energy'                 => 'energy-monitoring',
    'energy monitoring'      => 'energy-monitoring',
    'smart city'             => 'smart-city',
    'industrial'             => 'industrial-automation',
    'industrial automation'  => 'industrial-automation',
    'education'              => 'education',
];

/* ============================================================
   Helpers
   ============================================================ */
function log_msg( string $msg, string $level = 'info' ): void {
    global $verbose;
    $prefix = match( $level ) {
        'ok'    => '  ✓',
        'warn'  => '  ⚠',
        'error' => '  ✗',
        'skip'  => '  –',
        default => '   ',
    };
    if ( $level !== 'info' || $verbose ) {
        echo $prefix . ' ' . $msg . "\n";
    }
}

/** Load HTML file into DOMXPath, UTF-8 safe */
function html_xpath( string $file ): ?DOMXPath {
    if ( ! file_exists( $file ) ) return null;
    $html = file_get_contents( $file );
    $html = mb_convert_encoding( $html, 'HTML-ENTITIES', 'UTF-8' );
    libxml_use_internal_errors( true );
    $dom = new DOMDocument( '1.0', 'UTF-8' );
    $dom->loadHTML( $html, LIBXML_NOWARNING | LIBXML_NOERROR );
    libxml_clear_errors();
    return new DOMXPath( $dom );
}

/** Get trimmed text of first matching node */
function xq_text( DOMXPath $xp, string $query, ?DOMNode $ctx = null ): string {
    $nodes = $ctx ? $xp->query( $query, $ctx ) : $xp->query( $query );
    return $nodes->length ? trim( $nodes->item(0)->textContent ) : '';
}

/** Get innerHTML of first matching node */
function xq_html( DOMXPath $xp, string $query, ?DOMNode $ctx = null ): string {
    $nodes = $ctx ? $xp->query( $query, $ctx ) : $xp->query( $query );
    if ( ! $nodes->length ) return '';
    $node = $nodes->item(0);
    $out  = '';
    foreach ( $node->childNodes as $child ) {
        $out .= $node->ownerDocument->saveHTML( $child );
    }
    return trim( $out );
}

/** Get all text items from a list query */
function xq_list( DOMXPath $xp, string $query, ?DOMNode $ctx = null ): array {
    $nodes  = $ctx ? $xp->query( $query, $ctx ) : $xp->query( $query );
    $result = [];
    foreach ( $nodes as $n ) {
        $t = trim( $n->textContent );
        if ( $t ) $result[] = $t;
    }
    return $result;
}

/** Simple single-document YAML parser (handles our specific file format) */
function parse_simple_yaml( string $file ): array {
    if ( ! file_exists( $file ) ) return [];
    $lines  = file( $file, FILE_IGNORE_NEW_LINES );
    $result = [];
    $i      = 0;
    $total  = count( $lines );

    while ( $i < $total ) {
        $line = $lines[ $i ];
        // Skip blank and comment lines
        if ( trim( $line ) === '' || str_starts_with( trim( $line ), '#' ) ) { $i++; continue; }

        // Top-level key: value
        if ( preg_match( '/^(\w[\w_-]*):\s*(.*)$/', $line, $m ) ) {
            $key = $m[1];
            $val = $m[2];

            // Block scalar: |
            if ( trim( $val ) === '|' ) {
                $block = [];
                $i++;
                while ( $i < $total ) {
                    $bl = $lines[ $i ];
                    if ( $bl !== '' && ! str_starts_with( $bl, ' ' ) && ! str_starts_with( $bl, "\t" ) ) break;
                    $block[] = preg_replace( '/^  /', '', $bl );
                    $i++;
                }
                $result[ $key ] = implode( "\n", $block );
                continue;
            }

            // Inline quoted string
            if ( preg_match( "/^'(.*)'$/s", $val, $qm ) ) {
                $result[ $key ] = str_replace( "''", "'", $qm[1] );
                // Multi-line in single quotes: advance until unindented closing is found
                // handled by the regex consuming to end of line only; check for overflow
                $i++;
                continue;
            }

            // Sequence / array — val is empty, next lines start with '  - '
            if ( $val === '' ) {
                $seq = [];
                $i++;
                while ( $i < $total ) {
                    $sl = $lines[ $i ];
                    if ( ! preg_match( '/^  - (.*)/', $sl, $sm ) ) break;
                    $entry_val = trim( $sm[1] );
                    // Check if it's a mapping (next indented lines)
                    $entry = [];
                    if ( $entry_val !== '' ) {
                        // may be key: value on same line
                        if ( preg_match( '/^(\w[\w_-]*):\s*(.*)$/', $entry_val, $em ) ) {
                            $entry[ $em[1] ] = trim( $em[2], "'\"" );
                        }
                        $i++;
                        while ( $i < $total && preg_match( '/^    (\w[\w_-]*):\s*(.*)$/', $lines[$i], $em2 ) ) {
                            $entry[ $em2[1] ] = trim( $em2[2], "'\"" );
                            $i++;
                        }
                        $seq[] = count( $entry ) === 1 ? reset( $entry ) : $entry;
                    } else {
                        $i++;
                    }
                }
                $result[ $key ] = $seq;
                continue;
            }

            // Plain scalar (possibly multi-line folded)
            $scalar = trim( $val, "'" );
            $i++;
            while ( $i < $total && preg_match( '/^  (.*)/', $lines[$i], $cm ) ) {
                $scalar .= ' ' . trim( $cm[1] );
                $i++;
            }
            $result[ $key ] = $scalar;
            continue;
        }
        $i++;
    }

    // Handle body_html that starts with '  ...' continuation (already consumed by scalar handler)
    // But body_html may be a multi-line single-quoted block — re-read it properly
    return $result;
}

/** Better body_html extractor for pages (handles multi-line single-quoted YAML) */
function parse_yaml_body( string $file ): string {
    if ( ! file_exists( $file ) ) return '';
    $content = file_get_contents( $file );
    // Match body_html: 'all content until closing unescaped quote at line start or end'
    if ( preg_match( "/^body_html:\s*'(.*?)(?<!\\\\)'\\s*$/ms", $content, $m ) ) {
        return str_replace( "''", "'", $m[1] );
    }
    if ( preg_match( '/^body_html:\s*\|(.*)$/ms', $content, $m ) ) {
        return trim( $m[1] );
    }
    return '';
}

/** Map category name to taxonomy slug */
function resolve_cat_slug( string $name ): string {
    global $cat_map;
    $key = strtolower( trim( $name ) );
    return $cat_map[ $key ] ?? sanitize_title( $name );
}

/** Upsert a WordPress post — create or update if slug exists */
function upsert_post( array $args, string $post_type ): int|false {
    global $dry_run;

    // Check existing post by slug
    $existing = get_posts( [
        'name'           => $args['post_name'],
        'post_type'      => $post_type,
        'post_status'    => 'any',
        'posts_per_page' => 1,
        'fields'         => 'ids',
    ] );

    if ( $existing ) {
        $args['ID'] = $existing[0];
        if ( $dry_run ) {
            log_msg( "DRY-RUN: Would UPDATE [{$post_type}] {$args['post_name']}", 'skip' );
            return $existing[0];
        }
        $id = wp_update_post( $args, true );
        if ( is_wp_error( $id ) ) { log_msg( $id->get_error_message(), 'error' ); return false; }
        return (int) $id;
    }

    if ( $dry_run ) {
        log_msg( "DRY-RUN: Would CREATE [{$post_type}] {$args['post_name']}", 'skip' );
        return -1;
    }
    $id = wp_insert_post( $args, true );
    if ( is_wp_error( $id ) ) { log_msg( $id->get_error_message(), 'error' ); return false; }
    return (int) $id;
}

/* ============================================================
   Extract one difficulty level from a project XPath
   ============================================================ */
function extract_level( DOMXPath $xp, string $level ): array {
    $panel = $xp->query( "//*[@id='level-{$level}']" );
    if ( ! $panel->length ) return [];
    $ctx = $panel->item(0);

    /* Overview */
    $overview_node = $xp->query( ".//*[@id='sec-{$level}-overview']//div[contains(@class,'accordion-content')]", $ctx );
    $overview = $overview_node->length ? xq_html( $xp, ".//*[@id='sec-{$level}-overview']//div[contains(@class,'accordion-content')]", $ctx ) : '';

    /* Components */
    $comp_nodes = $xp->query( ".//*[@id='sec-{$level}-components']//li/span|.//*[@id='sec-{$level}-components']//li", $ctx );
    $components = [];
    foreach ( $comp_nodes as $n ) {
        $t = trim( $n->textContent );
        if ( $t ) $components[] = $t;
    }

    /* Wiring */
    $wiring = [];
    $rows = $xp->query( ".//*[@id='sec-{$level}-wiring']//tbody/tr", $ctx );
    foreach ( $rows as $row ) {
        $cells = $xp->query( './td', $row );
        if ( $cells->length >= 2 ) {
            $wiring[] = [
                'component_pin' => trim( $cells->item(0)->textContent ),
                'esp32_pin'     => trim( $cells->item(1)->textContent ),
                'notes'         => $cells->length >= 3 ? trim( $cells->item(2)->textContent ) : '',
            ];
        }
    }

    /* Code */
    $code_filename_node = $xp->query( ".//*[@id='sec-{$level}-code']//*[contains(@class,'code-bar')]/span", $ctx );
    $code_filename = $code_filename_node->length ? trim( $code_filename_node->item(0)->textContent ) : '';

    $code_node = $xp->query( ".//*[@id='sec-{$level}-code']//pre[contains(@class,'level-code')]", $ctx );
    $code = $code_node->length ? trim( $code_node->item(0)->textContent ) : '';
    // Decode common HTML entities left in code
    $code = html_entity_decode( $code, ENT_QUOTES | ENT_HTML5, 'UTF-8' );

    /* How it works */
    $how_nodes = $xp->query( ".//*[@id='sec-{$level}-how']//*[contains(@class,'step')]//p", $ctx );
    $how_steps = [];
    foreach ( $how_nodes as $n ) {
        $t = trim( $n->textContent );
        if ( $t ) $how_steps[] = $t;
    }

    /* Applications */
    $apps_nodes = $xp->query( ".//*[@id='sec-{$level}-apps']//*[contains(@class,'detail-list')]/li", $ctx );
    $applications = [];
    foreach ( $apps_nodes as $n ) {
        $t = trim( $n->textContent );
        if ( $t ) $applications[] = $t;
    }

    /* Troubleshooting */
    $trouble = [];
    $trouble_items = $xp->query( ".//*[@id='sec-{$level}-troubleshooting']//*[contains(@class,'trouble-item')]", $ctx );
    foreach ( $trouble_items as $item ) {
        $h = $xp->query( './/h4', $item );
        $p = $xp->query( './/p', $item );
        if ( $h->length && $p->length ) {
            $trouble[] = [
                'problem'  => trim( $h->item(0)->textContent ),
                'solution' => trim( $p->item(0)->textContent ),
            ];
        }
    }

    /* Upgrades */
    $upgrade_nodes = $xp->query( ".//*[@id='sec-{$level}-upgrades']//*[contains(@class,'detail-list')]/li", $ctx );
    $upgrades = [];
    foreach ( $upgrade_nodes as $n ) {
        $t = trim( $n->textContent );
        if ( $t ) $upgrades[] = $t;
    }

    /* FAQ */
    $faq = [];
    $faq_items = $xp->query( ".//*[@id='sec-{$level}-faq']//*[contains(@class,'faq-item')]", $ctx );
    foreach ( $faq_items as $item ) {
        $q_node = $xp->query( './/button[contains(@class,"faq-q")]', $item );
        $a_node = $xp->query( './/*[contains(@class,"faq-a")]/p', $item );
        if ( $q_node->length ) {
            $q_text = trim( $q_node->item(0)->textContent );
            $q_text = preg_replace( '/[+\-]\s*$/', '', $q_text );
            $faq[] = [
                'question' => trim( $q_text ),
                'answer'   => $a_node->length ? trim( $a_node->item(0)->textContent ) : '',
            ];
        }
    }

    return compact( 'overview', 'components', 'wiring', 'code_filename', 'code',
                    'how_steps', 'applications', 'trouble', 'upgrades', 'faq' );
}

/* ============================================================
   IMPORT PROJECTS
   ============================================================ */
function import_projects(): void {
    global $SRC, $report, $dry_run, $verbose;

    $files = glob( "$SRC/projects/*.html" );
    if ( ! $files ) { echo "No project HTML files found.\n"; return; }

    echo "\n=== PROJECTS (" . count( $files ) . " files) ===\n";

    foreach ( $files as $file ) {
        $slug = basename( $file, '.html' );
        echo "\n→ $slug\n";

        $xp = html_xpath( $file );
        if ( ! $xp ) { log_msg( "Cannot parse HTML", 'error' ); $report['projects']['failed']++; continue; }

        /* Title */
        $title = xq_text( $xp, '//h1' );
        if ( ! $title ) { log_msg( "No <h1> found", 'warn' ); $report['missing'][] = "$slug: title"; }

        /* Meta description */
        $meta_desc = '';
        $meta_nodes = $xp->query( '//meta[@name="description"]' );
        if ( $meta_nodes->length ) $meta_desc = $meta_nodes->item(0)->getAttribute( 'content' );

        /* Lead */
        $lead = xq_text( $xp, '//*[contains(@class,"article-lead")]' );

        /* Category */
        $cat_name = xq_text( $xp, '//*[contains(@class,"badge-cat")]' );
        $cat_slug = resolve_cat_slug( $cat_name );

        /* Icon class */
        $icon_class = 't-default';
        $thumb_nodes = $xp->query( '//*[contains(@class,"article-thumb")]|//*[contains(@class,"parent-thumb")]' );
        if ( $thumb_nodes->length ) {
            $classes = $thumb_nodes->item(0)->getAttribute( 'class' );
            if ( preg_match( '/\bt-(\w[\w-]*)\b/', $classes, $m ) ) {
                $icon_class = 't-' . $m[1];
            }
        }

        /* Read time — try JSON-LD schema for dependencies */
        $deps = '';
        $schema_nodes = $xp->query( '//script[@type="application/ld+json"]' );
        foreach ( $schema_nodes as $sn ) {
            $json = @json_decode( $sn->textContent, true );
            if ( $json && isset( $json['dependencies'] ) ) {
                $deps = $json['dependencies'];
                break;
            }
        }

        /* Difficulty levels */
        $levels = [];
        foreach ( [ 'beginner', 'intermediate', 'advanced' ] as $level ) {
            $data = extract_level( $xp, $level );
            if ( ! empty( $data['overview'] ) || ! empty( $data['code'] ) ) {
                $levels[ $level ] = $data;
            }
        }

        if ( empty( $levels ) ) {
            log_msg( "No difficulty level content found", 'warn' );
            $report['missing'][] = "$slug: level content";
        }

        /* Related projects */
        $related_slugs = [];
        $related_links = $xp->query( '//*[contains(@class,"related-card")]/@href' );
        foreach ( $related_links as $href ) {
            $rel_slug = basename( $href->value, '.html' );
            if ( $rel_slug && $rel_slug !== $slug ) $related_slugs[] = $rel_slug;
        }

        /* Date */
        $date_pub = '2026-06-14 00:00:00';
        $date_mod = '2026-06-18 00:00:00';
        foreach ( $schema_nodes as $sn ) {
            $json = @json_decode( $sn->textContent, true );
            if ( $json && isset( $json['datePublished'] ) ) {
                $date_pub = $json['datePublished'] . ' 00:00:00';
                $date_mod = ( $json['dateModified'] ?? $json['datePublished'] ) . ' 00:00:00';
                break;
            }
        }

        /* Check existing */
        $existing = get_posts( [ 'name' => $slug, 'post_type' => 'esp32_project', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ] );
        $is_update = ! empty( $existing );

        /* Upsert post */
        $post_args = [
            'post_type'     => 'esp32_project',
            'post_status'   => 'publish',
            'post_title'    => $title ?: ucwords( str_replace( '-', ' ', $slug ) ),
            'post_name'     => $slug,
            'post_excerpt'  => $meta_desc,
            'post_content'  => $lead,
            'post_date'     => $date_pub,
            'post_modified' => $date_mod,
        ];
        if ( $is_update ) $post_args['ID'] = $existing[0];

        $post_id = upsert_post( $post_args, 'esp32_project' );
        if ( ! $post_id ) { $report['projects']['failed']++; continue; }

        if ( $dry_run ) {
            if ( $is_update ) $report['projects']['updated']++;
            else $report['projects']['imported']++;
            log_msg( "DRY-RUN: Would write meta for $slug", 'skip' );
            continue;
        }

        /* Basic meta */
        update_post_meta( $post_id, 'project_icon_class',     $icon_class );
        update_post_meta( $post_id, 'project_lead',           $lead );
        update_post_meta( $post_id, 'project_dependencies',   $deps );
        update_post_meta( $post_id, '_meta_description',      $meta_desc );
        update_post_meta( $post_id, '_related_slugs',         $related_slugs );

        /* Difficulty level meta */
        foreach ( $levels as $level => $ld ) {
            update_post_meta( $post_id, $level . '_overview',        $ld['overview'] );
            update_post_meta( $post_id, $level . '_components',      $ld['components'] );
            update_post_meta( $post_id, $level . '_wiring',          $ld['wiring'] );
            update_post_meta( $post_id, $level . '_code_filename',   $ld['code_filename'] );
            update_post_meta( $post_id, $level . '_code',            $ld['code'] );
            update_post_meta( $post_id, $level . '_how_it_works',    $ld['how_steps'] );
            update_post_meta( $post_id, $level . '_applications',    $ld['applications'] );
            update_post_meta( $post_id, $level . '_troubleshooting', $ld['trouble'] );
            update_post_meta( $post_id, $level . '_upgrades',        $ld['upgrades'] );
            update_post_meta( $post_id, $level . '_faq',             $ld['faq'] );
        }

        /* Mirror beginner FAQ/how-it-works to top-level for schema */
        if ( isset( $levels['beginner'] ) ) {
            if ( ! empty( $levels['beginner']['faq'] ) )
                update_post_meta( $post_id, 'faq_items', $levels['beginner']['faq'] );
            if ( ! empty( $levels['beginner']['how_steps'] ) )
                update_post_meta( $post_id, 'howto_steps', $levels['beginner']['how_steps'] );
        }

        /* Category taxonomy */
        if ( $cat_slug ) {
            $term = get_term_by( 'slug', $cat_slug, 'project_category' );
            if ( $term ) {
                wp_set_post_terms( $post_id, [ $term->term_id ], 'project_category' );
            } else {
                // Create missing term
                $new_term = wp_insert_term( $cat_name, 'project_category', [ 'slug' => $cat_slug ] );
                if ( ! is_wp_error( $new_term ) ) {
                    wp_set_post_terms( $post_id, [ $new_term['term_id'] ], 'project_category' );
                    log_msg( "Created new category: $cat_name ($cat_slug)", 'warn' );
                }
            }
        }

        $report['urls'][] = "http://localhost/esp32/projects/$slug/";
        if ( $is_update ) { $report['projects']['updated']++; log_msg( "Updated post ID $post_id — " . count($levels) . " levels", 'ok' ); }
        else              { $report['projects']['imported']++; log_msg( "Imported post ID $post_id — " . count($levels) . " levels", 'ok' ); }
    }
}

/* ============================================================
   IMPORT GUIDES
   ============================================================ */
function import_guides(): void {
    global $SRC, $report, $dry_run, $verbose;

    $yaml_files = glob( "$SRC/content/guides/*.yaml" );
    if ( ! $yaml_files ) { echo "No guide YAML files found.\n"; return; }

    echo "\n=== GUIDES (" . count($yaml_files) . " files) ===\n";

    foreach ( $yaml_files as $yfile ) {
        $slug = basename( $yfile, '.yaml' );
        echo "\n→ $slug\n";

        $y = parse_simple_yaml( $yfile );
        if ( empty( $y ) ) { log_msg( "Failed to parse YAML", 'error' ); $report['guides']['failed']++; continue; }

        // Get body_html properly (multi-line single-quoted)
        $body_html = parse_yaml_body( $yfile );
        if ( ! $body_html && isset( $y['body_html'] ) ) $body_html = $y['body_html'];

        $title     = $y['headline'] ?? $y['title'] ?? ucwords( str_replace( '-', ' ', $slug ) );
        $meta_desc = $y['meta_description'] ?? '';
        $lead      = $y['lead'] ?? '';
        $phase     = isset( $y['phase'] ) ? 'Phase ' . $y['phase'] . ': ' . ( $y['proficiency_level'] ?? 'Getting Started' ) : '';
        $read_time = $y['reading_time'] ?? '';
        $faqs      = is_array( $y['faqs'] ?? null ) ? $y['faqs'] : [];
        $related   = is_array( $y['related_guides'] ?? null ) ? $y['related_guides'] : [];
        $date_pub  = ( $y['date_published'] ?? '2026-06-18' ) . ' 00:00:00';
        $date_mod  = ( $y['date_modified']  ?? '2026-06-18' ) . ' 00:00:00';

        // Build full post content from body_html
        $content = $lead ? "<p class=\"guide-lead\">{$lead}</p>\n\n" . $body_html : $body_html;

        $existing = get_posts( [ 'name' => $slug, 'post_type' => 'esp32_guide', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ] );
        $is_update = ! empty( $existing );

        $post_args = [
            'post_type'     => 'esp32_guide',
            'post_status'   => 'publish',
            'post_title'    => $title,
            'post_name'     => $slug,
            'post_excerpt'  => $meta_desc,
            'post_content'  => $content,
            'post_date'     => $date_pub,
            'post_modified' => $date_mod,
        ];
        if ( $is_update ) $post_args['ID'] = $existing[0];

        $post_id = upsert_post( $post_args, 'esp32_guide' );
        if ( ! $post_id ) { $report['guides']['failed']++; continue; }

        if ( $dry_run ) {
            if ( $is_update ) $report['guides']['updated']++; else $report['guides']['imported']++;
            continue;
        }

        update_post_meta( $post_id, 'guide_phase',     $phase );
        update_post_meta( $post_id, 'guide_read_time', $read_time );
        update_post_meta( $post_id, '_meta_description', $meta_desc );
        if ( $faqs )    update_post_meta( $post_id, 'faq_items',      $faqs );
        if ( $related ) update_post_meta( $post_id, '_related_guides', $related );

        $report['urls'][] = "http://localhost/esp32/guides/$slug/";
        if ( $is_update ) { $report['guides']['updated']++; log_msg( "Updated guide ID $post_id", 'ok' ); }
        else              { $report['guides']['imported']++; log_msg( "Imported guide ID $post_id", 'ok' ); }
    }
}

/* ============================================================
   IMPORT PAGES
   ============================================================ */
function import_pages(): void {
    global $SRC, $report, $dry_run;

    $page_yamls = glob( "$SRC/content/pages/*.yaml" );
    if ( ! $page_yamls ) { echo "No page YAML files found.\n"; return; }

    echo "\n=== PAGES (" . count($page_yamls) . " files) ===\n";

    foreach ( $page_yamls as $yfile ) {
        $slug = basename( $yfile, '.yaml' );
        echo "\n→ $slug\n";

        $y = parse_simple_yaml( $yfile );
        $body_html = parse_yaml_body( $yfile );
        if ( ! $body_html && isset( $y['body_html'] ) ) $body_html = $y['body_html'];

        $title     = $y['title'] ?? ucwords( $slug );
        $meta_desc = $y['meta_description'] ?? '';

        // Strip " | ESP32 Engine" from page titles
        $title = preg_replace( '/\s*\|\s*ESP32 Engine\s*$/i', '', $title );

        $existing = get_posts( [ 'name' => $slug, 'post_type' => 'page', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ] );
        $is_update = ! empty( $existing );

        $post_args = [
            'post_type'    => 'page',
            'post_status'  => 'publish',
            'post_title'   => $title,
            'post_name'    => $slug,
            'post_excerpt' => $meta_desc,
            'post_content' => $body_html,
        ];
        if ( $is_update ) $post_args['ID'] = $existing[0];

        $post_id = upsert_post( $post_args, 'page' );
        if ( ! $post_id ) { $report['pages']['failed']++; continue; }

        if ( $dry_run ) {
            if ( $is_update ) $report['pages']['updated']++; else $report['pages']['imported']++;
            continue;
        }

        update_post_meta( $post_id, '_meta_description', $meta_desc );

        $report['urls'][] = "http://localhost/esp32/$slug/";
        if ( $is_update ) { $report['pages']['updated']++; log_msg( "Updated page ID $post_id", 'ok' ); }
        else              { $report['pages']['imported']++; log_msg( "Imported page ID $post_id", 'ok' ); }
    }
}

/* ============================================================
   POST-IMPORT: Link related projects by slug → post_id
   ============================================================ */
function wire_related_projects(): void {
    global $dry_run;
    if ( $dry_run ) return;

    $projects = get_posts( [ 'post_type' => 'esp32_project', 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids' ] );
    foreach ( $projects as $pid ) {
        $related_slugs = get_post_meta( $pid, '_related_slugs', true );
        if ( ! is_array( $related_slugs ) || empty( $related_slugs ) ) continue;
        $related_ids = [];
        foreach ( $related_slugs as $slug ) {
            $rel = get_posts( [ 'name' => $slug, 'post_type' => 'esp32_project', 'post_status' => 'publish', 'posts_per_page' => 1, 'fields' => 'ids' ] );
            if ( $rel ) $related_ids[] = $rel[0];
        }
        if ( $related_ids ) update_post_meta( $pid, 'related_project_ids', $related_ids );
    }
    echo "\n✓ Related project links wired for " . count($projects) . " posts.\n";
}

/* ============================================================
   URL TESTING
   ============================================================ */
function test_urls(): void {
    global $report;
    $test_urls = array_merge(
        [ 'http://localhost/esp32/', 'http://localhost/esp32/projects/', 'http://localhost/esp32/guides/', 'http://localhost/esp32/category/iot-projects/' ],
        array_slice( $report['urls'], 0, 6 )
    );
    $test_urls = array_unique( $test_urls );

    echo "\n=== URL TESTS ===\n";
    foreach ( $test_urls as $url ) {
        $ctx  = stream_context_create( [ 'http' => [ 'timeout' => 5, 'ignore_errors' => true ] ] );
        $body = @file_get_contents( $url, false, $ctx );
        $code = 0;
        if ( isset( $http_response_header ) ) {
            preg_match( '/HTTP\/\d\.\d (\d{3})/', $http_response_header[0] ?? '', $m );
            $code = (int) ( $m[1] ?? 0 );
        }
        $mark = $code === 200 ? '✓' : ( $code > 0 ? '✗' : '?' );
        echo "  [$code] $mark $url\n";
    }
}

/* ============================================================
   PRINT REPORT
   ============================================================ */
function print_report(): void {
    global $report, $dry_run;

    $mode = $dry_run ? ' (DRY-RUN)' : '';
    echo "\n" . str_repeat( '=', 60 ) . "\n";
    echo "  IMPORT REPORT{$mode}\n";
    echo str_repeat( '=', 60 ) . "\n";

    $total_imported = $report['projects']['imported'] + $report['guides']['imported'] + $report['pages']['imported'];
    $total_updated  = $report['projects']['updated']  + $report['guides']['updated']  + $report['pages']['updated'];
    $total_failed   = $report['projects']['failed']   + $report['guides']['failed']   + $report['pages']['failed'];

    echo "\n  Projects : imported={$report['projects']['imported']}  updated={$report['projects']['updated']}  skipped={$report['projects']['skipped']}  failed={$report['projects']['failed']}\n";
    echo "  Guides   : imported={$report['guides']['imported']}   updated={$report['guides']['updated']}   skipped={$report['guides']['skipped']}   failed={$report['guides']['failed']}\n";
    echo "  Pages    : imported={$report['pages']['imported']}    updated={$report['pages']['updated']}    skipped={$report['pages']['skipped']}    failed={$report['pages']['failed']}\n";
    echo "\n  Total imported : $total_imported\n";
    echo "  Total updated  : $total_updated\n";
    echo "  Total failed   : $total_failed\n";

    if ( $report['errors'] ) {
        echo "\n  Errors:\n";
        foreach ( $report['errors'] as $e ) echo "    • $e\n";
    }
    if ( $report['missing'] ) {
        echo "\n  Missing metadata:\n";
        foreach ( array_slice( $report['missing'], 0, 20 ) as $m ) echo "    • $m\n";
        if ( count($report['missing']) > 20 ) echo "    … and " . (count($report['missing'])-20) . " more\n";
    }

    echo "\n  Imported URLs:\n";
    foreach ( $report['urls'] as $url ) echo "    $url\n";

    echo "\n" . str_repeat( '=', 60 ) . "\n";
}

/* ============================================================
   MAIN
   ============================================================ */
echo "ESP32 Engine Content Migrator\n";
echo "Source : $SRC\n";
echo "Target : http://localhost/esp32/\n";
if ( $dry_run ) echo "[DRY-RUN MODE — no changes will be written]\n";

if ( ! $only || $only === 'projects' ) import_projects();
if ( ! $only || $only === 'guides'   ) import_guides();
if ( ! $only || $only === 'pages'    ) import_pages();

if ( ! $dry_run ) wire_related_projects();

test_urls();
print_report();

echo "\nDone.\n";
