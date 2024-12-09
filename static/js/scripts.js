export function expandSummary(button) {
    const summaryBox = button.closest('.summary-box');
    const allSummaryBoxes = Array.from(document.getElementsByClassName('summary-box'));
    const otherBoxes = allSummaryBoxes.filter(box => box !== summaryBox);
    otherBoxes.forEach(box => box.classList.remove('expanded'));
    summaryBox.classList.toggle('expanded');
}
