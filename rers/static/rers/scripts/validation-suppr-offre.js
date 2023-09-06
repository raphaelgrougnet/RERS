document.addEventListener('DOMContentLoaded', function() {
    var btnSupprOffre = Array.from(document.getElementsByClassName('btnSupprOffre'));
    btnSupprOffre.forEach((btn) => {
        btn.addEventListener('click', function() {
            if(window.confirm("Êtes-vous sûr de vouloir supprimer cette offre?")){
                window.location.href = "/api/delete-offer/" + btn.dataset.id;
            }
        });
    })
});