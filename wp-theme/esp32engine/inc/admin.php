<?php
defined( 'ABSPATH' ) || exit;

/* ============================================================
   Admin enqueue
   ============================================================ */
add_action( 'admin_enqueue_scripts', function ( string $hook ) {
    if ( ! in_array( $hook, [ 'post.php', 'post-new.php' ], true ) ) return;
    $screen = get_current_screen();
    if ( ! $screen || ! in_array( $screen->post_type, [ 'esp32_project', 'esp32_guide' ], true ) ) return;

    wp_enqueue_style(
        'esp32-admin',
        get_template_directory_uri() . '/assets/css/admin.css',
        [],
        '20260619'
    );
    wp_enqueue_script(
        'esp32-admin',
        get_template_directory_uri() . '/assets/js/admin.js',
        [ 'jquery' ],
        '20260619',
        true
    );
} );

/* ============================================================
   Admin columns — Projects
   ============================================================ */
add_filter( 'manage_esp32_project_posts_columns', function ( array $cols ): array {
    unset( $cols['date'] );
    return array_merge( $cols, [
        'thumb_class' => 'Icon',
        'category'    => 'Category',
        'read_time'   => 'Read Time',
        'difficulty'  => 'Levels',
        'date'        => 'Published',
    ] );
} );

add_action( 'manage_esp32_project_posts_custom_column', function ( string $col, int $post_id ): void {
    switch ( $col ) {
        case 'thumb_class':
            $cls = get_post_meta( $post_id, 'project_icon_class', true ) ?: 't-default';
            echo '<span class="esp32-admin-dot ' . esc_attr( $cls ) . '" title="' . esc_attr( $cls ) . '">' . esc_html( str_replace( 't-', '', $cls ) ) . '</span>';
            break;
        case 'category':
            $terms = get_the_terms( $post_id, 'project_category' );
            echo $terms && ! is_wp_error( $terms ) ? esc_html( $terms[0]->name ) : '—';
            break;
        case 'read_time':
            echo esc_html( get_post_meta( $post_id, 'project_read_time', true ) ?: '—' );
            break;
        case 'difficulty':
            foreach ( [ 'beginner', 'intermediate', 'advanced' ] as $l ) {
                if ( get_post_meta( $post_id, $l . '_overview', true ) ) {
                    echo '<span class="esp32-level-badge esp32-level-' . esc_attr( $l ) . '">' . esc_html( ucfirst( $l[0] ) ) . '</span> ';
                }
            }
            break;
    }
}, 10, 2 );

/* ============================================================
   Admin columns — Guides
   ============================================================ */
add_filter( 'manage_esp32_guide_posts_columns', function ( array $cols ): array {
    unset( $cols['date'] );
    return array_merge( $cols, [
        'guide_phase'     => 'Phase',
        'guide_read_time' => 'Read Time',
        'date'            => 'Published',
    ] );
} );

add_action( 'manage_esp32_guide_posts_custom_column', function ( string $col, int $post_id ): void {
    if ( $col === 'guide_phase' )     echo esc_html( get_post_meta( $post_id, 'guide_phase', true ) ?: '—' );
    if ( $col === 'guide_read_time' ) echo esc_html( get_post_meta( $post_id, 'guide_read_time', true ) ?: '—' );
}, 10, 2 );

/* ============================================================
   Register meta boxes
   ============================================================ */
add_action( 'add_meta_boxes', function (): void {
    add_meta_box(
        'esp32_project_basics',
        'Project Details',
        'esp32_mb_project_basics',
        'esp32_project',
        'side',
        'high'
    );
    add_meta_box(
        'esp32_project_content',
        'Difficulty Level Content — Beginner | Intermediate | Advanced',
        'esp32_mb_project_content',
        'esp32_project',
        'normal',
        'high'
    );
    add_meta_box(
        'esp32_guide_details',
        'Guide Details',
        'esp32_mb_guide_details',
        'esp32_guide',
        'side',
        'high'
    );
} );

