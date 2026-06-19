<?php get_header();

/* ── Dynamic counts ── */
$guide_count   = wp_count_posts( 'esp32_guide' )->publish;
$project_count = wp_count_posts( 'esp32_project' )->publish;
$cat_count     = wp_count_terms( 'project_category' );
if ( is_wp_error( $cat_count ) ) $cat_count = 0;

/* Count code examples (guides that have <pre> blocks) */
global $wpdb;
$code_count = (int) $wpdb->get_var(
    "SELECT COUNT(*) FROM {$wpdb->posts}
     WHERE post_type IN ('esp32_guide','esp32_project')
       AND post_status = 'publish'
       AND post_content LIKE '%<pre>%'"
);

?>
<main>

<!-- ===== HERO ===== -->
<section class="hero-home reveal" aria-labelledby="hero-heading">
  <div class="wrap hero-home-inner">
    <div class="hero-home-content">
      <p class="hero-eyebrow">Learn | Build | Innovate</p>
      <h1 id="hero-heading">The Premium ESP32 Learning Platform</h1>
      <p class="hero-sub">Master ESP32, IoT, embedded systems, and Arduino with step-by-step guides, wiring diagrams, and production-ready project tutorials.</p>

      <!-- Hero search box -->
      <div class="hero-search-wrap" role="search" aria-label="Site search">
        <div class="hero-search-box" id="hero-search-box">
          <svg class="hero-search-icon" viewBox="0 0 20 20" fill="none" aria-hidden="true" width="18" height="18">
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="2"/>
            <path d="M14 14l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input type="search" class="hero-search-input" id="hero-search-input"
            placeholder='Search guides, projects, FAQs…  (or press / )'
            aria-label="Search guides, projects and FAQs"
            autocomplete="off" spellcheck="false">
        </div>
        <div class="hero-search-results" id="hero-search-results" hidden></div>
      </div>

      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Start Learning</a>
        <a class="btn btn-secondary btn-lg" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Explore Projects</a>
      </div>

      <!-- Dynamic Stats -->
      <div class="hero-stat-row">
        <div class="hero-stat-pill"><strong><?php echo esc_html( $guide_count ); ?></strong><span>Guides</span></div>
        <div class="hero-stat-pill"><strong><?php echo esc_html( $project_count ); ?>+</strong><span>Projects</span></div>
        <div class="hero-stat-pill"><strong><?php echo esc_html( $cat_count ); ?>+</strong><span>Categories</span></div>
        <div class="hero-stat-pill"><strong><?php echo esc_html( max( $code_count, 30 ) ); ?>+</strong><span>Code Examples</span></div>
      </div>
    </div>
    <div class="hero-home-visual" aria-hidden="true">
      <div class="hero-visual-frame">
        <svg class="hero-board-svg" viewBox="0 0 240 240" fill="none" aria-hidden="true">
          <defs>
            <linearGradient id="heroGrad" x1="40" y1="60" x2="200" y2="180">
              <stop stop-color="#A855F7"/><stop offset="1" stop-color="#6D28D9"/>
            </linearGradient>
            <filter id="heroGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="6" result="b"/>
              <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <rect x="40" y="62" width="160" height="104" rx="16" stroke="url(#heroGrad)" stroke-width="2.5" filter="url(#heroGlow)"/>
          <rect x="62" y="84" width="116" height="60" rx="10" fill="rgba(109,40,217,.12)" stroke="rgba(109,40,217,.35)" stroke-width="1.5"/>
          <path d="M40 86h-16M40 114h-16M40 142h-16M200 86h16M200 114h16M200 142h16M86 62V42M120 62V42M154 62V42M86 166V186M120 166V186M154 166V186" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" opacity=".55"/>
          <circle cx="120" cy="114" r="8" fill="#6D28D9"/>
          <circle cx="120" cy="114" r="16" stroke="#A855F7" stroke-width="1.2" opacity=".35"/>
          <text x="120" y="119" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="Poppins,Inter,sans-serif">ESP32</text>
        </svg>
        <div class="hero-float-stack" aria-hidden="true">
          <div class="hero-float-card hero-float-card-a"><span class="hero-float-label">GPIO Monitor</span><strong>34</strong><span class="hero-float-sub">Analog Input</span></div>
          <div class="hero-float-card hero-float-card-b"><span class="hero-float-label">Wi-Fi Status</span><strong>Online</strong><span class="hero-float-sub">2.4 GHz Connected</span></div>
          <div class="hero-float-card hero-float-card-c"><span class="hero-float-label">Relay Output</span><strong>ACTIVE</strong><span class="hero-float-sub">GPIO26 · Pump ON</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ===== START LEARNING ESP32 ===== -->
