function supports_html5_storage() {
    try {
        return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
        return false;
    }
}


if (supports_html5_storage()) {
    $(function(){
        /* Upon loading, set all language-specific tabs to the
           preferred language. */
        var language = localStorage.getItem("preferred-language");
        if (language) {
            var tabs = $jqTheme('a[data-toggle="tab"]');
            for (var i = 0; i < tabs.size(); ++i) {
                var href = tabs[i].href;
                if (href.split("_")[1] == language) {
                    $jqTheme('a[href="#' + href.split('#')[1] + '"]').tab("show");
                }
            }
        }

        /* When a tab is checked set it as the preferred language */
        $jqTheme(document).on('shown', 'a[data-toggle="tab"]', function (e) {
            var language = e.target.href.split("_")[1];
            localStorage.setItem("preferred-language", language);
        })
    })
}
