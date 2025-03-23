let currentIndex = 0;  // Keeps track of the current slide index
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    function showNextSlide() {
        // Calculate the width of one slide (100%)
        const slideWidth = slides[0].clientWidth;
        
        // Move to the next slide
        currentIndex = (currentIndex + 1) % totalSlides;  // Loop back to the first slide
        
        // Use transform to move the slides
        document.querySelector('.slides').style.transform = `translateX(-${currentIndex * slideWidth}px)`;
    }

    // Automatically change slides every 2 seconds
    setInterval(showNextSlide, 2000);