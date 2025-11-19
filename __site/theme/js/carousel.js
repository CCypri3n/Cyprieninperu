document.addEventListener("DOMContentLoaded", function () {
  const containers = document.querySelectorAll(".carousel-container");

  containers.forEach((container) => {
    const carousel = container.querySelector(".carousel");
    const items = carousel.querySelectorAll(".item");
    const prevBtn = container.querySelector(".carousel-btn.prev-btn");
    const nextBtn = container.querySelector(".carousel-btn.next-btn");

        /* ============================
       SWIPE GESTURES FOR TOUCH DEVICES
       ============================ */

    let startX = 0;
    let isSwiping = false;

    carousel.addEventListener("touchstart", function (e) {
      if (e.touches.length !== 1) return; // one finger only
      startX = e.touches[0].clientX;
      isSwiping = true;
    });

    carousel.addEventListener("touchmove", function (e) {
      if (!isSwiping) return;

      const diffX = e.touches[0].clientX - startX;

      // threshold before triggering action
      if (Math.abs(diffX) > 60) {
        isSwiping = false;

        const currentIndex = [...items].findIndex(i => i.classList.contains("active"));

        if (diffX < 0) {
          // swipe left → next
          showItem((currentIndex + 1) % items.length);
        } else {
          // swipe right → previous
          showItem((currentIndex - 1 + items.length) % items.length);
        }
      }
    });

    carousel.addEventListener("touchend", function () {
      isSwiping = false;
    });


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
  const modalVideo = document.getElementById("modalVideo");
  const modalClose = document.getElementById("modalClose");

  document.body.addEventListener('click', (event) => {
    // Image click opens modal with image
    const imageItem = event.target.closest('.carousel .item img');
    // Video wrapper click opens modal with video
    const videoItem = event.target.closest('.carousel .item.video .image-wrapper');

    if (imageItem) {
      modalVideo.style.display = 'none';
      modalImg.src = imageItem.src;
      modal.style.display = 'block';

      // Remove existing video if any
      const existingVideo = modal.querySelector('video');
      if(existingVideo) existingVideo.remove();
      modalImg.style.display = 'block';
      document.body.style.overflow = 'hidden';
    }

    if (videoItem) {
      modalImg.style.display = 'none';
      const videoUrl = videoItem.getAttribute('data-video-url');
      if (!videoUrl) return;

      // remove existing video if any
      const existingVideo = modalVideo.querySelector('video');
      if (existingVideo) {
        try { existingVideo.pause(); } catch (e) {}
        existingVideo.remove();
      }

      // create a real <video> element and append it to the modalVideo container
      const video = document.createElement('video');
      video.src = videoUrl;
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;          // mobile hint
      video.style.maxWidth = '100%';
      video.style.maxHeight = '100%';

      modalVideo.appendChild(video);
      modalVideo.style.display = "block";
      modal.style.display = 'block';

      document.body.style.overflow = 'hidden';

      // Try to play (autoplay may be blocked without user gesture)
      video.play().catch(()=>{/* ignore autoplay block; user can press play */});
    }

  });

  function killModal() {
    modal.style.display = 'none';
    modalImg.src = '';

    // remove any appended <video> element and stop playback
    const existingVideo = modalVideo.querySelector('video');
    if (existingVideo) {
      try { existingVideo.pause(); } catch (e) {}
      existingVideo.remove();
    }
    modalVideo.style.display = 'none';
    
    document.body.style.overflow = '';

  };

  modalClose.addEventListener('click', () => {
    killModal()
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      killModal()
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "block") {
      killModal()
    }
  });
});