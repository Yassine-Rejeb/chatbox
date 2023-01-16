//--------------- Floating settings window --------------->
    // Get a reference to the button and the floating window
    var toggleButton = document.getElementById('toggle-floating-window');
    var floatingWindow = document.getElementById('floating-window');

    // Add an event listener to the button that will toggle the floating window
    toggleButton.addEventListener('click', function() {
    // If the floating window is currently hidden, remove the 'hidden' class to show it
    if (floatingWindow.classList.contains('hidden')) {
        floatingWindow.classList.remove('hidden');
    }
    // If the floating window is currently visible, add the 'hidden' class to hide it
    else {
        floatingWindow.classList.add('hidden');
    }
    });
//--------------- End Floating settings window --------------->


// Hide the floating window
function hideFloatingWindow() {
    document.getElementById("floatingWindow").style.display = "none";
} 