/* ============================================================
   Project basics sidebar metabox
   ============================================================ */
function esp32_mb_project_basics( WP_Post $post ): void {
    wp_nonce_field( 'esp32_save_project', 'esp32_project_nonce' );

    $icon_class  = get_post_meta( $post->ID, 'project_icon_class', true );
    $lead        = get_post_meta( $post->ID, 'project_lead', true );
    $read_time   = get_post_meta( $post->ID, 'project_read_time', true );
    $deps        = get_post_meta( $post->ID, 'project_dependencies', true );
    $is_featured = get_post_meta( $post->ID, 'is_featured', true );

    $icon_options = [
        't-iot'         => 'IoT Projects',
        't-home'        => 'Home Automation',
        't-cam'         => 'ESP32-CAM',
        't-robot'       => 'Robotics',
        't-sensor'      => 'Sensor Projects',
        't-ai'          => 'AI Projects',
        't-security'    => 'Security',
        't-led'         => 'LED Projects',
        't-agriculture' => 'Agriculture / Environmental',
        't-default'     => 'Default / Other',
    ];
    ?>
    <div class="esp32-side-meta">

      <label class="esp32-label">Icon / Theme Color</label>
      <select name="project_icon_class" class="widefat">
        <?php foreach ( $icon_options as $val => $label ) : ?>
        <option value="<?php echo esc_attr( $val ); ?>"<?php selected( $icon_class, $val ); ?>><?php echo esc_html( $label ); ?></option>
        <?php endforeach; ?>
      </select>

      <label class="esp32-label">Lead / Intro Sentence</label>
      <textarea name="project_lead" class="widefat" rows="3" placeholder="One-sentence project intro for hero and cards."><?php echo esc_textarea( $lead ); ?></textarea>

      <label class="esp32-label">Read Time (e.g. 8 min)</label>
      <input type="text" name="project_read_time" class="widefat" value="<?php echo esc_attr( $read_time ); ?>" placeholder="8 min">

      <label class="esp32-label">Key Components Summary</label>
      <input type="text" name="project_dependencies" class="widefat" value="<?php echo esc_attr( $deps ); ?>" placeholder="ESP32 DevKit, DHT22, OLED display">

      <label class="esp32-label esp32-checkbox-label">
        <input type="checkbox" name="is_featured" value="1"<?php checked( $is_featured, '1' ); ?>>
        Feature on homepage carousel
      </label>

    </div>
    <?php
}

/* ============================================================
   Project content tabbed metabox
   ============================================================ */
