<?php get_header(); ?>
<main>

<section class="category-banner">
  <div class="wrap category-banner-inner">
    <div>
      <p class="hero-eyebrow">Learning paths</p>
      <h1>ESP32 Guides &amp; Tutorials</h1>
      <p class="hero-sub">Structured learning from chip fundamentals to Arduino IDE setup, sensors, and connected systems.</p>
      <div class="hero-badges">
        <span class="badge badge-light">Phase 1: Foundations</span>
        <span class="badge badge-light">Phase 2: Development</span>
        <span class="badge badge-light">100% Free</span>
      </div>
    </div>
    <div class="category-banner-visual">
      <svg viewBox="0 0 64 64" fill="none"><path d="M14 14H34C40 14 44 18 44 24V50C40 46 36 44 30 44H14V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M50 14H30C24 14 20 18 20 24V50C24 46 28 44 34 44H50V14Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
    </div>
  </div>
</section>

<div class="wrap guide-index-page">

  <div class="section-head" style="margin-top: 2rem;">
    <div>
      <p class="section-eyebrow">All guides</p>
      <h2>Complete Guide Library</h2>
    </div>
  </div>

  <?php if ( have_posts() ) : ?>
  <div class="guide-index-grid">
    <?php while ( have_posts() ) : the_post();
        $phase    = get_post_meta( get_the_ID(), 'guide_phase', true ) ?: 'Guide';
        $read_min = get_post_meta( get_the_ID(), 'guide_read_time', true ) ?: '10 min';
    ?>
    <a class="guide-index-card" href="<?php the_permalink(); ?>">
      <div class="guide-card-badges">
        <span class="badge badge-cat"><?php echo esc_html( $phase ); ?></span>
        <span class="badge badge-time"><?php echo esc_html( $read_min ); ?> read</span>
      </div>
      <h3><?php the_title(); ?></h3>
      <p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 25 ) ); ?></p>
      <span class="btn btn-card">Read Guide<span aria-hidden="true">→</span></span>
    </a>
    <?php endwhile; ?>
  </div>

  <div class="section-actions">
    <?php the_posts_pagination( [ 'prev_text' => '← Prev', 'next_text' => 'Next →' ] ); ?>
  </div>

  <?php else : ?>
  <p>No guides published yet. Check back soon!</p>
  <?php endif; ?>

</div>
</main>
<?php get_footer(); ?>
