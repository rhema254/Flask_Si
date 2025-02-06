/* Functions List

1. Getting current Date and populating respective div 
2. Getting current Month and populating respective div
3. Update Months: Previous Month and Next Month functionality.
4. 
*/

// Global variables to track state
// Global variables to track state
let currentDate = new Date();
let selectedDate = new Date();
let currentWeekStart = getWeekStart(currentDate);

// DOM Elements
const currentDateElement = document.getElementById('currentDate');
const currentMonthElement = document.getElementById('current-month');
const prevMonthElement = document.getElementById('prev-month');
const nextMonthElement = document.getElementById('next-month');
const prevWeekElement = document.getElementById('previous-week');
const nextWeekElement = document.getElementById('next-week');
const dayElements = Array.from({ length: 7 }, (_, i) => document.getElementById(`day${i + 1}`));

// Helper function to get Monday of current week
function getWeekStart(date) {
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1); // adjust when day is Sunday
    return new Date(date.setDate(diff));
}

// Update the display of current date
function updateCurrentDateDisplay() {
    currentDateElement.textContent = selectedDate.toLocaleDateString('en-us', {
        weekday: 'long',
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
}

// Update the display of current month
function updateCurrentMonthDisplay() {
    currentMonthElement.textContent = currentDate.toLocaleDateString('en-us', {
        month: 'long',
        year: 'numeric'
    });
}

// Update the week display
function updateWeekDisplay() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    dayElements.forEach((dayElement, index) => {
        const date = new Date(currentWeekStart);
        date.setDate(currentWeekStart.getDate() + index);
        dayElement.textContent = date.getDate();
        dayElement.value = date.getDate().toString().padStart(2, '0'); // Pad single digits with leading zero

        // Add data attribute to store full date information
        dayElement.setAttribute('data-full-date', date.toISOString());


        // Check if date is in the past
        if (date < today) {
            dayElement.disabled = true;
            dayElement.style.textDecoration = 'line-through';
            dayElement.style.opacity = '0.5';
        } else {
            dayElement.disabled = false;
            dayElement.style.textDecoration = 'none';
            dayElement.style.opacity = '1';
        }

        // Highlight selected date
        if (date.toDateString() === selectedDate.toDateString()) {
            dayElement.style.color = '#000';
            dayElement.classList.add('bg-white');

        } else {
            dayElement.classList.remove('bg-white');
            dayElement.style.color = '#fff' // Ensure previously selected day reverts
        }
    });
}

// Month navigation handlers
prevMonthElement.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    currentWeekStart = getWeekStart(currentDate);
    updateCurrentMonthDisplay();
    updateWeekDisplay();
});

nextMonthElement.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    currentWeekStart = getWeekStart(currentDate);
    updateCurrentMonthDisplay();
    updateWeekDisplay();
});

// Week navigation handlers
prevWeekElement.addEventListener('click', () => {
    currentWeekStart.setDate(currentWeekStart.getDate() - 7);
    currentDate = new Date(currentWeekStart);
    updateCurrentMonthDisplay();
    updateWeekDisplay();
});

nextWeekElement.addEventListener('click', () => {
    currentWeekStart.setDate(currentWeekStart.getDate() + 7);
    currentDate = new Date(currentWeekStart);
    updateCurrentMonthDisplay();
    updateWeekDisplay();
});

// Date selection a
dayElements.forEach((dayElement) => {
    dayElement.addEventListener('click', () => {
        if (!dayElement.disabled) {
            const selectedDay = new Date(dayElement.getAttribute('data-full-date'));
            selectedDate = selectedDay;
            currentDate = new Date(selectedDay);

            updateCurrentDateDisplay();
            updateWeekDisplay();
            updateTimeSlots();

        }
    });
});

// Initial render
updateCurrentDateDisplay();
updateCurrentMonthDisplay();
updateWeekDisplay();




// ------------------------ Timeslots Updater ---------------------------------



// Parses time string in 12-hour format to 24-hour format for comparison
function parseTime(time) {
    const [timePart, period] = time.split(' ');
    const [hour, minute] = timePart.split(':');
    let hourIn24 = parseInt(hour, 10);

    // Convert to 24-hour format
    if (period === 'pm' && hourIn24 !== 12) {
        hourIn24 += 12; // Convert PM hours except for 12
        
    } else if (period === 'am' && hourIn24 === 12) {
        hourIn24 = 0; // Convert 12 AM to 0 hours
    }

    return hourIn24 + (parseInt(minute, 10) / 60); // Return hours as a decimal (e.g., 1.5 for 1:30)
}

