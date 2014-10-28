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

$(onDocumentLoad);
