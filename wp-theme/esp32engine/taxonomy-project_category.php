<?php
get_header();
$term       = get_queried_object();
$thumb_cls  = esp32_category_thumb_class( $term->slug );
$icon_svg   = esp32_category_icon( $term->slug );

/* Category descriptions — hardcoded with fallback to term description */
$cat_intros = [
  'iot-projects'            => 'Build connected IoT projects that monitor, control, and report data wirelessly. From simple sensor nodes to full MQTT dashboards, ESP32 is the ideal platform for internet-of-things development.',
  'home-automation'         => 'Automate your home with ESP32-powered switches, relays, and sensors. Control lights, appliances, curtains, and security systems from your smartphone or voice assistant.',
  'sensor-projects'         => 'Interface ESP32 with temperature, humidity, pressure, gas, motion, ultrasonic, and dozens of other sensors. Every guide includes wiring diagrams and tested Arduino code.',
  'robotics'                => 'Build robots, robotic arms, and motor-controlled vehicles with ESP32. Learn PWM motor control, encoder feedback, servo driving, and wireless remote operation.',
  'esp32-cam'               => 'Work with the ESP32-CAM module for face detection, motion-triggered photography, live MJPEG streaming, and QR code scanning projects.',
  'led-projects'            => 'Control individual LEDs, PWM-dimmed strips, WS2812B NeoPixels, and HUB75 LED matrices. Create light effects, animations, and ambient lighting systems.',
  'agriculture'             => 'Build smart agriculture systems — soil moisture monitors, automated irrigation, greenhouse climate control, and livestock monitoring with ESP32.',
  'environmental'           => 'Monitor air quality, CO2 levels, UV index, noise pollution, and weather conditions. Log data to the cloud or display it on a local OLED screen.',
  'healthcare'              => 'ESP32 healthcare projects covering heart rate monitoring, temperature logging, pill dispensers, and patient alert systems.',
  'security-projects'       => 'Implement door access control, motion detection cameras, alarm systems, and RFID authentication with ESP32.',
  'energy-monitoring'       => 'Monitor household power consumption, solar output, battery state of charge, and energy usage trends with ESP32 and current sensors.',
  'industrial-automation'   => 'Apply ESP32 in industrial settings for PLC-style control, conveyor monitoring, predictive maintenance, and SCADA-lite dashboards.',
];
$cat_intro = $cat_intros[ $term->slug ] ?? ( $term->description ?: '' );

/* Related guides — search for guides mentioning the category name */
$related_guides = get_posts( [
    'post_type'      => 'esp32_guide',
    'post_status'    => 'publish',
    's'              => $term->name,
    'posts_per_page' => 4,
    'orderby'        => 'relevance',
] );

/* CollectionPage + BreadcrumbList schema */
$schema = [
    '@context' => 'https://schema.org',
    '@graph'   => [
        [
            '@type'       => 'CollectionPage',
            '@id'         => get_term_link( $term ) . '#collection',
            'name'        => $term->name . ' Projects — ESP32Engine',
            'description' => $cat_intro ?: $term->name . ' projects for ESP32',
            'url'         => get_term_link( $term ),
            'numberOfItems' => $term->count,
        ],
        [
            '@type'           => 'BreadcrumbList',
            'itemListElement' => [
                [ '@type' => 'ListItem', 'position' => 1, 'name' => 'Home',     'item' => home_url( '/' ) ],
                [ '@type' => 'ListItem', 'position' => 2, 'name' => 'Category', 'item' => home_url( '/category/' ) ],
                [ '@type' => 'ListItem', 'position' => 3, 'name' => $term->name, 'item' => get_term_link( $term ) ],
            ],
        ],
    ],
];
?>
<script type="application/ld+json"><?php echo wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ); ?></script>

<main>

