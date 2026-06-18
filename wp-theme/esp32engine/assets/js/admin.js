/* ESP32 Engine — Admin Metabox JS */
(function ($) {
  'use strict';

  /* ---- Tab switching ---- */
  $(document).on('click', '.esp32-tab-btn', function () {
    var $btn    = $(this);
    var $wrap   = $btn.closest('.esp32-tabs-wrap');
    var target  = $btn.data('target');

    $wrap.find('.esp32-tab-btn').removeClass('is-active').attr('aria-selected', 'false');
    $wrap.find('.esp32-tab-panel').removeClass('is-active');

    $btn.addClass('is-active').attr('aria-selected', 'true');
    $('#' + target).addClass('is-active');
  });

  /* ---- Add repeater row ---- */
  $(document).on('click', '.esp32-add-row', function () {
    var target   = $(this).data('target');
    var rowType  = $(this).data('type') || 'simple';
    var $repeater = $('[data-prefix="' + target + '"]');
    var $newRow;

    if (rowType === 'wiring') {
      $newRow = $(
        '<div class="esp32-row esp32-wiring-row">' +
          '<input type="text" name="' + target + '_pin[]" placeholder="Pin">' +
          '<input type="text" name="' + target + '_esp[]" placeholder="ESP32 Pin">' +
          '<input type="text" name="' + target + '_notes[]" placeholder="Notes">' +
          '<button type="button" class="esp32-remove-row button">–</button>' +
        '</div>'
      );
    } else if (rowType === 'pair') {
      var nameParts = target.split('_');
      var base      = nameParts.slice(0, -1).join('_');
      var section   = nameParts[nameParts.length - 1];
      if (section === 'troubleshooting') {
        $newRow = $(
          '<div class="esp32-row esp32-pair-row">' +
            '<input type="text" name="' + target + '_problem[]" placeholder="Problem…" class="widefat">' +
            '<input type="text" name="' + target + '_solution[]" placeholder="Solution…" class="widefat">' +
            '<button type="button" class="esp32-remove-row button">–</button>' +
          '</div>'
        );
      } else {
        $newRow = $(
          '<div class="esp32-row esp32-pair-row">' +
            '<input type="text" name="' + target + '_question[]" placeholder="Question…" class="widefat">' +
            '<textarea name="' + target + '_answer[]" rows="2" class="widefat" placeholder="Answer…"></textarea>' +
            '<button type="button" class="esp32-remove-row button">–</button>' +
          '</div>'
        );
      }
    } else {
      $newRow = $(
        '<div class="esp32-row">' +
          '<input type="text" name="' + target + '[]" class="widefat" placeholder="Add item…">' +
          '<button type="button" class="esp32-remove-row button">–</button>' +
        '</div>'
      );
    }

    $repeater.append($newRow);
    $newRow.find('input, textarea').first().focus();
  });

  /* ---- Remove repeater row ---- */
  $(document).on('click', '.esp32-remove-row', function () {
    var $repeater = $(this).closest('.esp32-repeater');
    var $row = $(this).closest('.esp32-row');

    // Keep at least one row
    var allRows = $repeater.find('.esp32-row:not(.esp32-row-header)');
    if (allRows.length > 1) {
      $row.remove();
    } else {
      $row.find('input, textarea').val('');
    }
  });

})(jQuery);
