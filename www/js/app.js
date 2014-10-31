// Global jQuery references
var $shareModal = null;
var $commentCount = null;

// Global state
var firstShareLoad = true;

/*
 * Run on page load.
 */
var onDocumentLoad = function(e) {
    // Cache jQuery references
    $shareModal = $('#share-modal');
    $commentCount = $('.comment-count');

    // Bind events
    $shareModal.on('shown.bs.modal', onShareModalShown);
    $shareModal.on('hidden.bs.modal', onShareModalHidden);

    // configure ZeroClipboard on share panel
    ZeroClipboard.config({ swfPath: 'js/lib/ZeroClipboard.swf' });
    var clippy = new ZeroClipboard($(".clippy"));

    clippy.on('ready', function(readyEvent) {
        clippy.on('aftercopy', onClippyCopy);
    });

    bindPlayerUtils();
    renderLocationCharts();
};

/*
 * Share modal opened.
 */
var onShareModalShown = function(e) {
    _gaq.push(['_trackEvent', APP_CONFIG.PROJECT_SLUG, 'open-share-discuss']);

    if (firstShareLoad) {
        loadComments();

        firstShareLoad = false;
    }
};

/*
 * Share modal closed.
 */
var onShareModalHidden = function(e) {
    _gaq.push(['_trackEvent', APP_CONFIG.PROJECT_SLUG, 'close-share-discuss']);
};

/*
 * Text copied to clipboard.
 */
var onClippyCopy = function(e) {
    alert('Copied to your clipboard!');

    _gaq.push(['_trackEvent', APP_CONFIG.PROJECT_SLUG, 'summary-copied']);
};

/*
 * Power Player card utilities
 */
var bindPlayerUtils = function() {
    $('.player-utils li a').click(function(e) {
        if ($(this).hasClass('embed'))
            embedModal(e);
        if ($(this).hasClass('copy-link'))
            copyURLModal(e);
        return false;
    });
};

var embedModal = function(e) {
    var target = $(e.currentTarget).parent().parent().parent(),
        slug = target.data('player-slug'),
        name = target.data('player-name'),
        deployment_target = APP_CONFIG.DEPLOYMENT_TARGET,
        embed_url = APP_CONFIG.S3_BASE_URL + '/embed/player/' + slug + '/',
        pym_url = APP_CONFIG.S3_BASE_URL + '/assets/js/pym.js';

    var modal = JST.embedModal({
        embed_url: embed_url,
        pym_url: pym_url,
        slug: slug,
        name: name
    });

    $(modal).modal();
};

var copyURLModal = function(e) {
    var target = $(e.currentTarget).parent().parent().parent(),
        slug = target.data('player-slug'),
        name = target.data('player-name'),
        deployment_target = APP_CONFIG.DEPLOYMENT_TARGET,
        url = APP_CONFIG.S3_BASE_URL + '/player/' + slug + '/';

    var modal = JST.copyURLModal({
        url: url,
        name: name
    });

    $(modal).modal();
}

/* Where did the money go? */
var renderLocationCharts = function() {
    if (typeof STATE_LOCATION_JSON !== 'undefined') {
        var data = STATE_LOCATION_JSON;

        $('.donation-breakdown').each(function() {
            var container = $(this).find('.location-container'),
                slug = $(this).data('player-slug'),
                player = data[slug];

            if (player) {
                var state = $(JST.breakdownBars({
                        type: 'state',
                        amount: '$' + Number(player.Total_state).formatMoney(),
                        width: (player.pct_state*100) + '%'
                    })),
                    federal = $(JST.breakdownBars({
                        type: 'federal',
                        amount: '$' + Number(player.Total_federal).formatMoney(),
                        width: (player.pct_federal*100) + '%'
                    }));

                if (Number(player.Total_state) > 0)
                    container.append(state);
                if (Number(player.Total_federal) > 0)
                    container.append(federal);

                state.fadeIn();
                federal.fadeIn();
            } else
                console.log("Couldn't find player: " + slug);
        });
    }
};

// From http://stackoverflow.com/questions/149055/how-can-i-format-numbers-as-money-in-javascript
Number.prototype.formatMoney = function(c, d, t){
    var n = this,
    c = isNaN(c = Math.abs(c)) ? 2 : c,
    d = d == undefined ? "." : d,
    t = t == undefined ? "," : t,
    s = n < 0 ? "-" : "",
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
    j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") +
        i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) +
        (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

$(onDocumentLoad);
