<?php get_header(); ?>
<main>

<!-- ═══ HERO BANNER ═══ -->
<section class="category-banner" aria-labelledby="guides-hero-heading">
  <div class="wrap category-banner-inner">
    <div>
      <p class="hero-eyebrow">Learning paths</p>
      <h1 id="guides-hero-heading">ESP32 Guides &amp; Tutorials</h1>
      <p class="hero-sub">Structured learning from chip fundamentals to Arduino IDE setup, sensors, and connected systems.</p>
      <div class="hero-badges">
        <span class="badge badge-light">Phase 1: Foundations</span>
        <span class="badge badge-light">Phase 2: Development</span>
        <span class="badge badge-light">100% Free</span>
      </div>
    </div>
    <div class="category-banner-visual" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none"><path d="M14 14H34C40 14 44 18 44 24V50C40 46 36 44 30 44H14V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M50 14H30C24 14 20 18 20 24V50C24 46 28 44 34 44H50V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
    </div>
  </div>
</section>

<div class="wrap guide-index-page">

  <?php
  /* Fetch all published guides */
  $all_guides = get_posts( [
      'post_type'      => 'esp32_guide',
      'posts_per_page' => -1,
      'orderby'        => 'menu_order',
      'order'          => 'ASC',
      'post_status'    => 'publish',
  ] );

  /* Group by phase */
  $grouped = [];
  foreach ( $all_guides as $g ) {
      $phase             = get_post_meta( $g->ID, 'guide_phase', true ) ?: 'Guides';
      $grouped[ $phase ][] = $g;
  }

  /* Collect unique phase names for filter tabs */
  $phase_names = array_keys( $grouped );
  ?>

  <!-- ═══ PHASE FILTER TABS ═══ -->
  <?php if ( count( $phase_names ) > 1 ) : ?>
  <div class="guide-phase-tabs" role="tablist" aria-label="Filter guides by phase">
    <button class="phase-tab is-active" data-phase-filter="" role="tab" aria-selected="true">All Guides
      <span style="font-weight:400;opacity:.7;margin-left:.3rem">(<?php echo count( $all_guides ); ?>)</span>
    </button>
    <?php foreach ( $phase_names as $pn ) : ?>
    <button class="phase-tab" data-phase-filter="<?php echo esc_attr( $pn ); ?>" role="tab" aria-selected="false">
      <?php echo esc_html( $pn ); ?>
      <span style="font-weight:400;opacity:.7;margin-left:.3rem">(<?php echo count( $grouped[ $pn ] ); ?>)</span>
    </button>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>

  <!-- ═══ GUIDES BY PHASE ═══ -->
  <?php if ( ! empty( $grouped ) ) : ?>

    <?php foreach ( $grouped as $phase_name => $guides ) : ?>
    <section class="guide-phase-section"
             id="phase-<?php echo esc_attr( sanitize_title( $phase_name ) ); ?>"
             data-phase-name="<?php echo esc_attr( $phase_name ); ?>">

      <div class="guide-phase-header">
        <span class="guide-phase-badge"><?php echo esc_html( $phase_name ); ?></span>
        <span class="guide-phase-count"><?php echo count( $guides ); ?> guides</span>
      </div>

      <div class="guide-index-grid">
        <?php foreach ( $guides as $guide ) :
          $read_min = get_post_meta( $guide->ID, 'guide_read_time', true ) ?: '10 min';
          $excerpt  = $guide->post_excerpt ?: wp_trim_words( wp_strip_all_tags( $guide->post_content ), 20 );
        ?>
        <a class="guide-index-card" href="<?php echo esc_url( get_permalink( $guide->ID ) ); ?>"
           data-phase="<?php echo esc_attr( $phase_name ); ?>">
          <div class="guide-card-badges">
            <span class="badge badge-cat"><?php echo esc_html( $phase_name ); ?></span>
            <span class="badge badge-time"><?php echo esc_html( $read_min ); ?> read</span>
          </div>
          <h3><?php echo esc_html( $guide->post_title ); ?></h3>
          <p><?php echo esc_html( wp_trim_words( $excerpt, 20 ) ); ?></p>
          <span class="btn btn-card">Read Guide <span aria-hidden="true">→</span></span>
        </a>
        <?php endforeach; ?>
      </div>

    </section>
    <?php endforeach; ?>

  <?php else : ?>
  <p style="padding:2rem 0;color:var(--text-muted)">No guides published yet — check back soon!</p>
  <?php endif; ?>

</div><!-- .wrap -->
</main>
<?php get_footer(); ?>
