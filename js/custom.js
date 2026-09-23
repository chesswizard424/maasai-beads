const form = document.getElementById("custom-form");

const params = new URLSearchParams(window.location.search);
const reference = params.get("reference");


// Pre-fill reference product if coming from a product page

if (reference) {
    document.getElementById("reference").value = reference;
}


// Handle custom design request

form.addEventListener("submit", function(event) {

    event.preventDefault();


    // Get information from the form

    const name =
        document.getElementById("name").value.trim();

    const type =
        document.getElementById("type").value;

    const colours =
        document.getElementById("colours").value.trim();

    const size =
        document.getElementById("size").value.trim();

    const quantity =
        document.getElementById("quantity").value;

    const referenceProduct =
        document.getElementById("reference").value.trim();

    const details =
        document.getElementById("details").value.trim();


    // Create WhatsApp message

    const message = `
Hello! I'd like to request a custom beadwork design.

Name: ${name}
Type of Beadwork: ${type}
Preferred Colours: ${colours || "Not specified"}
Preferred Size: ${size || "Not specified"}
Quantity: ${quantity}
Reference Product ID: ${referenceProduct || "None"}

Details:
${details}

Thank you!
`;


    // Maasai Beadwork WhatsApp number
    const phoneNumber = "254711936249";


    // Create WhatsApp link

    const whatsappURL =
        `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;


    // Open WhatsApp

    window.open(whatsappURL, "_blank");

});
