'use strict';

(function () {

    var allowedMimeTypes = ['image/png', 'image/jpeg', 'image/gif'];

    /**
     * A file upload avatar settings form.
     *
     * This form provides a preview of the uploaded avatar.
     */
    Djblets.Avatars.FileUploadSettingsFormView = Djblets.Avatars.ServiceSettingsFormView.extend({
        events: {
            'change #id_file-upload-avatar_upload': '_onFileChanged'
        },

        /**
         * Validate the form.
         *
         * If a file is selected, ensure it is has the correct MIME type.
         */
        validate: function validate() {
            var file = this.$('#id_file-upload-avatar_upload')[0].files[0];

            if (!file) {
                alert(gettext('You must choose a file.'));
                return false;
            }

            if (!allowedMimeTypes.some(function (el) {
                return el === file.type;
            })) {
                alert(gettext('Invalid file format'));
                return false;
            }

            return true;
        },


        /**
         * Render the form.
         *
         * Returns:
         *     Djblets.Avatars.FileUploadSettingsFormView:
         *     This view (for chaining).
         */
        render: function render() {
            this._$preview = this.$('.avatar-preview');

            return this;
        },


        /**
         * Handle to the selected file being changed.
         *
         * This will update the preview image.
         *
         * Args:
         *     e (Event):
         *         The change event.
         */
        _onFileChanged: function _onFileChanged(e) {
            var _this = this;

            var file = e.target.files[0];

            if (file) {
                var reader = new FileReader();
                reader.addEventListener('load', function () {
                    _this._$preview.children().eq(0).replaceWith($('<img />').attr('src', reader.result));
                });

                reader.readAsDataURL(file);
            }
        }
    });
})();

//# sourceMappingURL=fileUploadSettingsFormView.js.map