function collapseTopPicks(button) {
    // Remove .show from class list to collapse opened containers
    const collapseElements = document.querySelectorAll('.collapse.show');
    collapseElements.forEach(element => {element.classList.remove('show')})
}