<section class="category-banner">
  <div class="wrap category-banner-inner">
    <div>
      <?php
      esp32_breadcrumb( [
          [ 'url' => home_url( '/' ),         'label' => 'Home' ],
          [ 'url' => home_url( '/category/' ), 'label' => 'Category' ],
          [ 'url' => get_term_link( $term ),   'label' => $term->name ],
      ] );
      ?>
      <p class="hero-eyebrow">Category</p>
      <h1><?php echo esc_html( $term->name ); ?> Projects</h1>
      <?php if ( $cat_intro ) : ?>
      <p class="hero-sub"><?php echo esc_html( $cat_intro ); ?></p>
      <?php endif; ?>
      <div class="hero-badges">
        <span class="badge badge-light"><?php echo esc_html( $term->count ); ?> Projects</span>
        <span class="badge badge-light">3 Difficulty Levels</span>
        <span class="badge badge-light">Free Tutorials</span>
      </div>
    </div>
    <div class="category-banner-visual">
      <?php echo $icon_svg; ?>
    </div>
  </div>
</section>

<div class="wrap layout-with-sidebar">

  <!-- Category sidebar -->
  <aside class="sidebar-categories">
    <div class="sidebar-categories-inner">
      <p class="sidebar-title">All Categories</p>
      <nav class="sidebar-cat-nav">
        <?php
        $all_cats = get_terms( [ 'taxonomy' => 'project_category', 'hide_empty' => false ] );
        if ( $all_cats && ! is_wp_error( $all_cats ) ) :
            foreach ( $all_cats as $cat ) :
                $is_active = ( $cat->term_id === $term->term_id );
        ?>
        <a href="<?php echo esc_url( get_term_link( $cat ) ); ?>"
           class="<?php echo $is_active ? 'is-active' : ''; ?>">
          <span class="sidebar-cat-dot"></span>
          <?php echo esc_html( $cat->name ); ?>
        </a>
        <?php endforeach; endif; ?>
      </nav>

      <?php if ( ! empty( $related_guides ) ) : ?>
      <div class="sidebar-related-guides">
        <p class="sidebar-title">Related Guides</p>
        <?php foreach ( $related_guides as $g ) : ?>
        <a class="sidebar-guide-link" href="<?php echo esc_url( get_permalink( $g->ID ) ); ?>">
          <span class="sidebar-guide-title"><?php echo esc_html( $g->post_title ); ?></span>
          <span class="sidebar-guide-arrow">→</span>
        </a>
        <?php endforeach; ?>
      </div>
      <?php endif; ?>
    </div>
  </aside>

  <!-- Projects grid -->
  <div class="category-main">
    <div class="section-head">
      <div>
        <p class="section-eyebrow"><?php echo esc_html( $term->name ); ?></p>
        <h2>All <?php echo esc_html( $term->name ); ?> Projects</h2>
      </div>
    </div>

    <?php if ( have_posts() ) : ?>
    <div class="grid-projects">
      <?php while ( have_posts() ) : the_post();
          $icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: $thumb_cls;
          $icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
          $read_time  = get_post_meta( get_the_ID(), 'project_read_time', true ) ?: '8 min';
      ?>
      <article class="project-card-item">
        <div class="card-media card-thumb <?php echo esc_attr( $icon_class ); ?>">
          <?php echo $icon_svg ?: esp32_category_icon( $term->slug ); ?>
        </div>
        <div class="card-body">
          <div class="card-badges">
            <span class="badge badge-cat"><?php echo esc_html( $term->name ); ?></span>
            <span class="badge badge-beginner">Beginner</span>
            <span class="badge badge-intermediate">Intermediate</span>
            <span class="badge badge-advanced">Advanced</span>
            <span class="badge badge-time"><?php echo esc_html( $read_time ); ?> read</span>
          </div>
          <h2><?php the_title(); ?></h2>
          <p class="card-desc"><?php echo esc_html( wp_trim_words( get_the_excerpt(), 18 ) ); ?></p>
          <div class="card-footer">
            <a class="btn btn-card" href="<?php the_permalink(); ?>">Read Project<span aria-hidden="true">→</span></a>
          </div>
        </div>
      </article>
      <?php endwhile; ?>
    </div>

    <div class="section-actions">
      <?php the_posts_pagination( [ 'prev_text' => '← Prev', 'next_text' => 'Next →' ] ); ?>
    </div>

    <?php else : ?>
    <p class="cat-empty">No projects in this category yet. <a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Browse all projects →</a></p>
    <?php endif; ?>
  </div>

</div>
</main>
<?php get_footer(); ?>
