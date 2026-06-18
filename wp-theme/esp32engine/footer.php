<footer class="site-footer">
  <div class="wrap footer-grid">

    <div class="footer-brand">
      <strong>ESP32 Engine</strong>
      <p class="footer-tagline">Learn | Build | Innovate</p>
      <p>Premium ESP32 tutorials with wiring tables, Arduino code, and three difficulty levels for makers and engineers.</p>
      <div class="footer-social">
        <a href="https://github.com/abdulmubeen7876773-dotcom/esp32" rel="noopener noreferrer" target="_blank" aria-label="GitHub">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
        </a>
        <a href="https://www.youtube.com/@ESP32Engine" rel="noopener noreferrer" target="_blank" aria-label="YouTube">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        </a>
      </div>
    </div>

    <div class="footer-col">
      <h4>Explore</h4>
      <a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
      <a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>">Guides</a>
      <a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">All Projects</a>
      <?php if ( function_exists( 'wp_sitemap_get_provider' ) ) : ?>
      <a href="<?php echo esc_url( home_url( '/sitemap_index.xml' ) ); ?>">Sitemap</a>
      <?php endif; ?>
    </div>

    <div class="footer-col">
      <h4>Categories</h4>
      <?php
      $cats = get_terms( [ 'taxonomy' => 'project_category', 'number' => 5, 'hide_empty' => false ] );
      if ( $cats && ! is_wp_error( $cats ) ) :
          foreach ( $cats as $cat ) :
      ?>
      <a href="<?php echo esc_url( get_term_link( $cat ) ); ?>"><?php echo esc_html( $cat->name ); ?></a>
      <?php endforeach; else : ?>
      <a href="<?php echo esc_url( home_url( '/category/iot-projects/' ) ); ?>">IoT</a>
      <a href="<?php echo esc_url( home_url( '/category/esp32-cam/' ) ); ?>">ESP32-CAM</a>
      <a href="<?php echo esc_url( home_url( '/category/home-automation/' ) ); ?>">Smart Home</a>
      <a href="<?php echo esc_url( home_url( '/category/robotics/' ) ); ?>">Robotics</a>
      <a href="<?php echo esc_url( home_url( '/category/sensor-projects/' ) ); ?>">Sensor</a>
      <?php endif; ?>
    </div>

    <div class="footer-col">
      <h4>Company</h4>
      <a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About</a>
      <a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a>
      <a href="<?php echo esc_url( home_url( '/privacy/' ) ); ?>">Privacy Policy</a>
      <a href="<?php echo esc_url( home_url( '/terms/' ) ); ?>">Terms</a>
      <a href="<?php echo esc_url( home_url( '/disclaimer/' ) ); ?>">Disclaimer</a>
    </div>

  </div>
  <div class="wrap footer-bottom">
    <p>© <?php echo esc_html( gmdate( 'Y' ) ); ?> ESP32 Engine. All rights reserved.</p>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
