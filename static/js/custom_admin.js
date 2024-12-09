// Select all elements matching the selector
const selects = document.querySelectorAll('select');

// Apply the styles to each element
selects.forEach(select => {
    select.style.maxHeight = '400px'; // Adjust height as needed
    select.style.overflowY = 'auto';
    select.style.maxWidth = '400px'; // Adjust height as needed
    select.style.overflowX = 'auto';
});