// Helper function to check if the time slot is valid
function isSlotValid(slot) {


    if (slot === '11:30-12:00 am') {
        timeRange = '11:30-00:00';
    } else if (slot === '11:30-12:00 pm') {
        timeRange = '11:30-12:00';

    }

    let [timeRange, period] = slot.split(' ');
    let [startTime, endTime] = timeRange.split('–').map(t => t.trim());


    const startHour = parseTime(startTime + ' ' + period);

    // Parse end time to get the hour in 24-hour format
    let currentTime = new Date();
    currentTime.setHours(currentTime.getHours() + 1); // Add one hour


    const currentTimeIn24 = currentTime.getHours() + (currentTime.getMinutes() / 60); // Current time in decimal format
    
    return startHour > currentTimeIn24; // Return true if the slot is still valid
}







// -------------Timeslots-----------------

// 2. Populating the Timeslots dynamically.

const timeSlotsDiv = document.getElementById("timeSlots");
const headings = ["Morning", "Afternoon", "Evening"]
const morningTitle = headings[0]
const afternoonTitle = headings[1]
const eveningTitle = headings[2]

const morningSlots = [
    "12:00–12:30 am",
    "12:30–1:00 am",
    "1:00–1:30 am",
    "1:30–2:00 am",
    "2:00–2:30 am",
    "2:30–3:00 am",
    "3:00–3:30 am",
    "4:00–4:30 am",
    "4:30–5:00 am",
    "5:00–5:30 am",
    "5:30–6:00 am",
    "6:00–6:30 am",
    "6:30–7:00 am",
    "7:00–7:30 am",
    "7:30–8:00 am",
    "8:00–8:30 am",
    "8:30–9:00 am",
    "9:00–9:30 am",
    "9:30–10:00 am",
    "10:00–10:30 am",
    "10:30–11:00 am",
    "11:00–11:30 am",
    "11:30–12:00 am"

];

const afternoonSlots = [
    "12:00–12:30 pm",
    "12:30–1:00 pm",
    "1:00–1:30 pm",
    "1:30–2:00 pm",
    "2:00–2:30 pm",
    "2:30–3:00 pm",
    "3:00–3:30 pm",
    "3:30–4:00 pm",
    "4:00–4:30 pm",
    "4:30–5:00 pm",
    "5:00–5:30 pm",
    "5:30–6:00 pm"
];

const eveningSlots = [
    "6:00–6:30 pm",
    "6:30–7:00 pm",
    "7:00–7:30 pm",
    "7:30–8:00 pm",
    "8:00–8:30 pm",
    "8:30–9:00 pm",
    "9:00–9:30 pm",
    "9:30–10:00 pm",
    "10:00–10:30 pm",
    "10:30–11:00 pm",
    "11:00–11:30 pm",
    "11:30–12:00 am"
];


let selectedButton = null;
let selectedTime = selectedButton; // Track the currently selected button

let dateselected = selectedDate;

const today = new Date();
const no_availability = document.getElementById('no-availability');



function updateSelectedTime(time) {
    selectedTime = time;
    // Optional: Debugging
}




