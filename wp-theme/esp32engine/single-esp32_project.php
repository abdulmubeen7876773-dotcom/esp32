<?php
get_header();

while ( have_posts() ) : the_post();

$post_id    = get_the_ID();
$icon_class = get_post_meta( $post_id, 'project_icon_class', true ) ?: 't-default';
$icon_svg   = get_post_meta( $post_id, 'project_icon_svg', true );
$lead       = get_post_meta( $post_id, 'project_lead', true ) ?: get_the_excerpt();
$cats       = get_the_terms( $post_id, 'project_category' );
$cat        = ( $cats && ! is_wp_error( $cats ) ) ? $cats[0] : null;

// Difficulty level sections stored as serialized arrays in post meta.
// Each level: overview (html), components (array), wiring (array of [pin, esp32, notes]),
//             code_filename, code (raw), how_it_works (array of steps),
//             applications (array), troubleshooting (array of [problem, solution]),
//             upgrades (array), faq (array of [question, answer]).
$levels = [ 'beginner', 'intermediate', 'advanced' ];

function esp32_get_level_meta( int $id, string $level, string $key ) {
    return get_post_meta( $id, $level . '_' . $key, true );
}

// Related projects (same category, exclude current)
$related = new WP_Query( [
    'post_type'      => 'esp32_project',
    'posts_per_page' => 4,
    'post__not_in'   => [ $post_id ],
    'tax_query'      => $cat ? [ [ 'taxonomy' => 'project_category', 'field' => 'term_id', 'terms' => $cat->term_id ] ] : [],
    'orderby'        => 'rand',
] );
?>

