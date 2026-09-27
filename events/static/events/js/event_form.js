
document.addEventListener("DOMContentLoaded", function () {
    const attendanceRole = document.getElementById(
        "id_attendance_role"
    );

    const vehicleField = document.getElementById(
        "div_id_vehicle"
    );

    const coDriverField = document.getElementById(
        "div_id_co_driver"
    );

    if (!attendanceRole || !vehicleField || !coDriverField) {
        return;
    }

    function updateCompetitionFields() {
        const isCompetitor = attendanceRole.value === "Competitor";

        vehicleField.hidden = !isCompetitor;
        coDriverField.hidden = !isCompetitor;

        if (!isCompetitor) {
            document.getElementById("id_vehicle").value = "";
            document.getElementById("id_co_driver").value = "";
        }
    }

    attendanceRole.addEventListener(
        "change",
        updateCompetitionFields
    );

    updateCompetitionFields();
});
