'use strict';

{

    window.ReviewBot = window.ReviewBot || {};

    /**
     * The model for the configuration page.
     *
     * Model Attributes:
     *     brokerURL (string):
     *         The URL for the AMQP broker.
     *
     *     user (number):
     *         The ID of the user for Review Bot to post as.
     */
    ReviewBot.ExtensionConfig = Backbone.Model.extend({
        defaults: {
            brokerURL: '',
            user: null
        },

        /**
         * Initialize the model.
         *
         * Args:
         *     attributes (object):
         *         Initial attribute values for the model.
         *
         *     options (object):
         *         Additional options for the model.
         *
         * Option Args:
         *     integrationConfigURL (string):
         *         The URL of the integration list page.
         *
         *     userConfigURL (string):
         *         The URL of the user configuration endpoint.
         *
         *     workerStatusURL (string):
         *         The URL of the worker status endpoint.
         */
        initialize: function initialize(attributes, options) {
            Backbone.Model.prototype.initialize.call(this, attributes, options);
            this.options = options;
        }
    });

    /**
     * A view for configuring the Review Bot user.
     */
    var UserConfigView = Backbone.View.extend({
        tagName: 'fieldset',

        className: 'module aligned wide',

        id: 'reviewbot-user',

        events: {
            'click #reviewbot-user-create': '_createUser'
        },

        _template: _.template('<h2><%- titleText %></h2>\n<div class="form-row">\n <label class="required" for="reviewbot-user-field"><%- labelText %></label>\n <select class="related-object-options reviewbot-user-select"\n         name="reviewbot_user"\n         placeholder="<%- selectPlaceholderText %>"\n         id="reviewbot-user-field"></select>\n <span class="reviewbot-user-create-details">\n  <% if (!hasUser) { %><%= orHTML %><% } %>\n </span>\n <p class="help"><%- descriptionText %></p>\n</div>'),

        _optionTemplate: _.template('<div>\n<% if (avatarURL) { %>\n <img src="<%- avatarURL %>">\n<% } %>\n<% if (fullname) { %>\n <span class="title"><%- fullname %></span>\n <span class="description">(<%- username %>)</span>\n<% } else { %>\n <span class="title"><%- username %></span>\n<% } %>\n</div>'),

        /**
         * Render the view.
         *
         * Returns:
         *     UserConfigView:
         *     This object, for chaining.
         */
        render: function render() {
            var _this = this;

            var user = this.model.get('user');

            this.$el.html(this._template({
                titleText: gettext('Review Bot User'),
                labelText: gettext('Review Bot User:'),
                descriptionText: gettext('Review Bot will use this user account to post reviews.'),
                selectPlaceholderText: gettext('Select an existing user account'),
                orHTML: gettext('or <a href="#" id="reviewbot-user-create">create a new user for Review Bot</a>.'),
                hasUser: user !== null
            }));

            var currentItems = [];
            var currentOptions = [];

            if (user !== null) {
                currentItems.push(user.id);
                currentOptions.push(user);
            }

            this._$select = this.$('select');

            this._$select.selectize({
                closeAfterSelect: true,
                dropdownParent: 'body',
                hideSelected: true,
                maxItems: 1,
                preload: 'focus',
                items: currentItems,
                options: currentOptions,
                searchField: ['fullname', 'username'],
                valueField: 'id',
                load: function load(query, callback) {
                    var params = {
                        fullname: 1,
                        'only-fields': 'avatar_url,fullname,id,username',
                        'only-links': ''
                    };

                    if (query.length !== 0) {
                        params.q = query;
                    }

                    $.ajax({
                        type: 'GET',
                        url: SITE_ROOT + 'api/users/',
                        data: params,
                        success: function success(result) {
                            return callback(result.users);
                        },
                        error: function error(xhr, textStatus, errorThrown) {
                            alert('Unexpected error when querying for users: ' + errorThrown);
                            console.error('User query failed', xhr, textStatus, errorThrown);
                            callback();
                        }
                    });
                },
                render: {
                    item: function item(_item) {
                        return _this._optionTemplate({
                            avatarURL: _item.avatar_url,
                            id: _item.id,
                            fullname: _item.fullname,
                            username: _item.username
                        });
                    },
                    option: function option(item) {
                        return _this._optionTemplate({
                            avatarURL: item.avatar_url,
                            id: item.id,
                            fullname: item.fullname,
                            username: item.username
                        });
                    }
                }
            });

            this._selectize = this._$select[0].selectize;

            this.listenTo(this.model, 'change:user', function (model, value) {
                _this._setOption(value);
            });

            return this;
        },


        /**
         * Create a new user.
         *
         * Args:
         *     e (Event):
         *         The event which triggered the action.
         */
        _createUser: function _createUser(e) {
            var _this2 = this;

            e.preventDefault();
            e.stopPropagation();

            var $details = this.$('.reviewbot-user-create-details');
            this._selectize.lock();
            $details.html('<span class="fa fa-spinner fa-pulse">');

            $.ajax({
                type: 'POST',
                url: this.model.options.userConfigURL,
                complete: function complete() {
                    _this2._selectize.unlock();
                    _this2._selectize.blur();
                    $details.empty();
                },
                success: function success(result) {
                    _this2._setOption(result);
                },
                error: function error(xhr, textStatus, errorThrown) {
                    alert('Unexpected error when creating the user: ' + errorThrown);
                    console.error('Failed to update user', xhr, textStatus, errorThrown);
                }
            });
        },


        /**
         * Set the currently selected option.
         *
         * Args:
         *     user (object):
         *          The user details.
         */
        _setOption: function _setOption(user) {
            this._selectize.clear(true);
            this._selectize.clearOptions();
            this._selectize.addOption(user);
            this._selectize.setValue(user.id, true);
        }
    });

    /**
     * A view to show the current broker status.
     */
    var BrokerStatusView = Backbone.View.extend({
        className: 'colM',

        id: 'reviewbot-broker-status',

        events: {
            'click #reviewbot-broker-status-refresh': '_onRefreshClicked'
        },

        _updatingTemplate: _.template('<span class="fa fa-spinner fa-pulse"></span>\n<%- refreshingText %>'),

        _connectedTemplate: _.template('<div>\n <span class="fa fa-check"></span>\n <%- connectedText %>\n</div>\n<% if (workers.length === 0) { %>\n <div>\n  <span class="fa fa-exclamation-triangle"></span>\n  <%- workersText %>\n </div>\n<% } else { %>\n <div>\n  <span class="fa fa-check"></span>\n  <%- workersText %>\n  <ul>\n   <% _.each(workers, function(worker) { %>\n    <li>\n     <span class="fa fa-desktop"></span>\n     <%- worker.hostname %>\n    </li>\n   <% }); %>\n  </ul>\n </div>\n <div>\n  <span class="fa fa-cogs"></span>\n  <%- readyText %>\n  <%= configureIntegrationsHTML %>\n </div>\n<% } %>\n<div>\n <a href="#" id="reviewbot-broker-status-refresh"><%- refreshText %></a>\n</div>'),

        _errorTemplate: _.template('<div>\n <span class="fa fa-exclamation-triangle"></span>\n <%- errorText %>\n</div>\n<div>\n <a href="#" id="reviewbot-broker-status-refresh"><%- refreshText %></a>\n</div>'),

        /**
         * Initialize the view.
         */
        initialize: function initialize() {
            this._updating = false;
            this._connected = false;
            this._rendered = false;
            this._errorText = '';
            this._workers = [];

            this.listenTo(this.model, 'change', this._update);
            this._update();
        },


        /**
         * Render the view.
         *
         * Returns:
         *     BrokerStatusView:
         *     This object, for chaining.
         */
        render: function render() {
            $('<h1 class="title">').text(gettext('Broker Status')).appendTo(this.$el);

            var $wrapper = $('<div id="content-main">').appendTo(this.$el);

            this._$content = $('<div class="form-row">').appendTo($wrapper);

            this._rendered = true;

            this._updateDisplay();

            return this;
        },


        /**
         * Update the displayed status.
         */
        _updateDisplay: function _updateDisplay() {
            if (!this._rendered) {
                return;
            }

            if (this._updating) {
                this._$content.html(this._updatingTemplate({
                    refreshingText: gettext('Checking broker...')
                }));
            } else if (this._connected) {
                var workersText = void 0;

                if (this._workers.length === 0) {
                    workersText = gettext('No worker nodes found.');
                } else {
                    workersText = interpolate(ngettext('%s worker node:', '%s worker nodes:', this._workers.length), [this._workers.length]);
                }

                this._$content.html(this._connectedTemplate({
                    connectedText: gettext('Connected to broker.'),
                    workersText: workersText,
                    refreshText: gettext('Refresh'),
                    workers: this._workers,
                    readyText: gettext('Review Bot is ready!'),
                    configureIntegrationsHTML: interpolate(gettext('To configure when Review Bot tools are run, set up <a href="%s">integration configurations</a>.'), [this.model.options.integrationConfigURL])
                }));
            } else {
                this._$content.html(this._errorTemplate({
                    errorText: this._errorText,
                    refreshText: gettext('Refresh')
                }));
            }
        },


        /**
         * Handler for when the "Refresh" link is clicked.
         *
         * Args:
         *     e (Event):
         *         The event which triggered the action.
         */
        _onRefreshClicked: function _onRefreshClicked(e) {
            e.preventDefault();
            e.stopPropagation();

            this._update();
        },


        /**
         * Request status from the server and update the UI.
         */
        _update: function _update() {
            var _this3 = this;

            this._updating = true;
            this._updateDisplay();

            $.ajax({
                type: 'GET',
                url: this.model.options.workerStatusURL,
                success: function success(result) {
                    _this3._workers = result.hosts || [];
                    _this3._connected = result.state === 'success';
                    _this3._errorText = result.error || '';
                    _this3._updating = false;
                    _this3._updateDisplay();
                },
                error: function error(xhr, textStatus, errorThrown) {
                    console.error('Failed to get broker status', xhr, textStatus, errorThrown);
                    _this3._errorText = gettext('Unable to connect to broker.');
                    _this3._workers = [];
                    _this3._connected = false;
                    _this3._updating = false;
                    _this3._updateDisplay();
                }
            });
        }
    });

    /**
     * A view for configuring the broker URL.
     */
    var BrokerConfigView = Backbone.View.extend({
        tagName: 'fieldset',

        id: 'reviewbot-broker',

        className: 'module aligned wide',

        _template: _.template('<h2><%- titleText %></h2>\n<div class="form-row">\n <label class="required" for="reviewbot-broker-field"><%- labelText %></label>\n <input id="reviewbot-broker-field" name="reviewbot_broker_url"\n        type="text" value="<%- brokerURL %>">\n <p class="help"><%- descriptionText %></p>\n</div>'),

        /**
         * Render the view.
         *
         * Returns:
         *     BrokerConfigView:
         *     This object, for chaining.
         */
        render: function render() {
            this.$el.html(this._template({
                titleText: gettext('Broker'),
                labelText: gettext('Broker URL:'),
                descriptionText: gettext('The URL to your AMQP broker.'),
                brokerURL: this.model.get('brokerURL')
            }));

            return this;
        }
    });

    /**
     * A view containing the entire Review Bot extension configuration.
     */
    ReviewBot.ExtensionConfigView = Backbone.View.extend({
        events: {
            'click input[type="submit"]': '_onSaveClicked'
        },

        /**
         * Initialize the view.
         */
        initialize: function initialize() {
            this._userConfigView = new UserConfigView({
                model: this.model
            });

            this._brokerConfigView = new BrokerConfigView({
                model: this.model
            });

            this._brokerStatusView = new BrokerStatusView({
                model: this.model
            });
        },


        /**
         * Render the view.
         *
         * Returns:
         *     ReviewBot.ExtensionConfigView:
         *     This object, for chaining.
         */
        render: function render() {
            this._userConfigView.render();
            this._brokerConfigView.render();
            this._brokerStatusView.render();

            this._$form = $('<form>').append(this._userConfigView.$el).append(this._brokerConfigView.$el).appendTo(this.$el);

            this._$saveButton = $('<input type="submit" class="default">').val(gettext('Save'));

            $('<div class="submit-row">').append(this._$saveButton).appendTo(this.$el);

            $('#content_container').append(this._brokerStatusView.$el);

            return this;
        },


        /**
         * Callback for when the "Save" button is clicked.
         *
         * This saves the form and updates the model.
         */
        _onSaveClicked: function _onSaveClicked(e) {
            var _this4 = this;

            e.preventDefault();
            e.stopPropagation();

            this._$saveButton.prop('disabled', true);

            var $spinner = $('<span class="fa fa-spinner fa-pulse">').insertBefore(this._$saveButton);

            $.ajax({
                type: 'POST',
                url: window.location.pathname,
                data: this._$form.serialize(),
                complete: function complete() {
                    _this4._$saveButton.prop('disabled', false);
                    $spinner.remove();
                },
                success: function success(response) {
                    if (response.result === 'success') {
                        if (response.broker_url) {
                            _this4.model.set('brokerURL', response.broker_url);
                        }

                        if (response.user) {
                            _this4.model.set('user', response.user);
                        }
                    } else if (response.result === 'error') {
                        console.error('Failed to save Review Bot configuration', response);
                        alert(response.error);
                    } else {
                        console.error('Unexpected response from server when ' + 'saving Review Bot configuration.', response);
                    }
                },
                error: function error(xhr, textStatus, errorThrown) {
                    alert('Unexpected error when querying broker: ' + errorThrown);
                    console.error('Failed to update broker', xhr, textStatus, errorThrown);
                }
            });
        }
    });
}

//# sourceMappingURL=extensionConfig.js.map