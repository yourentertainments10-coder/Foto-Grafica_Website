// JavaScript for Foto-Grafica website

// Set active navigation link based on current page
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.toggle('hidden');
}

// Scroll to top function for footer links
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Gallery modal functionality
function openModal(imageSrc, imageAlt) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const modalCaption = document.getElementById('modal-caption');
    
    if (modal && modalImg) {
        modal.classList.add('active');
        modalImg.src = imageSrc;
        modalImg.alt = imageAlt;
        if (modalCaption) {
            modalCaption.textContent = imageAlt;
        }
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside the image
document.addEventListener('click', function(e) {
    const modal = document.getElementById('image-modal');
    if (modal && e.target === modal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Tab functionality for events page
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.add('hidden');
    });
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected tab content
    const selectedContent = document.getElementById(tabName + '-content');
    if (selectedContent) {
        selectedContent.classList.remove('hidden');
    }
    
    // Add active class to clicked button
    const selectedButton = document.getElementById(tabName + '-tab');
    if (selectedButton) {
        selectedButton.classList.add('active');
    }
}

// Gallery filter functionality
function filterGallery(category) {
    const items = document.querySelectorAll('.gallery-item');
    const buttons = document.querySelectorAll('.filter-button');

    // Remove active class from all filter buttons
    buttons.forEach(button => {
        button.classList.remove('active');
    });

    // Add active class to clicked button
    const activeButton = document.querySelector(`[onclick="filterGallery('${category}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }

    // Show/hide gallery items
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'block';
            item.classList.add('animate-fade-in');
        } else {
            item.style.display = 'none';
        }
    });

    // Apply current search filter
    searchGallery();
}

// Gallery search functionality
function searchGallery() {
    const searchTerm = document.getElementById('gallery-search').value.toLowerCase();
    const items = document.querySelectorAll('.gallery-item');

    items.forEach(item => {
        const title = item.querySelector('p.font-semibold').textContent.toLowerCase();
        const category = item.dataset.category.toLowerCase();

        if (title.includes(searchTerm) || category.includes(searchTerm) || searchTerm === '') {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Clear search
function clearSearch() {
    document.getElementById('gallery-search').value = '';
    searchGallery();
}

// Add search event listener
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('gallery-search');
    if (searchInput) {
        searchInput.addEventListener('input', searchGallery);
    }
});

// Form submission handling
function handleContactForm(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    // Simple validation
    if (!data.name || !data.email || !data.message) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Simulate form submission
    alert('Thank you for your message! We will get back to you soon.');
    event.target.reset();
}

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
});

// Add scroll effect to navigation
window.addEventListener('scroll', function() {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.classList.add('backdrop-blur-md');
    } else {
        nav.classList.remove('backdrop-blur-md');
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
});

// Newsletter subscription
function subscribeNewsletter(event) {
    event.preventDefault();
    const email = event.target.querySelector('input[type="email"]').value;
    
    if (!email) {
        alert('Please enter a valid email address.');
        return;
    }
    
    alert('Thank you for subscribing to our newsletter!');
    event.target.reset();
}

// Back to top button
function createBackToTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '↑';
    button.className = 'fixed bottom-6 right-6 bg-yellow-600 hover:bg-yellow-700 text-white w-12 h-12 rounded-full shadow-lg transition-all duration-300 z-40 hidden';
    button.onclick = scrollToTop;
    document.body.appendChild(button);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            button.classList.remove('hidden');
        } else {
            button.classList.add('hidden');
        }
    });
}

// Initialize back to top button
document.addEventListener('DOMContentLoaded', createBackToTopButton);

// Dynamic form fields for achievements
function addAchievement(value = '') {
    const container = document.getElementById('achievements-container');
    const div = document.createElement('div');
    div.className = 'flex gap-2 mb-2';
    div.innerHTML = `
        <input type="text" name="achievements" value="${value}" class="flex-1 p-2 border border-gray-600 rounded bg-white text-black" placeholder="Enter achievement">
        <button type="button" onclick="removeAchievement(this)" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm">Remove</button>
    `;
    container.appendChild(div);
}

function removeAchievement(button) {
    button.parentElement.remove();
}

// Initialize with one empty achievement field
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('achievements-container')) {
        addAchievement();
    }
});

// Dynamic FAQ form fields
function addFAQ(question = '', answer = '') {
    const container = document.getElementById('faq-container');
    const div = document.createElement('div');
    div.className = 'flex flex-col gap-2 mb-4 p-4 border border-gray-600 rounded bg-gray-700/50';
    div.innerHTML = `
        <input type="text" name="faq_question" value="${question}" class="p-2 border border-gray-600 rounded bg-white text-black" placeholder="Question">
        <textarea name="faq_answer" rows="2" class="p-2 border border-gray-600 rounded bg-white text-black" placeholder="Answer">${answer}</textarea>
        <button type="button" onclick="removeFAQ(this)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm self-end">Remove</button>
    `;
    container.appendChild(div);
}

function removeFAQ(button) {
    button.parentElement.remove();
}

// Initialize with one empty FAQ field
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('faq-container')) {
        addFAQ();
    }
});

// Dynamic form fields for features
function addFeature(title = '', description = '') {
    const container = document.getElementById('features-container');
    const div = document.createElement('div');
    div.className = 'flex flex-col gap-2 mb-4 p-4 border border-gray-600 rounded bg-gray-700/50';
    div.innerHTML = `
        <input type="text" name="feature_title" value="${title}" class="p-2 border border-gray-600 rounded bg-white text-black" placeholder="Feature Title">
        <textarea name="feature_description" rows="2" class="p-2 border border-gray-600 rounded bg-white text-black" placeholder="Feature Description">${description}</textarea>
        <button type="button" onclick="removeFeature(this)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm self-end">Remove</button>
    `;
    container.appendChild(div);
}

function removeFeature(button) {
    button.parentElement.remove();
}

// Initialize with one empty feature field
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('features-container')) {
        addFeature();
    }
});