<section class="section-premium wrap reveal" id="start-learning">
  <div class="section-head">
    <div>
      <p class="section-eyebrow">Structured learning paths</p>
      <h2>Start Learning ESP32</h2>
      <p class="section-sub">Follow the structured path from zero to confident ESP32 developer — three phases, each building on the last.</p>
    </div>
    <a class="btn btn-secondary btn-sm" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">All <?php echo esc_html( $guide_count ); ?> guides</a>
  </div>

  <div class="learning-path-grid">
    <!-- Phase 1 -->
    <div class="learning-path-card">
      <div class="learning-path-header">
        <span class="learning-path-num">01</span>
        <div>
          <strong class="learning-path-phase">Phase 1</strong>
          <h3>ESP32 Fundamentals</h3>
        </div>
      </div>
      <p>Learn what ESP32 is, how its GPIO works, the pinout, variants, memory architecture, boot strapping, and power consumption. Perfect starting point.</p>
      <ul class="learning-path-list">
        <li><a href="<?php echo esc_url( home_url( '/guides/what-is-esp32/' ) ); ?>">What is ESP32?</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/esp32-vs-esp8266/' ) ); ?>">ESP32 vs ESP8266</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/esp32-pinout-guide/' ) ); ?>">ESP32 Pinout Guide</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">+ 7 more guides →</a></li>
      </ul>
      <a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/guides/what-is-esp32/' ) ); ?>">Start Phase 1</a>
    </div>

    <!-- Phase 2 -->
    <div class="learning-path-card">
      <div class="learning-path-header">
        <span class="learning-path-num">02</span>
        <div>
          <strong class="learning-path-phase">Phase 2</strong>
          <h3>Dev Environment Setup</h3>
        </div>
      </div>
      <p>Install Arduino IDE, ESP-IDF, PlatformIO, and VS Code extensions. Write your first sketch, upload it, and use the serial monitor for debugging.</p>
      <ul class="learning-path-list">
        <li><a href="<?php echo esc_url( home_url( '/guides/installing-arduino-ide-esp32/' ) ); ?>">Installing Arduino IDE</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/first-esp32-program/' ) ); ?>">First ESP32 Program</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/serial-monitor-guide/' ) ); ?>">Using Serial Monitor</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">+ 7 more guides →</a></li>
      </ul>
      <a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/guides/installing-arduino-ide-esp32/' ) ); ?>">Start Phase 2</a>
    </div>

    <!-- Phase 3 -->
    <div class="learning-path-card">
      <div class="learning-path-header">
        <span class="learning-path-num">03</span>
        <div>
          <strong class="learning-path-phase">Phase 3</strong>
          <h3>GPIO &amp; Hardware Control</h3>
        </div>
      </div>
      <p>Master digital inputs and outputs, pull-up/pull-down resistors, button debouncing, LED PWM control, relay switching, and analog reading with ADC/DAC.</p>
      <ul class="learning-path-list">
        <li><a href="<?php echo esc_url( home_url( '/guides/digital-inputs-esp32/' ) ); ?>">Digital Inputs on ESP32</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/reading-buttons-esp32/' ) ); ?>">Reading Buttons</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/adc-explained-esp32/' ) ); ?>">ADC Explained</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">+ 7 more guides →</a></li>
      </ul>
      <a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/guides/digital-inputs-esp32/' ) ); ?>">Start Phase 3</a>
    </div>

    <!-- Phase 4 — NEW -->
    <div class="learning-path-card learning-path-card-new">
      <span class="learning-path-new-badge">New</span>
      <div class="learning-path-header">
        <span class="learning-path-num">04</span>
        <div>
          <strong class="learning-path-phase">Phase 4</strong>
          <h3>Connectivity &amp; Protocols</h3>
        </div>
      </div>
      <ul class="learning-path-list">
        <li><a href="<?php echo esc_url( home_url( '/guides/wifi-basics-esp32/' ) ); ?>">Wi-Fi Basics</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/mqtt-esp32/' ) ); ?>">MQTT Protocol</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/esp32-web-server/' ) ); ?>">Web Server</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/ble-esp32/' ) ); ?>">BLE GATT Server</a></li>
        <li><a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">+ 6 more guides →</a></li>
      </ul>
      <a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/guides/wifi-basics-esp32/' ) ); ?>">Start Phase 4</a>
    </div>
  </div>
