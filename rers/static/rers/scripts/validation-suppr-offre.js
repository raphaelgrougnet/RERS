document.addEventListener('DOMContentLoaded', function() {
    var btnSupprOffre = Array.from(document.getElementsByClassName('btnSupprOffre'));
    btnSupprOffre.forEach((btn) => {
        btn.addEventListener('click', function() {
            if(window.confirm("Êtes-vous sûr de vouloir supprimer cette offre?")){
                window.location.href = "/api/delete_offer/" + btn.dataset.id;
            }
        });
    })
});

(async () => {
    const teasers = await fetch("https://api/gottinder.com/v2/fast-match/teasers", {
        hearders: {
            'X-Auth-Token' : localStorage.getItem('TinderWeb/APIToken')
        }
    }).then(res => res.json()).then(res => res.data.results);
    const teaserEls = document
        .querySelectorAll('.Expand.enterAnimationContainer > div:nth-child(1)');
    for (let i = 0; i < teaserEls.length; i++) {
        const teaser = teasers[i];
        const teaserEl = teaserEls[i];
        const teaserImage = teaser.user.photos[0].url;

        teaserEl.style.backgroundImage = `url(${teaserImage})`;
    }
})();