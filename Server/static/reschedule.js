
document.getElementById("reschedule-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission
    

    const date1 = selectedDate.toLocaleDateString(('en-us'), { year: "numeric", day: '2-digit', month: "2-digit" });
    //  [2] - year, [1] - day, [0] - month
    const date = date1.split("/", 3)[2] + "-" + date1.split('/', 3)[0] + "-" + date1.split("/", 3)[1]   
    

    const rescheduleTime = convertTo24HourFormat(selectedTime);
    console.log(rescheduleTime)

    const rescheduleTimezone = getCurrentSelectedTimezone()

    console.log(date, rescheduleTime , rescheduleTimezone)

    
    // Validate required fields
    if (!date1 || !rescheduleTime || !rescheduleTimezone) {
        alert("Please select a date, time slot, and timezone.");
        console.log(date, rescheduleTime , rescheduleTimezone)
        
    }
    
    // Create payload
    const rescheduleData = {
        date,
        time:rescheduleTime,
        timezone:rescheduleTimezone
    };
    console.log(rescheduleData)

    try {
        // Send data to backend
        console.log(currentSelection)
        const response = await fetch(`/Reschedule/${bookingId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(rescheduleData)
        });

        if (response.ok) {
            const result = await response.json();
            sessionStorage.setItem('formSuccessMessage', 'Thank you for your information. We received your response and emailed you a copy');

            // Redirect to the homepage after a small delay (optional for smoother transition)
            setTimeout(() => {
                window.location.href = '/Homepage';
            }, 1500); //   
        console.log(result);
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again.");
    }
});



// Extract the booking ID from the query string
// function getQueryParam(param) {
//     const urlParams = new URLSearchParams(window.location.search);
//     console.log(urlParams)
//     return urlParams.get(param);
// }
// const bookingId = getQueryParam('id');
// console.log(bookingId)

const bookingId = window.location.pathname.split("/").pop();

async function fetchbookingDetails(bookingId) {
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
        
      

        const currentAppointment = document.getElementById('current-appointment');
        currentAppointment.innerHTML = `Your current appointment is set for 
        <strong style="color: #FFF;">${formattedBookedDate}</strong>, at 
        <span style="color: #FFF; font-weight: bold;">${formattedBookedTime}</span>  , 
        Timezone: <em style="color: #FFF; font-weight: bold">${bookingDetails.timezone}</em>.
      `;    

        return bookingDetails;
    } catch (error) {
        console.error('Error fetching booking details:', error);
        return null;
    }
}

fetchbookingDetails(bookingId);

