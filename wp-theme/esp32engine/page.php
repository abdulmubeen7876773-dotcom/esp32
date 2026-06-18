<?php get_header(); ?>
<main>
<div class="wrap static-page" style="max-width: 860px; padding: 2rem 0 3rem;">

  <?php while ( have_posts() ) : the_post(); ?>

  <?php
  esp32_breadcrumb( [
      [ 'url' => home_url( '/' ), 'label' => 'Home' ],
      [ 'url' => get_permalink(), 'label' => get_the_title() ],
  ] );
  ?>

  <h1><?php the_title(); ?></h1>

  <div class="article-main" style="padding: 1.5rem 2rem; margin-top: 1rem;">
    <?php the_content(); ?>
  </div>

  <?php endwhile; ?>

</div>
</main>
<?php get_footer(); ?>
