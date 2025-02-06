// const apiURL = config.apiUrl;


function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

async function cancelBooking() {
    const button = document.getElementById("cancel-button");
    // const overlay = document.getElementById("loading-overlay");

    try {
        // Show "Please Wait..." text and overlay
        button.disabled = true;
        button.textContent = "Please Wait...";
        // overlay.classList.remove("hidden");

        
        // Send data to backend
        const response = await fetch(`/Cancel/${bookingId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(cancel_body)
        });

        if (response.ok) {
            const result = await response.json();

            // Redirect to the homepage after a small delay (optional for smoother transition)
            setTimeout(() => { 
                window.location.href = '/Homepage'; }, 500); //  
            
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    }
    catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again.");
    }
}

// Extract the booking ID from the query string

// const bookingId = getQueryParam('id');
// console.log("Booking ID:", bookingId);

const bookingId = window.location.pathname.split("/").pop()


const cancel_body = {status:'Cancelled'};


async function fetchBookingDetails(bookingId) {
    try {
        const response = await fetch(`/bookings/${bookingId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch booking details');
        }

         const bookingDetails = await response.json();
        
    
        const bookedDate = new Date(bookingDetails.date);
        const formattedBookedDate = bookedDate.toLocaleDateString('en-us', {month: 'long', day:'numeric', year:'numeric' });


        const [hours, minutes] = (bookingDetails.time).split(":").map(Number);
        const period = hours >= 12 ? "pm" : "am";
        const formattedHours = hours % 12 || 12; // '0' becomes '12' in 12-hour format
       const formattedBookedTime = `${formattedHours}:${minutes.toString().padStart(2, "0")} ${period}`;
        
       
        const canceldata = document.getElementById('canceldata')

        canceldata.innerHTML = `You are about to cancel your appointment on ${formattedBookedDate} at ${formattedBookedTime}, <strong> ${bookingDetails.timezone}</strong> Time. <br>
        Please confirm.`

        
        return bookingDetails;
    } catch (error) {
        console.error('Error fetching booking details:', error);
        return null;
    }
}

fetchBookingDetails(bookingId);