function populateTimeSlots(headings, slots, divName) {
    const filteredSlots = slots.filter(isSlotValid);
    const div = document.createElement("div");
    div.classList.add(divName, 'cursor-pointer');
    const p = document.createElement("p");
    div.appendChild(p);

    p.textContent = headings;

    slots.forEach(slot => {
        const button = document.createElement("div");
        let fulltime = slot;
        let shortest = slot.split("–")[0];
        let shorter = slot.split(" ")[1];

        let shorttime = null

        if (fulltime === '11:30–12:00 pm') {
            shorttime = '11:30 am';
        } else if (fulltime === '11:30–12:00 am') {
            shorttime = '11:30 pm'
            fulltime === '11:30–12:00 pm'
        } else {
            shorttime = shortest + " " + shorter;
        }




        if (window.innerWidth < 321) { // Adjust the breakpoint as needed
            p.classList.add("text-center", "mb-3", "p-2", "w-20", "text-[14px]",'z-4')
            button.textContent = shorttime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[8px]", "mb-[10px]", "p-[5px]", "w-[100%]", "hover:bg-white", "hover:text-black");
        } else if (window.innerWidth < 396) {
            p.classList.add("text-center", "mb-3", "p-2", "w-20", "text-[14px]",'z-4')
            button.textContent = shorttime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[12px]", "mb-[10px]", "p-[5px]", "w-[100%]", "hover:bg-white", "hover:text-black");
        } else if (window.innerWidth < 496) {
            p.classList.add("text-center", "mb-3", "p-2", "w-20", "text-[14px]",'z-4')
            button.style.color = 'black';
            button.textContent = shorttime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[12px]", "mb-[10px]", "p-[5px]", "w-[100%]", "hover:bg-white", "hover:text-black");
        } else if (window.innerWidth < 620) {
            p.classList.add("text-center", "mb-3", "p-2", "w-20", "text-[14px]",'z-4')
            button.textContent = shorttime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[12px]", "mb-[10px]", "p-[5px]", "w-[100%]", "hover:bg-white", "hover:text-black");
        } else if (window.innerWidth < 767) {
            p.classList.add("text-center", "mb-3", "p-2", "w-20", "text-[16px]",)
            button.textContent = shorttime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[16px]", "mb-[10px]", "p-[5px]", "w-[100%]", "hover:bg-white", "hover:text-black");
        }
        else {
            p.classList.add("text-center", "mx-3", "p-2", "w-40")
            button.textContent = fulltime;
            button.classList.add("border", "border-white-800", "border-1", "text-center", "text-[16px]", "mb-[10px]", "p-[5px]", "w-[100%]", "text-white");

        }


        button.addEventListener("click", () => {
            // Reset styles for previously selected button
            if (selectedButton) {
                selectedButton.classList.remove('bg-white');
                selectedButton.style.color = '#fff';
                
            }

            // Update the selected button
            selectedButton = button;

            // Apply styles to the new selection
            button.classList.add('bg-white', 'text-black');
            button.style.color = '#000';

            // Update the selected time
            updateSelectedTime(button.textContent);
        });
        div.appendChild(button);
    });
    timeSlotsDiv.appendChild(div);
}






function disableOtherButtons(selectedButton) {
    const allButtons = document.querySelectorAll("#timeSlots div");

    allButtons.forEach(button => {
        if (button !== selectedButton) {
            button.disabled = true;

        }
    });
}

function updateTimeSlots() {
    // Clear existing timeslots
    timeSlotsDiv.innerHTML = "";

    const dayOfWeek = selectedDate.getDay(); // Get the day of the week (0 = Sunday, 6 = Saturday)
    const isToday = selectedDate.toDateString() === today.toDateString(); // Check if the date is today
 
    const isTomorrow = selectedDate.toDateString() === new Date(today.getTime() + 24 * 60 * 60 * 1000).toDateString(); // Check if the date is tomorrow
    const presentTime = today.getHours() * 60 + today.getMinutes(); // Current time in minutes
    
    const inputsection = document.getElementById("input-section");
    const timezoneSelectElement = document.getElementById("timezone")

    // Handle weekends
    if (dayOfWeek === 0 || dayOfWeek === 6) {
        inputsection.classList.add("hidden");
        no_availability.style.display = "block";
        timezoneSelectElement.classList.add('hidden')
        return;
    } else {
        inputsection.classList.remove("hidden");
        no_availability.style.display = "none";
        timezoneSelectElement.classList.remove('hidden')
    }

   
    // Populate timeslots based on the selected day
    if (isToday) {
        // Filter slots for today only
        populateTimeSlots(morningTitle, morningSlots.filter(isSlotValid), "morning");
        populateTimeSlots(afternoonTitle, afternoonSlots.filter(isSlotValid), "afternoon");
        populateTimeSlots(eveningTitle, eveningSlots.filter(isSlotValid), "evening");
    } else if (isToday && presentTime >= '1370') {
        // Populate tomorrow's slots (all valid since it's a new day)
        populateTimeSlots(morningTitle, morningSlots.filter((slot) => isSlotValid(slot, "tomorrow")), "morning");
        populateTimeSlots(afternoonTitle, afternoonSlots.filter((slot) => isSlotValid(slot, "tomorrow")), "afternoon");
        populateTimeSlots(eveningTitle, eveningSlots.filter((slot) => isSlotValid(slot, "tomorrow")), "evening");
    } else {
        // For future weekdays, populate all slots without filtering
        populateTimeSlots(morningTitle, morningSlots, "morning");
        populateTimeSlots(afternoonTitle, afternoonSlots, "afternoon");
        populateTimeSlots(eveningTitle, eveningSlots, "evening");
    }
}

// Trigger `updateTimeSlots` when the date changes
document.getElementById("day-elements").addEventListener("change", (event) => {
    selectedDate = new Date(event.target.value); // Update the selected date
    updateTimeSlots(); // Update the timeslots
});

