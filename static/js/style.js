$(document).ready(function () { 
    const parentClassName = '.slick-track'; // Example class name of the parent element.

    // Replace 'child' with the class name you want to count.
    const childClassName = '.product-col'; // Example class name of the children.

    // Use .children() to select the children and then use .length to get the count.
    const numberOfChildren = $(parentClassName).children(childClassName).length;

    console.log(`Number of children with class "${childClassName}": ${numberOfChildren}`);
    console.log($('.slick-track').length)
    if($('.slick-track:has(.product-col)').length< 3){
        $('.slick-track:has(.product-col)').attr('style', 'opacity: 1; width: 100%; transform: translate3d(0px, 0px, 0px);');
        
    }
})