function esp32_mb_project_content( WP_Post $post ): void {
    $levels = [ 'beginner', 'intermediate', 'advanced' ];
    ?>
    <div class="esp32-tabs-wrap" id="esp32-difficulty-tabs">
      <nav class="esp32-tab-nav" role="tablist">
        <?php foreach ( $levels as $i => $level ) : ?>
        <button type="button"
                class="esp32-tab-btn<?php echo $i === 0 ? ' is-active' : ''; ?>"
                data-target="esp32-panel-<?php echo esc_attr( $level ); ?>"
                role="tab"
                aria-selected="<?php echo $i === 0 ? 'true' : 'false'; ?>">
          <?php echo esc_html( ucfirst( $level ) ); ?>
        </button>
        <?php endforeach; ?>
      </nav>

      <?php foreach ( $levels as $i => $level ) :
          $prefix          = $level;
          $overview        = get_post_meta( $post->ID, $prefix . '_overview', true );
          $components_raw  = get_post_meta( $post->ID, $prefix . '_components', true );
          $components      = is_array( $components_raw ) ? $components_raw : [];
          $wiring_raw      = get_post_meta( $post->ID, $prefix . '_wiring', true );
          $wiring          = is_array( $wiring_raw ) ? $wiring_raw : [];
          $code_filename   = get_post_meta( $post->ID, $prefix . '_code_filename', true );
          $code            = get_post_meta( $post->ID, $prefix . '_code', true );
          $how_raw         = get_post_meta( $post->ID, $prefix . '_how_it_works', true );
          $how_steps       = is_array( $how_raw ) ? $how_raw : [];
          $apps_raw        = get_post_meta( $post->ID, $prefix . '_applications', true );
          $apps            = is_array( $apps_raw ) ? $apps_raw : [];
          $trouble_raw     = get_post_meta( $post->ID, $prefix . '_troubleshooting', true );
          $troubleshooting = is_array( $trouble_raw ) ? $trouble_raw : [];
          $upgrades_raw    = get_post_meta( $post->ID, $prefix . '_upgrades', true );
          $upgrades        = is_array( $upgrades_raw ) ? $upgrades_raw : [];
          $faq_raw         = get_post_meta( $post->ID, $prefix . '_faq', true );
          $faq             = is_array( $faq_raw ) ? $faq_raw : [];
      ?>
      <div class="esp32-tab-panel<?php echo $i === 0 ? ' is-active' : ''; ?>"
           id="esp32-panel-<?php echo esc_attr( $level ); ?>"
           role="tabpanel">

        <!-- Overview -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Overview <span class="esp32-hint">(HTML allowed)</span></label>
          <textarea name="<?php echo esc_attr( $prefix ); ?>_overview"
                    class="widefat esp32-code-area"
                    rows="5"
                    placeholder="Describe what this difficulty level builds and why."><?php echo esc_textarea( $overview ); ?></textarea>
        </div>

        <!-- Components -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Components List</label>
          <div class="esp32-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_components" data-type="simple">
            <?php foreach ( $components as $j => $comp ) :
                $val = is_array( $comp ) ? ( $comp['name'] ?? ( $comp[0] ?? '' ) ) : $comp; ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_components[]"
                     value="<?php echo esc_attr( $val ); ?>" placeholder="e.g. MQ135 Gas Sensor" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $components ) : ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_components[]" placeholder="e.g. ESP32 DevKit" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_components">+ Add Component</button>
        </div>

        <!-- Wiring Table -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Wiring Table</label>
          <div class="esp32-repeater esp32-wiring-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_wiring" data-type="wiring">
            <div class="esp32-row esp32-row-header">
              <span>Component Pin</span><span>ESP32 Pin</span><span>Notes</span><span></span>
            </div>
            <?php foreach ( $wiring as $row ) :
                if ( ! is_array( $row ) ) continue;
                $pin   = $row['component_pin'] ?? $row[0] ?? '';
                $esp   = $row['esp32_pin']     ?? $row[1] ?? '';
                $notes = $row['notes']          ?? $row[2] ?? '';
            ?>
            <div class="esp32-row esp32-wiring-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_pin[]"   value="<?php echo esc_attr( $pin ); ?>"   placeholder="VCC">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_esp[]"   value="<?php echo esc_attr( $esp ); ?>"   placeholder="3.3V">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_notes[]" value="<?php echo esc_attr( $notes ); ?>" placeholder="Power supply">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $wiring ) : ?>
            <div class="esp32-row esp32-wiring-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_pin[]"   placeholder="VCC">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_esp[]"   placeholder="3.3V">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_wiring_notes[]" placeholder="Power supply">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_wiring" data-type="wiring">+ Add Wiring Row</button>
        </div>

        <!-- Arduino Code -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Arduino Code Filename</label>
          <input type="text" name="<?php echo esc_attr( $prefix ); ?>_code_filename"
                 class="widefat" value="<?php echo esc_attr( $code_filename ); ?>"
                 placeholder="<?php echo esc_attr( $level ); ?>_project.ino">
          <label class="esp32-section-label" style="margin-top:10px">Arduino Code</label>
          <textarea name="<?php echo esc_attr( $prefix ); ?>_code"
                    class="widefat esp32-code-area esp32-code-arduino"
                    rows="12"
                    placeholder="Paste full .ino sketch here..."><?php echo esc_textarea( $code ); ?></textarea>
        </div>

        <!-- How It Works -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">How It Works (steps)</label>
          <div class="esp32-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_how_it_works" data-type="simple">
            <?php foreach ( $how_steps as $step ) :
                $text = is_array( $step ) ? ( $step['text'] ?? ( $step[0] ?? '' ) ) : $step; ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_how_it_works[]"
                     value="<?php echo esc_attr( $text ); ?>" placeholder="Describe one step…" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $how_steps ) : ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_how_it_works[]" placeholder="The ESP32 reads the sensor on GPIO34." class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_how_it_works">+ Add Step</button>
        </div>

        <!-- Applications -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Real-World Applications</label>
          <div class="esp32-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_applications" data-type="simple">
            <?php foreach ( $apps as $app ) :
                $text = is_array( $app ) ? ( $app[0] ?? '' ) : $app; ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_applications[]"
                     value="<?php echo esc_attr( $text ); ?>" placeholder="Greenhouse monitoring" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $apps ) : ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_applications[]" placeholder="Smart home integration" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_applications">+ Add Application</button>
        </div>

        <!-- Troubleshooting -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Troubleshooting (Problem → Solution pairs)</label>
          <div class="esp32-repeater esp32-pair-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_troubleshooting" data-type="pair">
            <?php foreach ( $troubleshooting as $item ) :
                $prob = is_array( $item ) ? ( $item['problem'] ?? $item[0] ?? '' ) : $item;
                $sol  = is_array( $item ) ? ( $item['solution'] ?? $item[1] ?? '' ) : '';
            ?>
            <div class="esp32-row esp32-pair-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_troubleshooting_problem[]"
                     value="<?php echo esc_attr( $prob ); ?>" placeholder="Problem…" class="widefat">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_troubleshooting_solution[]"
                     value="<?php echo esc_attr( $sol ); ?>" placeholder="Solution…" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $troubleshooting ) : ?>
            <div class="esp32-row esp32-pair-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_troubleshooting_problem[]" placeholder="Sensor reads 0 always">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_troubleshooting_solution[]" placeholder="Check power wiring on breadboard">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_troubleshooting" data-type="pair">+ Add Issue</button>
        </div>

        <!-- Upgrades -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">Possible Upgrades</label>
          <div class="esp32-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_upgrades" data-type="simple">
            <?php foreach ( $upgrades as $up ) :
                $text = is_array( $up ) ? ( $up[0] ?? '' ) : $up; ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_upgrades[]"
                     value="<?php echo esc_attr( $text ); ?>" placeholder="Add OLED display…" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $upgrades ) : ?>
            <div class="esp32-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_upgrades[]" placeholder="Add Bluetooth notifications" class="widefat">
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_upgrades">+ Add Upgrade</button>
        </div>

        <!-- FAQ -->
        <div class="esp32-field-group">
          <label class="esp32-section-label">FAQ (Question → Answer pairs)</label>
          <div class="esp32-repeater esp32-pair-repeater" data-prefix="<?php echo esc_attr( $prefix ); ?>_faq" data-type="pair">
            <?php foreach ( $faq as $item ) :
                $q = is_array( $item ) ? ( $item['question'] ?? $item[0] ?? '' ) : $item;
                $a = is_array( $item ) ? ( $item['answer']   ?? $item[1] ?? '' ) : '';
            ?>
            <div class="esp32-row esp32-pair-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_faq_question[]"
                     value="<?php echo esc_attr( $q ); ?>" placeholder="Question…" class="widefat">
              <textarea name="<?php echo esc_attr( $prefix ); ?>_faq_answer[]"
                        rows="2" class="widefat" placeholder="Answer…"><?php echo esc_textarea( $a ); ?></textarea>
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endforeach; ?>
            <?php if ( ! $faq ) : ?>
            <div class="esp32-row esp32-pair-row">
              <input type="text" name="<?php echo esc_attr( $prefix ); ?>_faq_question[]" placeholder="What hardware do I need?" class="widefat">
              <textarea name="<?php echo esc_attr( $prefix ); ?>_faq_answer[]" rows="2" class="widefat" placeholder="You need an ESP32 DevKit, …"></textarea>
              <button type="button" class="esp32-remove-row button">–</button>
            </div>
            <?php endif; ?>
          </div>
          <button type="button" class="esp32-add-row button button-secondary" data-target="<?php echo esc_attr( $prefix ); ?>_faq" data-type="pair">+ Add FAQ Item</button>
        </div>

      </div><!-- /.esp32-tab-panel -->
      <?php endforeach; ?>
    </div><!-- /.esp32-tabs-wrap -->
    <?php
}