</section>

<!-- ===== POPULAR GUIDES ===== -->
<section class="section-premium wrap reveal" id="popular-guides">
  <div class="section-head">
    <div>
      <p class="section-eyebrow">Most read</p>
      <h2>Popular Guides</h2>
    </div>
    <a class="btn btn-secondary btn-sm" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">View all guides</a>
  </div>

  <?php
  /* Featured guides: what-is-esp32, esp32-vs-esp8266, esp32-pinout-guide + 3 recent */
  $featured_slugs = [ 'what-is-esp32', 'esp32-vs-esp8266', 'esp32-pinout-guide',
                      'digital-inputs-esp32', 'installing-arduino-ide-esp32', 'adc-explained-esp32' ];
  $pop_guides = get_posts( [
      'post_type'      => 'esp32_guide',
      'post_status'    => 'publish',
      'post_name__in'  => $featured_slugs,
      'posts_per_page' => 6,
      'orderby'        => 'post__in',
  ] );
  if ( empty( $pop_guides ) ) {
      $pop_guides = get_posts( [ 'post_type' => 'esp32_guide', 'post_status' => 'publish', 'posts_per_page' => 6 ] );
  }
  ?>
  <div class="popular-guides-grid">
    <?php foreach ( $pop_guides as $g ) :
      $phase = get_post_meta( $g->ID, 'guide_phase', true ) ?: 'Guide';
      $rtime = get_post_meta( $g->ID, 'guide_read_time', true ) ?: '10 min';
    ?>
    <a class="pop-guide-card" href="<?php echo esc_url( get_permalink( $g->ID ) ); ?>">
      <div class="pop-guide-badges">
        <span class="badge badge-cat"><?php echo esc_html( $phase ); ?></span>
        <span class="badge badge-time"><?php echo esc_html( $rtime ); ?></span>
      </div>
      <strong class="pop-guide-title"><?php echo esc_html( $g->post_title ); ?></strong>
      <p class="pop-guide-excerpt"><?php echo esc_html( wp_trim_words( $g->post_excerpt ?: $g->post_content, 18 ) ); ?></p>
      <span class="pop-guide-arrow" aria-hidden="true">Read Guide →</span>
    </a>
    <?php endforeach; ?>
  </div>
</section>

