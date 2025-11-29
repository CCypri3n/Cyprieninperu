document.addEventListener('DOMContentLoaded', function () {
  // Delegate clicks for the copy-link button
  document.body.addEventListener('click', function (ev) {
    const el = ev.target.closest('.share-button.link');
    if (!el) return;
    ev.preventDefault();

    // URL to copy can be provided via data-copy-url, fallback to href
    const url = el.getAttribute('data-copy-url') || el.getAttribute('href') || window.location.href;

    // Use Clipboard API when available
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(() => {
        showCopiedState(el);
      }).catch(() => {
        // Fallback to older execCommand path
        fallbackCopyTextToClipboard(url, el);
      });
    } else {
      fallbackCopyTextToClipboard(url, el);
    }
  });

  function fallbackCopyTextToClipboard(text, el) {
    try {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      const ok = document.execCommand('copy');
      textarea.remove();
      if (ok) showCopiedState(el);
      else alert('Copy failed — please select and copy the link manually.');
    } catch (e) {
      alert('Copy not supported in this browser.');
    }
  }

  function showCopiedState(el) {
    // Provide a short visual confirmation: add `data-copied` attribute and restore after timeout
    el.setAttribute('data-copied', 'true');
    const prevLabel = el.getAttribute('aria-label');
    el.setAttribute('aria-label', 'Copied');
    setTimeout(() => {
      el.removeAttribute('data-copied');
      if (prevLabel) el.setAttribute('aria-label', prevLabel);
      else el.removeAttribute('aria-label');
    }, 1800);
  }
});