/* ============================================================
   Guide details metabox
   ============================================================ */
function esp32_mb_guide_details( WP_Post $post ): void {
    wp_nonce_field( 'esp32_save_guide', 'esp32_guide_nonce' );

    $phase     = get_post_meta( $post->ID, 'guide_phase', true );
    $read_time = get_post_meta( $post->ID, 'guide_read_time', true );
    ?>
    <div class="esp32-side-meta">
      <label class="esp32-label">Learning Phase</label>
      <input type="text" name="guide_phase" class="widefat"
             value="<?php echo esc_attr( $phase ); ?>"
             placeholder="e.g. Phase 1: Getting Started">

      <label class="esp32-label">Read Time</label>
      <input type="text" name="guide_read_time" class="widefat"
             value="<?php echo esc_attr( $read_time ); ?>"
             placeholder="e.g. 15 min">
    </div>
    <?php
}

/* ============================================================
   Save project meta
   ============================================================ */
add_action( 'save_post_esp32_project', function ( int $post_id ): void {
    if (
        ! isset( $_POST['esp32_project_nonce'] ) ||
        ! wp_verify_nonce( $_POST['esp32_project_nonce'], 'esp32_save_project' ) ||
        defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ||
        ! current_user_can( 'edit_post', $post_id )
    ) return;

    // Simple scalar fields
    $scalar = [
        'project_icon_class',
        'project_lead',
        'project_read_time',
        'project_dependencies',
    ];
    foreach ( $scalar as $key ) {
        if ( isset( $_POST[ $key ] ) ) {
            update_post_meta( $post_id, $key, sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) );
        }
    }

    // Featured flag
    update_post_meta( $post_id, 'is_featured', isset( $_POST['is_featured'] ) ? '1' : '' );

    // Per-level fields
    foreach ( [ 'beginner', 'intermediate', 'advanced' ] as $level ) {

        // Overview (allow basic HTML)
        if ( isset( $_POST[ $level . '_overview' ] ) ) {
            update_post_meta(
                $post_id,
                $level . '_overview',
                wp_kses_post( wp_unslash( $_POST[ $level . '_overview' ] ) )
            );
        }

        // Code + filename (raw text)
        foreach ( [ '_code', '_code_filename' ] as $suffix ) {
            if ( isset( $_POST[ $level . $suffix ] ) ) {
                update_post_meta(
                    $post_id,
                    $level . $suffix,
                    sanitize_textarea_field( wp_unslash( $_POST[ $level . $suffix ] ) )
                );
            }
        }

        // Simple repeatable arrays
        $simple_repeaters = [ '_components', '_how_it_works', '_applications', '_upgrades' ];
        foreach ( $simple_repeaters as $suffix ) {
            $key = $level . $suffix;
            $raw = isset( $_POST[ $key ] ) && is_array( $_POST[ $key ] ) ? $_POST[ $key ] : [];
            $clean = array_filter( array_map( 'sanitize_text_field', array_map( 'wp_unslash', $raw ) ) );
            update_post_meta( $post_id, $key, array_values( $clean ) );
        }

        // Wiring table (3 parallel arrays → array of assoc)
        $pins   = isset( $_POST[ $level . '_wiring_pin' ] )   && is_array( $_POST[ $level . '_wiring_pin' ] )   ? $_POST[ $level . '_wiring_pin' ]   : [];
        $esps   = isset( $_POST[ $level . '_wiring_esp' ] )   && is_array( $_POST[ $level . '_wiring_esp' ] )   ? $_POST[ $level . '_wiring_esp' ]   : [];
        $notess = isset( $_POST[ $level . '_wiring_notes' ] ) && is_array( $_POST[ $level . '_wiring_notes' ] ) ? $_POST[ $level . '_wiring_notes' ] : [];
        $wiring = [];
        foreach ( $pins as $i => $pin ) {
            $pin = sanitize_text_field( wp_unslash( $pin ) );
            $esp = sanitize_text_field( wp_unslash( $esps[ $i ] ?? '' ) );
            if ( $pin || $esp ) {
                $wiring[] = [
                    'component_pin' => $pin,
                    'esp32_pin'     => $esp,
                    'notes'         => sanitize_text_field( wp_unslash( $notess[ $i ] ?? '' ) ),
                ];
            }
        }
        update_post_meta( $post_id, $level . '_wiring', $wiring );

        // Troubleshooting pairs
        $probs = isset( $_POST[ $level . '_troubleshooting_problem' ] )  && is_array( $_POST[ $level . '_troubleshooting_problem' ] )  ? $_POST[ $level . '_troubleshooting_problem' ]  : [];
        $sols  = isset( $_POST[ $level . '_troubleshooting_solution' ] ) && is_array( $_POST[ $level . '_troubleshooting_solution' ] ) ? $_POST[ $level . '_troubleshooting_solution' ] : [];
        $trouble = [];
        foreach ( $probs as $i => $prob ) {
            $prob = sanitize_text_field( wp_unslash( $prob ) );
            $sol  = sanitize_text_field( wp_unslash( $sols[ $i ] ?? '' ) );
            if ( $prob ) $trouble[] = [ 'problem' => $prob, 'solution' => $sol ];
        }
        update_post_meta( $post_id, $level . '_troubleshooting', $trouble );

        // FAQ pairs
        $qs = isset( $_POST[ $level . '_faq_question' ] ) && is_array( $_POST[ $level . '_faq_question' ] ) ? $_POST[ $level . '_faq_question' ] : [];
        $as = isset( $_POST[ $level . '_faq_answer' ] )   && is_array( $_POST[ $level . '_faq_answer' ] )   ? $_POST[ $level . '_faq_answer' ]   : [];
        $faq = [];
        foreach ( $qs as $i => $q ) {
            $q = sanitize_text_field( wp_unslash( $q ) );
            $a = sanitize_textarea_field( wp_unslash( $as[ $i ] ?? '' ) );
            if ( $q ) $faq[] = [ 'question' => $q, 'answer' => $a ];
        }
        update_post_meta( $post_id, $level . '_faq', $faq );

        // HowTo steps + FAQ items (top-level for schema, mirrors beginner level)
        if ( $level === 'beginner' ) {
            $how_raw = get_post_meta( $post_id, 'beginner_how_it_works', true );
            if ( is_array( $how_raw ) ) {
                update_post_meta( $post_id, 'howto_steps', $how_raw );
            }
            if ( $faq ) {
                update_post_meta( $post_id, 'faq_items', $faq );
            }
        }
    }
} );

/* ============================================================
   Save guide meta
   ============================================================ */
add_action( 'save_post_esp32_guide', function ( int $post_id ): void {
    if (
        ! isset( $_POST['esp32_guide_nonce'] ) ||
        ! wp_verify_nonce( $_POST['esp32_guide_nonce'], 'esp32_save_guide' ) ||
        defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ||
        ! current_user_can( 'edit_post', $post_id )
    ) return;

    foreach ( [ 'guide_phase', 'guide_read_time' ] as $key ) {
        if ( isset( $_POST[ $key ] ) ) {
            update_post_meta( $post_id, $key, sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) );
        }
    }
} );
