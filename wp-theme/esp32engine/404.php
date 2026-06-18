<?php get_header(); ?>
<main>
<div class="wrap" style="text-align:center; padding: 5rem 1rem;">
  <p style="font-size:5rem; margin:0;" aria-hidden="true">404</p>
  <h1>Page Not Found</h1>
  <p class="hero-sub" style="margin: 1rem auto 2rem; max-width: 34rem;">
    The page you're looking for doesn't exist or was moved. Try browsing our projects or guides instead.
  </p>
  <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
    <a class="btn btn-primary btn-lg" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">Browse Projects</a>
    <a class="btn btn-secondary btn-lg" href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Read Guides</a>
    <a class="btn btn-secondary btn-lg" href="<?php echo esc_url( home_url( '/' ) ); ?>">Go Home</a>
  </div>
</div>
</main>
<?php get_footer(); ?>
