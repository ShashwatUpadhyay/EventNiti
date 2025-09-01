
function downloadCertificatePDF() {
const element = document.getElementById("certificate");
const opt = {
    margin:       0.5,
    filename:     'certificate.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
};

// Wait a moment for animations to complete (optional)
html2pdf().set(opt).from(element).save();
}