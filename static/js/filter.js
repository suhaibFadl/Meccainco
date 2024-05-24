$(document).ready(function() {
    // document.getElementsByClassName('active').style.backgroundColor = '#f76d2b'
    const brandSelect = $('#brand-select');
    const carSelect = $('#car-select');
    const yearSelect = $('#year-select');

    const form = document.getElementById("filter-form");
    const resetButton = document.getElementById("reset-button");
    
    resetButton.addEventListener("click", function () {
        console.log("reset")
        form.reset();
        brandSelect.append('<option value="" disabled selected>Select Brand</option>');
        carSelect.empty().append('<option value="" disabled selected>Select Model</option>').prop('disabled', true);
        yearSelect.empty().append('<option value="" disabled selected>Select Year</option>').prop('disabled', true);
    });

    // Load brands using AJAX on page load
    $.get(load_brands_url, function(data) {
        // brandSelect.empty().append('<option value="">Select Brand</option>');
        data.brands.forEach(function(brand) {
            brandSelect.append(`<option value="${brand.name}">${brand.name}</option>`);
        });
    });

    brandSelect.on('change', function() {
        const selectedBrand = $(this).val();
        if (selectedBrand) {
            carSelect.prop('disabled', false);
            yearSelect.prop('disabled', true);

            // Load cars using AJAX
            $.get(load_cars_url, { brand: selectedBrand }, function(data) {
                // carSelect.empty().append('<option value="">Select Car</option>');
                console.log(data);
                console.log(data.cars);
                data.cars.forEach(function(car) {
                    carSelect.append(`<option value="${car.name}">${car.name}</option>`);
                });
            });
        } else {
            carSelect.prop('disabled', true);
            yearSelect.prop('disabled', true);
            carSelect.empty().append('<option value="">Select Car</option>');
            yearSelect.empty().append('<option value="">Select Year</option>');
        }
    });

    carSelect.on('change', function() {
        const selectedCar = $(this).val();
        if (selectedCar) {
            yearSelect.prop('disabled', false);

            // Load years using AJAX
            $.get(load_years_url, { car: selectedCar }, function(data) {
                yearSelect.empty().append('<option value="" disabled selected>Select Year</option>');
                data.years.forEach(function(year) {
                    yearSelect.append(`<option value="${year}">${year}</option>`);
                });
            });
        } else {
            yearSelect.prop('disabled', true);
            yearSelect.empty().append('<option value="" disabled selected>Select Year</option>');
        }
    });
});