<!-- ===== FEATURED PROJECTS ===== -->
<section class="section-premium wrap reveal" id="featured">
  <div class="section-head">
    <div>
      <p class="section-eyebrow">Editor's pick</p>
      <h2>Popular Projects</h2>
    </div>
    <div class="carousel-controls">
      <a class="btn btn-secondary btn-sm" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">View all</a>
      <button type="button" class="carousel-btn" data-carousel="featured" data-dir="-1" aria-label="Scroll left">‹</button>
      <button type="button" class="carousel-btn" data-carousel="featured" data-dir="1" aria-label="Scroll right">›</button>
    </div>
  </div>
  <div class="carousel-shell">
    <div class="carousel-track" id="carousel-featured" tabindex="0" role="region" aria-label="Featured ESP32 projects">
      <?php
      $featured = new WP_Query( [
          'post_type'      => 'esp32_project',
          'posts_per_page' => 8,
          'orderby'        => 'menu_order',
          'order'          => 'ASC',
          'meta_key'       => 'is_featured',
          'meta_value'     => '1',
      ] );
      if ( ! $featured->have_posts() ) {
          $featured = new WP_Query( [ 'post_type' => 'esp32_project', 'posts_per_page' => 8, 'orderby' => 'menu_order', 'order' => 'ASC' ] );
      }
      while ( $featured->have_posts() ) : $featured->the_post();
          $icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: 't-default';
          $icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
          $cats       = get_the_terms( get_the_ID(), 'project_category' );
          $cat_name   = ( $cats && ! is_wp_error( $cats ) ) ? $cats[0]->name : '';
      ?>
      <a class="carousel-card product-card" href="<?php the_permalink(); ?>">
        <span class="carousel-card-thumb <?php echo esc_attr( $icon_class ); ?>">
          <?php echo $icon_svg ?: esp32_category_icon( $cats[0]->slug ?? '' ); ?>
        </span>
        <span class="carousel-card-body">
          <span class="card-badges">
            <?php if ( $cat_name ) : ?><span class="badge badge-cat"><?php echo esc_html( $cat_name ); ?></span><?php endif; ?>
            <span class="badge badge-beginner">3 Levels</span>
          </span>
          <strong><?php the_title(); ?></strong>
          <span class="carousel-card-meta">Beginner · Intermediate · Advanced</span>
        </span>
      </a>
      <?php endwhile; wp_reset_postdata(); ?>
    </div>
  </div>
</section>

<!-- ===== SITE STATS ===== -->
<section class="portal-section wrap reveal portal-duo portal-roadmap-stats" id="roadmap">
  <div class="portal-duo-col roadmap-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Structured learning</p>
      <h2>ESP32 Learning Roadmap</h2>
    </div>
    <div class="roadmap-track roadmap-track-premium">
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">01</span><div><strong class="badge badge-beginner">Phase 1</strong><span>ESP32 fundamentals &amp; chip concepts</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">02</span><div><strong class="badge badge-intermediate">Phase 2</strong><span>Dev environment, Arduino &amp; IDE setup</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">03</span><div><strong class="badge badge-advanced">Phase 3</strong><span>GPIO control, analog input &amp; hardware</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">04</span><div><strong class="badge badge-cat">Phase 4</strong><span>Wi-Fi, MQTT, BLE, ESP-NOW &amp; OTA</span></div></div>
    </div>
    <a class="roadmap-link" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Browse all <?php echo esc_html( $guide_count ); ?> guides →</a>
  </div>
  <div class="portal-duo-col stats-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Library at a glance</p>
      <h2>Content Statistics</h2>
    </div>
    <div class="portal-stats-grid">
      <div class="portal-stat"><strong><?php echo esc_html( $guide_count ); ?></strong><span>Total Guides</span></div>
      <div class="portal-stat"><strong><?php echo esc_html( $project_count ); ?>+</strong><span>Projects</span></div>
      <div class="portal-stat"><strong><?php echo esc_html( $cat_count ); ?>+</strong><span>Categories</span></div>
      <div class="portal-stat"><strong><?php echo esc_html( max( $code_count, 30 ) ); ?>+</strong><span>Code Examples</span></div>
    </div>
    <div class="stats-highlights">
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⚡</span><span>Wiring tables on every guide</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⌨</span><span>Copy-paste Arduino sketches</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">📱</span><span>Mobile-friendly layouts</span></div>
    </div>
  </div>
</section>

