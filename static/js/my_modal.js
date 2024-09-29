function getTodayDate() {
    var today = new Date();
    var day = ('0' + today.getDate()).slice(-2);  // Add leading zero if needed
    var month = ('0' + (today.getMonth() + 1)).slice(-2);  // Months are zero-indexed
    var year = today.getFullYear();
    return year + '-' + month + '-' + day;
}

reserveModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var reservationId = button.getAttribute('data-id');
    var reservationStatus = button.getAttribute('data-status');
    var reservedDate = button.getAttribute('data-date');
    var reservedNote = button.getAttribute('data-note');

    var todayDate = getTodayDate();

    // // Update the modal's title and body content
    // var modalTitle = reserveModal.querySelector('.modal-title');
    // var modalBodyContent = reserveModal.querySelector('#modalBodyContent');

    // modalTitle.textContent = 'Reservation ID: ' + reservationId;

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
                    <label for="reserved_note">Reservation Note (optioal)</label>
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
                    <label for="reserved_note">Reservation Note (optioal)</label>
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

deleteModal.addEventListener('show.bs.modal', function(event) {
    var button = event.relatedTarget;
    var reservationId = button.getAttribute('data-id');
    var form = deleteModal.querySelector('form');
    if (form && reservationId) {
        form.action = `/reservation/delete_reservation/${reservationId}/`;
    }
});

