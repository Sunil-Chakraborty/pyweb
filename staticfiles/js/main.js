// Import jQuery
import 'https://code.jquery.com/jquery-3.5.1.min.js';

// Import Bootstrap JS
import 'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js';

// Import Popper.js (required for Bootstrap tooltips and popovers)
import 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js';

// Import Lodash
import 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js';

// Import Axios for HTTP requests
import 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';

// Custom scripts
$(document).ready(function() {
    console.log('Document is ready!');

    // Example of using jQuery
    $('#myButton').on('click', function() {
        alert('Button clicked!');
    });

    // Example of using Lodash
    const numbers = [10, 5, 100, 2, 1000];
    const sortedNumbers = _.sortBy(numbers);
    console.log('Sorted numbers:', sortedNumbers);

    // Example of using Axios
    axios.get('https://jsonplaceholder.typicode.com/posts')
        .then(response => {
            console.log('Data fetched:', response.data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
