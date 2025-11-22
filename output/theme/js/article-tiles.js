// Make entire article tiles clickable while preserving inner anchor behavior.
(function(){
        document.addEventListener('click', function(e){
                // If an anchor was clicked, let it behave normally
                if (e.target.closest('a')) return;
                var tile = e.target.closest && e.target.closest('.tile');
                if (!tile) return;
                var href = tile.getAttribute('data-href');
                if (href) window.location.href = href;
        }, false);

        // Keyboard support: Enter on a focused tile
        document.addEventListener('keydown', function(e){
                if (e.key !== 'Enter') return;
                var active = document.activeElement;
                if (!active) return;
                var tile = active.closest && active.closest('.tile');
                if (!tile) return;
                // If focus is inside an actual link, don't override
                if (active.closest('a')) return;
                var href = tile.getAttribute('data-href');
                if (href) {
                        // Give browsers a chance to follow other handlers
                        e.preventDefault();
                        window.location.href = href;
                }
        }, false);
})();