<main>
<div class="wrap article-shell parent-project-shell">

  <!-- Left sidebar: difficulty + section TOC -->
  <aside class="sidebar-left">
    <div class="sidebar-sticky">
      <h3>Difficulty</h3>
      <ul class="side-list side-toc side-levels">
        <li><a href="#beginner" data-level-link="beginner">Beginner</a></li>
        <li><a href="#intermediate" data-level-link="intermediate">Intermediate</a></li>
        <li><a href="#advanced" data-level-link="advanced">Advanced</a></li>
      </ul>
      <h3 class="sidebar-divider">Sections</h3>
      <ul class="side-list side-toc side-sections" id="section-toc">
        <li><a href="#sec-beginner-overview" data-section="overview">Overview</a></li>
        <li><a href="#sec-beginner-components" data-section="components">Components</a></li>
        <li><a href="#sec-beginner-wiring" data-section="wiring">Wiring</a></li>
        <li><a href="#sec-beginner-code" data-section="code">Arduino Code</a></li>
        <li><a href="#sec-beginner-how" data-section="how">How It Works</a></li>
        <li><a href="#sec-beginner-apps" data-section="apps">Applications</a></li>
        <li><a href="#sec-beginner-troubleshooting" data-section="troubleshooting">Troubleshooting</a></li>
        <li><a href="#sec-beginner-upgrades" data-section="upgrades">Upgrades</a></li>
        <li><a href="#sec-beginner-faq" data-section="faq">FAQ</a></li>
      </ul>
      <?php if ( $cat ) : ?>
      <h3 class="sidebar-divider">Category</h3>
      <ul class="side-list">
        <li><a href="<?php echo esc_url( get_term_link( $cat ) ); ?>"><?php echo esc_html( $cat->name ); ?></a></li>
      </ul>
      <?php endif; ?>
    </div>
  </aside>

  <!-- Main article -->
  <article class="article-main parent-article">
    <header class="article-header">

      <?php
      $crumbs = [ [ 'url' => home_url( '/' ), 'label' => 'Home' ] ];
      if ( $cat ) $crumbs[] = [ 'url' => get_term_link( $cat ), 'label' => $cat->name ];
      $crumbs[] = [ 'url' => get_permalink(), 'label' => get_the_title() ];
      esp32_breadcrumb( $crumbs );
      ?>

      <div class="parent-hero-row project-hero-banner">
        <div class="parent-hero-text">
          <h1><?php the_title(); ?></h1>
          <div class="article-badges">
            <?php if ( $cat ) : ?>
            <span class="badge badge-cat"><?php echo esc_html( $cat->name ); ?></span>
            <?php endif; ?>
            <span class="badge badge-beginner">Beginner</span>
            <span class="badge badge-intermediate">Intermediate</span>
            <span class="badge badge-advanced">Advanced</span>
          </div>
          <?php if ( $lead ) : ?>
          <p class="article-lead"><?php echo esc_html( $lead ); ?></p>
          <?php endif; ?>
        </div>
        <div class="article-thumb project-hero-image <?php echo esc_attr( $icon_class ); ?> parent-thumb">
          <?php echo $icon_svg ?: esp32_category_icon( $cat ? $cat->slug : '' ); ?>
        </div>
      </div>
    </header>

    <!-- Difficulty switcher (CSS radio trick — same as static site) -->
    <div class="difficulty-switcher">
      <input type="radio" name="difficulty-level" id="level-radio-beginner"     class="level-radio" checked aria-hidden="true" tabindex="-1">
      <input type="radio" name="difficulty-level" id="level-radio-intermediate" class="level-radio" aria-hidden="true" tabindex="-1">
      <input type="radio" name="difficulty-level" id="level-radio-advanced"     class="level-radio" aria-hidden="true" tabindex="-1">

      <div class="difficulty-tabs" role="tablist" aria-label="Difficulty level">
        <label for="level-radio-beginner"     class="difficulty-tab" id="tab-beginner"     data-level="beginner"     role="tab">Beginner</label>
        <label for="level-radio-intermediate" class="difficulty-tab" id="tab-intermediate" data-level="intermediate" role="tab">Intermediate</label>
        <label for="level-radio-advanced"     class="difficulty-tab" id="tab-advanced"     data-level="advanced"     role="tab">Advanced</label>
      </div>

      <div class="mobile-section-nav">
        <label class="visually-hidden" for="mobile-nav-select">Jump to section</label>
        <select id="mobile-nav-select" class="mobile-nav-select" aria-label="Jump to section">
          <option value="">Jump to section…</option>
          <option value="sec-beginner-overview">Overview</option>
          <option value="sec-beginner-components">Components</option>
          <option value="sec-beginner-wiring">Wiring</option>
          <option value="sec-beginner-code">Arduino Code</option>
          <option value="sec-beginner-how">How It Works</option>
          <option value="sec-beginner-apps">Applications</option>
          <option value="sec-beginner-troubleshooting">Troubleshooting</option>
          <option value="sec-beginner-upgrades">Upgrades</option>
          <option value="sec-beginner-faq">FAQ</option>
          <option value="related">Related Projects</option>
        </select>
      </div>

      <div class="difficulty-sections">
        <?php foreach ( $levels as $level ) :
            $overview        = esp32_get_level_meta( $post_id, $level, 'overview' );
            $components      = (array) ( esp32_get_level_meta( $post_id, $level, 'components' ) ?: [] );
            $wiring          = (array) ( esp32_get_level_meta( $post_id, $level, 'wiring' ) ?: [] );
            $code_filename   = esp32_get_level_meta( $post_id, $level, 'code_filename' ) ?: get_the_slug() . '_' . $level . '.ino';
            $code            = esp32_get_level_meta( $post_id, $level, 'code' );
            $how_steps       = (array) ( esp32_get_level_meta( $post_id, $level, 'how_it_works' ) ?: [] );
            $apps            = (array) ( esp32_get_level_meta( $post_id, $level, 'applications' ) ?: [] );
            $troubleshooting = (array) ( esp32_get_level_meta( $post_id, $level, 'troubleshooting' ) ?: [] );
            $upgrades        = (array) ( esp32_get_level_meta( $post_id, $level, 'upgrades' ) ?: [] );
            $faq             = (array) ( esp32_get_level_meta( $post_id, $level, 'faq' ) ?: [] );
        ?>
        <div class="difficulty-content level-<?php echo esc_attr( $level ); ?>-panel"
             data-level="<?php echo esc_attr( $level ); ?>"
             id="level-<?php echo esc_attr( $level ); ?>"
             role="tabpanel"
             aria-labelledby="tab-<?php echo esc_attr( $level ); ?>">

          <!-- Overview -->
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-overview" data-section="overview" open>
            <summary class="accordion-header">Overview</summary>
            <div class="accordion-content">
              <?php if ( $overview ) : ?>
                <?php echo wp_kses_post( $overview ); ?>
              <?php else : ?>
                <p><?php echo esc_html( ucfirst( $level ) ); ?> level content for <?php the_title(); ?> — add via WordPress admin using the custom fields panel.</p>
              <?php endif; ?>
            </div>
          </details>

          <!-- Components -->
          <?php if ( $components ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-components" data-section="components">
            <summary class="accordion-header">Components</summary>
            <div class="accordion-content">
              <ul class="parts-grid parts-grid-compact">
                <?php foreach ( $components as $comp ) : ?>
                <li><span><?php echo esc_html( is_array( $comp ) ? ( $comp['name'] ?? $comp[0] ?? '' ) : $comp ); ?></span></li>
                <?php endforeach; ?>
              </ul>
            </div>
          </details>
          <?php endif; ?>

          <!-- Wiring -->
          <?php if ( $wiring ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-wiring" data-section="wiring">
            <summary class="accordion-header">Wiring</summary>
            <div class="accordion-content">
              <div class="wiring-table-wrap">
                <table class="wiring-table">
                  <thead><tr><th>Component Pin</th><th>ESP32 Pin</th><th>Notes</th></tr></thead>
                  <tbody>
                    <?php foreach ( $wiring as $row ) :
                        if ( ! is_array( $row ) ) continue;
                        $pin     = $row['component_pin'] ?? $row[0] ?? '';
                        $esp32   = $row['esp32_pin']     ?? $row[1] ?? '';
                        $notes   = $row['notes']         ?? $row[2] ?? '';
                    ?>
                    <tr>
                      <td><?php echo esc_html( $pin ); ?></td>
                      <td><?php echo esc_html( $esp32 ); ?></td>
                      <td><?php echo esc_html( $notes ); ?></td>
                    </tr>
                    <?php endforeach; ?>
                  </tbody>
                </table>
              </div>
            </div>
          </details>
          <?php endif; ?>

          <!-- Arduino Code -->
          <?php if ( $code ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-code" data-section="code">
            <summary class="accordion-header">Arduino Code</summary>
            <div class="accordion-content">
              <div class="code-block">
                <div class="code-bar">
                  <span><?php echo esc_html( $code_filename ); ?></span>
                  <button type="button" class="copy-btn">Copy</button>
                </div>
                <pre class="level-code"><?php echo esc_html( $code ); ?></pre>
              </div>
            </div>
          </details>
          <?php endif; ?>

          <!-- How It Works -->
          <?php if ( $how_steps ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-how" data-section="how">
            <summary class="accordion-header">How It Works</summary>
            <div class="accordion-content">
              <div class="steps steps-compact">
                <?php foreach ( $how_steps as $i => $step ) : ?>
                <div class="step">
                  <span class="step-no"><?php echo esc_html( str_pad( $i + 1, 2, '0', STR_PAD_LEFT ) ); ?></span>
                  <p><?php echo esc_html( is_array( $step ) ? ( $step['text'] ?? $step[0] ?? '' ) : $step ); ?></p>
                </div>
                <?php endforeach; ?>
              </div>
            </div>
          </details>
          <?php endif; ?>

          <!-- Applications -->
          <?php if ( $apps ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-apps" data-section="apps">
            <summary class="accordion-header">Applications</summary>
            <div class="accordion-content">
              <ul class="detail-list">
                <?php foreach ( $apps as $app ) : ?>
                <li><?php echo esc_html( is_array( $app ) ? ( $app['item'] ?? $app[0] ?? '' ) : $app ); ?></li>
                <?php endforeach; ?>
              </ul>
            </div>
          </details>
          <?php endif; ?>

          <!-- Troubleshooting -->
          <?php if ( $troubleshooting ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-troubleshooting" data-section="troubleshooting">
            <summary class="accordion-header">Troubleshooting</summary>
            <div class="accordion-content">
              <div class="trouble-list">
                <?php foreach ( $troubleshooting as $item ) :
                    $problem  = is_array( $item ) ? ( $item['problem']  ?? '' ) : $item;
                    $solution = is_array( $item ) ? ( $item['solution'] ?? '' ) : '';
                ?>
                <div class="trouble-item">
                  <h4><?php echo esc_html( $problem ); ?></h4>
                  <?php if ( $solution ) : ?><p><?php echo esc_html( $solution ); ?></p><?php endif; ?>
                </div>
                <?php endforeach; ?>
              </div>
            </div>
          </details>
          <?php endif; ?>

          <!-- Upgrades -->
          <?php if ( $upgrades ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-upgrades" data-section="upgrades">
            <summary class="accordion-header">Upgrades</summary>
            <div class="accordion-content">
              <ul class="detail-list">
                <?php foreach ( $upgrades as $up ) : ?>
                <li><?php echo esc_html( is_array( $up ) ? ( $up['item'] ?? $up[0] ?? '' ) : $up ); ?></li>
                <?php endforeach; ?>
              </ul>
            </div>
          </details>
          <?php endif; ?>

          <!-- FAQ -->
          <?php if ( $faq ) : ?>
          <details class="accordion-item" id="sec-<?php echo esc_attr( $level ); ?>-faq" data-section="faq">
            <summary class="accordion-header">FAQ</summary>
            <div class="accordion-content">
              <div class="faq-list">
                <?php foreach ( $faq as $item ) :
                    $q = is_array( $item ) ? ( $item['question'] ?? '' ) : $item;
                    $a = is_array( $item ) ? ( $item['answer']   ?? '' ) : '';
                ?>
                <div class="faq-item">
                  <button type="button" class="faq-q"><?php echo esc_html( $q ); ?><span class="plus">+</span></button>
                  <div class="faq-a"><p><?php echo esc_html( $a ); ?></p></div>
                </div>
                <?php endforeach; ?>
              </div>
            </div>
          </details>
          <?php endif; ?>

          <!-- If no meta set yet, show full post content as a fallback -->
          <?php if ( $level === 'beginner' && ! $overview && ! $code ) : ?>
          <div class="accordion-item">
            <div class="accordion-content">
              <?php the_content(); ?>
            </div>
          </div>
          <?php endif; ?>

        </div>
        <?php endforeach; ?>
      </div><!-- .difficulty-sections -->
    </div><!-- .difficulty-switcher -->

    <!-- Related Projects -->
    <?php if ( $related->have_posts() ) : ?>
    <section id="related" style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
      <h2 style="font-size: 1.125rem; margin-bottom: 1rem;">Related Projects</h2>
      <div class="related-grid">
        <?php while ( $related->have_posts() ) : $related->the_post();
            $r_icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: 't-default';
            $r_icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
            $r_cats       = get_the_terms( get_the_ID(), 'project_category' );
            $r_cat        = ( $r_cats && ! is_wp_error( $r_cats ) ) ? $r_cats[0] : null;
        ?>
        <a class="related-card" href="<?php the_permalink(); ?>">
          <span class="related-thumb <?php echo esc_attr( $r_icon_class ); ?>">
            <?php echo $r_icon_svg ?: esp32_category_icon( $r_cat ? $r_cat->slug : '' ); ?>
          </span>
          <span class="related-meta">
            <strong><?php the_title(); ?></strong>
            <?php if ( $r_cat ) : ?><span class="meta"><?php echo esc_html( $r_cat->name ); ?></span><?php endif; ?>
          </span>
        </a>
        <?php endwhile; wp_reset_postdata(); ?>
      </div>
    </section>
    <?php endif; ?>

  </article><!-- .article-main -->

  <!-- Right sidebar -->
  <aside class="sidebar-right">
    <div class="sidebar-sticky">
      <div class="promo-box">
        <strong>Free ESP32 Resources</strong>
        <p>All projects include wiring tables, copy-paste Arduino code, and troubleshooting guides.</p>
        <a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">All Projects</a>
      </div>
    </div>
  </aside>

</div><!-- .article-shell -->
</main>

<style>
.level-radio{position:absolute;opacity:0;width:0;height:0;margin:0;padding:0;pointer-events:none}
.difficulty-switcher .difficulty-content{display:none!important}
.difficulty-switcher #level-radio-beginner:checked~.difficulty-sections #level-beginner{display:block!important}
.difficulty-switcher #level-radio-intermediate:checked~.difficulty-sections #level-intermediate{display:block!important}
.difficulty-switcher #level-radio-advanced:checked~.difficulty-sections #level-advanced{display:block!important}
details.accordion-item>summary{list-style:none;cursor:pointer}
details.accordion-item>summary::-webkit-details-marker{display:none}
</style>

<?php endwhile; ?>
<?php get_footer(); ?>