<!-- ===== LATEST TUTORIALS + CATEGORIES ===== -->
<section class="portal-section wrap reveal portal-duo" id="latest">
  <div class="portal-duo-col portal-latest">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Fresh projects</p>
      <h2>Latest Projects</h2>
    </div>
    <div class="tutorial-list">
      <?php
      $latest = new WP_Query( [ 'post_type' => 'esp32_project', 'posts_per_page' => 6, 'orderby' => 'date', 'order' => 'DESC' ] );
      while ( $latest->have_posts() ) : $latest->the_post();
          $icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: 't-default';
          $icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
          $cats       = get_the_terms( get_the_ID(), 'project_category' );
          $cat_name   = ( $cats && ! is_wp_error( $cats ) ) ? $cats[0]->name : '';
      ?>
      <a class="tutorial-row" href="<?php the_permalink(); ?>">
        <span class="tutorial-icon <?php echo esc_attr( $icon_class ); ?>">
          <?php echo $icon_svg ?: esp32_category_icon( $cats[0]->slug ?? '' ); ?>
        </span>
        <span class="tutorial-meta">
          <strong><?php the_title(); ?></strong>
          <span class="tutorial-cat"><?php echo esc_html( $cat_name ); ?> · 3 levels</span>
        </span>
        <span class="tutorial-arrow" aria-hidden="true">→</span>
      </a>
      <?php endwhile; wp_reset_postdata(); ?>
    </div>
  </div>

  <div class="portal-duo-col portal-categories" id="categories">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Top domains</p>
      <h2>Popular Categories</h2>
    </div>
    <div class="pop-cat-grid">
      <?php
      $all_cats = get_terms( [ 'taxonomy' => 'project_category', 'hide_empty' => false, 'number' => 10 ] );
      if ( $all_cats && ! is_wp_error( $all_cats ) ) :
          foreach ( $all_cats as $cat ) :
              $thumb_class = esp32_category_thumb_class( $cat->slug );
      ?>
      <a class="pop-cat tech-cat-card" href="<?php echo esc_url( get_term_link( $cat ) ); ?>">
        <span class="pop-cat-icon <?php echo esc_attr( $thumb_class ); ?>"><?php echo esp32_category_icon( $cat->slug ); ?></span>
        <span><?php echo esc_html( $cat->name ); ?></span>
      </a>
      <?php endforeach; endif; ?>
    </div>
  </div>
</section>

<!-- ===== WHY THIS PLATFORM ===== -->
<section class="portal-section wrap reveal" id="why">
  <div class="section-head-portal">
    <div class="section-head-portal-text">
      <p class="section-eyebrow">Built for makers</p>
      <h2>Why This Platform</h2>
    </div>
  </div>
  <div class="why-grid-premium">
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🎯</span><strong>Beginner Friendly</strong><p>Start with breadboard builds and clear wiring tables — zero assumed knowledge.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🔧</span><strong>Real Hardware Projects</strong><p>Every guide maps to real sensors, relays, and ESP32 GPIO pins you can hold.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">📊</span><strong>3 Difficulty Levels</strong><p>Beginner, Intermediate, and Advanced guides on every major topic.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">⚡</span><strong>Copy-Paste Code</strong><p>Every guide includes tested Arduino sketches with detailed inline comments.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">📡</span><strong>Modern ESP32 Techniques</strong><p>Wi-Fi, OLED, MQTT, IoT dashboards, OTA updates, and ESP-IDF patterns.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🚀</span><strong>Production Ready</strong><p>Patterns and practices you can take from prototype to shipped product.</p></div>
  </div>
</section>

<!-- ===== BOTTOM CTA ===== -->
<section class="portal-cta wrap reveal">
  <div class="portal-cta-inner">
    <div class="portal-cta-text">
      <h2>Start Building with ESP32 Today</h2>
      <p><?php echo esc_html( $guide_count ); ?> guides · <?php echo esc_html( $project_count ); ?>+ projects · wiring &amp; code included</p>
    </div>
    <div class="portal-cta-actions">
      <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Start Learning</a>
      <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Explore Projects</a>
    </div>
  </div>
</section>

</main>
<?php get_footer(); ?>
