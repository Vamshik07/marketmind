// ==================== MAIN.JS ====================

// Set active navigation link
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Utility function to format markdown to HTML
function formatText(text) {
    let formatted = text;
    
    // Bold text
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Headers
    formatted = formatted.replace(/^### (.*?)$/gm, '<h4>$1</h4>');
    formatted = formatted.replace(/^## (.*?)$/gm, '<h3>$1</h3>');
    formatted = formatted.replace(/^# (.*?)$/gm, '<h2>$1</h2>');
    
    // Lists (unordered)
    formatted = formatted.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    
    // Paragraphs
    formatted = '<p>' + formatted.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>') + '</p>';
    
    return formatted;
}

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
});

// Log when page loads
console.log('MarketAI Suite loaded successfully');