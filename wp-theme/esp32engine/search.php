<?php
get_header();
$query = get_search_query();
?>
<main>
<div class="wrap" style="padding: 2rem 0 3rem;">

  <div class="section-head">
    <div>
      <p class="section-eyebrow">Search results</p>
      <h1>Results for "<?php echo esc_html( $query ); ?>"</h1>
      <?php if ( have_posts() ) : ?>
      <p class="section-sub"><?php echo esc_html( $wp_query->found_posts ); ?> result<?php echo $wp_query->found_posts !== 1 ? 's' : ''; ?> found.</p>
      <?php endif; ?>
    </div>
  </div>

  <?php if ( have_posts() ) : ?>
  <div class="grid-projects">
    <?php while ( have_posts() ) : the_post();
        $pt         = get_post_type();
        $icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: 't-default';
        $icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
        $cats       = get_the_terms( get_the_ID(), 'project_category' );
        $cat_name   = ( $cats && ! is_wp_error( $cats ) ) ? $cats[0]->name : '';
        $cat_slug   = ( $cats && ! is_wp_error( $cats ) ) ? $cats[0]->slug : '';
    ?>
    <article class="project-card-item">
      <?php if ( $pt === 'esp32_project' || $pt === 'esp32_guide' ) : ?>
      <div class="card-media card-thumb <?php echo esc_attr( $icon_class ); ?>">
        <?php echo $icon_svg ?: esp32_category_icon( $cat_slug ); ?>
      </div>
      <?php endif; ?>
      <div class="card-body">
        <div class="card-badges">
          <?php if ( $cat_name ) : ?><span class="badge badge-cat"><?php echo esc_html( $cat_name ); ?></span><?php endif; ?>
          <span class="badge badge-time"><?php echo esc_html( $pt === 'esp32_guide' ? 'Guide' : 'Project' ); ?></span>
        </div>
        <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
        <p class="card-desc"><?php echo esc_html( wp_trim_words( get_the_excerpt(), 18 ) ); ?></p>
        <div class="card-footer">
          <a class="btn btn-card" href="<?php the_permalink(); ?>">Read More<span aria-hidden="true">→</span></a>
        </div>
      </div>
    </article>
    <?php endwhile; ?>
  </div>
  <div class="section-actions"><?php the_posts_pagination(); ?></div>

  <?php else : ?>
  <div style="text-align:center; padding: 3rem 0;">
    <p>No results for "<?php echo esc_html( $query ); ?>". Try a different term.</p>
    <div style="margin-top:1rem; display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
      <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Browse All Projects</a>
      <a class="btn btn-secondary" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Browse Guides</a>
    </div>
  </div>
  <?php endif; ?>

</div>
</main>
<?php get_footer(); ?>
