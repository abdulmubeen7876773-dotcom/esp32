<?php
get_header();
$term       = get_queried_object();
$thumb_cls  = esp32_category_thumb_class( $term->slug );
$icon_svg   = esp32_category_icon( $term->slug );
?>
<main>

<section class="category-banner">
  <div class="wrap category-banner-inner">
    <div>
      <nav class="breadcrumb breadcrumb-light" aria-label="Breadcrumb">
        <ol>
          <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li>
          <li aria-current="page"><?php echo esc_html( $term->name ); ?></li>
        </ol>
      </nav>
      <p class="hero-eyebrow">Category</p>
      <h1><?php echo esc_html( $term->name ); ?> Projects</h1>
      <?php if ( $term->description ) : ?>
      <p class="hero-sub"><?php echo esc_html( $term->description ); ?></p>
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
    <p>No projects in this category yet.</p>
    <?php endif; ?>
  </div>

</div>
</main>
<?php get_footer(); ?>
