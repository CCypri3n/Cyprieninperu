document.addEventListener("DOMContentLoaded", () => {
  const tilesContainer = document.getElementById("tilesContainer");

  // Shared modal (same structure as carousel)
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImage");
  const modalVideo = document.getElementById("modalVideo");
  const modalClose = document.getElementById("modalClose");

  // Fetch your gallery data
  fetch('/gallery.json')
    .then(res => res.json())
    .then(items => {
      // Create tiles with data-src attribute for lazy loading
      items.forEach(item => {
        const tile = document.createElement("div");
        tile.classList.add("tileItem");

        if (item.type === 'video') {
          tile.classList.add("videoTile");
          tile.dataset.videoUrl = item.video_url;
          // Set a placeholder background, actual image loads lazily later
          tile.dataset.bgUrl = `url(${item.thumbnail_url})`;
        } else {
          const imgUrl = item.url.startsWith('http')
            ? item.url
            : `${item.url.startsWith('/') ? '' : '/'}${item.url}`;
          tile.dataset.bgUrl = `url(${imgUrl})`;
        }

        // Append tile without setting backgroundImage yet
        tilesContainer.appendChild(tile);
      });

      // Set up Intersection Observer for lazy loading
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const tile = entry.target;

            // Load background image
            const bgUrl = tile.dataset.bgUrl;
            if (bgUrl) {
              tile.style.backgroundImage = bgUrl;
            }

            // If video, handle differently if needed
            if (tile.classList.contains("videoTile")) {
              // Optional: load video thumbnail or setup
            }

            // Stop observing once loaded
            obs.unobserve(tile);
          }
          else {
            tile.style.backgroundImage = '';
          }
        });
      }, {
        rootMargin: '200px' // Preload a bit before they enter viewport
      });

      // Observe all tiles
      document.querySelectorAll('.tileItem').forEach(tile => {
        observer.observe(tile);
      });
    })
    .catch(console.error);

  /* ============================
     Open Modal — same as carousel
     ============================ */

  tilesContainer.addEventListener("click", (event) => {
    const tile = event.target.closest(".tileItem");
    if (!tile) return;

    // Disable body scroll
    document.body.style.overflow = 'hidden';

    // If VIDEO tile
    if (tile.classList.contains("videoTile")) {
      modalImg.style.display = "none";

      const videoUrl = tile.dataset.videoUrl;
      if (!videoUrl) return;

      // Remove existing video
      const oldVid = modalVideo.querySelector("video");
      if (oldVid) { try { oldVid.pause(); } catch {}; oldVid.remove(); }

      // Create video element
      const vid = document.createElement("video");
      vid.src = videoUrl;
      vid.controls = true;
      vid.autoplay = true;
      vid.playsInline = true;

      modalVideo.appendChild(vid);
      modalVideo.style.display = "block";

      modal.style.display = "block";
      return;
    }

    // If IMAGE tile
    const bg = tile.style.backgroundImage;
    const url = bg.slice(5, -2);

    modalVideo.style.display = "none";
    const oldVid = modalVideo.querySelector("video");
    if (oldVid) { try { oldVid.pause(); } catch {}; oldVid.remove(); }

    modalImg.src = url;
    modalImg.style.display = "block";
    modal.style.display = "block";
  });

  /* ============================
     Close Modal — same as carousel
     ============================ */

  function closeModal() {
    modal.style.display = "none";
    document.body.style.overflow = '';

    modalImg.src = "";

    const vid = modalVideo.querySelector("video");
    if (vid) { try { vid.pause(); } catch {}; vid.remove(); }

    modalVideo.style.display = "none";
  }

  modalClose.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "block") {
      closeModal();
    }
  });
});
