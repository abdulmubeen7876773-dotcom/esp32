<?php
get_header();
while ( have_posts() ) : the_post();

$phase    = get_post_meta( get_the_ID(), 'guide_phase', true ) ?: 'Guide';
$read_min = get_post_meta( get_the_ID(), 'guide_read_time', true ) ?: '10 min';
$faqs     = get_post_meta( get_the_ID(), 'faq_items', true ) ?: [];
$related  = get_post_meta( get_the_ID(), '_related_guides', true ) ?: [];
?>
<main>

<div class="wrap">
  <?php
  esp32_breadcrumb( [
      [ 'url' => home_url( '/' ),        'label' => 'Home' ],
      [ 'url' => home_url( '/guides/' ),  'label' => 'Guides' ],
      [ 'url' => get_permalink(),         'label' => get_the_title() ],
  ] );
  ?>
</div>

<div class="wrap guide-docs-wrap">
  <div class="guide-docs-layout">

    <!-- ═══ LEFT SIDEBAR: TOC + Guide Info ═══ -->
    <aside class="guide-toc-sidebar" aria-label="Table of contents">

      <div class="toc-nav">
        <p class="toc-title">On this page</p>
        <div id="toc-list"></div>
      </div>

      <div class="toc-nav">
        <p class="toc-title">Guide info</p>
        <div class="guide-info-list">
          <div class="guide-info-row">
            <span class="guide-info-label">Phase</span>
            <span class="badge badge-cat" style="font-size:0.75rem"><?php echo esc_html( $phase ); ?></span>
          </div>
          <div class="guide-info-row">
            <span class="guide-info-label">Read time</span>
            <span class="guide-info-val"><?php echo esc_html( $read_min ); ?></span>
          </div>
          <div class="guide-info-row">
            <span class="guide-info-label">Updated</span>
            <span class="guide-info-val"><?php echo esc_html( get_the_modified_date( 'M j, Y' ) ); ?></span>
          </div>
          <?php if ( ! empty( $faqs ) ) : ?>
          <div class="guide-info-row">
            <span class="guide-info-label">FAQs</span>
            <span class="guide-info-val"><?php echo count( $faqs ); ?> answers</span>
          </div>
          <?php endif; ?>
        </div>
      </div>

      <a class="toc-back-link" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">← All Guides</a>

    </aside>

    <!-- ═══ MAIN COLUMN ═══ -->
    <div class="guide-main-col">

      <!-- Article header -->
      <header class="guide-article-header">
        <div class="article-badges">
          <span class="badge badge-cat"><?php echo esc_html( $phase ); ?></span>
          <span class="badge badge-time"><?php echo esc_html( $read_min ); ?> read</span>
        </div>
        <h1><?php the_title(); ?></h1>
        <?php if ( get_the_excerpt() ) : ?>
        <p class="article-lead"><?php echo esc_html( get_the_excerpt() ); ?></p>
        <?php endif; ?>
        <p class="meta">Updated <?php echo esc_html( get_the_modified_date( 'F j, Y' ) ); ?></p>
      </header>

      <!-- Article body — theme.js reads headings from here for TOC -->
      <article class="guide-article-body" id="article-body">
        <?php the_content(); ?>
      </article>

      <!-- ─── FAQ Section ─── -->
      <?php if ( ! empty( $faqs ) ) : ?>
      <section class="guide-faq-section" aria-labelledby="faq-heading">
        <h2 class="guide-faq-title" id="faq-heading">Frequently Asked Questions</h2>
        <div class="faq-list">
          <?php foreach ( $faqs as $faq ) :
            if ( ! is_array( $faq ) ) continue;
            $q = $faq['q'] ?? ( $faq[0] ?? '' );
            $a = $faq['a'] ?? ( $faq[1] ?? '' );
            if ( ! $q || ! $a ) continue;
          ?>
          <div class="faq-item">
            <button class="faq-q" aria-expanded="false">
              <span><?php echo esc_html( $q ); ?></span>
              <span class="plus" aria-hidden="true">+</span>
            </button>
            <div class="faq-a"><?php echo wp_kses_post( $a ); ?></div>
          </div>
          <?php endforeach; ?>
        </div>
      </section>
      <?php endif; ?>

      <!-- ─── Related Guides ─── -->
      <?php
      $related_posts = [];
      if ( ! empty( $related ) ) {
          $related_posts = get_posts( [
              'post_type'      => 'esp32_guide',
              'post_status'    => 'publish',
              'post_name__in'  => array_map( 'sanitize_title', (array) $related ),
              'posts_per_page' => 4,
              'orderby'        => 'title',
              'order'          => 'ASC',
          ] );
      }
      if ( ! empty( $related_posts ) ) :
      ?>
      <section class="guide-related-section" aria-labelledby="related-heading">
        <h2 id="related-heading">Related Guides</h2>
        <div class="related-guides-grid">
          <?php foreach ( $related_posts as $rp ) :
            $rphase = get_post_meta( $rp->ID, 'guide_phase', true ) ?: 'Guide';
            $rtime  = get_post_meta( $rp->ID, 'guide_read_time', true ) ?: '10 min';
          ?>
          <a class="related-guide-card" href="<?php echo esc_url( get_permalink( $rp->ID ) ); ?>">
            <div class="related-guide-badges">
              <span class="badge badge-cat"><?php echo esc_html( $rphase ); ?></span>
              <span class="badge badge-time"><?php echo esc_html( $rtime ); ?></span>
            </div>
            <strong><?php echo esc_html( $rp->post_title ); ?></strong>
            <span class="related-guide-arrow" aria-hidden="true">→</span>
          </a>
          <?php endforeach; ?>
        </div>
      </section>
      <?php endif; ?>

      <!-- Bottom nav -->
      <div class="guide-bottom-nav">
        <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">← All Guides</a>
        <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Explore Projects</a>
      </div>

    </div><!-- .guide-main-col -->
  </div><!-- .guide-docs-layout -->
</div><!-- .wrap -->

</main>
<?php endwhile; ?>
<?php get_footer(); ?>
