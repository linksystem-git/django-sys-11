document.addEventListener("DOMContentLoaded", function () {
  const tableRows = document.querySelectorAll(".datatable tbody tr");
  const editFormContainer = document.getElementById("crees");
  const closeBtn = document.querySelector(".Btnfermer");

  const formInputs = {
    numrecharge: document.getElementById("numrecharge"),
    site: document.getElementById("site"),
    simNumber: document.getElementById("simNumber"),
    idprospect: document.getElementById("idprospect"),
    volume: document.getElementById("volume"),
    rechargeDate: document.getElementById("rechargeDate"),
    expirationDate: document.getElementById("expirationDate"),
  };

  function openEditForm(rowData) {
    console.log("Données de la ligne sélectionnée:", rowData);

    formInputs.numrecharge.value = rowData[0];
    formInputs.site.value = rowData[1];
    formInputs.simNumber.value = rowData[2];

    console.log("Valeur du prospect:", rowData[3]);
    setSelectValue(formInputs.idprospect, rowData[3]);

    formInputs.volume.value = rowData[4];

    const rechargeDate = reformatDateString(rowData[5]);
    const expirationDate = reformatDateString(rowData[6]);

    formInputs.rechargeDate.value = convertDate(rechargeDate);
    formInputs.expirationDate.value = convertDate(expirationDate);

    editFormContainer.classList.add("show");
  }

  function setSelectValue(selectElement, value) {
    const options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
      if (options[i].text.trim().toLowerCase() === value.trim().toLowerCase()) {
        selectElement.selectedIndex = i;
        console.log("Prospect sélectionné:", options[i].text);
        break;
      }
    }
  }

  function reformatDateString(dateStr) {
    const [day, monthStr, year] = dateStr.split(" ");
    const months = {
      janvier: "01",
      février: "02",
      mars: "03",
      avril: "04",
      mai: "05",
      juin: "06",
      juillet: "07",
      août: "08",
      septembre: "09",
      octobre: "10",
      novembre: "11",
      décembre: "12",
    };
    const month = months[monthStr.toLowerCase()] || "01";
    return `${day}-${month}-${year}`;
  }

  function convertDate(dateStr) {
    if (!dateStr) return "";
    const [jour, mois, annee] = dateStr.split("-");
    return `${annee}-${mois.padStart(2, "0")}-${jour.padStart(2, "0")}`;
  }

  function addRowClickEvents() {
    tableRows.forEach((row) => {
      row.addEventListener("click", function () {
        tableRows.forEach((r) => r.classList.remove("selected"));
        this.classList.add("selected");

        const rowData = Array.from(this.children).map((td) =>
          td.textContent.trim()
        );
        openEditForm(rowData);
      });
    });
  }

  addRowClickEvents();

  closeBtn.addEventListener("click", function () {
    editFormContainer.classList.remove("show");
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const deleteButton = document.querySelector("#edit-form .btn-danger");
  const editForm = document.getElementById("edit-form");

  // Confirmation de la suppression
  deleteButton.addEventListener("click", function () {
    const volumeId = document.getElementById("volume").value;
    if (confirm("Voulez-vous vraiment supprimer cette recharge ?")) {
      // Soumettre le formulaire de suppression via AJAX
      fetch("/delete_data/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({ volume: volumeId }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert("Recharge supprimée avec succès.");
            // Optionnel : recharger la page ou mettre à jour l'affichage
            location.reload();
          } else {
            alert("Erreur lors de la suppression.");
          }
        });
    }
  });

  // Soumettre le formulaire de modification
  editForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(editForm);

    fetch("/edit_data/", {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Recharge modifiée avec succès.");
          location.reload();
        } else {
          alert("Erreur lors de la modification.");
        }
      });
  });
});
