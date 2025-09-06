// Get current slide number from the filename
function getCurrentSlideNumber() {
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1);
    const slideNumber = filename.match(/slide(\d+)\.html/);
    return slideNumber ? parseInt(slideNumber[1]) : 1;
}

// Navigate to a specific slide with smooth transition
function goToSlide(slideNumber, direction = 'next') {
    // Check if slide exists
    const totalSlides = 19; // Based on the files we saw
    if (slideNumber >= 1 && slideNumber <= totalSlides) {
        // Add smooth fade out effect
        const slide = document.querySelector('.slide');
        if (slide) {
            slide.style.opacity = '0.7';
            slide.style.transform = direction === 'next' ? 'translateX(-20px)' : 'translateX(20px)';
            slide.style.transition = 'all 0.25s ease';
        }
        
        // Navigate after animation
        setTimeout(() => {
            window.location.href = `slide${slideNumber}.html`;
        }, 250);
    }
}

// Smooth slide entrance effect
function initPageFade() {
    const slide = document.querySelector('.slide');
    if (slide) {
        slide.style.opacity = '0';
        slide.style.transform = 'translateX(20px)';
        slide.style.transition = 'all 0.4s ease';
        
        // Animate in after page loads
        setTimeout(() => {
            slide.style.opacity = '1';
            slide.style.transform = 'translateX(0)';
        }, 100);
        
        // Clean up styles after animation
        setTimeout(() => {
            slide.style.transition = '';
        }, 500);
    }
}

// Scroll to top of page
function scrollToTop() {
    window.scrollTo(0, 0);
}

// Simple slide initialization
function initSlideAnimation() {
    // Just ensure the page fades in smoothly
    initPageFade();
}

// Add simple button feedback
function addButtonFeedback() {
    const buttons = document.querySelectorAll('.nav-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Simple click feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initSlideAnimation();
    addButtonFeedback();
});

// Override goToSlide to scroll to top
const originalGoToSlide = goToSlide;
goToSlide = function(slideNumber) {
    // Scroll to top before navigating
    scrollToTop();
    // Call original function
    originalGoToSlide(slideNumber);
};

// Navigate to next slide
function nextSlide() {
    const currentSlide = getCurrentSlideNumber();
    goToSlide(currentSlide + 1, 'next');
}

// Navigate to previous slide
function previousSlide() {
    const currentSlide = getCurrentSlideNumber();
    goToSlide(currentSlide - 1, 'prev');
}

// Add keyboard navigation
document.addEventListener('keydown', function(event) {
    // Check if user is not typing in an input field
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
    }
    
    // Left arrow key for previous slide
    if (event.keyCode === 37) {
        // Only navigate if user is at the top of the page or there's no scrollbar
        if (window.scrollY === 0) {
            previousSlide();
        }
    }
    // Right arrow key for next slide
    else if (event.keyCode === 39) {
        // Only navigate if user is at the bottom of the page or there's no scrollbar
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            nextSlide();
        }
    }
});

// Prevent accidental text selection during navigation
document.addEventListener('selectstart', function(e) {
    if (e.target.closest('.nav-button')) {
        e.preventDefault();
    }
});

// Touch swipe navigation support
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', function(event) {
    touchStartX = event.changedTouches[0].screenX;
}, false);

document.addEventListener('touchend', function(event) {
    touchEndX = event.changedTouches[0].screenX;
    handleSwipe();
}, false);

function handleSwipe() {
    const swipeThreshold = 50; // Minimum distance for swipe
    const diff = touchStartX - touchEndX;
    
    // Swipe right (previous slide)
    if (diff > swipeThreshold) {
        nextSlide();
    }
    // Swipe left (next slide)
    else if (diff < -swipeThreshold) {
        previousSlide();
    }
}
