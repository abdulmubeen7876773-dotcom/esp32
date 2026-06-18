<?php
get_header();
while ( have_posts() ) : the_post();
$phase    = get_post_meta( get_the_ID(), 'guide_phase', true ) ?: 'Guide';
$read_min = get_post_meta( get_the_ID(), 'guide_read_time', true ) ?: '10 min';
?>
<main>
<div class="wrap guide-page" style="padding: 2rem 0 3rem; max-width: 860px;">

  <?php
  esp32_breadcrumb( [
      [ 'url' => home_url( '/' ), 'label' => 'Home' ],
      [ 'url' => home_url( '/guides/' ), 'label' => 'Guides' ],
      [ 'url' => get_permalink(), 'label' => get_the_title() ],
  ] );
  ?>

  <header style="margin-bottom: 2rem;">
    <div class="article-badges" style="margin-bottom: 0.75rem;">
      <span class="badge badge-cat"><?php echo esc_html( $phase ); ?></span>
      <span class="badge badge-time"><?php echo esc_html( $read_min ); ?> read</span>
    </div>
    <h1><?php the_title(); ?></h1>
    <p class="article-lead"><?php echo esc_html( get_the_excerpt() ); ?></p>
    <p class="meta">Published <?php echo esc_html( get_the_date() ); ?> · Updated <?php echo esc_html( get_the_modified_date() ); ?></p>
  </header>

  <div class="article-main" style="padding: 1.5rem 2rem;">
    <?php the_content(); ?>
  </div>

  <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
    <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">← All Guides</a>
    <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>" style="margin-left: 0.5rem;">Explore Projects</a>
  </div>

</div>
</main>
<?php endwhile; ?>
<?php get_footer(); ?>
