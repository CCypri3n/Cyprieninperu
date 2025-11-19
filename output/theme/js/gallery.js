document.addEventListener("DOMContentLoaded", () => {
  const tilesContainer = document.getElementById("tilesContainer");
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImage");
  const modalClose = document.getElementById("modalClose");

  // Fetch and build tiles
  fetch('/gallery.json')
    .then(response => response.json())
    .then(items => {
      items.forEach(item => {
        const tile = document.createElement("div");
        tile.classList.add("tileItem");

        if (item.type === 'video') {
          tile.style.backgroundImage = `url(${item.thumbnail_url})`;
          tile.classList.add('videoTile');
          tile.dataset.videoUrl = item.video_url;
          const playIcon = document.createElement('div');
          playIcon.classList.add('play-icon');
          tile.appendChild(playIcon);  // Append to tile
        } else {
          let imageUrl = item.url.startsWith('http') ? item.url : `${item.url.startsWith('/') ? '' : '/'}${item.url}`;
          tile.style.backgroundImage = `url(${imageUrl})`;
        }

        tile.style.backgroundSize = "cover";
        tile.style.backgroundPosition = "center";

        tilesContainer.appendChild(tile);
      });
    })
    .catch(err => {
      console.error("Error loading gallery.json:", err);
    });

  // Delegate click events on tilesContainer
  tilesContainer.addEventListener("click", (e) => {
    const target = e.target.closest('.tileItem');
    if (!target) return;

    if (target.classList.contains('videoTile')) {
      modalImg.style.display = 'none';
      const videoUrl = target.dataset.videoUrl;
      if (!videoUrl) return;
      console.log('Play video:', videoUrl);
      let video = document.createElement('video');
      video.src = videoUrl;
      video.controls = true;
      video.autoplay = true;
      video.style.maxWidth = '90vw';
      video.style.maxHeight = '90vh';
      video.style.borderRadius = '12px';
      modal.appendChild(video);
      modal.style.display = 'block';
    } else {
      let bg = target.style.backgroundImage;
      let url = bg.slice(5, -2); // extract url(...) string without url()
      console.log('Show image:', url);
      modalImg.src = url;
      modal.style.display = "block";
      const existingVideo = modal.querySelector('video');
      if(existingVideo) existingVideo.remove();
      modalImg.style.display = 'block';
    }
  });

  // Modal close handlers
  modalClose.addEventListener("click", () => {
    modal.style.display = "none";
    modalImg.src = "";
    const video = modal.querySelector('video');
    if(video) video.remove();
    // If you have video modal, pause/stop video here
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
      modalImg.src = "";
      const video = modal.querySelector('video');
      if(video) video.remove();
      // Pause/stop video modal if needed
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "block") {
      modal.style.display = "none";
      modalImg.src = "";
      const video = modal.querySelector('video');
      if(video) video.remove();
      // Pause/stop video modal if needed
    }
  });
});
