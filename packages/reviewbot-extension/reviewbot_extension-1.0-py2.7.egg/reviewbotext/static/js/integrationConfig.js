'use strict';

$(function () {
    var $tool = $('#id_tool');
    var $toolOptions = $('#row-tool_options');

    if ($tool.length === 1 && $toolOptions.length === 1) {
        var changeToolVisibility = function changeToolVisibility() {
            var selectedTool = parseInt($tool.val(), 10);
            var $lastVisibleChild = null;

            $toolOptions.find('.form-row').each(function (i, el) {
                var $el = $(el);

                if ($el.data('tool-id') === selectedTool) {
                    $el.show();
                    $lastVisibleChild = $el;
                } else {
                    $el.hide();
                }
            });

            /*
             * Normally, the :last-child rule would hide this border. Instead,
             * we have to override it because the parent has a bunch of other
             * children after the last one that happen to be hidden.
             */
            if ($lastVisibleChild !== null) {
                $lastVisibleChild.css('border-bottom', 0);
                $itemAboveOptions.css('border-bottom', '');
            } else {
                $itemAboveOptions.css('border-bottom', 0);
            }
        };

        var $itemAboveOptions = $toolOptions.prev();

        $tool.change(function () {
            return changeToolVisibility();
        });
        changeToolVisibility();
    }
});

//# sourceMappingURL=integrationConfig.js.map