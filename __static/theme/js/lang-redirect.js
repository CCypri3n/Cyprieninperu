(function(){
  'use strict';

  var supported = ['en','fr','de'];
  var defaultLang = document.documentElement.getAttribute('data-default-lang') || 'en';

  function getCurrentLangFromPath(){
    var p = window.location.pathname || '/';
    var parts = p.split('/');
    if(parts.length > 1 && parts[1]){
      var candidate = parts[1].toLowerCase();
      if(supported.indexOf(candidate) !== -1) return candidate;
    }
    return null;
  }

  function getPreferredFromStorage(){
    try { return localStorage.getItem('preferredLang'); } catch(e){ return null; }
  }

  function detectPreferred(){
    var stored = getPreferredFromStorage();
    if(stored && supported.indexOf(stored) !== -1) return stored;
    var navs = (navigator.languages && navigator.languages.slice()) || [navigator.language || navigator.userLanguage || defaultLang];
    for(var i=0;i<navs.length;i++){
      var lang = navs[i];
      if(!lang) continue;
      var prefix = lang.split('-')[0].toLowerCase();
      if(supported.indexOf(prefix) !== -1) return prefix;
    }
    return defaultLang;
  }

  function normalizePathForPrefix(prefix){
    var p = window.location.pathname || '/';
    // remove any existing supported prefix
    var parts = p.split('/');
    if(parts.length > 1 && supported.indexOf(parts[1]) !== -1){
      parts.splice(1,1); // remove existing lang
    }
    // ensure leading slash
    var remainder = parts.join('/');
    if(!remainder.startsWith('/')) remainder = '/' + remainder;
    // join with chosen prefix
    if(prefix === defaultLang){
      // default site served at root — do not prefix
      return remainder;
    }
    // avoid double slashes
    var target = '/' + prefix + remainder;
    target = target.replace(/\/+/g, '/');
    return target;
  }

  // Respect a session flag to avoid redirect loops during a single visit
  try{ if(sessionStorage && sessionStorage.getItem('langRedirected')) return; } catch(e){}

  var preferred = detectPreferred();
  var current = getCurrentLangFromPath();

  // If user already on a different language by explicit click, don't override
  // localStorage preferredLang is set by language links (see base template), so we honor it above.

  if(current !== preferred){
    var target = normalizePathForPrefix(preferred);
    // If target equals current path, do nothing
    var currentPath = window.location.pathname + (window.location.search || '') + (window.location.hash || '');
    var absoluteTarget = target + (window.location.search || '') + (window.location.hash || '');
    if(absoluteTarget !== currentPath){
      try{ sessionStorage.setItem('langRedirected','1'); } catch(e){}
      // Use replace() so browser history isn't polluted with redirect
      window.location.replace(absoluteTarget);
    }
  }

  // Add a small helper: if user clicks a lang-link, remember preference (defensive for older browsers)
  try{
    var links = document.querySelectorAll('a.lang-link[data-lang]');
    for(var j=0;j<links.length;j++){
      (function(a){
        a.addEventListener('click', function(){
          try{ var l = a.getAttribute('data-lang'); if(l) localStorage.setItem('preferredLang', l); } catch(e){}
        }, false);
      })(links[j]);
    }
  }catch(e){}

})();
