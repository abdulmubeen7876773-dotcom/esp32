<?php get_header(); ?>
<main>

<!-- ===== HERO ===== -->
<section class="hero-home reveal" aria-labelledby="hero-heading">
  <div class="wrap hero-home-inner">
    <div class="hero-home-content">
      <p class="hero-eyebrow">Learn | Build | Innovate</p>
      <h1 id="hero-heading">The Premium ESP32 Learning Platform</h1>
      <p class="hero-sub">Master ESP32, IoT, embedded systems, and Arduino with step-by-step guides, wiring diagrams, and production-ready project tutorials.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Explore Projects</a>
        <a class="btn btn-secondary btn-lg" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Start Learning</a>
      </div>
      <div class="hero-stat-row">
        <div class="hero-stat-pill"><strong>15+</strong><span>Parent Projects</span></div>
        <div class="hero-stat-pill"><strong>45+</strong><span>Difficulty Levels</span></div>
        <div class="hero-stat-pill"><strong>10+</strong><span>Categories</span></div>
        <div class="hero-stat-pill"><strong>100%</strong><span>Free Learning</span></div>
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

<!-- ===== GUIDES ===== -->
<section class="section-premium wrap reveal" id="guides">
  <div class="section-head">
    <div>
      <p class="section-eyebrow">Learning paths</p>
      <h2>ESP32 Guides &amp; Tutorials</h2>
      <p class="section-sub">Structured paths from chip fundamentals to Arduino IDE setup and beyond.</p>
    </div>
    <a class="btn btn-secondary btn-sm" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">All guides</a>
  </div>

  <div class="guide-tracks-grid">
    <a class="guide-track-card" href="<?php echo esc_url( home_url( '/guides/what-is-esp32/' ) ); ?>">
      <span class="guide-track-badge">Phase 1</span>
      <h3>Beginner Guides</h3>
      <p>Foundations, chip basics, and your first breadboard builds.</p>
      <span class="btn btn-card">Browse<span aria-hidden="true">→</span></span>
    </a>
    <a class="guide-track-card" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">
      <span class="guide-track-badge">Phase 2</span>
      <h3>Intermediate Guides</h3>
      <p>OLED feedback, calibration, and multi-sensor workflows.</p>
      <span class="btn btn-card">Browse<span aria-hidden="true">→</span></span>
    </a>
    <a class="guide-track-card" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">
      <span class="guide-track-badge">Coming soon</span>
      <h3>ESP-IDF Tutorials</h3>
      <p>Native SDK concepts for production firmware.</p>
      <span class="btn btn-card">Browse<span aria-hidden="true">→</span></span>
    </a>
    <a class="guide-track-card" href="<?php echo esc_url( home_url( '/guides/installing-arduino-ide-esp32/' ) ); ?>">
      <span class="guide-track-badge">Setup</span>
      <h3>Arduino Tutorials</h3>
      <p>IDE setup, board packages, and sketch workflows.</p>
      <span class="btn btn-card">Browse<span aria-hidden="true">→</span></span>
    </a>
  </div>

  <?php
  $guides = new WP_Query( [
      'post_type'      => 'esp32_guide',
      'posts_per_page' => 2,
      'orderby'        => 'menu_order',
      'order'          => 'ASC',
  ] );
  if ( $guides->have_posts() ) :
  ?>
  <div class="guide-home-grid">
    <?php while ( $guides->have_posts() ) : $guides->the_post();
        $phase = get_post_meta( get_the_ID(), 'guide_phase', true ) ?: 'Guide';
    ?>
    <a class="guide-home-card" href="<?php the_permalink(); ?>">
      <div class="guide-card-badges"><span class="badge badge-cat"><?php echo esc_html( $phase ); ?></span></div>
      <h3><?php the_title(); ?></h3>
      <p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 20 ) ); ?></p>
      <span class="btn btn-card">Read Guide<span aria-hidden="true">→</span></span>
    </a>
    <?php endwhile; wp_reset_postdata(); ?>
  </div>
  <?php endif; ?>
</section>

<!-- ===== FEATURED PROJECTS CAROUSEL ===== -->
<section class="section-premium wrap reveal" id="featured">
  <div class="section-head">
    <div>
      <p class="section-eyebrow">Editor's pick</p>
      <h2>Featured Projects</h2>
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

