/**
 * Input fields handlers
 */

function toggleWrapperClass(class_name, callable) {
    let func = function(bool) {
        if (bool === undefined)
            bool = callable.apply(this);
        this.wrapper.toggleClass(class_name, bool);
    };
    return func;
}

let Input = function(field) {

    this.dom_field = field;
    this.field = $(field);
    this.wrapper = $(field).closest('.input-wrapper');

    // initialization
    this.update_focus();
    this.update_has_value();

    // register event handlers
    this.field.focus( () => this.on_focus() );
    this.field.blur( () => this.on_blur() );
    this.field.on('change', () => this.on_change() );
};

Input.prototype = {
    has_value: function()   { return this.field.val() ? true : false; },
    has_focus: function()   { return this.field.is(':focus'); },
    has_error: function()   { return !this.has_value() && this.field.prop('required'); },

    on_focus: function()    { this.update_focus(true); },
    on_blur: function()     { this.update_focus(false); },
    on_change: function() {
        this.update_has_value();
        this.update_error();
    }
};

$.extend(Input.prototype, {
    update_focus: toggleWrapperClass('input-focused', Input.prototype.has_focus),
    update_error: function () {
        let has_error = this.has_error();
        toggleWrapperClass('input-error').bind(this)(has_error);
        if (!has_error) {
            this.wrapper.find('.messages .error-desc').hide();
        }
    },
    update_has_value: toggleWrapperClass('input-has-value', Input.prototype.has_value),
});


$(function () {
    let fields = $('input.field');
    fields.map( function() { return new Input(this); });
});

$(function () {
    let choice_yes = $('.choice-yes');
    let choice_no = $('.choice-no');

    choice_yes.click(function () {
        $(this).siblings('input').prop('checked', true);
        $(this).addClass('focus');
        $(this).siblings('.choice-no').removeClass('focus');
    });

    choice_no.click(function () {
        $(this).siblings('input').prop('checked', true);
        $(this).addClass('focus');
        $(this).siblings('.choice-yes').removeClass('focus');
    });

});

/**
 * Keyboard shortcuts
 *
 * - A method can be selected by pressing Ctrl+Alt+(first letter of method name)
 * (or second if first is already used...)
 */

function prepareShorcuts() {
    let shortcuts = {};

    $('.method-wrapper a').each( function() {
        let name = $(this).text();

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
