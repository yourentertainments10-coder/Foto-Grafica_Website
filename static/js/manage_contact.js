function addFAQ() {
    const container = document.getElementById('faq-container');
    const faqItem = document.createElement('div');
    faqItem.className = 'faq-item mb-2 p-2 border border-gray-600 rounded bg-gray-700/50';
    faqItem.innerHTML = `
        <label class="block text-sm font-medium text-gray-300 mb-1">Question</label>
        <input type="text" name="faq-${container.children.length}-question" class="w-full p-2 border border-gray-600 rounded bg-white text-black mb-1" required>
        <label class="block text-sm font-medium text-gray-300 mb-1">Answer</label>
        <textarea name="faq-${container.children.length}-answer" class="w-full p-2 border border-gray-600 rounded bg-white text-black" required></textarea>
        <button type="button" class="remove-faq mt-1 bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm" onclick="removeFAQ(this)">Remove</button>
    `;
    container.appendChild(faqItem);
}

function removeFAQ(button) {
    button.parentElement.remove();
    updateFAQNames();
}

function updateFAQNames() {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach((item, index) => {
        const question = item.querySelector('input[type="text"]');
        const answer = item.querySelector('textarea');
        if (question) question.name = `faq-${index}-question`;
        if (answer) answer.name = `faq-${index}-answer`;
    });
}
