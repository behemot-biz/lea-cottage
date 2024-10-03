/*
 * Retrieves today's date in the format 'YYYY-MM-DD'.
 * 
 * - Creates a new Date object for the current date.
 * - Extracts the day, month, and year from the date object.
 * - Adds a leading zero to the day and month if needed.
 * - Returns the formatted date string.
 */
function getTodayDate() {
    var today = new Date();
    var day = ('0' + today.getDate()).slice(-2);  // Add leading zero if needed
    var month = ('0' + (today.getMonth() + 1)).slice(-2);  // Months are zero-indexed
    var year = today.getFullYear();
    return year + '-' + month + '-' + day;
}

/*
 * Initializes reservation modal functionality for displaying and editing reservations.
 * 
 * - Selects the reserveModal element from the DOM.
 * - Adds an event listener for when the modal is shown (triggered by Bootstrap's modal events).
 * - For each triggered event:
 *   - Retrieves the reservation ID, status, date, and note from the triggering button.
 *   - Uses the getTodayDate function to get the current date.
 *   - Depending on the reservation status:
 *     - Populates the modal body with a form to either create or edit the reservation.
 *     - Sets the form's action to store or edit the reservation based on the reservation ID.
 *     - Includes the CSRF token for security in the form.
 */
const reserveModal = document.getElementById('reserveModal'); // Replace with the actual modal element ID
const deleteModal = document.getElementById('deleteModal'); // Replace with the actual delete modal element ID
let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // Ensure this fetches the correct CSRF token

reserveModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var reservationId = button.getAttribute('data-id');
    var reservationStatus = button.getAttribute('data-status');
    var reservedDate = button.getAttribute('data-date');
    var reservedNote = button.getAttribute('data-note');

    var todayDate = getTodayDate();

    // Declare modalBodyContent variable
    let modalBodyContent = reserveModal.querySelector('#modalBodyContent');

    // Update content based on reservation status
    if (reservationStatus == 0) {
        modalBodyContent.innerHTML = `
            <form method="post" action="/reservation/store_reservation/${reservationId}/">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <div class="mb-3">
                    <label for="reserved_date">Pickup Date</label>
                        <input type="date" id="reserved_date" name="reserved_date" class="form-control" value="${reservedDate}" min="${todayDate}">
                </div>
                <div class="mb-3">
                    <label for="reserved_note">Reservation Note (optional)</label>
                    <textarea id="reserved_note" name="reserved_note" class="form-control">${reservedNote || ''}</textarea>
                </div>
                <div class="modal-btn-align">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Complete Reservation</button>
                </div>
            </form>
        `;
    } else if (reservationStatus == 1) {
        modalBodyContent.innerHTML = `
            <form method="post" action="/reservation/edit_reservation/${reservationId}/">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <div class="mb-3">
                    <label for="reserved_date">Pickup Date</label>
                        <input type="date" id="reserved_date" name="reserved_date" class="form-control" value="${reservedDate}" min="${todayDate}">
                </div>
                <div class="mb-3">
                    <label for="reserved_note">Reservation Note (optional)</label>
                    <textarea id="reserved_note" name="reserved_note" class="form-control">${reservedNote || ''}</textarea>
                </div>
                <div class="modal-btn-align">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </div>
            </form>
        `;
    }
});

/*
 * Initializes delete functionality for the delete modal.
 * 
 * - Selects the deleteModal element from the DOM.
 * - Adds an event listener for when the modal is shown (triggered by Bootstrap's modal events).
 * - For each triggered event:
 *   - Retrieves the reservation ID from the triggering button.
 *   - Updates the form's action attribute to the delete reservation endpoint with the reservation ID.
 */
deleteModal.addEventListener('show.bs.modal', function(event) {
    var button = event.relatedTarget;
    var reservationId = button.getAttribute('data-id');
    var form = deleteModal.querySelector('form');
    if (form && reservationId) {
        form.action = `/reservation/delete_reservation/${reservationId}/`;
    }
});