<!-- ===== LATEST TUTORIALS + CATEGORIES ===== -->
<section class="portal-section wrap reveal portal-duo" id="latest">
  <div class="portal-duo-col portal-latest">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Fresh guides</p>
      <h2>Latest Tutorials</h2>
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
      <?php endforeach; else : ?>
      <a class="pop-cat tech-cat-card" href="<?php echo esc_url( home_url( '/category/iot-projects/' ) ); ?>"><span class="pop-cat-icon t-iot"><?php echo esp32_category_icon( 'iot-projects' ); ?></span><span>IoT</span></a>
      <a class="pop-cat tech-cat-card" href="<?php echo esc_url( home_url( '/category/home-automation/' ) ); ?>"><span class="pop-cat-icon t-home"><?php echo esp32_category_icon( 'home-automation' ); ?></span><span>Automation</span></a>
      <a class="pop-cat tech-cat-card" href="<?php echo esc_url( home_url( '/category/sensor-projects/' ) ); ?>"><span class="pop-cat-icon t-sensor"><?php echo esp32_category_icon( 'sensor-projects' ); ?></span><span>Sensors</span></a>
      <a class="pop-cat tech-cat-card" href="<?php echo esc_url( home_url( '/category/robotics/' ) ); ?>"><span class="pop-cat-icon t-robot"><?php echo esp32_category_icon( 'robotics' ); ?></span><span>Robotics</span></a>
      <?php endif; ?>
    </div>
  </div>
</section>

<!-- ===== ROADMAP + STATS ===== -->
<section class="portal-section wrap reveal portal-duo portal-roadmap-stats" id="roadmap">
  <div class="portal-duo-col roadmap-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Structured learning</p>
      <h2>ESP32 Learning Roadmap</h2>
    </div>
    <div class="roadmap-track roadmap-track-premium">
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">01</span><div><strong class="badge badge-beginner">Beginner</strong><span>Sensors, serial output, threshold logic</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">02</span><div><strong class="badge badge-intermediate">Intermediate</strong><span>OLED, calibration, manual/auto modes</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">03</span><div><strong class="badge badge-advanced">Advanced</strong><span>Wi-Fi dashboards, alerts, logging</span></div></div>
    </div>
    <a class="roadmap-link" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Browse all 15 projects →</a>
  </div>
  <div class="portal-duo-col stats-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Library at a glance</p>
      <h2>Project Statistics</h2>
    </div>
    <div class="portal-stats-grid">
      <div class="portal-stat"><strong>15+</strong><span>Parent Projects</span></div>
      <div class="portal-stat"><strong>45+</strong><span>Difficulty Levels</span></div>
      <div class="portal-stat"><strong>10+</strong><span>Categories</span></div>
      <div class="portal-stat"><strong>100%</strong><span>Free Learning</span></div>
    </div>
    <div class="stats-highlights">
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⚡</span><span>Wiring tables on every guide</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⌨</span><span>Copy-paste Arduino sketches</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">📱</span><span>Mobile-friendly layouts</span></div>
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
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🎯</span><strong>Beginner Friendly</strong><p>Start with breadboard builds and clear wiring tables.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🔧</span><strong>Real Hardware Projects</strong><p>Every guide maps to sensors, relays, and ESP32 pins.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">📊</span><strong>Multiple Difficulty Levels</strong><p>Beginner, Intermediate, and Advanced on every project.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">⚡</span><strong>Practical Learning</strong><p>Copy-paste Arduino code with troubleshooting steps.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">📡</span><strong>Modern ESP32 Techniques</strong><p>Wi-Fi, OLED, MQTT, and IoT dashboards.</p></div>
    <div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">🚀</span><strong>Production Ready Concepts</strong><p>Patterns you can ship beyond the prototype stage.</p></div>
  </div>
</section>

<!-- ===== COMMUNITY PANEL ===== -->
<section class="portal-section wrap reveal" id="community">
  <div class="community-panel">
    <div class="community-panel-icon" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none" width="40" height="40"><circle cx="32" cy="22" r="8" stroke="currentColor" stroke-width="2"/><path d="M12 52c0-11 9-18 20-18s20 7 20 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </div>
    <div class="community-panel-body">
      <p class="section-eyebrow">Stay connected</p>
      <h2>Newsletter &amp; Community</h2>
      <p class="community-lead">Get project updates, share builds, and connect with makers learning ESP32.</p>
    </div>
    <div class="community-panel-actions">
      <a class="btn btn-primary" href="https://github.com/abdulmubeen7876773-dotcom/esp32" rel="noopener noreferrer" target="_blank">Star on GitHub</a>
      <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Join Discussion</a>
    </div>
  </div>
</section>

<!-- ===== BOTTOM CTA ===== -->
<section class="portal-cta wrap reveal">
  <div class="portal-cta-inner">
    <div class="portal-cta-text">
      <h2>Start Building with ESP32 Today</h2>
      <p>15 parent projects · 3 difficulty levels · wiring &amp; code included</p>
    </div>
    <div class="portal-cta-actions">
      <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Explore Projects</a>
      <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/category/iot-projects/' ) ); ?>">Browse IoT</a>
    </div>
  </div>
</section>

</main>
<?php get_footer(); ?>
