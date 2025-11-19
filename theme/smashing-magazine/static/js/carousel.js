document.addEventListener("DOMContentLoaded", function () {
  const containers = document.querySelectorAll(".carousel-container");

  containers.forEach((container) => {
    const carousel = container.querySelector(".carousel");
    const items = carousel.querySelectorAll(".item");
    const prevBtn = container.querySelector(".btn.prev");
    const nextBtn = container.querySelector(".btn.next");

    function showItem(index) {
      items.forEach((item, idx) => {
        item.classList.toggle("active", idx === index);
      });
    }

    prevBtn.addEventListener("click", () => {
      const currentIndex = [...items].findIndex(i => i.classList.contains("active"));
      showItem((currentIndex - 1 + items.length) % items.length);
    });

    nextBtn.addEventListener("click", () => {
      const currentIndex = [...items].findIndex(i => i.classList.contains("active"));
      showItem((currentIndex + 1) % items.length);
    });
  });

  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modalImage");
  const modalClose = document.getElementById("modalClose");

  document.body.addEventListener('click', (event) => {
    // Image click opens modal with image
    const imageItem = event.target.closest('.carousel .item img');
    // Video wrapper click opens modal with video
    const videoItem = event.target.closest('.carousel .item.video .image-wrapper');

    if (imageItem) {
      modalImg.src = imageItem.src;
      modal.style.display = 'block';

      // Remove existing video if any
      const existingVideo = modal.querySelector('video');
      if(existingVideo) existingVideo.remove();
      modalImg.style.display = 'block';
    }

    if (videoItem) {
      modalImg.style.display = 'none';
      const videoUrl = videoItem.getAttribute('data-video-url');
      if (!videoUrl) return;

      // Create video element for modal playback
      let video = document.createElement('video');
      video.src = videoUrl;
      video.controls = true;
      video.autoplay = true;
      video.style.maxWidth = '90vw';
      video.style.maxHeight = '90vh';
      video.style.borderRadius = '12px';
      modal.appendChild(video);
      modal.style.display = 'block';
    }
  });

  modalClose.addEventListener('click', () => {
    modal.style.display = 'none';
    modalImg.src = '';
    const video = modal.querySelector('video');
    if(video) video.remove();
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      modalImg.src = '';
      const video = modal.querySelector('video');
      if(video) video.remove();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "block") {
      modal.style.display = "none";
      modalImg.src = "";
      const video = modal.querySelector('video');
      if(video) video.remove();
    }
  });
});
