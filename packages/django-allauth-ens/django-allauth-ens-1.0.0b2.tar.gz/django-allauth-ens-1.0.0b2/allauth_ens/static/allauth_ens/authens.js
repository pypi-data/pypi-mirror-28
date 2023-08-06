/**
 * Input fields handlers
 */

let WIDGET_CLS = {
    has_error: 'input-error',
    has_focus: 'input-focused',
    has_value: 'input-has-value'
};

let Widget = function($wrapper) {
    this.$wrapper = $wrapper;

    this.$field = $wrapper.find('input');

    this.update_has_value();

    // register event handlers
    this.$field.focus( () => this.on_focus() );
    this.$field.blur( () => this.on_blur() );
    this.$field.on('change', () => this.on_change() );

    // initialization
    if (this.has_focus())
        this.$field.focus();
};

Widget.prototype = {
    has_value: function () {
        return Boolean(this.$field.val());
    },

    has_focus: function () {
        return this.$field.is(':focus');
    },

    has_error: function () {
        return this.$field.prop('required') && !this.has_value();
    },

    on_focus: function () {
        this.$wrapper.addClass(WIDGET_CLS.has_focus);
    },

    on_blur: function () {
        this.$wrapper.removeClass(WIDGET_CLS.has_focus);
    },

    on_change: function () {
        this.update_has_value();
        this.update_error();
    },

    update_has_value: function () {
        this.$wrapper.toggleClass(WIDGET_CLS.has_value, this.has_value());
    },

    update_error: function () {
        let has_error = this.has_error();
        this.$wrapper.toggleClass(WIDGET_CLS.has_error, has_error);
        if (!has_error)
            this.$wrapper.find('.messages .error-desc').hide();
    }
};

let CheckboxInput = function ($wrapper) {
    this.$wrapper = $wrapper;

    this.$field = $wrapper.find('input');
    this.$buttons = $wrapper.find('button');

    this.$buttons.click( (e) => this.on_click(e) );
    this.$buttons.focus( () => this.on_focus() );
    this.$buttons.blur( () => this.on_blur() );
};

CheckboxInput.prototype = {
    on_click: function (e) {
        let $button = $(e.target);
        let checked = $button.hasClass('choice-yes');

        this.$field.prop('checked', checked);
        this.$buttons.removeClass('selected');
        $button.addClass('selected');
    },

    on_focus: function () {
        this.$wrapper.addClass(WIDGET_CLS.has_focus);
    },

    on_blur: function () {
        this.$wrapper.removeClass(WIDGET_CLS.has_focus);
    }
};

let RadioSelect = function ($wrapper) {
    this.$wrapper = $wrapper;

    this.$buttons = $wrapper.find('button');

    this.$buttons.click( (e) => this.on_click(e) );
    this.$buttons.focus( () => this.on_focus() );
    this.$buttons.blur( () => this.on_blur() );
};

RadioSelect.prototype = {
    on_click: function (e) {
        let $button = $(e.target);
        let $field = $button.find('input');

        if (!$field.prop('checked')) {
            $field.prop('checked', true);
            this.$buttons.removeClass('selected');
            $button.addClass('selected');
        }
    },

    on_focus: function () { this.$wrapper.addClass(WIDGET_CLS.has_focus); },
    on_blur: function () { this.$wrapper.removeClass(WIDGET_CLS.has_focus); }
};

$(function () {
    $('.input-wrapper').each(function () {
        let $wrapper = $(this);
        let widget_type = $wrapper.data('widget-type');

        if (widget_type == 'checkboxinput') {
            new CheckboxInput($wrapper);
        } else if (widget_type == 'radioselect') {
            new RadioSelect($wrapper);
        } else if (widget_type == 'select') {
            new Select($wrapper);
        } else {
            new Widget($wrapper);
        }
    });
});

let Select = function ($wrapper) {
    this.$wrapper = $wrapper;

    this.$field = $wrapper.find('select');

    this.$field.focus( () => this.on_focus() );
    this.$field.blur( () => this.on_blur() );
};

Select.prototype = {
    on_focus: function () { this.$wrapper.addClass(WIDGET_CLS.has_focus); },
    on_blur: function () { this.$wrapper.removeClass(WIDGET_CLS.has_focus); }
};


/**
 * Keyboard shortcuts
 *
 * - A method can be selected by pressing Ctrl+Alt+(first letter of method name)
 * (or second if first is already used...)
 */

function prepareShorcuts() {
    let shortcuts = {};

    $('.method-wrapper a').each( function() {
        let name = $(this).text().trim();

        for (let i=0; i < name.length; i++) {
            let key = name[i].toLowerCase();
            if (key !== '' && shortcuts[key] === undefined) {
                shortcuts[key] = this;
                break;
            }
        }
    });

    window.methodsShortcuts = shortcuts;

    // Shorcuts handler
    $(document).keydown( function(e) {
        if (e.ctrlKey && e.altKey) {
            let methodLink = shortcuts[e.key];
            if (methodLink !== undefined)
                methodLink.click();
        }
    });
}
