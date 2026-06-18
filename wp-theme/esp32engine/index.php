<?php get_header(); ?>

<main>
  <div class="wrap" style="padding: 3rem 0;">
    <?php if ( have_posts() ) : ?>
      <div class="grid-projects">
        <?php while ( have_posts() ) : the_post(); ?>
          <article class="project-card-item">
            <div class="card-body">
              <h2 class="card-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
              <p class="card-desc"><?php the_excerpt(); ?></p>
            </div>
          </article>
        <?php endwhile; ?>
      </div>
      <?php the_posts_pagination(); ?>
    <?php else : ?>
      <p>Nothing found.</p>
    <?php endif; ?>
  </div>
</main>

<?php get_footer(); ?>
