function toggleContent(element) {
    // Find the next sibling with the class 'content' and toggle its display
    const content = element.parentElement.nextElementSibling;
    if (content && content.classList.contains('content')) {
        content.style.display = content.style.display === 'block' ? 'none' : 'block';
        // Change button text to indicate state
        element.textContent = content.style.display === 'block' ? 'Hide all' : 'Show all';
    }
}