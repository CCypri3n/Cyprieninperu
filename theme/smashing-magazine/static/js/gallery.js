document.addEventListener("DOMContentLoaded", () => {
  const tilesContainer = document.getElementById("tilesContainer");

  // Shared modal (same structure as carousel)
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImage");
  const modalVideo = document.getElementById("modalVideo");
  const modalClose = document.getElementById("modalClose");

  /* ============================
     Build Gallery Tiles
     ============================ */

  fetch('/gallery.json')
    .then(res => res.json())
    .then(items => {
      items.forEach(item => {
        const tile = document.createElement("div");
        tile.classList.add("tileItem");

        if (item.type === 'video') {
          tile.classList.add("videoTile");
          tile.dataset.videoUrl = item.video_url;
          tile.style.backgroundImage = `url(${item.thumbnail_url})`;

          const playBtn = document.createElement('div');
            playBtn.classList.add('play-icon');

            playBtn.innerHTML = `
              <svg viewBox="0 0 24 24">
                <polygon points="8,5 19,12 8,19" fill="white"></polygon>
              </svg>
            `;

            tile.appendChild(playBtn);


        } else {
          const imgUrl = item.url.startsWith('http')
            ? item.url
            : `${item.url.startsWith('/') ? '' : '/'}${item.url}`;
          tile.style.backgroundImage = `url(${imgUrl})`;
        }

        tilesContainer.appendChild(tile);
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
