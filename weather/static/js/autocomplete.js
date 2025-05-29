document.addEventListener('DOMContentLoaded', () => {
    const cityInput = document.getElementById('city-input');
    const autocompleteResults = document.getElementById('autocomplete-results');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');

    let timeout;
    cityInput.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const query = cityInput.value;
            if (query.length < 2) {
                autocompleteResults.innerHTML = '';
                return;
            }

            fetch(`/autocomplete/?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    autocompleteResults.innerHTML = '';
                    data.forEach(city => {
                        const item = document.createElement('div');
                        item.className = 'dropdown-item';
                        item.textContent = city.name;
                        item.addEventListener('click', () => {
                            cityInput.value = city.name;
                            latitudeInput.value = city.latitude;
                            longitudeInput.value = city.longitude;
                            autocompleteResults.innerHTML = '';
                        });
                        autocompleteResults.appendChild(item);
                    });
                })
                .catch(error => console.error('Error fetching autocomplete:', error));
        }, 300);
    });
});