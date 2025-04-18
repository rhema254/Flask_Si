
// const apiUrl = config.apiUrl;

/* 
    Functions here:
    1. Populating the dropdown using list in timezone.js
    2. Getting the currentSelectedTimezone from the dropdown.
    3. Getting the date, time and heading selection.
    4. An event listener to update selected time
*/


// Populate the dropdown

const timezoneSelect = document.getElementById('timezone');

timezones.forEach((timezone) => {
    const option = document.createElement('option');
    option.value = timezone.value;
    option.textContent = timezone.label;
    timezoneSelect.appendChild(option);

});


// Function to get the currently selected value
function getCurrentSelectedTimezone() {
    let timezonefield = document.getElementById('timezonefield');
    timezonefield = timezoneSelect.value;

    return timezoneSelect.value;
}

// Example usage:
const currentSelection = getCurrentSelectedTimezone();

// Add an event listener to update the value when the selection changes
timezoneSelect.addEventListener('change', () => {
    const selectedTimezone = timezoneSelect.value;

    getCurrentSelectedTimezone();
});





// Function to convert short or long time formats into 24-hour format
function convertTo24HourFormat(inputTime) {
    const timeHyphen = "–";
    let resultTime = null;

    try {
        if (inputTime.length >= 9) {
            // Long time format (e.g., "10:00-11:30 am")
            let startTime = inputTime.split("–")[0];
            let ampm = inputTime.split(" ")[1];

            const start24 = convertSingleTime(startTime, ampm);
            resultTime = `${start24}`;
        } else {
            // Short time format (e.g., "10:00 am")
            let startTime = inputTime.split(" ")[0];
            let ampm = inputTime.split(" ")[1];
            resultTime = convertSingleTime(startTime, ampm);
        }

        return resultTime;
    } catch (error){
        console.error("Error converting time to 24-hour format:", error);

        alert("Please select a valid time.");

    }

}

// Helper function to convert a single time (e.g. 10:00 am) into 24-hour format
function convertSingleTime(startTime, ampm) {
    let [hours, minutes] = startTime.split(":").map(Number);


    if (ampm.toLowerCase() === "pm" && hours !== 12) {
        hours += 12;
    } else if (ampm.toLowerCase() === "am" && hours === 12) {
        hours = 0;
    }

    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:00`;
}




document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the form from refreshing the page

        //1. Capture Form data.
        const fullname = document.getElementById('fullname')
        const name = fullname.value;

        const email = form.querySelector('input[type="email"]').value;

        const phoneInput = document.getElementById('phoneInput');
        const phone = phoneInput.value;

        const form_message = document.getElementById('description');
        const description = form_message.value;

        const date1 = selectedDate.toLocaleDateString(('en-us'), { year: "numeric", day: '2-digit', month: "2-digit" });
        //  [2] - year, [1] - day, [0] - month
        const date = date1.split("/", 3)[2] + "-" + date1.split('/', 3)[0] + "-" + date1.split("/", 3)[1]



        let initialTime = selectedTime;

        const time = convertTo24HourFormat(initialTime);
        

        const servicesArray = Array.from(form.querySelectorAll('input[type="checkbox"]:checked'))
            .map((checkbox) => checkbox.value);
       
        const servicesObject = {
            services: servicesArray // Structure the services as an object
        };
        const currentSelection = getCurrentSelectedTimezone();
        const timezone = currentSelection;

        const formData = {
            fullname: name,
            email: email,
            phone: phone,
            timezone: timezone,
            date: date,
            time: time,
            services: servicesObject,
            description: description,
        };

        console.log('Form Data:', formData); 

        try {
            //3. Sending data to the backend
            const response = await fetch(`/Booking`, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                sessionStorage.setItem('formSuccessMessage', 'Thank you for your information. We received your response and emailed you a copy');

                // Redirect to the homepage after a small delay (optional for smoother transition)
                setTimeout(() => {
                    window.location.href = '/Homepage';
                }, 1500); //   
            } else {
                alert('Failed to submit the form. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while submitting the form.');
        }
    });
});
