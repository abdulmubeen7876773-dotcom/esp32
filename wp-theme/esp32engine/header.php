<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#6D28D9">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="icon" href="<?php echo esc_url( home_url( '/favicon.svg' ) ); ?>" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="<?php bloginfo( 'name' ); ?>" href="<?php echo esc_url( get_feed_link() ); ?>">
<script>document.documentElement.classList.add("js")</script>
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div class="site-nav-sticky" id="site-nav">
  <header class="site-header">
    <div class="wrap header-inner">

      <?php echo esp32_logo_html(); ?>

      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>

      <nav class="top-nav" aria-label="Main">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>"<?php echo is_front_page() ? ' class="active"' : ''; ?>>Home</a>
        <a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>"<?php echo is_post_type_archive( 'esp32_guide' ) || is_singular( 'esp32_guide' ) ? ' class="active"' : ''; ?>>Guides</a>
        <a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"<?php echo is_post_type_archive( 'esp32_project' ) || is_singular( 'esp32_project' ) || is_tax( 'project_category' ) ? ' class="active"' : ''; ?>>Projects</a>
        <a href="<?php echo esc_url( home_url( '/about/' ) ); ?>"<?php echo is_page( 'about' ) ? ' class="active"' : ''; ?>>About</a>
        <a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"<?php echo is_page( 'contact' ) ? ' class="active"' : ''; ?>>Contact</a>
      </nav>

      <div class="header-actions">
        <button type="button" class="icon-btn" id="search-open" aria-label="Search">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3" stroke-linecap="round"/></svg>
        </button>
        <a class="icon-btn" href="https://github.com/abdulmubeen7876773-dotcom/esp32" rel="noopener noreferrer" target="_blank" aria-label="GitHub">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
        </a>
        <a class="icon-btn" href="https://www.youtube.com/@ESP32Engine" rel="noopener noreferrer" target="_blank" aria-label="YouTube">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        </a>
      </div>

    </div>
  </header>
</div>

<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-overlay-backdrop" data-close-search></div>
  <div class="search-overlay-panel" role="dialog" aria-label="Search projects">
    <form class="search-overlay-form" action="<?php echo esc_url( home_url( '/projects/' ) ); ?>" method="get">
      <label class="visually-hidden" for="global-search">Search projects</label>
      <input id="global-search" name="s" type="search" placeholder="Search ESP32 projects, guides, categories…" autocomplete="off">
      <button type="submit" class="btn btn-primary">Search</button>
      <button type="button" class="search-close" data-close-search aria-label="Close search">×</button>
    </form>
  </div>
</div>
