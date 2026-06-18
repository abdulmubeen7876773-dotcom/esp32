<?php
get_header();

// Gather all projects for client-side filter (mirrors current projects.js approach)
$all_projects = new WP_Query( [
    'post_type'      => 'esp32_project',
    'posts_per_page' => -1,
    'orderby'        => 'title',
    'order'          => 'ASC',
] );

$search_query = sanitize_text_field( get_search_query() ?: ( $_GET['s'] ?? '' ) );
?>
<main>

<div class="filters-sticky">
  <div class="wrap filters-bar">
    <div class="search-panel">
      <input type="search" id="project-search" placeholder="Search projects…" value="<?php echo esc_attr( $search_query ); ?>" autocomplete="off">
      <select id="filter-category" aria-label="Filter by category">
        <option value="">All Categories</option>
        <?php
        $cats = get_terms( [ 'taxonomy' => 'project_category', 'hide_empty' => false ] );
        if ( $cats && ! is_wp_error( $cats ) ) :
            foreach ( $cats as $cat ) :
        ?>
        <option value="<?php echo esc_attr( $cat->slug ); ?>"><?php echo esc_html( $cat->name ); ?></option>
        <?php endforeach; endif; ?>
      </select>
      <select id="filter-difficulty" aria-label="Filter by difficulty">
        <option value="">All Difficulties</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
    </div>
    <p class="filter-meta meta" id="filter-count"></p>
  </div>
</div>

<div class="wrap" style="padding: 2rem 0 3rem;">

  <div class="section-head">
    <div>
      <p class="section-eyebrow">All projects</p>
      <h1>ESP32 Projects</h1>
      <p class="section-sub">15 parent projects · 3 difficulty levels each · wiring, code, and troubleshooting included.</p>
    </div>
  </div>

  <div class="grid-projects" id="projects-grid">
    <?php while ( $all_projects->have_posts() ) : $all_projects->the_post();
        $icon_class = get_post_meta( get_the_ID(), 'project_icon_class', true ) ?: 't-default';
        $icon_svg   = get_post_meta( get_the_ID(), 'project_icon_svg', true );
        $read_time  = get_post_meta( get_the_ID(), 'project_read_time', true ) ?: '8 min';
        $cats       = get_the_terms( get_the_ID(), 'project_category' );
        $cat_name   = '';
        $cat_slug   = '';
        if ( $cats && ! is_wp_error( $cats ) ) {
            $cat_name = $cats[0]->name;
            $cat_slug = $cats[0]->slug;
        }
        $difficulties = get_the_terms( get_the_ID(), 'difficulty_level' );
        $diff_slugs   = [];
        if ( $difficulties && ! is_wp_error( $difficulties ) ) {
            $diff_slugs = wp_list_pluck( $difficulties, 'slug' );
        }
        if ( ! $diff_slugs ) $diff_slugs = [ 'beginner', 'intermediate', 'advanced' ];
    ?>
    <article class="project-card-item modern-card post-card"
             data-title="<?php echo esc_attr( strtolower( get_the_title() ) ); ?>"
             data-category="<?php echo esc_attr( $cat_slug ); ?>"
             data-difficulties="<?php echo esc_attr( implode( ',', $diff_slugs ) ); ?>">
      <div class="card-media card-thumb <?php echo esc_attr( $icon_class ); ?>">
        <?php echo $icon_svg ?: esp32_category_icon( $cat_slug ); ?>
      </div>
      <div class="card-body">
        <div class="card-badges">
          <?php if ( $cat_name ) : ?>
          <span class="badge badge-cat"><?php echo esc_html( $cat_name ); ?></span>
          <?php endif; ?>
          <?php foreach ( $diff_slugs as $d ) : ?>
          <span class="badge badge-<?php echo esc_attr( $d ); ?>"><?php echo esc_html( ucfirst( $d ) ); ?></span>
          <?php endforeach; ?>
          <span class="badge badge-time"><?php echo esc_html( $read_time ); ?> read</span>
        </div>
        <h2><?php the_title(); ?></h2>
        <p class="card-desc"><?php echo esc_html( wp_trim_words( get_the_excerpt(), 18 ) ); ?></p>
        <div class="card-footer">
          <a class="btn btn-card" href="<?php the_permalink(); ?>">Read Project<span aria-hidden="true">→</span></a>
        </div>
      </div>
    </article>
    <?php endwhile; wp_reset_postdata(); ?>
  </div>

  <div id="no-results" class="section-actions hidden">
    <p>No projects match your search. <button type="button" class="btn btn-secondary" id="clear-filters">Clear filters</button></p>
  </div>

</div>
</main>

<script>
(function () {
  var grid    = document.getElementById('projects-grid');
  var search  = document.getElementById('project-search');
  var catSel  = document.getElementById('filter-category');
  var diffSel = document.getElementById('filter-difficulty');
  var count   = document.getElementById('filter-count');
  var noRes   = document.getElementById('no-results');
  var clear   = document.getElementById('clear-filters');
  var cards   = Array.from(grid ? grid.querySelectorAll('.project-card-item') : []);

  function filter() {
    var q    = (search ? search.value.toLowerCase() : '');
    var cat  = catSel  ? catSel.value  : '';
    var diff = diffSel ? diffSel.value : '';
    var shown = 0;
    cards.forEach(function (card) {
      var title    = card.dataset.title   || '';
      var cardCat  = card.dataset.category || '';
      var cardDiff = (card.dataset.difficulties || '').split(',');
      var ok = (!q || title.includes(q))
            && (!cat  || cardCat === cat)
            && (!diff || cardDiff.includes(diff));
      card.classList.toggle('hidden', !ok);
      if (ok) shown++;
    });
    if (count) count.textContent = shown + ' project' + (shown !== 1 ? 's' : '');
    if (noRes) noRes.classList.toggle('hidden', shown > 0);
  }

  if (search)  search.addEventListener('input', filter);
  if (catSel)  catSel.addEventListener('change', filter);
  if (diffSel) diffSel.addEventListener('change', filter);
  if (clear) {
    clear.addEventListener('click', function () {
      if (search)  search.value  = '';
      if (catSel)  catSel.value  = '';
      if (diffSel) diffSel.value = '';
      filter();
    });
  }

  // Run once on load to apply any URL ?s= param
  filter();

  <?php if ( $search_query ) : ?>
  if (search) { search.value = <?php echo wp_json_encode( $search_query ); ?>; filter(); }
  <?php endif; ?>
})();
</script>

<?php get_footer(); ?>
