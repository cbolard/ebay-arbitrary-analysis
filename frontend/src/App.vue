<template>
  <div>

    <div class="Polaris-Page Polaris-Page--fullWidth">
      <div class="Polaris-Page__Content">
        <div class="Polaris-Layout">
          <div class="Polaris-Layout__Section">
            <div class="Polaris-LegacyCard">
              <div class="Polaris-LegacyCard__Header Polaris-LegacyCard__FirstSectionPadding">
                <h2 class="Polaris-Text--root Polaris-Text--headingSm">Scraper de produits Amazon</h2>
              </div>
              <div class="Polaris-LegacyCard__Section Polaris-LegacyCard__LastSectionPadding">
                <div class="Polaris-BlockStack" style="--pc-block-stack-order:column;--pc-block-stack-gap-xs:var(--p-space-400)">
                  <div class="Polaris-FormLayout__Item Polaris-FormLayout--grouped">
                    <div class="">
                      <div class="Polaris-Labelled__LabelWrapper">
                        <div class="Polaris-Label">
                          <label id=":R2q6:Label" for=":R2q6:" class="Polaris-Label__Text">Produit recherché</label>
                        </div>
                      </div>
                      <div class="Polaris-Connected">
                        <div class="Polaris-Connected__Item Polaris-Connected__Item--primary">
                          <div class="Polaris-TextField">
                            <input   v-model="searchTerm" placeholder="Entrez votre recherche Amazon"  id=":R2q6:" autocomplete="off" class="Polaris-TextField__Input" type="text" aria-labelledby=":R2q6:Label" aria-invalid="false" data-1p-ignore="true" data-lpignore="true" data-form-type="other" value="">
                            <div class="Polaris-TextField__Backdrop">
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="!isLoading" class="Polaris-FormLayout__Item Polaris-FormLayout--grouped">
                    <div class="">
                      <button @click="submitSearch" class="Polaris-Button Polaris-Button--pressable Polaris-Button--variantPrimary Polaris-Button--sizeMedium Polaris-Button--textAlignCenter" type="button">
                        <span class="">Générer le CSV</span>
                      </button>
                    </div>
                  </div>
                  <div v-else class="Polaris-FormLayout__Item Polaris-FormLayout--grouped">
                    <div class="">
                      <button class="Polaris-Button Polaris-Button--pressable Polaris-Button--variantSecondary Polaris-Button--sizeMedium Polaris-Button--textAlignCenter Polaris-Button--disabled Polaris-Button--loading" aria-disabled="true" type="button" aria-busy="true" tabindex="-1">
                        <span class="Polaris-Button__Spinner">
                          <span class="Polaris-Spinner Polaris-Spinner--sizeSmall">
                            <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.229 1.173a9.25 9.25 0 1011.655 11.412 1.25 1.25 0 10-2.4-.698 6.75 6.75 0 11-8.506-8.329 1.25 1.25 0 10-.75-2.385z">
                              </path>
                            </svg>
                          </span>
                          <span role="status">
                            <span class="Polaris-Text--root Polaris-Text--visuallyHidden">Loading</span>
                          </span>
                        </span>
                        <span class="">Save product</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>



  </div>
</template>

<script setup>
import { ref } from 'vue';

const searchTerm = ref('');
const isLoading = ref(false);

const genererNomFichier = (url) => {
  // Extrait le terme de recherche de l'URL. 
  // Cette regex suppose que le terme de recherche est après `?k=` ou `&k=`.
  const match = url.match(/[?&]k=([^&]+)/);
  const termeRecherche = match ? match[1] : 'inconnu';
  // Remplace les caractères spéciaux et les espaces par des tirets
  const nomPropre = termeRecherche.replace(/[^a-zA-Z0-9]/g, '-');
  return `amazon-${nomPropre}.csv`;
};


const submitSearch = async () => {
  isLoading.value = true;
  const baseUrl = 'https://www.amazon.fr/s?k=';
  const searchUrl = `${baseUrl}${encodeURIComponent(searchTerm.value)}`; // Utilisez .value pour accéder à la valeur de la référence

  try {
    const response = await fetch('http://localhost:5000/generate-csv', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: searchUrl }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `amazon-${searchTerm.value.replace(/\s+/g, '-')}.csv`; // Notez l'utilisation de .value ici
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(downloadUrl);
    isLoading.value = false;
  } catch (error) {
    console.error('There was a problem with your fetch operation:', error);
  }
};





</script>
