document.addEventListener("DOMContentLoaded", function () {
  const tableRows = document.querySelectorAll(".datatable tbody tr");
  const editFormContainer = document.getElementById("crees");
  const closeBtn = document.querySelector(".Btnfermer");
  const formInputs = {
    idincident: document.getElementById("idincident"),
    rechargeDate: document.getElementById("rechargeDate"),
    heureincident: document.querySelector("input[name='heureincident']"),
    client: document.querySelector("select[name='client']"),
    Site: document.getElementById("Site"),
    description: document.querySelector("textarea"),
    responsabilite: document.querySelector("select[name='responsabilite']"),
  };

  // Fonction pour ouvrir le formulaire de modification et remplir les champs
  function openEditForm(rowData) {
    formInputs.idincident.value = rowData[0];
    formInputs.rechargeDate.value = convertDate(rowData[1]);
    formInputs.heureincident.value = rowData[2];
    setSelectValue(formInputs.client, rowData[3]);
    formInputs.Site.value = rowData[4];
    formInputs.description.value = rowData[5];
    setSelectValue(formInputs.responsabilite, rowData[6]);

    editFormContainer.classList.add("show");
  }

  // Fonction pour sélectionner la bonne valeur dans un élément <select>
  function setSelectValue(selectElement, value) {
    const options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
      if (options[i].text.trim() === value.trim()) {
        selectElement.selectedIndex = i;
        break;
      }
    }
  }

  // Convertir le format de date au format requis par l'input type date
  function convertDate(dateStr) {
    const [jour, mois, annee] = dateStr.split("/");
    return `${annee}-${mois}-${jour.padStart(2, "0")}`;
  }

  // Ajouter les événements de clic à chaque ligne du tableau
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

  // Fermer le formulaire lorsque le bouton de fermeture est cliqué
  closeBtn.addEventListener("click", function () {
    editFormContainer.classList.remove("show");
  });
});

//--------------------------------------------------------

// Fonction pour obtenir le token CSRF à partir des cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Vérifiez si ce cookie commence par le nom du token CSRF
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Ajouter l'événement de clic sur le bouton de suppression
document.querySelector(".delete-btn").addEventListener("click", function () {
  const incidentId = document.getElementById("idincident").value;

  // Demande de confirmation avant de supprimer
  if (confirm("Êtes-vous sûr de vouloir supprimer cet incident ?")) {
    fetch("/incidents/supprimer/" + incidentId + "/", {
      method: "DELETE",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"), // Utilisez la fonction pour obtenir le token
        "Content-Type": "application/json", // Ajoutez ce type de contenu si nécessaire
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erreur de réseau : " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        if (data.status === "success") {
          alert(data.message);
          // Recharger la page après la suppression réussie
          location.reload();
        } else {
          alert(data.message);
        }
      })
      .catch((error) => console.error("Erreur:", error));
  }
});

//---------------------------------------------------------------------
document
  .getElementById("edit-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const incidentId = document.getElementById("idincident").value;
    const url = `http://127.0.0.1:8000/modifier_incident/${incidentId}/`;

    const data = {
      Date_incident: document.getElementById("rechargeDate").value,
      heureincident: document.querySelector('input[name="heureincident"]')
        .value,
      client: document.querySelector('select[name="client"]').value,
      Site: document.getElementById("Site").value,
      description: document.querySelector("textarea").value,
      responsabilite: document.querySelector('select[name="responsabilite"]')
        .value,
    };

    fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((responseData) => {
        console.log("Modification réussie:", responseData);
        // Afficher un message de confirmation avant de recharger la page
        alert("Incident modifié avec succès.");
        window.location.reload();
      })
      .catch((error) => {
        console.error("Erreur:", error);
        alert(
          "Erreur lors de la modification de l'incident. Veuillez réessayer."
        );
      });
  });
